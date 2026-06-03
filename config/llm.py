from langchain_google_genai import GoogleGenerativeAI

def load_llm(api_key):
    llm = GoogleGenerativeAI(
        model = 'gemini-2.5-flash', 
        api_key = api_key
    )

    return llm 