import os
from openai import OpenAI
import requests

# Set your key in the environment before running:
#   export GEMINI_API_KEY="your_key_here"
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

models = ["gemini-pro", "gemini-1.5-flash-latest", "gemini-1.5-flash-001", "gemini-1.5-flash-002", "gemini-1.0-pro"]

for m in models:
    try:
        response = client.chat.completions.create(
            model=m,
            messages=[{"role": "user", "content": "Hello"}]
        )
        print(f"SUCCESS with {m}")
    except Exception as e:
        print(f"ERROR with {m}: {e}")

# Try to list models using REST
try:
    res = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}")
    print("\nModels available via REST:")
    data = res.json()
    for model in data.get('models', []):
        if 'generateContent' in model.get('supportedGenerationMethods', []):
            print(model['name'])
except Exception as e:
    print(f"REST ERROR: {e}")
