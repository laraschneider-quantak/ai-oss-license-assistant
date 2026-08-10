from models.plan_step import PlanStep


def create_plan(
    user_request: str,
) -> list[PlanStep]:
    """
    Create a simple execution plan
    from the user's request.
    """

    request = user_request.lower()

    plan = []

    if "scan" in request:
        plan.append(
            PlanStep(
                name="scan_repository",
            )
        )

    if (
        "generate spdx" in request
        or "spdx report" in request
    ):
        plan.append(
            PlanStep(
                name="generate_spdx",
                depends_on=[
                    "scan_repository",
                ],
            )
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
            PlanStep(
                name="generate_ai_advice",
                depends_on=[
                    "scan_repository",
                ],
            )
        )

    return plan