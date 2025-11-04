# 날짜: 2025-11-03
# 작성자: 황민준
# 목적: LangChain 도구 정의 및 도구 호출 wrap_tool_call 미들웨어 사용 -> 오류 처리 예제

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
from langchain_core.messages import ToolMessage
# ToolMessage: 도구 호출 결과를 나타내는 메시지 객체
from langchain.agents.middleware.types import ToolCallRequest, Command
# ToolCallRequest: 도구 호출에 대한 요청을 나타내는 객체
# Command: 도구 호출을 단축 종료할 때 반환하는 객체
from typing import Callable
# Callable: 함수형 타입 힌팅에 사용  

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

# 라이프사이클 - 도구 호출 미들웨어
## 1. 에이전트가 LLM 응답에서 툴 호출 계획을 생성한 뒤(툴을 쓰기로 결정한 뒤)
## 2. 미들웨어가 ToolCallRequest 객체를 받음
## 3. 미들웨어에서 사전검증/변환/정책 적용 수행 -> 인자 누락, 타입 점검, 기본값 주입 등
## 4. (필요 시) 쇼트서킷/우회 -> 조건 충족 시 handler 호출 없이 Command 객체 반환으로 실행 중단 및 우회 가능
### 언제 쓰나? 예: 토큰 제한 초과, 민감 정보 포함, 캐시 히트(같은 인자가 캐시에 있을 때)
## 5. handler(request) 호출로 실제 도구 실행
## 6. ToolMessage 반환 -> 에이전트 상태 업데이트(대화 히스토리에 ToolMessage 추가, 필요 시 LLM 재호출로 최종 답변 생성)
## 7. 한 턴에 툴을 여러 번 호출하면 위 과정을 반복
@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest , 
    handler: Callable[[ToolCallRequest], ToolMessage | Command]
) -> ToolMessage | Command:
    """
    도구 호출 중 발생하는 오류를 처리합니다.
    """
    try:
        # raise Exception("도구 호출 중 오류 발생") # 일부러 예외 발생 테스트
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"입력 값을 확인하고 다시 시도해주세요. {str(e)}",
            tool_call_id=request.tool_call['id']
        )

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

agent = create_agent(
    model = llm,
    tools = [search, get_weather],
    middleware=[handle_tool_errors]
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "서울의 날씨 알려줘"}]}
)

pprint(result.get("messages")[-1].content)