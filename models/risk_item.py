from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class RiskItem:
    """
    Structured governance risk identified during a workflow run.
    """

    run_id: str
    repo_name: str
    source: str
    risk_level: str
    policy_decision: str

    risk_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    status: str = "open"
    mitigation: str | None = None