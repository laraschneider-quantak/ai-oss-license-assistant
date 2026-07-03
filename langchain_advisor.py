from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import ChatOpenAI

from config import (
    OPENAI_API_KEY,
    AI_MODEL
)

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a senior Open Source Compliance Consultant."
            )
        ),
        (
            "human",
            (
                "Analyze the following sanitized scan results:\n\n"
                "{scan_results}"
            )
        )
    ]
)

LLM = ChatOpenAI(
    model=AI_MODEL,
    api_key=OPENAI_API_KEY
)

CHAIN = PROMPT | LLM

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


