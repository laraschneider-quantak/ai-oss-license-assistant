def create_plan(
    user_request: str,
) -> list[str]:
    """
    Create a simple execution plan
    from the user's request.
    """

    request = user_request.lower()

    plan = []

    if "scan" in request:
        plan.append(
            "scan_repository"
        )

    if (
        "generate spdx" in request
        or "spdx report" in request
    ):
        plan.append(
            "generate_spdx"
        )

    if any(
        phrase in request
        for phrase in [
            "compliance advice",
            "compliance assessment",
            "risk advice",
        ]
    ):
        plan.append(
            "generate_ai_advice"
        )

    return plan