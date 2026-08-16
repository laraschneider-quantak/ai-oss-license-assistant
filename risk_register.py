from models.risk_item import RiskItem


def create_risk_items(
    run_id: str,
    repo_name: str,
    scan_results: list[dict],
) -> list[RiskItem]:
    """
    Create structured risk items
    from repository scan results.
    """

    risk_items = []

    for result in scan_results:
        if result["Policy Decision"] == "Approved":
            continue

        risk_item = RiskItem(
            run_id=run_id,
            repo_name=repo_name,
            source=result["File"],
            risk_level=result["Risk"],
            policy_decision=result["Policy Decision"],
        )

        risk_items.append(
            risk_item
        )

    return risk_items