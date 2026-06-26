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