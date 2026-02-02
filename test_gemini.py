from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

env_path = os.path.join("scripts", ".env")
load_dotenv(env_path)

models_to_try = ["gemini-pro", "gemini-1.0-pro", "gemini-1.5-flash-latest", "gemini-1.5-pro-latest"]

for model_name in models_to_try:
    print(f"\n--- Trying model: {model_name} ---")
    llm = ChatGoogleGenerativeAI(model=model_name)
    try:
        res = llm.invoke("Qual seu nome?")
        print(f"Success with {model_name}!")
        print(res.content)
        break
    except Exception as e:
        print(f"Failed with {model_name}: {e}")
