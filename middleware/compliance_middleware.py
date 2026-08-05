from langchain.agents.middleware import before_agent
from langchain.messages import AIMessage

@before_agent(
    can_jump_to=["end"],
)
def log_agent_request(
    state: ComplianceAgentState,
    runtime,
) -> dict | None:
    """
    Log incoming requests and block scan-dependent requests
    when no successful repository scan is available.
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
        ">>> MIDDLEWARE: valid scan available:",
        has_scan_result,
    )

    if requires_scan and not has_scan_result:
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
            "jump_to": "end",
        }

    return None