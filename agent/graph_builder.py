# agent/graph_builder.py

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from agent.state import AgentState

from agent.routers import (
    router_node,
    retrieval_router
)

from agent.nodes import (
    retrieval_node,
    sentiment_node,
    statistics_node,
    reasoning_node,
    out_of_scope_node
)


def build_graph(
    llm,
    retrieve_reviews,
    analyze_sentiment,
    review_statistics
):

    graph = StateGraph(
        AgentState
    )

    # wrapper supaya dependency bisa masuk

    graph.add_node(
        "retrieval",
        lambda state: retrieval_node(
            state,
            retrieve_reviews
        )
    )

    graph.add_node(
        "sentiment",
        lambda state: sentiment_node(
            state,
            analyze_sentiment
        )
    )

    graph.add_node(
        "statistics",
        lambda state: statistics_node(
            state,
            review_statistics
        )
    )

    graph.add_node(
        "reasoning",
        lambda state: reasoning_node(
            state,
            llm
        )
    )

    graph.add_node(
        "out_of_scope",
        out_of_scope_node
    )

    graph.add_conditional_edges(
        START,
        lambda state: router_node(
            state,
            llm
        ),
        {
            "retrieval": "retrieval",
            "out_of_scope": "out_of_scope"
        }
    )

    graph.add_conditional_edges(
        "retrieval",
        retrieval_router,
        {
            "sentiment": "sentiment",
            "statistics": "statistics",
            "reasoning": "reasoning"
        }
    )

    graph.add_edge(
        "sentiment",
        "reasoning"
    )

    graph.add_edge(
        "statistics",
        "reasoning"
    )

    graph.add_edge(
        "reasoning",
        END
    )

    graph.add_edge(
        "out_of_scope",
        END
    )

    app = graph.compile()

    return app