import google.generativeai as genai
import os
from dotenv import load_dotenv

env_path = os.path.join("scripts", ".env")
load_dotenv(env_path)
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("No API key found in .env")
else:
    genai.configure(api_key=api_key)
    try:
        models = genai.list_models()
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")
