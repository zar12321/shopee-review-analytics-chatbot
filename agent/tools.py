from langchain.tools import tool
from data_pipeline.database import get_connection


def create_tools(
    retriever,
    llm
):

    @tool
    def retrieve_reviews(question: str):
        """
        Retrieve Shopee reviews dari FAISS
        """

        docs = retriever.invoke(question)

        results = []

        for doc in docs:

            results.append(
                f"""
                Review ID: {doc.metadata.get("review_id")}
                Rating: {doc.metadata.get("rating")}
                Review: {doc.page_content}
                Review Date: {doc.metadata.get("review_date")}
                Reply: {doc.metadata.get("reply_text") if doc.metadata.get("reply_text") else "Tidak ada balasan"}
                Reply Date: {doc.metadata.get("reply_date") if doc.metadata.get("reply_date") else "Tidak ada tanggal balasan"}
                """
            )

        return "\n\n".join(results)

    @tool
    def analyze_sentiment(review: str):
        """
        Analyze sentiment of review.
        """

        prompt = f"""
                Analyze the sentiment.

                Categories:
                - Positive
                - Neutral
                - Negative

                Review:
                {review}
                """

        response = llm.invoke(prompt)

        return response

    @tool
    def review_statistics():
        """
        Generate statistics of reviews in database.
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) AS total_reviews,
                AVG(rating) AS avg_rating,
                COUNT(*) FILTER (WHERE rating = 1) AS rating_1,
                COUNT(*) FILTER (WHERE rating = 2) AS rating_2,
                COUNT(*) FILTER (WHERE rating = 3) AS rating_3,
                COUNT(*) FILTER (WHERE rating = 4) AS rating_4,
                COUNT(*) FILTER (WHERE rating = 5) AS rating_5
            FROM shopee_reviews
        """)

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return {
            "total_reviews": result[0],
            "avg_rating": float(result[1]) if result[1] else 0,
            "rating_1": result[2],
            "rating_2": result[3],
            "rating_3": result[4],
            "rating_4": result[5],
            "rating_5": result[6]
        }

    return {
        "retrieve_reviews": retrieve_reviews,
        "analyze_sentiment": analyze_sentiment,
        "review_statistics": review_statistics
    }