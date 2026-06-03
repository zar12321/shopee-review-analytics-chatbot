from langchain_google_genai import GoogleGenerativeAI

def load_llm(api_key, model):
    llm = GoogleGenerativeAI(
        model = model, 
        api_key = api_key
    )
    return llm 