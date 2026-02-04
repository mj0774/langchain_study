# LangChain & LangGraph Study

LangChain과 LangGraph의 실행 구조, 미들웨어, 에이전트 루프, ReAct 패턴을 중심으로 LLM 애플리케이션과 에이전트 시스템의 동작 원리를 실험·분석한 노트북 모음입니다.
단순 사용법이 아니라, 모델 호출 흐름, Tool 연계, 상태 관리, 출력 제어, 가드레일 적용 방식을 코드로 검증하는 데 초점을 맞췄습니다.

## 프로젝트 구성
```
.
├── LangChain
├── LangGraph
└── README.md
```

## 개발 환경
- Python 3.11.9
- langchain==1.0.3
- langchain_openai==1.0.1
- langgraph==1.0.2
- langsmith==0.4.40
- langchain-mcp-adapters==0.1.12
- mcp==1.21.0
- fastmcp==2.13.0.2

> 패키지 버전은 `requirements.txt`에 맞춰 설치하는 것을 권장합니다.

## 노트북 목록

### LangChain
| No | 파일명 | 주요 학습 내용 | 핵심 개념 |
|----|---------|----------------|------------|
| 1 | **1_LangChain_구동방식** | ChatModel의 `invoke()` 기본 구조와 메시지 형식 비교(`SystemMessage`, `HumanMessage`, `AIMessage` vs dict 구조). | ChatModel, Message 구조 |
| 2 | **2_LangChain_모델미들웨어(데코레이터)** | `@wrap_model_call`로 모델 호출 미들웨어 제어. 요청 전후 수정, 동적 모델 선택, 로깅 구조. | ModelMiddleware, ModelRequest/Response |
| 3 | **3_LangChain_도구미들웨어(데코레이터)** | `@wrap_tool_call`로 툴 호출 입력/출력 제어. 툴 결과 검증, 로깅, 예외처리 실습. | ToolMiddleware, ToolContext |
| 4 | **4_LangChain_시스템프롬프트** | 시스템 프롬프트 역할과 초기 컨텍스트 설계. LLM 동작 일관성 유지 방법. | SystemPrompt, PromptTemplate |
| 5 | **5_LangChain_동적시스템프롬프트** | 사용자 입력에 따라 시스템 메시지를 동적으로 변경. 프롬프트 관리 패턴. | Dynamic Prompting |
| 6 | **6_LangChain_미들웨어중첩사용** | 모델/도구 미들웨어 중첩 적용 실습. 호출 순서(before_model → model → after_model) 흐름 분석. | Middleware Chaining |
| 7 | **7_LangChain_출력형식제어(툴)** | `ToolStrategy`로 구조적 출력 강제(JSON Schema 기반). 툴 호출로 응답 포맷 일치. | ToolStrategy, Structured Output |
| 8 | **8_LangChain_출력형식제어(모델)** | `ProviderStrategy`로 구조적 출력 강제. `str_output_parser` 대비 장단점 비교. | ProviderStrategy, OutputParser 비교 |
| 9 | **9_LangChain_스트리밍** | `stream_mode` 옵션(messages, custom, updates 등) 차이 실습. 실시간 토큰 스트림 처리. | Streaming Mode, Callback |
| 10 | **10_LangChain_에이전트미들웨어** | `AgentMiddleware` 훅(before/after_model, before/after_tool)으로 LLM-Tool 루프 제어. | AgentState, AgentMiddleware |
| 11 | **11_LangChain_미들웨어총정리** | Built-in 미들웨어(`SummarizationMiddleware`, `HumanInTheLoopMiddleware`, `PIIMiddleware`) 개념과 활용 정리. | Built-in Middleware |
| 12 | **12_LangChain_가드레일** | 입력/출력 안전성 확보를 위한 가드레일 전략과 적용 방식 정리. | Guardrails, Safety |
| 13 | **13_LangChain_런타임** | 런타임 설정과 실행 환경 구성 방식 정리. | Runtime Configuration |
| 14 | **14_LangChain_컨텍스트엔지니어링** | 컨텍스트 설계, 압축, 메모리 전략 정리. | Context Engineering |
| 15 | **15_LangChain_MCP** | MCP 기반 연동 개념 및 LangChain 어댑터 활용 방식. | MCP, Adapters |
| 16 | **16_LangChain_다중에이전트** | 다중 에이전트 협업 구조와 라우팅 패턴 정리. | Multi-Agent Systems |

### LangGraph
| No | 파일명 | 주요 학습 내용 | 핵심 개념 |
|----|---------|----------------|------------|
| 1 | **1_LangGraph_기본사용** | LangGraph 기본 구성과 노드 연결 방식. | Graph Basics |
| 2 | **2_LangGraph_리액트구조** | LangGraph 기반 ReAct 노드 설계 및 실행 흐름. | ReAct Pattern |
| 3 | **3_LangGraph_에이전트설계** | 상태 기반 에이전트 설계와 분기 처리 실습. | Agent Design |

## 빠른 시작
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

노트북은 `LangChain/`, `LangGraph/` 폴더에서 열어 실행하면 됩니다.

## 참고 자료
- LangChain docs: https://docs.langchain.com/oss/python/langchain/overview
