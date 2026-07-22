from tools.repository_tools import scan_repository_tool
from tools.report_tools import generate_spdx_tool


def run_compliance_workflow(
    repo_path: str,
    repo_name: str,
) -> dict:
    """
    Run the repository scan first and generate an SPDX report afterwards.
    """

    print(">>> WORKFLOW: starting repository scan")

    scan_result = scan_repository_tool.invoke(
        {
            "repo_path": repo_path,
            "repo_name": repo_name,
        }
    )

    print(">>> WORKFLOW: repository scan finished")
    print(">>> WORKFLOW: starting SPDX generation")

    spdx_result = generate_spdx_tool.invoke(
        {
            "repo_name": repo_name,
        }
    )

    print(">>> WORKFLOW: SPDX generation finished")

    return {
        "scan_result": scan_result,
        "spdx_result": spdx_result,
    }


if __name__ == "__main__":
    result = run_compliance_workflow(
        repo_path="external_repos/requests",
        repo_name="requests",
    )

    print("\nWORKFLOW RESULT:")
    print(result)