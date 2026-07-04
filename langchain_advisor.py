from prompts.prompt_registry import (
    PROMPTS,
    DEFAULT_PROMPT_VERSION
)

from langchain_openai import ChatOpenAI

from config import (
    OPENAI_API_KEY,
    AI_MODEL
)

from config import AI_PROMPT_VERSION

LLM = ChatOpenAI(
    model=AI_MODEL,
    api_key=OPENAI_API_KEY
)

if AI_PROMPT_VERSION not in PROMPTS["compliance"]:
    raise ValueError(
        f"Unsupported prompt version: {AI_PROMPT_VERSION}"
    )

CHAIN = (
    PROMPTS["compliance"][AI_PROMPT_VERSION]
    | LLM
)

def generate_langchain_compliance_advice(
    scan_results
):
    """
    Generate compliance advice using LangChain.
    """

    response = CHAIN.invoke(
        {
            "scan_results": scan_results
        }
    )

    return response.content


