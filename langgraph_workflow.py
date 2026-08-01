from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from scanner_service import run_repository_scan

from spdx_service import generate_spdx_report

from ai_advisor import generate_compliance_advice

class ComplianceState(TypedDict, total=False):
    repo_path: str
    repo_name: str
    scan_result: dict
    ai_advice: object
    spdx_result: str


def scan_repository_node(
    state: ComplianceState,
) -> dict:
    """
    Scan the repository and store the result in the graph state.
    """

    print(">>> LANGGRAPH: scan_repository_node called")

    scan_result = run_repository_scan(
        repo_path=state["repo_path"],
        repo_name=state["repo_name"],
    )

    return {
        "scan_result": scan_result,
    }


def generate_spdx_node(
    state: ComplianceState,
) -> dict:
    """
    Generate an SPDX result from the repository scan results
    and store it in the graph state.
    """

    print(">>> LANGGRAPH: generate_spdx_node called")

    scan_result = state["scan_result"]

    spdx_result = generate_spdx_report(
        repo_name=state["repo_name"],
        scan_results=scan_result["scan_results"],
    )

    return {
        "spdx_result": spdx_result,
    }

def generate_ai_advice_node(
    state: ComplianceState,
) -> dict:
    """
    Generate AI compliance advice from scan results.
    """

    print(">>> LANGGRAPH: generate_ai_advice_node called")

    scan_result = state["scan_result"]

    advice = generate_compliance_advice(
        scan_result["scan_results"]
    )

    return {
        "ai_advice": advice,
    }

def route_after_scan(
    state: ComplianceState,
) -> str:
    """
    Decide whether SPDX generation should continue.
    """

    scan_result = state["scan_result"]

    if scan_result["success"]:
        return "generate_spdx"

    return "end"


def build_compliance_graph():
    """
    Build and compile the compliance workflow.
    """

    graph_builder = StateGraph(ComplianceState)

    graph_builder.add_node(
        "scan_repository",
        scan_repository_node,
    )

    graph_builder.add_node(
        "generate_ai_advice",
        generate_ai_advice_node,
    )

    graph_builder.add_node(
        "generate_spdx",
        generate_spdx_node,
    )

    graph_builder.add_edge(
        START,
        "scan_repository",
    )

    graph_builder.add_conditional_edges(
        "scan_repository",
        route_after_scan,
        {
            "generate_spdx": "generate_ai_advice",
            "end": END,
        },
    )

    graph_builder.add_edge(
        "generate_ai_advice",
        "generate_spdx",
    )

    graph_builder.add_edge(
        "generate_spdx",
        END,
    )

    return graph_builder.compile()


if __name__ == "__main__":
    graph = build_compliance_graph()

    result = graph.invoke(
        {
            "repo_path": r"C:\AI-Projects\license_scanner\test_repo",
            "repo_name": "Test-Repo",
        }
    )

    print(result)