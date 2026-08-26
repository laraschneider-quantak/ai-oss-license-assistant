from dataclasses import dataclass, field
from uuid import uuid4

from models.governance_decision_record import (
    GovernanceDecisionRecord,
)

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

    governance_decision_records: list[
        GovernanceDecisionRecord
    ] = field(
        default_factory=list
    )