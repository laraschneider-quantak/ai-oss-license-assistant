from policy_loader import load_license_policy

from policy_loader import load_license_policy


LICENSE_POLICY = load_license_policy(
    "config/policies/license_policy.json"
)


def get_risk_level(
        license_name,
    ):
        policy = LICENSE_POLICY.get(
            license_name,
            LICENSE_POLICY["Unknown"],
        )

        return policy["risk"]


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


def get_policy_decision(
    license_name,
):
    policy = LICENSE_POLICY.get(
        license_name,
        LICENSE_POLICY["Unknown"],
    )

    return policy["decision"]