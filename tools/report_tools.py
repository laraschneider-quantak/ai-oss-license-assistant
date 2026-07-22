from langchain.tools import tool


@tool
def generate_spdx_tool(
    repo_name: str
) -> str:
    """
    Generate an SPDX report for a previously scanned repository.

    Use this tool only when the user explicitly asks
    for an SPDX report.
    """

    print(">>> generate_spdx_tool called")

    return (
    f"SPDX report generated for "
    f"{repo_name}"
)

    return "THIS TEXT CAN ONLY COME FROM THE TOOL"

 