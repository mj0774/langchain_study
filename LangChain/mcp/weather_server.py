# weather_server.py가 서버이기 때문에 먼저 실행시키고 client.py 실행
from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    return f"It's always sunny in {location}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")