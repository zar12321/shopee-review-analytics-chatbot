# agent/routers.py

from typing import Literal
from agent.state import AgentState


def router_node(
    state: AgentState,
    llm
) -> Literal[
    "retrieval",
    "out_of_scope"
]:

    question = state["messages"][-1].content

    prompt = f"""
        Anda adalah classifier.

        Tentukan apakah pertanyaan berikut masih dapat dijawab
        menggunakan data review aplikasi Shopee di Google Play Store.

        Contoh REVIEW:
        - Apa keluhan yang paling sering muncul?
        - Bagaimana distribusi rating?
        - Apa sentimen pengguna terhadap ShopeeFood?
        - Masalah voucher apa yang sering terjadi?
        - Apakah banyak pengguna mengeluhkan kurir?

        Contoh OUT_OF_SCOPE:
        - Siapa presiden Indonesia?
        - Buatkan kode Python sorting.
        - Jelaskan machine learning.
        - Berapa luas Indonesia?

        Jawab hanya:

        REVIEW

        atau

        OUT_OF_SCOPE

        Pertanyaan:
        {question}
        """

    try:
        response = llm.invoke(prompt)
    except Exception as e:
        print("ROUTER ERROR =", repr(e))
        raise
    
    response = str(response).upper()

    if "REVIEW" in response:
        return "retrieval"

    return "out_of_scope"


def retrieval_router(
    state: AgentState
) -> Literal[
    "sentiment",
    "statistics",
    "reasoning"
]:

    task = state["task_type"]

    if task == "sentiment":
        return "sentiment"

    if task == "statistics":
        return "statistics"

    return "reasoning"