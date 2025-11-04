# 날짜: 2025-11-03
# 작성자: 황민준
# 목적: LangChain 동적으로 시스템 프롬프트 변경 -> dynamic_prompt 미들웨어 사용

import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from typing import TypedDict

from langchain.agents.middleware import dynamic_prompt, ModelRequest
# dynamic_prompt: 실행 시점에 프롬프트를 동적으로 수정하는 미들웨어 데코레이터 -> 모델 호출 전 
# ModelRequest: LLM에게 보낼 요청(프롬프트, 파라미터 등)을 담는 객체 -> LLM 호출 직전

load_dotenv()

llm = ChatOpenAI(
    model='gpt-4o-mini',
    api_key=os.getenv("OPENAI_API_KEY")
)

class Context(TypedDict):
    user_role: str

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """
    사용자 역할에 따라 시스템 프롬프트를 생성하세요.
    """
    user_role = request.runtime.context.get('user_role', 'user')
    base_prompt = '너는 유용한 어시스턴트이다.'

    if user_role == 'expert':
        return f'{base_prompt} 자세한 기술적 답변을 제공하세요.'
    elif user_role == 'beginner':
        return f'{base_prompt} 개념을 간단하게 설명하고 전문 용어는 피하세요.'

    return base_prompt

agent = create_agent(
    model=llm,
    tools=[],
    middleware=[user_role_prompt],
    context_schema=Context
) 
# context_schema를 명시하여 내부 구조를 보장시킨다. 
# -> 넣지 않으면 None이나 키 에러 위험이 있음

result = agent.invoke(
    {'messages': [{'role': 'user', 'content': '머신러닝에 대해서 설명해라.'}]},
    context=Context(user_role='expert')
)

print(result)

# 미들웨어 총 정리
## dynamic_prompt: context, 사용자 상태, 시간 등에 따라 system prompt 수정
## wrap_model_call: LLM에게 보낼 요청 또는 응답을 가로채서 수정/검증/단축 종료
## wrap_tool_call: 에이전트가 선택한 툴 호출의 입력/출력을 감싸서 처리

# 실행 순서
## 1. 사용자 입력
## 2. @dynamic_prompt -> 시스템 프롬프트 생성
## 3. @wrap_model_call -> LLM 호출 전후 개입 (prompt, 모델 교체 등)
## 4. LLM 판단 (어떤 툴 쓸지 결정)
## 5. @wrap_tool_call -> 선택된 툴 실행 전후 개입
## 6. 툴 결과 Observation 생성
## 7. @wrap_model_call -> 다시 LLM 호출 (결과 요약 또는 최종 응답 생성)
## 8. 최종 출력