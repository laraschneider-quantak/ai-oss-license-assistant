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

from parsers.output_parser import AI_OUTPUT_PARSER

from rag_retriever import retrieve_knowledge_for_scan

from schemas.ai_advice_schema import AIComplianceAdvice

from audit_logger import log_rag_retrieval

LLM = ChatOpenAI(
    model=AI_MODEL,
    api_key=OPENAI_API_KEY
)

if AI_PROMPT_VERSION not in PROMPTS["compliance"]:
    raise ValueError(
        f"Unsupported prompt version: {AI_PROMPT_VERSION}"
    )

# Data flow:
# input variables -> prompt -> LLM response -> AIComplianceAdvice object
CHAIN = (
    PROMPTS["compliance"][AI_PROMPT_VERSION]
    | LLM
    | AI_OUTPUT_PARSER
)

def generate_langchain_compliance_advice(
        scan_results: list[dict]
    ) -> AIComplianceAdvice:
    
  
    """
    Generate compliance advice using LangChain.
    """
    knowledge_context, retrieval_strategy = (
        retrieve_knowledge_for_scan(
            scan_results
        )
    )

    log_rag_retrieval(
        strategy=retrieval_strategy,
        knowledge_retrieved=bool(knowledge_context)
    )

    response = CHAIN.invoke(
    {
        "scan_results": scan_results,
        "knowledge_context": knowledge_context,
        "format_instructions": (
            AI_OUTPUT_PARSER.get_format_instructions()
        )
    }
    )

    print(
        "LANGCHAIN RESPONSE TYPE:",
        type(response).__name__
    )

    print(
        "LANGCHAIN RESPONSE:",
        response
    )

    return response
        


