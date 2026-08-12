from dataclasses import dataclass, field
from enum import Enum


class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class PlanStep:
    name: str

    depends_on: list[str] = field(
        default_factory=list
    )

    status: StepStatus = StepStatus.PENDING