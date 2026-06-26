import json
from datetime import datetime


def generate_spdx_report(
    repo_name,
    scan_results
):
    spdx_report = {
        "spdxVersion": "SPDX-2.3",
        "SPDXID": "SPDXRef-DOCUMENT",
        "dataLicense": "CC0-1.0",
        "name": repo_name,
        "documentNamespace":
            f"https://example.com/spdx/{repo_name}",

        "creationInfo": {
            "created": datetime.now().isoformat(),
            "creators": [
                "Tool: OSS Compliance Assistant"
            ]
        },

        "packages": []
    }

    for index, result in enumerate(
        scan_results,
        start=1
    ):
        spdx_report["packages"].append(
            {
                "SPDXID": f"SPDXRef-Package-{index}",
                "name": result["File"],
                "downloadLocation": "NOASSERTION",
                "filesAnalyzed": False,
                "licenseConcluded": result["SPDX"],
                "licenseDeclared": result["SPDX"],
                "copyrightText": "NOASSERTION"
            }
        )

    spdx_json = json.dumps(
        spdx_report,
        indent=4
    )

    return spdx_json