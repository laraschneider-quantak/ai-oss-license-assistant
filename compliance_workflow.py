from executor.plan_executor import (
    create_execution_context,
    execute_plan,
)

from planner.request_planner import (
    create_plan,
)


def run_compliance_workflow(
    user_request: str,
    repo_path: str,
    repo_name: str,
):
    """
    Create and execute a deterministic
    OSS compliance workflow.
    """

    plan = create_plan(
        user_request
    )

    print(
        "\nPLAN:",
        plan,
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

    result = run_compliance_workflow(
        user_request=user_request,
        repo_path="external_repos/requests",
        repo_name="requests",
    )

    print(
        "RESULT TYPE:",
        type(result).__name__,
    )

    print(
        "\nEXECUTION SUMMARY:"
    )

    print(
        "Scan successful:",
        result.scan_result["success"],
    )

    print(
        "SPDX generated:",
        result.spdx_result is not None,
    )

    print(
        "AI advice generated:",
        result.ai_advice is not None,
    )

    print(
        "Governance decision records:",
        len(result.governance_decision_records),
    )

    for record in result.governance_decision_records:
        print(
            "\nDECISION RECORD:"
        )
        print(
            "Decision ID:",
            record.decision_id,
        )
        print(
            "Run ID:",
            record.run_id,
        )
        print(
            "Finding:",
            record.finding,
        )
        print(
            "Evidence:",
            record.deterministic_evidence,
        )
        print(
            "AI recommendation:",
            record.ai_recommendation,
        )
        print(
            "Uncertainty:",
            record.uncertainty,
        )
        print(
            "Human review required:",
            record.human_review_required,
        )
        print(
            "Final decision:",
            record.final_decision,
        )
        print(
            "Timestamp:",
            record.timestamp,
        )