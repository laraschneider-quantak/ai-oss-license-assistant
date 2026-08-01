from langchain.tools import tool

from spdx_service import generate_spdx_report


@tool
def generate_spdx_tool(
    repo_name: str,
    scan_results: list[dict],
) -> str:
    """
    Generate an SPDX report for a previously scanned repository.

    Use this tool only when the user explicitly asks
    for an SPDX report.
    """

    print(">>> generate_spdx_tool called")

    return generate_spdx_report(
        repo_name=repo_name,
        scan_results=scan_results,
    )