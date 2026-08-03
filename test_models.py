import os
import requests

# Set your key in the environment before running:
#   export GEMINI_API_KEY="your_key_here"
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Check standard Google AI Studio endpoint
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
try:
    res = requests.get(url)
    print(f"Status Code: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        models = [m['name'] for m in data.get('models', [])]
        print("Available models:", models)
    else:
        print("Response:", res.text)
except Exception as e:
    print(f"Error: {e}")
