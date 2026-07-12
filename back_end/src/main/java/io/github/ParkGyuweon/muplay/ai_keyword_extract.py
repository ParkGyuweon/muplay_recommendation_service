from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='C:/Users/박규원/Desktop/muplay/muplay_recommendation_service/back_end/.env')
api_key_env = os.environ.get("GOOGLE_API_KEY", "").strip()

client = genai.Client(api_key=api_key_env)
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=types.Part.from_text(text='뮤지컬 인화에 대해 설명해줘'),
    config=types.GenerateContentConfig(
        temperature=0,
        top_p=0.95,
        top_k=20,
    ),
)

print(response.text)