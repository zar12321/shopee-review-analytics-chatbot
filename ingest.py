from rag.documents import create_document
from rag.embeddings import get_embedding_model

from langchain_community.vectorstores import FAISS


def ingest():

    print("=" * 50)
    print("MEMULAI PROSES INGESTION")
    print("=" * 50)

    # Ambil seluruh review dari PostgreSQL
    print("Loading documents...")

    documents = create_document()

    print(f"Total documents: {len(documents)}")

    # Load embedding model
    print("Loading embedding model...")

    embedding_model = get_embedding_model()

    # Buat FAISS index
    print("Creating FAISS index...")

    vectorstore = FAISS.from_documents(
        documents,
        embedding_model
    )

    # Simpan index
    print("Saving FAISS index...")

    vectorstore.save_local(
        "shopee_faiss_index"
    )

    print("=" * 50)
    print("INGESTION BERHASIL")
    print("=" * 50)


if __name__ == "__main__":
    ingest()