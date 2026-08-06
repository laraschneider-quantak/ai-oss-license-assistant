def execute_plan(
    plan: list[str],
) -> None:
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