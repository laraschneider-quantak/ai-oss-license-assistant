import json


def load_license_policy(
    policy_path: str,
) -> dict:
    """
    Load license policy decisions from a JSON file.
    """

    with open(
        policy_path,
        "r",
        encoding="utf-8",
    ) as policy_file:
        return json.load(
            policy_file
        )