# 날짜: 2025-11-03
# 작성자: 황민준
# 목적: LangChain create_agent 확인(툴 호출 → Observation → 최종응답 흐름 확인)
# 설명: 

import os
from dotenv import load_dotenv

from langchain.agents import create_agent 
# create_agent: 도구방식 에이전트 생성 함수
from langchain.tools import tool
# tool: 도구임을 명시하는 데코레이터
from langchain_openai import ChatOpenAI
# LangChain용 OpenAI LLM 래퍼

from pprint import pprint

load_dotenv()

# 툴 정의
@tool # 툴이라고 명시하는 데코레이터 
def get_weather(city: str) -> str:
    # 설명(description)을 명시하지 않으면 오류 발생
    # 설명이 부족하면 LLM이 툴을 올바르게 사용하지 못할 수 있음
    """
    주어진 도시의 현재 날씨를 반환합니다.
    """ 

    return f"오늘 {city}의 날씨는 맑음입니다."

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)

agent = create_agent(
    model = llm,
    tools = [get_weather],
    system_prompt="당신은 날씨 정보를 제공하는 유용한 도우미입니다."
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "광주광역시의 날씨는 어떻습니까?"}]}
)

pprint(result.get("messages")[-1].content)

# 구성 동작 사이클
# 1. HumanMessage: 사용자의 질문 수신
# 2. AIMessage: tool_calls 포함, 도구 호출 지시
# 3. ToolMessage: 툴 실행 결과(Observation)
# 4. AIMessage: 사용자에게 보여줄 최종 응답 생성 및 반환