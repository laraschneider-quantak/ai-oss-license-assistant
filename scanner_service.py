from scanner import scan_repository


def run_repository_scan(
    repo_path: str,
    repo_name: str,
) -> dict:
    """
    Run a repository scan and return the scan results.
    """

    return scan_repository(
        repo_path=repo_path,
        repo_name=repo_name,
    )