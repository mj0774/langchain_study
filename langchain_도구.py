# 날짜: 2025-11-03
# 작성자: 황민준
# 목적: LangChain 도구 정의 및 도구 오류 처리

import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import wrap_tool_call
# wrap_tool_call: 에이전트가 "도구를 호출"하는 순간을 감싸는 미들웨어 데코레이터
## wrap_model_call와 차이점
## -> wrap_model_call: LLM 호출 시점
## -> wrap_tool_call: 도구 호출 시점

from pprint import pprint

load_dotenv()

@tool
def search(query: str) -> str:
    """
    정보를 검색합니다.
    """
    return f"검색 결과: {query}"

@tool
def get_weather(location: str) -> str:
    """
    주어진 위치의 현재 날씨를 반환합니다.
    """
    return f"{location}의 현재 날씨는 맑음이고 20°C입니다."

llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

agent = create_agent(
    model = llm,
    tools = [search, get_weather]
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "서울의 날씨와 최신 뉴스 검색 결과를 알려줘."}]}
)

pprint(result.get("messages")[-1].content)