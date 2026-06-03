from langchain_openai import ChatOpenAI

def load_llm(api_key):
    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        api_key=api_key,
        temperature=0
    )

    return llm