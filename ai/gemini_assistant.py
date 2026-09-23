import requests


# OpenRouter free model router
OPENROUTER_MODEL = "openrouter/free"

SYSTEM_PROMPT = """
You are an AI cricket coaching assistant inside an application called
AI Cricket Coach.

Your job is to help amateur and college-level cricket players understand
their batting technique and improve their training.

Give practical, understandable cricket advice.

When player analysis data is provided, use it as context.

Important rules:
- Do not claim that the computer vision analysis is professionally validated.
- Do not diagnose injuries or medical conditions.
- Clearly distinguish measured data from general cricket advice.
- Give practical cricket drills whenever useful.
- Keep explanations understandable for a college-level cricket player.
- If the player asks about their own analysis, use the provided analysis data.
- Be concise but useful.
"""


def ask_gemini(question, analysis=None, api_key=None):
    """
    This function keeps the old function name so that we can minimize
    changes to the rest of the application.

    The actual AI request is now sent through OpenRouter.
    """

    if not api_key:
        raise ValueError("OpenRouter API key is missing.")

    analysis_context = ""

    if analysis:
        analysis_context = f"""
Here is the player's current AI batting analysis:

{analysis}

Use these measurements when answering questions
about this player's batting technique.
"""

    user_prompt = f"""
{analysis_context}

Player's question:

{question}
"""

    url = "https://openrouter.ai/api/v1/chat/completions"

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "temperature": 0.4
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "AI Cricket Coach"
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=(10, 60)
        )

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "OpenRouter request timed out. Please try again."
        )

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Could not connect to OpenRouter: {exc}"
        )

    if response.status_code != 200:
        try:
            error_data = response.json()

            error_message = (
                error_data
                .get("error", {})
                .get("message", response.text)
            )

        except Exception:
            error_message = response.text

        raise RuntimeError(
            f"OpenRouter API error {response.status_code}: "
            f"{error_message}"
        )

    try:
        data = response.json()

        answer = (
            data["choices"][0]
            ["message"]["content"]
        )

        if not answer:
            raise RuntimeError(
                "OpenRouter returned an empty response."
            )

        return answer

    except (KeyError, IndexError, TypeError):
        raise RuntimeError(
            "OpenRouter returned an unexpected response."
        )