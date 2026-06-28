from dashboard import calculate_compliance_score


def test_compliance_score_perfect():

    scan_results = [
        {
            "Risk": "Low Risk",
            "Policy Decision": "Approved"
        }
    ]

    assert (
        calculate_compliance_score(scan_results)
        == 100
    )

def test_compliance_score_high_risk():

    scan_results = [
        {
            "Risk": "High Risk",
            "Policy Decision": "Approved"
        }
    ]

    assert (
        calculate_compliance_score(scan_results)
        == 75
    )

def test_compliance_score_review_required():

    scan_results = [
        {
            "Risk": "Low Risk",
            "Policy Decision": "Review Required"
        }
    ]

    assert (
        calculate_compliance_score(scan_results)
        == 90
    )

def test_compliance_score_high_risk_and_review():

    scan_results = [
        {
            "Risk": "High Risk",
            "Policy Decision": "Review Required"
        }
    ]

    assert (
        calculate_compliance_score(scan_results)
        == 65
    )