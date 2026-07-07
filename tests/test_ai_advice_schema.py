from schemas.ai_advice_schema import AIComplianceAdvice


def test_ai_compliance_advice_schema():
    advice = AIComplianceAdvice(
        executive_summary="Test summary",
        detected_licenses=["MIT"],
        risk_assessment="Low",
        compliance_actions=[
            "Keep license notice"
        ],
        legal_review_recommended=False,
        disclaimer="Not legal advice."
    )

    assert advice.executive_summary == "Test summary"
    assert advice.detected_licenses == ["MIT"]
    assert advice.legal_review_recommended is False