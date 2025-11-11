# weather_server.py가 서버이기 때문에 먼저 실행시키고 client.py 실행
from typing import List
# from mcp.server.fastmcp import FastMCP
# mcp.server.fastmcp: 공식 MCP SDK(mcp 패키지)
## host/port/path 없음 -> stdio 중심(가장 호환/안정)
## 로컬/에이전트 붙일 때 사용
from fastmcp import FastMCP 
# fastmcp: 별도 fastmcp 패키지
## host/port/path 제공
## HTTP 방식에 사용 

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    return f"It's always sunny in {location}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8001, path="/test/mcp", host="127.0.0.1")