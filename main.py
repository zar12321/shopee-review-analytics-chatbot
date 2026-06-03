from getpass import getpass

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

# config
from config.llm import load_llm

# rag
from rag.embeddings import load_embedding_model
from rag.vectorstore import load_vectorstore
from rag.retriever import create_retriever

# tools
from agent.tools import create_tools

# graph
from agent.graph_builder import build_graph


def main():

    print("=" * 50)
    print("Shopee Review Analysis Agent")
    print("=" * 50)

    api_key = getpass(
        "Masukkan API Key Gemini: "
    )

    # LLM
    llm = load_llm(api_key)

    # RAG
    embedding_model = load_embedding_model()

    vectorstore = load_vectorstore(
        embedding_model
    )

    retriever = create_retriever(
        vectorstore
    )

    # Tools
    tools = create_tools(
        retriever,
        llm
    )

    # Graph
    app = build_graph(
        llm=llm,
        retrieve_reviews=tools["retrieve_reviews"],
        analyze_sentiment=tools["analyze_sentiment"],
        review_statistics=tools["review_statistics"]
    )

    conversation_history = []

    while True:

        user_input = input(
            "\nUser: "
        )

        if user_input.lower() in [
            "exit",
            "keluar"
        ]:
            print(
                "\nTerima kasih telah menggunakan Shopee Review Analysis Agent."
            )
            break

        conversation_history.append(
            HumanMessage(
                content=user_input
            )
        )

        result = app.invoke(
            {
                "messages": conversation_history
            }
        )

        answer = result[
            "final_answer"
        ]

        conversation_history.append(
            AIMessage(
                content=answer
            )
        )

        print(
            f"\nShopee Assistant: {answer}"
        )


if __name__ == "__main__":
    main()