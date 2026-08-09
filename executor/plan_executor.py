from ai_advisor import generate_compliance_advice
from scanner_service import run_repository_scan
from spdx_service import generate_spdx_report


STEP_HANDLERS = {
    "scan_repository": run_repository_scan,
    "generate_spdx": generate_spdx_report,
    "generate_ai_advice": generate_compliance_advice,
}

def create_execution_context(
    repo_path: str,
    repo_name: str,
) -> dict:
    """
    Create the shared context used during plan execution.
    """

    return {
        "repo_path": repo_path,
        "repo_name": repo_name,
        "scan_result": None,
        "spdx_result": None,
        "ai_advice": None,
    }


def execute_plan(
    plan: list[str],
    context: dict,
) -> dict:
    """
    Execute a generated plan step by step.
    """

    for index, step in enumerate(
        plan,
        start=1,
    ):
        print(
            f">>> EXECUTOR: Step {index}: {step}"
        )

        if step == "scan_repository":
            context["scan_result"] = run_repository_scan(
                repo_path=context["repo_path"],
                repo_name=context["repo_name"],
            )

        elif step == "generate_spdx":
            context["spdx_result"] = generate_spdx_report(
                repo_name=context["repo_name"],
                scan_results=context["scan_result"][
                    "scan_results"
                ],
            )

        elif step == "generate_ai_advice":
            context["ai_advice"] = generate_compliance_advice(
                scan_results=context["scan_result"][
                    "scan_results"
                ]
            )
   

    return context