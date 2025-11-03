# 날짜: 2025-11-03
# 작성자: 황민준
# 목적: LangChain 미들웨어를 통해 동적 모델 선택

import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
# wrap_model_call: 에이전트가 "LLM을 호출"하는 순간을 감싸는 미들웨어 데코레이터
## 요청을 바꾸거나(프롬프트/파라미터/툴 선택), 호출을 가로채거나(단축 종료), 재시도, 폴백 같은 제어를 넣을 수 있음.
## 한 번만 호출해도 되고, 0~N번 호출할 수도 있음

# ModelRequest: LLM에 대한 요청을 나타내는 객체
## 대표적으로 messages(대화형 메시지 시퀀스), 모델 파라미터(온도, 최대 토큰 수 등)를 포함

# ModelResponse: LLM으로부터의 응답을 나타내는 객체
## result(보통 AIMessage 객체), structured_response(구조화 출력 지정 시 파싱 결과)를 포함

from pprint import pprint
from datetime import datetime

load_dotenv()

basic_model = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
advanced_model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

# 라이프사이클
# 1. 에이전트가 체인/노드 실행 중 LLM 호출 직전
# 2. 에이전트가 LLM을 호출할 때 ModelRequest 객체를 받음
# 3. 내부에서 필요하면 요청을 수정한 뒤 핸들러(handler)를 불러 실제 모델을 호출
# 4. 모델의 응답 객체(ModelResponse 객체)을 받아 후처리 가능
# 5. 응답을 검증, 수정하거나 필요 시 대체 응답을 반환 
## -> 최종 응답이 다음 단계(툴 선택/상태 업데이트/ 출력 반환)로 전달
@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """
    대화의 복잡성에 따라 모델을 선택하세요.
    """
    messages_count = len(request.state["messages"])
    print("현재 메시지 수:", messages_count)
    # 메시지 객체들의 총 개수(시스템/사용자/AI/툴 메시지 포함)
    # 모델 결과가 출력되기 전에 호출되기 때문에 최종 응답 메시지는 아직 포함되지 않음
    # -> 마지막 return 부분의 handler(request)에서 모델을 실제로 호출하기 때문에 예상한 메시지 개수보다 1개 적음
    # 예시:
    ## 사용자가 처음 질문
    ## 현재 messages_count가 1
    ## print 메시지 수 출력 -> 1 출력
    ## return handler(request)에서 모델 호출 -> 툴 호출 지시가 이 때 생성되어 messages에 추가됨
    if messages_count > 10: 
        model = advanced_model
    else:
        model = basic_model

    request.model = model
    return handler(request)

@tool("get_current_time_kr", return_direct=False) 
# return_direct=False: 결과값을 LLM에게 전달하여 요약/포맷팅/추가설명 단계를 거쳐 최종 응답에 반영
# return_direct=True: 결과값을 바로 사용자에게 반환
def get_current_time_kr() -> str:
    """
    현재 시간을 YYYY-MM-DD h24:mm:ss로 반환한다.
    입력: 없음
    출력: 문자열 (예: "2025-11-03 12:00:00")
    실패 시: "ERROR" 문자열을 반환합니다.
    사용 시점: 사용자가 '지금 시간', '현재 시각'을 묻거나, 타임스탬프가 필요할 때 호출합니다.
    """
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now
    except Exception:
        return "ERROR"

agent = create_agent(
    model = advanced_model, # 기본 모델 설정 (동적 선택 미들웨어 wrap_model_call로 최종 결정된다.)
    tools = [get_current_time_kr],
    middleware=[dynamic_model_selection], # 미들웨어 등록
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "현재 시간이 몇 시야?"}]}
)

pprint(result.get("messages")[-1].content)