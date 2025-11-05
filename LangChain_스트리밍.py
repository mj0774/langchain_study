# 날짜: 2025-11-04
# 작성자: 황민준
# 목적: 실시간 업데이트 표면화를 위해 스트리밍 구현하여 UX를 향상시키자. -> LLM의 지연 시간을 처리할 때 사용

import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.config import get_stream_writer  

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """
    주어진 도시의 현재 날씨를 반환합니다.
    """
    return f'{city}는 항상 맑음입니다.'

# custom 모드 확인용 툴
## 내부에서 사용자 정의 이벤트를 사용하여 임의의 내용을 출력한다.
@tool
def get_weather2(city: str) -> str:
    """
    주어진 도시의 현재 날씨를 반환합니다.
    """
    writer = get_stream_writer()
    writer(f'도시에 대한 데이터 조회: {city}')
    writer(f'도시에 대한 데이터 획득: {city}')
    return f'{city}는 항상 맑음입니다.'

llm = ChatOpenAI(
    model='gpt-4o-mini',
    api_key=os.getenv('OPENAI_API_KEY')
)

agent = create_agent(
    model=llm,
    tools=[get_weather],
)

# custom 모드 확인용 에이전트
custom_agent = create_agent(
    model=llm,
    tools=[get_weather2],
)

# 1. updates
## 각 스텝(노드 실행) 후 상태 변화를 필터링 
## 도구 호출 -> 응답 -> 최종 응답같은 에이전트 진행 상황을 단계별로 확인 가능
## 사용처: 현재 무슨 단계인지 UI에 로그/타임라인 출력할 때
## 전체 상태가 아니라 변경점만 오므로 누적 관리 필요
for chunk in agent.stream(
    {'messages': [{'role': 'user', 'content': '서울의 날씨는 어때?'}]},
    stream_mode='updates'
):
    for step, data in chunk.items():
        print(f'step: {step}')
        print(f'content: {data["messages"][-1].content_blocks}')

# 2. messages
## LLM의 토큰/메시지 청크 + 메타데이터
## 사용처: 토큰 단위 출력(타이핑 효과), 특정 노드별 토큰만 필터링할 때
## UX는 향상되지만 상태 변화는 직접 계산해야 함
for token, metadata in agent.stream(
    {'messages': [{'role': 'user', 'content': '서울의 날씨는 어때?'}]},
    stream_mode='messages'
):
    print(f'node: {metadata["langgraph_node"]}')
    print(f'content: {token.content_blocks}')
    print('\n')

# 3. custom
## 노드/툴 내부에서 임의로 get_stream_writer()로 사용자 정의 이벤트를 출력
## 사용처: LLM외 임의 내용(진행률, 중간 산출물 등) 또는 LangChain이 아닌 LLM 클라이언트 토큰을 흘릴 때
## 유연하지만 직접 이벤트를 작성하고 파싱 규칙을 스스로 정해야 함
for chunk in custom_agent.stream(
    {'messages': [{'role': 'user', 'content': '서울의 날씨는 어때?'}]},
    stream_mode='custom'
):
    print(chunk)

# 이외 stream_mode 종류
## values: 각 스텝(노드) 실행 직후의 "전체 상태 스냅샷"이 출력 -> updates는 변경 부분, values는 전체 상태
## debug: 실행 전반의 디버그/트레이스 이벤트 출력 -> 개발 단계에서 추적할 때만 사용

# 설명
## stream_mode는 리스트 형태로 ['messages', 'updates', ...]로 지정할 수도 있다.
## 이 때 순서는 중요하지 않다. 
## -> 지정한 모든 이벤트를 감시하느라 부하가 증가할 수 있음
## -> mode별로 다른 데이터 구조가 들어오므로, 구분해서 처리해야 한다.