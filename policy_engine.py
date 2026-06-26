


def get_risk_level(license_name):
    risk_map = {
        "MIT": "Low Risk",
        "Apache": "Low Risk",
        "BSD": "Low Risk",
        "MPL": "Medium Risk",
        "EPL": "Medium Risk",
        "CDDL": "Medium Risk",
        "LGPL": "Medium Risk",
        "GPL": "High Risk",
        "AGPL": "Very High Risk"
    }
    
    return risk_map.get(
        license_name,
        "Unknown Risk"
    )


def get_spdx_id(license_name):
    spdx_map = {
        "MIT": "MIT",
        "Apache": "Apache-2.0",
        "BSD": "BSD-3-Clause",
        "MPL": "MPL-2.0",
        "LGPL": "LGPL-2.1-only",
        "GPL": "GPL-3.0-only",
        "AGPL": "AGPL-3.0-only",
        "EPL": "EPL-2.0",
        "CDDL": "CDDL-1.0"
    }

    return spdx_map.get(
            license_name,
            "UNKNOWN"
        )


def get_policy_decision(license_name):
    policy_map = {
        "MIT": "Approved",
        "Apache": "Approved",
        "BSD": "Approved",
        "MPL": "Review Required",
        "EPL": "Review Required",
        "CDDL": "Review Required",
        "LGPL": "Review Required",
        "GPL": "Legal Review Required",
        "AGPL": "Blocked / High Review",
        "Unknown": "Manual Review"
    }

    return policy_map.get(
        license_name,
        "Manual Review"
    )
