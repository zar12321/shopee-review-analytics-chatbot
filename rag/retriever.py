def create_retriever(vectorstore):
    retriever = vectorstore.as_retriever(
        search_type = 'mmr', 
        search_kwargs = {
            'k': 50, 
            'fetch_k': 100, 
            'lambda_mult': 0.5
        }
    )

    return retriever