
from groq import Groq
import os

# IMPORTANT: ONLY UPDATE YOUR API KEY BELOW

API_KEY = "API KEY"
CLIENT = Groq(api_key=API_KEY)

def query_llm(message: str) -> str:
    """
    Provided function to query the LLM.
    Args:
        message: The prompt to send to the LLM
    Returns:
        The LLM's response as a string
    """
    try:
        response = CLIENT.chat.completions.create(
            model="gemma2-9b-it",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        if "401" in str(e) or "invalid_api_key" in str(e).lower():
            return "Error: Invalid API key. Please update your Groq API key in utils.py"
        else:
            return f"Error connecting to LLM: {str(e)}"
    