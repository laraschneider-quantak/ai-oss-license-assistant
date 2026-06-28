def calculate_compliance_score(
    scan_results
):
    compliance_score = 100

    high_risk_count = sum(
        1
        for result in scan_results
        if result["Risk"] in [
            "High Risk",
            "Very High Risk"
        ]
    )

    compliance_score -= high_risk_count * 25

    review_count = sum(
        1
        for result in scan_results
        if result["Policy Decision"] in [
            "Review Required",
            "Manual Review"
        ]
    )

    compliance_score -= review_count * 10

    if compliance_score < 0:
        compliance_score = 0

    return compliance_score

def calculate_overall_policy(
    scan_results
):
    policy_priority = {
        "Approved": 1,
        "Review Required": 2,
        "Manual Review": 3,
        "Legal Review Required": 4,
        "Blocked / High Review": 5
    }

    overall_policy = "Approved"

    for result in scan_results:

        current_policy = result[
            "Policy Decision"
        ]

        if (
            policy_priority[current_policy]
            >
            policy_priority[overall_policy]
        ):
            overall_policy = current_policy

    return overall_policy


def calculate_risk_summary(
    scan_results
):
    risk_summary = {}

    for result in scan_results:

        risk = result["Risk"]

        risk_summary[risk] = (
            risk_summary.get(
                risk,
                0
            ) + 1
        )

    return risk_summary

def calculate_policy_summary(
    scan_results
):
    policy_summary = {}

    for result in scan_results:

        policy = result["Policy Decision"]

        policy_summary[policy] = (
            policy_summary.get(
                policy,
                0
            ) + 1
        )

    return policy_summary


def calculate_dashboard_metrics(
    scan_results
):
    license_count = len(
        scan_results
    )

    unique_licenses = len(
        set(
            result["License"]
            for result in scan_results
        )
    )

    high_risk_count = sum(
        1
        for result in scan_results
        if result["Risk"] in [
            "High Risk",
            "Very High Risk"
        ]
    )

    approved_count = sum(
        1
        for result in scan_results
        if result["Policy Decision"] == "Approved"
    )

    return (
        license_count,
        unique_licenses,
        high_risk_count,
        approved_count
    )