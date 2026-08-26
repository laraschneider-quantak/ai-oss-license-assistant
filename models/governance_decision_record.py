from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class GovernanceDecisionRecord:
    """
    Auditable record of an AI-assisted
    governance decision.
    """

    run_id: str
    finding: str
    deterministic_evidence: str
    retrieved_context: str | None

    ai_provider: str
    ai_model: str
    ai_recommendation: str

    uncertainty: str | None
    human_review_required: bool

    final_decision: str | None = None

    decision_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    timestamp: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )