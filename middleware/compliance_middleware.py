from langchain.agents.middleware import before_agent
from langchain.messages import AIMessage

from schemas.agent_state import ComplianceAgentState


@before_agent(
    can_jump_to=["end"],
)
def log_agent_request(
    state: ComplianceAgentState,
    runtime,
) -> dict | None:
    """
    Log incoming requests, create a simple execution plan,
    and block scan-dependent requests when no successful
    repository scan is available.
    """

    messages = state.get(
        "messages",
        [],
    )

    last_message = ""

    if messages:
        last_message = str(
            messages[-1].content
        ).lower()

    requests_scan = any(
        phrase in last_message
        for phrase in [
            "scan the repository",
            "scan repository",
            "scan the repo",
            "scan repo",
        ]
    )

    requires_scan = any(
        phrase in last_message
        for phrase in [
            "generate spdx",
            "spdx report",
            "compliance advice",
            "compliance assessment",
            "risk advice",
        ]
    )

    scan_result = state.get(
        "scan_result"
    )

    has_scan_result = bool(
        scan_result
        and scan_result.get("success")
    )

    plan = []

    if requests_scan:
        plan.append(
            "scan_repository"
        )

    if (
        "generate spdx" in last_message
        or "spdx report" in last_message
    ):
        plan.append(
            "generate_spdx"
        )

    if any(
        phrase in last_message
        for phrase in [
            "compliance advice",
            "compliance assessment",
            "risk advice",
        ]
    ):
        plan.append(
            "generate_ai_advice"
        )

    print(
        ">>> MIDDLEWARE: agent request received"
    )

    print(
        ">>> MIDDLEWARE: stored messages:",
        len(messages),
    )

    print(
        ">>> MIDDLEWARE: requires scan:",
        requires_scan,
    )

    print(
        ">>> MIDDLEWARE: requests scan:",
        requests_scan,
    )

    print(
        ">>> MIDDLEWARE: valid scan available:",
        has_scan_result,
    )

    print(
        ">>> MIDDLEWARE: plan:",
        plan,
    )

    if (
        requires_scan
        and not has_scan_result
        and not requests_scan
    ):
        return {
            "messages": [
                AIMessage(
                    content=(
                        "Please scan a repository first. "
                        "An SPDX report or compliance assessment "
                        "requires valid repository scan results."
                    )
                )
            ],
            "plan": plan,
            "jump_to": "end",
        }

    return {
        "plan": plan,
    }