from models.governance_decision_record import (
    GovernanceDecisionRecord,
)


def create_governance_decision_record(
    run_id: str,
    finding: dict,
    ai_advice,
    retrieved_context: str | None,
    ai_provider: str,
    ai_model: str,
) -> GovernanceDecisionRecord:
    """
    Create an auditable governance decision record
    from deterministic findings and AI advice.
    """

    license_id = finding.get(
        "SPDX",
        "UNKNOWN",
    )

    policy_decision = finding.get(
        "Policy Decision",
        "Manual Review",
    )

    deterministic_evidence = (
        f"File: {finding.get('File')} | "
        f"License: {license_id} | "
        f"Risk: {finding.get('Risk')} | "
        f"Policy Decision: {policy_decision}"
    )

    if license_id == "UNKNOWN":
        uncertainty = (
            "License could not be determined "
            "from deterministic scan evidence."
        )
    else:
        uncertainty = None

    return GovernanceDecisionRecord(
        run_id=run_id,
        finding=str(
            finding.get("File")
        ),
        deterministic_evidence=deterministic_evidence,
        retrieved_context=retrieved_context,
        ai_provider=ai_provider,
        ai_model=ai_model,
        ai_recommendation=(
            ai_advice.executive_summary
        ),
        uncertainty=uncertainty,
        human_review_required=(
            ai_advice.legal_review_recommended
        ),
        final_decision=None,
    )

def create_governance_decision_records(
    run_id: str,
    scan_results: list[dict],
    ai_advice,
    retrieved_context: str | None,
    ai_provider: str,
    ai_model: str,
) -> list[GovernanceDecisionRecord]:
    """
    Create governance decision records only
    for findings that require human review.
    """

    records = []

    for finding in scan_results:
        policy_decision = finding.get(
            "Policy Decision",
            "Manual Review",
        )

        if policy_decision == "Approved":
            continue

        record = create_governance_decision_record(
            run_id=run_id,
            finding=finding,
            ai_advice=ai_advice,
            retrieved_context=retrieved_context,
            ai_provider=ai_provider,
            ai_model=ai_model,
        )

        records.append(
            record
        )

    return records