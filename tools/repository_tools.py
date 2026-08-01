from langchain.tools import tool

from scanner_service import run_repository_scan

@tool
def scan_repository_tool(
    repo_path: str,
    repo_name: str
) -> str:
    """
    Scan a local Open Source repository for license files.

    Use this tool when the user asks to scan, inspect, or analyze
    a repository for Open Source license compliance.

    The repo_path must point to an existing local repository.
    """

    print(">>> scan_repository_tool called")

    scan_result = run_repository_scan(
        repo_path=repo_path,
        repo_name=repo_name,
    )

    return scan_result