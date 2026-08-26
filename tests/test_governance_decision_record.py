from governance_decision_service import (
    create_governance_decision_record,
)


class FakeAIAdvice:
    executive_summary = (
        "Unknown license requires manual review."
    )
    legal_review_recommended = True


def test_governance_decision_record_for_unknown_license():
    finding = {
        "File": "example/LICENSE",
        "SPDX": "UNKNOWN",
        "Risk": "Unknown Risk",
        "Policy Decision": "Manual Review",
    }

    record = create_governance_decision_record(
        run_id="test-run-123",
        finding=finding,
        ai_advice=FakeAIAdvice(),
        retrieved_context=None,
        ai_provider="OpenAI",
        ai_model="test-model",
    )

    assert record.run_id == "test-run-123"
    assert record.finding == "example/LICENSE"

    assert "UNKNOWN" in (
        record.deterministic_evidence
    )

    assert record.uncertainty is not None
    assert record.human_review_required is True
    assert record.final_decision is None

    assert record.decision_id
    assert record.timestamp