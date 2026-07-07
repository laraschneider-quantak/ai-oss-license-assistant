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

from rag_retriever import (
    build_license_query,
    retrieve_relevant_knowledge
)

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
    | AI_OUTPUT_PARSER
)

def generate_langchain_compliance_advice(
    scan_results
):
    """
    Generate compliance advice using LangChain.
    """
    
    license_query = build_license_query(
        scan_results
    )

    knowledge_context = retrieve_relevant_knowledge(
        license_query
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


    return response.model_dump_json(
        indent=2
    )

    


