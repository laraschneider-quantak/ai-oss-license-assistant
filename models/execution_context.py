from dataclasses import dataclass


@dataclass
class ExecutionContext:
    """
    Shared execution context for workflow execution.
    """

    repo_path: str

    repo_name: str

    scan_result: dict | None = None

    spdx_result: str | None = None

    ai_advice: object | None = None