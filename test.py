import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")

url = "https://api.ollama.com"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "llama3.1",
    "messages": [
        {"role": "user", "content": "What is the weather forecast for today in Surigao?"}
    ]
}

response = requests.post(url, headers=headers, json=data)

print("Status:", response.status_code)
print("Response text:")
print(response.text)