from langchain.agents import AgentState


class ComplianceAgentState(AgentState):
    repo_path: str
    repo_name: str
    scan_result: dict
    highest_risk: str
    highest_policy: str
    detected_licenses: list[str]
    