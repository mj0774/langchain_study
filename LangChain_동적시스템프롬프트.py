# 날짜: 2025-11-03
# 작성자: 황민준
# 목적: LangChain 동적으로 시스템 프롬프트 변경 -> 미들웨어 사용

import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()