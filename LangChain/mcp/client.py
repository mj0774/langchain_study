import os
from dotenv import load_dotenv
import sys
import asyncio
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

load_dotenv()

# math_server.py가 client.py와 같은 폴더(mcp)에 있다고 가정
SERVER = (Path(__file__).parent / "math_server.py").resolve()

async def main():
    client = MultiServerMCPClient({
        "Math": {
            "transport": "stdio",
            "command": sys.executable, # 현재 venv 파이썬로 서브프로세스 실행
            "args": [str(SERVER)], # 서버 스크립트 절대경로
        },
        "Weather": {
            "transport": "streamable_http",
            "url": "http://127.0.0.1:8001/test/mcp",
        }
    })

    tools = await client.get_tools()

    llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

    agent = create_agent(model=llm, tools=tools)
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]
    })
    print(result["messages"][-1].content)

    result2 = await agent.ainvoke({
        "messages": [{"role": "user", "content": "what is the weather in Seoul?"}]
    })
    print(result2["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
