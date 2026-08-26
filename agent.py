from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from config import (
    AI_MODEL,
    OPENAI_API_KEY,
)

from executor.plan_executor import (
    execute_plan,
)

from middleware.compliance_middleware import (
    log_agent_request,
)

from planner.request_planner import (
    create_plan,
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

from executor.plan_executor import (
    create_execution_context,
    execute_plan,
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


if __name__ == "__main__":
    config = {
        "configurable": {
            "thread_id": "planning-test",
        }
    }

    user_request = (
        "Scan the repository at "
        "external_repos/requests, "
        "generate an SPDX report, "
        "and provide compliance advice."
    )

    plan = create_plan(
        user_request
    )

    print("\nPLAN:")
    print(plan)

    context = create_execution_context(
        repo_path="external_repos/requests",
        repo_name="requests",
    )

    context = execute_plan(
        plan,
        context,
    )

    print("\nAI ADVICE:")
    print(
        context.ai_advice
    )

    print(
        "\nEXECUTOR SPDX RESULT:"
    )

    print(
        context.spdx_result
    )

    print("\nEXECUTION CONTEXT:")
    print(context)

    print(
        "\nSPDX RESULT:"
    )

    print(
        context.spdx_result
    )

    if __name__ == "__main__":
        user_request = (
        "Scan the repository at "
        "external_repos/requests, "
        "generate an SPDX report, "
        "and provide compliance advice."
    )

    plan = create_plan(
        user_request
    )

    print("\nPLAN:")
    print(plan)

    context = create_execution_context(
        repo_path="external_repos/requests",
        repo_name="requests",
    )

    context = execute_plan(
        plan,
        context,
    )

    print("\nEXECUTION SUMMARY:")

    print(
        "Scan successful:",
        context.scan_result["success"]
    )

    print(
        "SPDX generated:",
        context.spdx_result is not None,
    )

    print(
        "AI advice generated:",
        context.ai_advice is not None,
    )