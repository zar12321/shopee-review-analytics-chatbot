# agent/nodes.py

from agent.state import AgentState


def retrieval_node(
    state: AgentState,
    retrieve_reviews
):
    
    recent_message = state["messages"][-5:]
    question = "\n".join(
        [
            # misal, iterasi 1 -> msg = HumanMessage("Halo")
            # msg.__class__.__name__ adalah HumanMessafe
            # msg.content adalah "Halo"
            f"{msg.__class__.__name__}: {msg.content}"
            for msg in recent_message
        ]
    ).lower()

    retrieved_docs = retrieve_reviews.invoke(
        question
    )

    task_type = "reasoning"

    if any(
        word in question
        for word in [
            "sentimen",
            "sentiment",
            "positif",
            "negatif"
        ]
    ):
        task_type = "sentiment"

    elif any(
        word in question
        for word in [
            "statistik",
            "jumlah review",
            "rating rata-rata",
            "average rating",
            "distribusi rating"
        ]
    ):
        task_type = "statistics"

    return {
        "retrieved_docs": retrieved_docs,
        "task_type": task_type
    }


def sentiment_node(
    state: AgentState,
    analyze_sentiment
):

    docs = state["retrieved_docs"]

    sentiment = analyze_sentiment.invoke(
        docs
    )

    return {
        "sentiment_result": sentiment
    }


def statistics_node(
    state: AgentState,
    review_statistics
):

    stats = review_statistics.invoke({})

    return {
        "statistics_result": stats
    }


def reasoning_node(
    state: AgentState,
    llm
):
    
    recent_message = state["messages"][-5:]
    question = "\n".join(
        [
            f"{msg.__class__.__name__}:{msg.content}"
            for msg in recent_message
        ]
    ).lower()

    docs = state.get(
        "retrieved_docs",
        ""
    )

    sentiment = state.get(
        "sentiment_result",
        ""
    )

    stats = state.get(
        "statistics_result",
        ""
    )

    prompt = f"""
        Anda adalah analis review Shopee yang mengambil sumber review dari Google Play Store.

        Riwayat Percakapan:
        {question}

        Review yang ditemukan:
        {docs}

        Hasil Analisis Sentimen:
        {sentiment}

        Statistik Review:
        {stats}

        Instruksi:
        1. Analisis seluruh review yang ditemukan.
        2. Cari pola yang berulang.
        3. Identifikasi masalah utama.
        4. Berikan ringkasan yang mudah dipahami.
        5. Gunakan beberapa review sebagai dasar analisis.
        6. Jangan mengarang informasi di luar review yang tersedia.
        7. Jawab menggunakan bahasa yang sama dengan pengguna.

        Jawaban:
        """

    response = llm.invoke(prompt)

    if hasattr(response, "content"):
        answer = response.content
    else:
        answer = str(response)

    return {
        "final_answer": answer
    }


def out_of_scope_node(
    state: AgentState
):

    return {
        "final_answer": (
            "Maaf, saya hanya dapat menjawab pertanyaan "
            "yang berkaitan dengan review pengguna aplikasi "
            "Shopee di Google Play Store."
        )
    }