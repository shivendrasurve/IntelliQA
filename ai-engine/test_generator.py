from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── API spec for our Mock FinTech API ────────────────────────────
API_SPEC = """
BASE URL: http://localhost:3000

ENDPOINTS:

1. POST /payments
   Body: { "amount": number, "currency": string, "account_id": string }
   Success: 201, { "id": "pay_xxx", "amount": 100, "currency": "EUR", "account_id": "acc_001", "status": "success" }
   Errors:
     - amount missing or <= 0 → 400, { "error": "Invalid amount" }
     - currency missing → 400, { "error": "Currency is required" }
     - account not found → 404, { "error": "Account not found" }
     - insufficient funds → 400, { "error": "Insufficient funds" }

2. GET /payments/:id
   Success: 200, payment object
   Error: payment not found → 404, { "error": "Payment not found" }

3. POST /refunds
   Body: { "payment_id": string, "amount": number }
   Success: 201, { "id": "ref_xxx", "payment_id": "pay_xxx", "amount": 50, "status": "refunded" }
   Errors:
     - payment not found → 404, { "error": "Payment not found" }
     - refund > original amount → 400, { "error": "Refund exceeds original payment" }

4. GET /accounts/:id
   Success: 200, { "id": "acc_001", "owner": "John Doe", "balance": 5000 }
   Error: account not found → 404, { "error": "Account not found" }

5. POST /transfers
   Body: { "from_account": string, "to_account": string, "amount": number }
   Success: 200, { "status": "success", "from": "acc_001", "to": "acc_002", "amount": 100 }
   Errors:
     - account not found → 404, { "error": "Account not found" }
     - insufficient funds → 400, { "error": "Insufficient funds" }

EXISTING TEST ACCOUNTS:
  acc_001: John Doe, balance 5000
  acc_002: Jane Smith, balance 3000
"""

def generate_tests(endpoint_name: str, endpoint_spec: str) -> str:
    prompt = f"""
You are an expert Python test automation engineer.

Generate executable Python pytest test code for this REST API endpoint.

API SPECIFICATION:
{endpoint_spec}

STRICT RULES:
1. Use the `requests` library to make HTTP calls
2. Base URL is http://localhost:3000
3. Each test function must start with test_
4. Use assert statements to verify status codes and response body
5. Cover: happy path, edge cases, negative scenarios
6. Do NOT use any mock or fake HTTP calls - use real requests
7. Do NOT include any markdown, backticks, or explanation
8. Output ONLY raw Python code, nothing else
9. Import requests and pytest at the top
10. Generate minimum 5 test functions

Generate tests for: {endpoint_name}
"""
    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {"role": "system", "content": "You are an expert test automation engineer. Output only raw executable Python code. No markdown. No backticks. No explanation."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def save_tests(filename: str, code: str):
    path = f"/Users/shivendra/FinalSemesterProject/IntelliQA/test-suite/api-tests/{filename}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Clean any markdown backticks if AI included them
    code = code.replace("```python", "").replace("```", "").strip()
    
    with open(path, "w") as f:
        f.write(code)
    print(f"✅ Saved: {filename}")
    return path

if __name__ == "__main__":
    print("🤖 IntelliQA - AI Test Code Generator")
    print("=" * 50)
    
    endpoints = [
        ("POST /payments",    "payments",  "POST /payments endpoint\n" + API_SPEC),
        ("GET /payments/:id", "get_payment","GET /payments/:id endpoint\n" + API_SPEC),
        ("POST /refunds",     "refunds",   "POST /refunds endpoint\n" + API_SPEC),
        ("GET /accounts/:id", "accounts",  "GET /accounts/:id endpoint\n" + API_SPEC),
        ("POST /transfers",   "transfers", "POST /transfers endpoint\n" + API_SPEC),
    ]
    
    for endpoint_name, file_prefix, spec in endpoints:
        print(f"\n📝 Generating tests for: {endpoint_name}")
        code = generate_tests(endpoint_name, spec)
        filename = f"test_{file_prefix}.py"
        save_tests(filename, code)
    
    print("\n" + "=" * 50)
    print("✅ All test files generated!")
    print(f"📁 Location: test-suite/api-tests/")
    print("\nRun tests with:")
    print("  pytest test-suite/api-tests/ -v")
