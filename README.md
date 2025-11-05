# LangChain & LangGraph Study

## 프로젝트 개요
LangChain + LangGraph 구조를 기초부터 미들웨어, 에이전트, ReAct 패턴까지 단계적으로 학습한 노트북 모음입니다.  
각 노트북은 **LangChain docs**의 구조를 기반으로 실제 코드 실습과 상세 주석을 포함합니다.

## 개발 환경
#### python 3.11.9
#### langchain 1.0.3
#### langchain-openai 1.0.1
#### langgraph 1.0.2
#### langsmith 0.4.40


## 주요 학습 내용
| No | 파일명 | 주요 학습 내용 | 핵심 개념 |
|----|---------|----------------|------------|
| 1 | **1_LangChain_구동방식** | ChatModel의 `invoke()` 기본 구조와 messages 형식 비교 (`SystemMessage`, `HumanMessage`, `AIMessage` vs dict 구조). | ChatModel, Message 구조 |
| 2 | **2_LangChain_모델미들웨어(데코레이터)** | `@wrap_model_call`을 통한 모델 호출 미들웨어 제어. 요청 전후 수정, 동적 모델 선택, 로깅 구조. | ModelMiddleware, ModelRequest/Response |
| 3 | **3_LangChain_도구미들웨어(데코레이터)** | `@wrap_tool_call`로 툴 호출 시 입력/출력 제어. 툴 결과 검증, 로깅, 예외처리 실습. | ToolMiddleware, ToolContext |
| 4 | **4_LangChain_시스템프롬프트** | 시스템 프롬프트의 역할과 초기 컨텍스트 설계. LLM 동작 일관성 유지 방법. | SystemPrompt, PromptTemplate |
| 5 | **5_LangChain_동적시스템프롬프트** | 사용자 입력에 따라 시스템 메시지를 동적으로 변경. 프롬프트 관리 패턴. | Dynamic Prompting |
| 6 | **6_LangChain_미들웨어중첩사용** | 모델/도구 미들웨어를 중첩 적용하는 실습. 호출 순서(before_model → model → after_model) 흐름 분석. | Middleware Chaining |
| 7 | **7_LangChain_출력형식제어(툴)** | `ToolStrategy`를 통한 구조적 출력 강제(JSON Schema 기반). 툴 호출로 응답 포맷 일치. | ToolStrategy, Structured Output |
| 8 | **8_LangChain_출력형식제어(모델)** | `response_format` 기반 모델 출력 구조 강제. `str_output_parser` 대비 장단점 비교. | ResponseFormat, OutputParser 비교 |
| 9 | **9_LangChain_스트리밍** | `stream_mode` 옵션(messages, custom, updates 등)의 차이 실습. 실시간 토큰 스트림 처리. | Streaming Mode, Callback |
| 10 | **10_LangChain_에이전트미들웨어** | `AgentMiddleware` 훅(before/after_model, before/after_tool)으로 LLM-Tool 루프 제어. | AgentState, AgentMiddleware |
| 11 | **11_LangChain_미들웨어총정리** | Built-in 미들웨어(`SummarizationMiddleware`, `HumanInTheLoopMiddleware`, `PIIMiddleware`) 개념과 활용 정리. | Built-in Middleware |
| 12 | **12_LangChain_리액트구조** | ReAct(Reasoning + Action) 패턴 구조 분석. LangGraph 기반 ReAct 노드 설계 이해. | ReAct Pattern, LangGraph |

## 참고 자료
- LangChain docs
  - https://docs.langchain.com/oss/python/langchain/overview
