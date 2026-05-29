from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# Configure Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_gemini(prompt: str) -> str:
    """
    Core AI function used by all pillars.
    Powered by Groq (llama-3.3-70b) - free and fast.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an expert QA engineer specialising in test automation, API testing, and software quality assurance."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content

# Quick test
if __name__ == "__main__":
    test_prompt = """
    You are an expert QA engineer.
    I have a REST API endpoint:
    POST /payments
    Body: { amount, currency, account_id }
    
    Generate 3 test cases for this endpoint.
    For each test case write:
    - Test name
    - Input data
    - Expected result
    """

    print("Sending request to Groq AI...")
    print("-" * 50)
    response = ask_gemini(test_prompt)
    print(response)
    print("-" * 50)
    print("✅ Groq AI is connected and working!")
