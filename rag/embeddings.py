from langchain_community.embeddings import HuggingFaceBgeEmbeddings

def load_embedding_model():
    embedding_model = HuggingFaceBgeEmbeddings(
        model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    return embedding_model