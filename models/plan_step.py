from dataclasses import dataclass, field

@dataclass
class PlanStep:
    name: str
    depends_on: list[str] = field(
        default_factory=list
    )