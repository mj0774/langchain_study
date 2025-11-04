# 날짜: 2025-11-03
# 작성자: 황민준
# 목적: 에이전트가 특정 형식으로 반환하도록 설정 -> response_format

import os, json
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents.structured_output import ToolStrategy
# ToolStrategy: 툴 호출(tool calling)을 이용해 LLM이 지정된 스키마에 정확히 맞춘 결과를 생성하게 만드는 클래스
from pydantic import BaseModel
# BaseModel: 딕셔너리/객체 형태 + 런타임 검증/변환/직렬화까지 제공하는 스키마 엔진
# TypedDict와의 차이점?
## TypedDict는 딕셔너리 형태를 정적 타입으로 설명하는 힌트 -> 런타임 검증/변환은 없고 가볍고 표준이다.

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

agent = create_agent(
    model = llm,
    response_format=ToolStrategy(ContactInfo)
)

result = agent.invoke(
    {'messages': [{'role': 'user', 
                   'content': '다음에서 연락처 정보 추출해라: 홍길동, test@example.com, 010-1234-5678'}]}
)

# 1) JSON 문자열로 바로 출력 (Pydantic v2)
print(result["structured_response"].model_dump_json(ensure_ascii=False, indent=2))
# ensure_ascii=False: 한글/유니코드를 이스케이프하지 말고 그대로 출력
# indent: 들여쓰기 -> 보기 좋게 하기 위함

# 2) dict로 받고 싶으면:
print(result["structured_response"].model_dump())