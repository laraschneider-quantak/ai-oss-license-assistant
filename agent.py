from langchain_openai import ChatOpenAI

from config import (
    AI_MODEL,
    OPENAI_API_KEY,
)

from tools.repository_tools import (
    scan_repository_tool,
)

from langchain.agents import create_agent

from tools.report_tools import (
    generate_spdx_tool,
)

from tools.advice_tools import (
    generate_ai_advice_tool,
)

from langchain_core.messages import AIMessage, ToolMessage

LLM = ChatOpenAI(
    model=AI_MODEL,
    api_key=OPENAI_API_KEY,
)

TOOLS = [
    scan_repository_tool,
    generate_ai_advice_tool,
    generate_spdx_tool,
]

AGENT = create_agent(
    model=LLM,
    tools=TOOLS,
    system_prompt=( "You are an OSS compliance assistant. "
        "Use available tools when they are needed. "
        "Do not claim that a repository was scanned "
        "unless a scan tool was actually called. "
        "When the user asks to scan a repository and then "
        "generate an SPDX report, you must first call "
        "scan_repository_tool and only after that call "
        "generate_spdx_tool."
    ),
)

if __name__ == "__main__":
    result = AGENT.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Scan the repository at "
                        "external_repos/requests "
                        "and generate an SPDX report. "
                        "Do not provide AI compliance advice."
                    ),
                }
            ]
        }
    )
    
  
    final_message = result["messages"][-1]

    print(
            "FINAL RESPONSE:"
        )
    print(
            final_message.content
        )