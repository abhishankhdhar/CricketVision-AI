import requests
import tomllib


# Read API key from Streamlit secrets
with open(".streamlit/secrets.toml", "rb") as f:
    secrets = tomllib.load(f)

api_key = secrets["GEMINI_API_KEY"]

url = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.8-flash:generateContent"
)

payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Reply with exactly: Gemini connection successful!"
                }
            ]
        }
    ]
}

headers = {
    "Content-Type": "application/json",
    "x-goog-api-key": api_key
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=60
)

print("Status code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    answer = data["candidates"][0]["content"]["parts"][0]["text"]
    print("Gemini response:", answer)
else:
    print("Gemini API error:")
    print(response.text)