from langchain_core.output_parsers import (
    PydanticOutputParser
)

from schemas.ai_advice_schema import (
    AIComplianceAdvice
)


AI_OUTPUT_PARSER = PydanticOutputParser(
    pydantic_object=AIComplianceAdvice
)