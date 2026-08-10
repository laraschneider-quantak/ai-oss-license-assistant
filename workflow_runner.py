from executor.plan_executor import (
    create_execution_context,
    execute_plan,
)

from planner.request_planner import (
    create_plan,
)


def run_workflow(
    user_request: str,
    repo_path: str,
    repo_name: str,
) -> dict:
    """
    Create and execute a deterministic compliance workflow.
    """

    plan = create_plan(
        user_request
    )

    context = create_execution_context(
        repo_path=repo_path,
        repo_name=repo_name,
    )

    context = execute_plan(
        plan,
        context,
    )

    return context


if __name__ == "__main__":
    user_request = (
        "Scan the repository at "
        "external_repos/requests, "
        "generate an SPDX report, "
        "and provide compliance advice."
    )

    result = run_workflow(
        user_request=user_request,
        repo_path="external_repos/requests",
        repo_name="requests",
    )

    print("\nEXECUTION SUMMARY:")

    print(
        "Scan successful:",
        result["scan_result"]["success"],
    )

    print(
        "SPDX generated:",
        result["spdx_result"] is not None,
    )

    print(
        "AI advice generated:",
        result["ai_advice"] is not None,
    )