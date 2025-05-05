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
        self.exit_stack = AsyncExitStack()
        self.openAI = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # methods will go here

    # 사용 가능한 서버를 반환한다.
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

        # 비동기 자원의 수명을 하나의 블록 생성.
        stack = AsyncExitStack() 

        # async with 블록 내부에서만 자원 사용 → 해당 Task 내에서 안전하게 관리
        async with stack:
            stdio, write = await stack.enter_async_context(stdio_client(server_params))
            session = await stack.enter_async_context(ClientSession(stdio, write))
            await session.initialize()

            # 서버가 제공하는 도구 목록요청
            response = await session.list_tools()
            tools = response.tools
            print("\nConnected to server with tools:", [tool.name for tool in tools])


# 쿼리 처리와 도구 호출
import json
async def main():
    with open("mcp_servers_config.json") as f:
        config = json.load(f)
    weather_server = config["mcpServers"]["weather"]
    client = MCPClient()
    await client.connect_to_server(weather_server)


asyncio.run(main())