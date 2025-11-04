# 날짜: 2025-11-03
# 작성자: 황민준
# 목적: LangChain 시스템프롬프트 사용

import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

agent = create_agent(
    model = llm,
    tools = [],
    system_prompt="너는 유용한 어이스턴트이다. 간결하고 정확하게 대답해라."
)
# PromptTemplate = SystemPrompt + UserPrompt + ToolContext
## 예시:
## SystemPrompt: "너는 유용한 어이스턴트이다. 간결하고 정확하게 대답해라."
## ToolContext: "사용 가능한 도구: search(query), get_weather(location)"
## UserPrompt: "서울의 날씨가 어때?"

