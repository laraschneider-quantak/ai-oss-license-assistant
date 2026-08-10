from agent import AGENT
from workflow_runner import run_workflow


def route_request(
    user_request: str,
) -> str:
    """
    Decide whether a request should use
    the deterministic workflow or the agent.
    """

    request = user_request.lower()

    workflow_keywords = [
        "scan",
        "generate spdx",
        "spdx report",
        "compliance advice",
    ]

    if any(
        keyword in request
        for keyword in workflow_keywords
    ):
        return "workflow"

    return "agent"


def handle_request(
    user_request: str,
    repo_path: str | None = None,
    repo_name: str | None = None,
):
    """
    Route and execute a user request.
    """

    route = route_request(
        user_request
    )

    print(
        ">>> ROUTER:",
        route,
    )

    if route == "workflow":
        if not repo_path or not repo_name:
            raise ValueError(
                "Workflow requests require repo_path and repo_name."
            )

        return run_workflow(
            user_request=user_request,
            repo_path=repo_path,
            repo_name=repo_name,
        )

    config = {
        "configurable": {
            "thread_id": "router-agent",
        }
    }

    return AGENT.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_request,
                }
            ]
        },
        config=config,
    )