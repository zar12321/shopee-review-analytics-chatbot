import pandas as pd 

def create_document():
    from data_pipeline.database import get_connection
    
    conn = get_connection()
    cursor = conn.cursor()

    df_db = pd.read_sql(
        "select * from shopee_reviews",
        conn
    )
    df_db.head()

    from langchain_core.documents import Document

    # dokumen adalah format standar langchain untuk menyimpan teks dan metadata
    documents = []

    # for untuk mengiterasi setiap baris pada dataframe df_db
    # _ sebenarnya sama saja dengan "index"
    # iterrows untuk mengembalikan index dan row untuk setiap baris
    for _, row in df_db.iterrows():
        doc = Document(
            page_content = row["review_text"],
            metadata = {
                "review_id": row["review_id"],
                "username": row["username"],
                "rating": int(row["rating"]),
                "review_date": str(row["review_date"]),
                "reply_text": row["reply_text"] if pd.notna(row["reply_text"]) else None,
                "reply_date": str(row["reply_date"] if pd.notna(row["reply_date"]) else None)
            }
        )
        documents.append(doc)
    cursor.close()
    conn.close()

    return documents