from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from config import OPENAI_API_KEY
from logger import logger


def generate_langchain_compliance_advice(scan_results):
    """
    Generate AI compliance advice using LangChain.
    """

    try:
        model = ChatOpenAI(
            model="gpt-5",
            api_key=OPENAI_API_KEY
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a senior Open Source Compliance Consultant."
                ),
                (
                    "user",
                    """
                    Analyze the following open source license scan results.

                    Focus on:
                    - license risks
                    - policy decisions
                    - AI usage concerns
                    - recommended next steps

                    Scan results:
                    {scan_results}
                    """
                )
            ]
        )

        chain = prompt | model

        response = chain.invoke(
            {
                "scan_results": scan_results
            }
        )

        return response.content

    except Exception as error:
        logger.error(
            "LangChain compliance advice generation failed: %s",
            error
        )

        return "AI compliance advice could not be generated."