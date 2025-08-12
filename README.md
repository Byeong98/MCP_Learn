# MCP_Learn

Model Context Protocol (MCP)을 학습하고 구현한 프로젝트입니다.

### 사용방법 

1. 디렉토리 이동 `cd mcp_clients`
2. mcp clients 실행 `uv run clients.py`

```
# .env file
OPENWEATHERMAP_APIKEY = 
OPENAI_API_KEY = 

```

### 디렉토리 구조 

```
MCP_Learn/
├── .git/
├── .venv/ 
├── MCP_Clients/ # MCP 클라이언트 관련 코드
│ ├── clients.py # MCP 클라이언트 구현 파일
│ └── mcp_servers_config.json # MCP 서버 설정 파일
├── MCP_Server/ # MCP 서버 관련 코드
│ ├── weather.py # 날씨 API 서버 구현
│ └── weather_api_test.py # 날씨 API 테스트 파일
├── .gitignore 
├── .python-version 
├── pyproject.toml 
├── uv.lock 
└── README.md 

```


### 주요 구성 요소

- **MCP_Clients/**: MCP 클라이언트 구현 및 설정
- **MCP_Server/**: MCP 서버 구현 (날씨 API 예제)

### 기술 스택

- **Python**: 메인 프로그래밍 언어
- **uv**: Python 패키지 매니저
- **MCP**: Model Context Protocol 구현
