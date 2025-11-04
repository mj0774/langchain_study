# 날짜: 2025-11-03
# 작성자: 황민준
# 목적: LangChain 동적으로 시스템 프롬프트 변경 -> dynamic_prompt 미들웨어 사용

import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import wrap_model_call, wrap_tool_call

load_dotenv()

# middleware에 같은 종류의 데코레이터를 여러 개 사용할 수 있을까?
## 답: 
## 같은 종류의 데코레이터를 여러 개 사용할 수 있다.
## 실행 순서는 middleware 리스트의 앞에서 뒤로 감싸지고, 호출 후에는 반대 방향으로 풀린다.
### 예시) 
### middleward = [mw1, mw2, tw1, tw2]
### 1. mw1(before) -> 모델 호출 전에 가드레일 체크
### 2. mw2(before) -> 프롬프트에 타임스탬프 추가
### 3. LLM호출 -> LLM이 "get_weather 툴 써야겠다" 결정
### 4. tw1(before) -> 툴 입력이 빈 값이면 "서울"로 보정
### 5. tw2(before) -> 툴 호출 로깅 시작
### 6. 툴 실행(get_weather)
### 7. tw2(after) -> 툴 결과 로깅 종료
### 8. tw1(after) -> 툴 결과가 None이면 "데이터 없음"으로 대체
### 9. LLM 재호출 -> Observation 반영하여 최종 답 생성
### 10. mw2(after) -> 응답 톤을 "간결"로 정리
### 11. mw1(after) -> 금지 정보가 없는지 검사
### 12. 최종 응답 반환

# middleware=[mw1, mw2, tw1, tw2] 라면
# 모델 단계: mw1(before) -> mw2(before) -> (LLM) -> mw2(after) -> mw1(after)
# 툴 단계:   tw1(before) -> tw2(before) -> (TOOL) -> tw2(after) -> tw1(after)

llm = ChatOpenAI(
    model='gpt-4o-mini',
    api_key=os.getenv('OPENAI_API_KEY')
)

@tool
def get_weather(city: str) -> str:
    """주어진 도시의 현재 날씨를 반환합니다."""
    print("[TOOL 실행 중: get_weather]")
    return f"오늘 {city}의 날씨는 맑음입니다."

@wrap_model_call
def mw1(req, call_next):
    print("mw1(before)")
    out = call_next(req)
    print("mw1(after)")
    return out

@wrap_model_call
def mw2(req, call_next):
    print("mw2(before)")
    out = call_next(req)
    print("mw2(after)")
    return out

@wrap_tool_call
def tw1(call, call_next):
    print("tw1(before)")
    out = call_next(call)
    print("tw1(after)")
    return out

@wrap_tool_call
def tw2(call, call_next):
    print("tw2(before)")
    out = call_next(call)
    print("tw2(after)")
    return out

agent = create_agent(
    model=llm,
    tools=[get_weather],
    middleware=[mw1, mw2, tw1, tw2]
)

result = agent.invoke({'messages': [{'role':'user', 'content': '부산 날씨 어때?'}]})

# 1. 모델 호출 (플래닝 단계)
## -> mw1(before) → mw2(before) → (LLM) → mw2(after) → mw1(after)
# 2. 툴 호출
## -> tw1(before) → tw2(before) → (TOOL) → tw2(after) → tw1(after)
# 3. 모델 호출 (최종 답 생성 단계)
## -> mw1(before) → mw2(before) → (LLM) → mw2(after) → mw1(after)