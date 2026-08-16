from dataclasses import dataclass, field
from uuid import uuid4
from models.risk_item import RiskItem


@dataclass
class ExecutionContext:
    """
    Shared execution context for workflow execution.
    """

    repo_path: str
    repo_name: str

    run_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    scan_result: dict | None = None
    spdx_result: str | None = None
    ai_advice: object | None = None

    risk_items: list[RiskItem] = field(
        default_factory=list
    )