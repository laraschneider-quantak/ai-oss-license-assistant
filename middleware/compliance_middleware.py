from langchain.agents.middleware import before_agent
from langchain.messages import AIMessage

from schemas.agent_state import ComplianceAgentState


@before_agent(
    state_schema=ComplianceAgentState,
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