from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from config import (
    AI_MODEL,
    OPENAI_API_KEY,
)

from middleware.compliance_middleware import (
    log_agent_request,
)

from schemas.agent_state import (
    ComplianceAgentState,
)

from tools.advice_tools import (
    generate_ai_advice_tool,
)

from tools.report_tools import (
    generate_spdx_tool,
)

from tools.repository_tools import (
    scan_repository_tool,
)


LLM = ChatOpenAI(
    model=AI_MODEL,
    api_key=OPENAI_API_KEY,
)

MEMORY = InMemorySaver()

TOOLS = [
    scan_repository_tool,
    generate_ai_advice_tool,
    generate_spdx_tool,
]

AGENT = create_agent(
    model=LLM,
    tools=TOOLS,
    system_prompt=(
        "You are an OSS compliance assistant. "
        "Use available tools when they are needed. "
        "Do not claim that a repository was scanned "
        "unless a scan tool was actually called. "
        "When the user asks to scan a repository and then "
        "generate an SPDX report, you must first call "
        "scan_repository_tool and only after that call "
        "generate_spdx_tool."
    ),
    checkpointer=MEMORY,
    state_schema=ComplianceAgentState,
    middleware=[
        log_agent_request,
    ],
)