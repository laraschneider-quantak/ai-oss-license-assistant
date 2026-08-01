from spdx_export import (
    generate_spdx_report as generate_spdx_json,
)


def generate_spdx_report(
    repo_name: str,
    scan_results: list[dict],
) -> str:
    """
    Generate an SPDX 2.3 JSON report from repository scan data.
    """

    return generate_spdx_json(
        repo_name=repo_name,
        scan_results=scan_results,
    )