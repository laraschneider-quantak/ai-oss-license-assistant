from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command

from scanner_service import run_repository_scan

@tool
def scan_repository_tool(
    repo_path: str,
    repo_name: str,
    runtime: ToolRuntime,
) -> Command:
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

    return Command(
        update={
            "repo_path": repo_path,
            "repo_name": repo_name,
            "scan_result": scan_result,
            "messages": [
                ToolMessage(
                    content=str(scan_result),
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )