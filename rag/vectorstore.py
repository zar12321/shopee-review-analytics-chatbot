from langchain_community.vectorstores import FAISS

def create_vector(
        documents, 
        embedding_model
):
    """
    Membuat FAISS vector database 
    lalu menyimpannya ke folder lokal
    """

    vectorstore = FAISS.from_documents(
        documents, 
        embedding_model
    )

    vectorstore.save_local(
        "shopee_faiss_index"
    )

    print("FAISS berhasil dibuat dan disimpan")

    return vectorstore


def load_vectorstore(
        embedding_model
):
    """
    Memuat FAISS yang sudah pernah disimpan 
    """

    vectorstore = FAISS.load_local(
        "shopee_faiss_index", 
        embedding_model, 
        allow_dangerous_deserialization=True
    )

    print("FAISS berhasil diload")

    return vectorstore