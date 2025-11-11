# math_server.py를 로컬 방식이기 때문에 클라이언트 측에서 호출하여 실행할 것임

from mcp.server.fastmcp import FastMCP
# mcp.server.fastmcp: 공식 MCP SDK(mcp 패키지)
## host/port/path 없음 -> stdio 중심(가장 호환/안정)
## 로컬/에이전트 붙일 때 사용

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")