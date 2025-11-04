# 날짜: 2025-11-04
# 작성자: 황민준
# 목적: LangChain 리액트 구조 이해

# ReAct 구조란? 
## LLM이 생각(Reasoning)과 행동(Action)을 반복하며 문제를 푸는 패턴이다.

# 템플릿 흐름:
## 1. 생각(Thought): LLM이 문제를 분석하고 다음 행동을 결정하는 과정
## 2. 행동(Action): LLM이 적절한 Tool을 선택하고 인자(arguments)를 함께 호출하는 과정
## 3. 관찰(Observation): 도구 호출 결과나 외부 정보로부터 얻은 데이터
## 4. 필요 시 위 1~3번 반복
## 5. 최종 답변(Final Answer): 최종 답변 도출

# 문자열 기반 ReAct와 노드 기반 ReAct의 차이
## 예전 방식은 LLM 호출 안에서 프롬프트 문장으로 Thought -> Action -> Observation 구조를 강제하였다.
## LangGraph의 등장 이후 노드 기반으로 대체되어 생각노드/도구노드/출력노드와 같이 구성된다.

import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END

load_dotenv()

# 상태 정의
class AgentState(TypedDict, total=False):
    question: str           # 사용자 질문 (초기 입력)
    action: str             # 선택된 행동 (예: "get_weather" 등)
    observation: str        # 행동 결과 요약
    retry: int              # 재시도 횟수

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

# 노드 정의
def reason(state: AgentState) -> AgentState:
    """생각(Thought) 노드: 다음에 어떤 행동을 할지 결정"""
    # 간단 프롬프트: 질문을 보고 수행할 '행동 토큰'만 뽑도록 유도
    prompt = (
        "다음 질문을 해결하기 위해 취할 단 하나의 행동 토큰을 출력하라.\n"
        "가능한 값: get_weather, unknown\n"
        f"질문: {state.get('question','')}\n"
        "행동:"
    )
    res = llm.invoke(prompt)
    action = (res.content or "").strip().split()[0]
    if action not in {"get_weather", "unknown"}:
        action = "unknown"

    print(f"[Reason] 선택된 행동: {action}")
    return {"action": action}

def act(state: AgentState) -> AgentState:
    """행동(Action) 노드: 선택된 행동을 수행하고 관찰값 생성"""
    action = state.get("action", "unknown")
    question = state.get("question", "")

    # 학습용으로 간단 구현(실전에서는 @tool 호출 또는 외부 API 호출)
    if action == "get_weather":
        # 질문 내 도시 키워드 간단 추출(학습용)
        city = "서울" if "서울" in question else "부산" if "부산" in question else "서울"
        observation = f"{city}의 날씨는 맑음 ☀️"
    else:
        observation = "적절한 도구를 찾지 못함"

    print(f"[Act] 관찰 결과: {observation}")
    return {"observation": observation}

def next_step_after_observe(state: AgentState) -> str:
    """관찰(Observation) 후 다음 노드 결정(조건부 엣지)"""
    retry = state.get("retry", 0)
    observation = state.get("observation", "")

    # 관찰 결과가 충분히 만족스럽거나 이미 한 번 재시도 했으면 종료
    if ("맑음" in observation) or (retry >= 1):
        print("[Observe] 결과 만족 혹은 재시도 한계 도달 → 종료")
        return END
    # 아니면 다시 Reason으로 루프
    print("[Observe] 결과 불만족 → Reason으로 재시도")
    return "reason"

def observe(state: AgentState) -> AgentState:
    """관찰 평가 노드: 만족/불만족 여부를 상태에 반영(여기서는 retry만 증가)"""
    return {"retry": state.get("retry", 0) + 1}

# 그래프 구성
graph = StateGraph(AgentState)

graph.add_node("reason", reason)
graph.add_node("act", act)
graph.add_node("observe", observe)

# 흐름: START -> reason -> act -> observe -> (조건부) reason 또는 END
graph.add_edge(START, "reason")
graph.add_edge("reason", "act")
graph.add_edge("act", "observe")
graph.add_conditional_edges("observe", next_step_after_observe)

app = graph.compile()

# 실행
final_state = app.invoke({"question": "서울의 날씨 알려줘"})
print("\n[Final State]\n", final_state)