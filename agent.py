from langchain_openai import ChatOpenAI

from config import (
    AI_MODEL,
    OPENAI_API_KEY,
)

from tools.repository_tools import (
    scan_repository_tool,
)

from langchain.agents import create_agent

from tools.report_tools import (
    generate_spdx_tool,
)

from tools.advice_tools import (
    generate_ai_advice_tool,
)

from langgraph.checkpoint.memory import InMemorySaver

from langchain.agents.middleware import before_agent

from schemas.agent_state import (
    ComplianceAgentState,
)

from langchain.messages import AIMessage

from middleware.compliance_middleware import (
    log_agent_request,
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

MEMORY = InMemorySaver()

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

if __name__ == "__main__":
    config = {
        "configurable": {
            "thread_id": "planning-test",
        }
    }

    result = AGENT.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Scan the repository at "
                        "external_repos/requests, "
                        "generate an SPDX report, "
                        "and provide compliance advice."
                    ),
                }
            ]
        },
        config=config,
    )

    print("\nFINAL RESPONSE:")
    print(
        result["messages"][-1].content
    )

    state_snapshot = AGENT.get_state(
        config
    )

    print("\nSTORED PLAN:")
    print(
        state_snapshot.values.get("plan")
    )