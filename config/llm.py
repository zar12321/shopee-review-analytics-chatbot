from langchain_google_genai import GoogleGenerativeAI

def load_llm(api_key, model_name):
    llm = GoogleGenerativeAI(
        model_name = model_name, 
        api_key = api_key
    )
    return llm 