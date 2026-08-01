from prompts.prompt_registry import PROMPTS


def test_compliance_prompt_v1_exists():
    assert "compliance" in PROMPTS
    assert "v1" in PROMPTS["compliance"]