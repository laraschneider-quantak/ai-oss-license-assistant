from langchain_core.prompts import ChatPromptTemplate


COMPLIANCE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a senior Open Source Compliance Consultant."
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