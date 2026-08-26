from ai_advisor import generate_compliance_advice
from scanner_service import run_repository_scan
from spdx_service import generate_spdx_report
from config import AI_MODEL

from models.execution_context import (
    ExecutionContext,
)

from models.plan_step import (
    PlanStep,
    StepStatus,
)

from audit_logger import (
    log_workflow_event,
)

from governance_decision_service import (
    create_governance_decision_records,
)

STEP_HANDLERS = {
    "scan_repository": run_repository_scan,
    "generate_spdx": generate_spdx_report,
    "generate_ai_advice": generate_compliance_advice,
}


def create_execution_context(
    repo_path: str,
    repo_name: str,
) -> ExecutionContext:
    """
    Create the shared execution context.
    """

    return ExecutionContext(
        repo_path=repo_path,
        repo_name=repo_name,
    )


def execute_plan(
    plan: list[PlanStep],
    context: ExecutionContext,
) -> ExecutionContext:
    """
    Execute a generated plan step by step.
    """

    completed_steps = set()

    for index, step in enumerate(
        plan,
        start=1,
    ):
        print(
            f">>> EXECUTOR: Step {index}: {step.name}"
        )

        missing_dependencies = [
            dependency
            for dependency in step.depends_on
            if dependency not in completed_steps
        ]

        if missing_dependencies:
            raise RuntimeError(
                f"Cannot execute '{step.name}'. "
                f"Missing dependencies: "
                f"{missing_dependencies}"
            )

        step.status = StepStatus.RUNNING

        log_workflow_event(
            {
                "run_id": context.run_id,
                "event_type": "step_started",
                "repo_name": context.repo_name,
                "step_name": step.name,
                "status": step.status.value,
            }
        )

        print(
            f">>> EXECUTOR: {step.name} status: "
            f"{step.status.value}"
        )

        try:
            if step.name == "scan_repository":
                context.scan_result = run_repository_scan(
                    repo_path=context.repo_path,
                    repo_name=context.repo_name,
                )

              
            elif step.name == "generate_spdx":
                context.spdx_result = generate_spdx_report(
                    repo_name=context.repo_name,
                    scan_results=context.scan_result[
                        "scan_results"
                    ],
                )

            elif step.name == "generate_ai_advice":
                context.ai_advice = generate_compliance_advice(
                    scan_results=context.scan_result[
                        "scan_results"
                    ]
                )

                context.governance_decision_records = (
                    create_governance_decision_records(
                        run_id=context.run_id,
                        scan_results=context.scan_result[
                            "scan_results"
                        ],
                        ai_advice=context.ai_advice,
                        retrieved_context=None,
                        ai_provider="OpenAI",
                        ai_model=AI_MODEL,
                    )
                )

            else:
                raise ValueError(
                    f"Unknown plan step: {step.name}"
                )

        except Exception:
            step.status = StepStatus.FAILED

            log_workflow_event(
                {
                    "run_id": context.run_id,
                    "event_type": "step_failed",
                    "repo_name": context.repo_name,
                    "step_name": step.name,
                    "status": step.status.value,
                }
            )

            print(
                f">>> EXECUTOR: {step.name} status: "
                f"{step.status.value}"
            )

            raise

        step.status = StepStatus.COMPLETED

        log_workflow_event(
            {
                "run_id": context.run_id,
                "event_type": "step_completed",
                "repo_name": context.repo_name,
                "step_name": step.name,
                "status": step.status.value,
            }
        )

        print(
            f">>> EXECUTOR: {step.name} status: "
            f"{step.status.value}"
        )

        completed_steps.add(
            step.name
        )

    return context