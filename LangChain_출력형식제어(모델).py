# 날짜: 2025-11-04
# 작성자: 황민준
# 목적: ProviderStrategy를 활용하여 에이전트가 특정 형식으로 반환하도록 설정 -> response_format

import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.agents.structured_output import ProviderStrategy
# ProviderStrategy: 모델 제공자(OpenAI 등)의 네이티브 구조화 출력 기능을 그대로 사용하여 
# LLM이 지정된 스키마에 정확히 맞춘 결과를 생성하게 만드는 클래스
from pydantic import BaseModel, Field
# Field: Pydantic 모델의 각 필드에 기본값/제약/메타데이터를 붙이는 헬퍼 함수

load_dotenv()

class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")

agent = create_agent(
    model="gpt-5",
    response_format=ContactInfo  # Auto-selects ProviderStrategy
)

result = agent.invoke({
    "messages": [{"role": "user", 
                  "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

print(result["structured_response"])

## 특징
## OpenAI, Grok등 네이티브 구조화 출력 지원 모델에서만 지원한다. -> 구조 준수 확률이 가장 높음
## response_format=Schema 만 지정해도 모델이 지원한다면 자동으로 ProviderStrategy 적용

# ProviderStrategy의 구조 강제 원리
## LLM 제공자가 API 레벨에서 JSON Schema를 강제하도록 설계한 구조화 출력 모드
## 모델 내부의 디코더가 Schema Validation을 강제하도록 요청
## 토큰 생성 시마다 실시간 검사 -> 모델이 틀린 Schema를 생성 자체를 할 수 없음