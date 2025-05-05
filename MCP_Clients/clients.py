import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import json
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack() # 비동기 자원의 수명을 하나의 블록 생성.
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # methods will go here

    # 단일 서버 반환
    async def connect_to_server(self, servers_config: dict):
        # 서버 설정이 비어 있는지 확인하고 예외 발생
        if not servers_config:
            raise ValueError("Server script must be a server config .json")

        # MCP 서버를 실행하기 위한 파라미터 구성
        server_params = StdioServerParameters(
            command=servers_config['command'],
            args=servers_config['args'],
            env=None
        )

        # 해당 Task 내에서 안전하게 관리
        stdio, write = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))
        await self.session.initialize()

        # 서버가 제공하는 도구 목록요청
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])


    # 쿼리 처리와 도구 호출
    async def process_query(self, query: str) -> str:
        """ 사용 가능한 도구를 이용해서 쿼리 처리 """
            
        # 한국어 입력시 영어로 변환
        messages = [
            {
                "role": "user",
                "content": query
            },
            {
                "role": "system",
                "content": ("query의 location은 영어로 변환 후 전송."
                            "단 location이 영어면 그대로 답변.")
            }
        ]

        # 사용 가능한 tool리스 가져오기
        available_tools = []

        if self.session:
            response = await self.session.list_tools()
            for tool in response.tools:
                available_tools.append({
                            "type": "function",
                            "function": {
                                "name": tool.name,
                                "description": tool.description,
                                "parameters": tool.inputSchema
                            }
                        })

        # openai 첫 요청 
        response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    tools=available_tools
                )
        
        # 최종 답변
        final_text = []

        # tool 사용요청 상태 확인 
        tool_call = response.choices[0].message.tool_calls
        
        if tool_call: # tool_call 값이 있는 경우에만 실행 
            for call in tool_call:
                tool_name = call.function.name
                tool_args = json.loads(call.function.arguments)

                # tool 사용 -> MCP server를 이용해서 값을 가져온다
                tool_result = await self.session.call_tool(tool_name,tool_args)

                # tool 사용 요청 메시지 저장
                messages.append(response.choices[0].message)

                # tool 실행결과 추가
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": tool_result.content[0].text
                })
            
            # 다시 openai 요청
            final_response = self.openai_client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=messages,
                                tools=available_tools
                            )

            final_text.append(final_response.choices[0].message.content)
        else:
            # 일반 메시지 저장
            final_text.append(response.choices[0].message.content)
        
        return "\n".join(final_text)
        
    
    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

# 실행 함수
async def main():
    with open("mcp_servers_config.json") as f:
        config = json.load(f)
    weather_server = config["mcpServers"]["weather"]

    client = MCPClient()
    try:
        await client.connect_to_server(weather_server)
        await client.chat_loop()
    finally:
        await client.cleanup()

asyncio.run(main())