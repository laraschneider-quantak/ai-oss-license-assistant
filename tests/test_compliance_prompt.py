from prompts.compliance_prompt import (
    COMPLIANCE_PROMPT
)


def test_prompt_exists():
    assert COMPLIANCE_PROMPT is not None


def test_prompt_contains_messages():
    messages = COMPLIANCE_PROMPT.messages

    assert len(messages) == 2

def test_prompt_contains_important_rules():
    prompt_text = str(COMPLIANCE_PROMPT)

    assert "Do not invent licenses" in prompt_text
    assert "Do not provide legal advice" in prompt_text
    assert "Use only the provided scan results" in prompt_text