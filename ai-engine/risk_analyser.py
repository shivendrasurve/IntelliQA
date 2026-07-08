from groq import Groq
from dotenv import load_dotenv
import os
import subprocess
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

RISK_RULES = {
    "payments":    {"priority": 1, "reason": "Core financial transaction - highest business impact"},
    "refunds":     {"priority": 2, "reason": "Financial reversal - direct customer impact"},
    "transfers":   {"priority": 2, "reason": "Fund movement - balance integrity risk"},
    "accounts":    {"priority": 3, "reason": "Read-only data - lower mutation risk"},
    "get_payment": {"priority": 3, "reason": "Read-only data - lower mutation risk"},
}

def get_changed_files():
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True, text=True,
            cwd="/Users/shivendra/FinalSemesterProject/IntelliQA"
        )
        changed = result.stdout.strip().split("\n")
        return [f for f in changed if f]
    except Exception as e:
        print(f"Git diff error: {e}")
        return []

def map_files_to_modules(changed_files):
    module_map = {
        "mock-api/server.js":                       ["payments", "refunds", "transfers", "accounts", "get_payment"],
        "ai-engine/test_generator.py":              ["payments", "refunds", "transfers", "accounts", "get_payment"],
        "test-suite/api-tests/test_payments.py":    ["payments"],
        "test-suite/api-tests/test_refunds.py":     ["refunds"],
        "test-suite/api-tests/test_transfers.py":   ["transfers"],
        "test-suite/api-tests/test_accounts.py":    ["accounts"],
        "test-suite/api-tests/test_get_payment.py": ["get_payment"],
    }
    affected = set()
    for f in changed_files:
        for pattern, modules in module_map.items():
            if pattern in f or f in pattern:
                affected.update(modules)
    if not affected:
        affected = set(RISK_RULES.keys())
    return list(affected)

def ai_risk_score(changed_files, affected_modules):
    prompt = f"""
You are a senior QA engineer analysing code changes for risk.

Changed files in this commit:
{json.dumps(changed_files, indent=2)}

Affected test modules:
{json.dumps(affected_modules, indent=2)}

For each affected module provide:
1. Risk level: HIGH, MEDIUM, or LOW
2. One sentence explaining why

Format:
MODULE: <name>
RISK: <HIGH/MEDIUM/LOW>
REASON: <one sentence>

Be concise. No other text.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a senior QA engineer. Be concise and precise."},
            {"role": "user",   "content": prompt}
        ]
    )
    return response.choices[0].message.content

def prioritise_tests(affected_modules):
    test_files = {
        "payments":    "test-suite/api-tests/test_payments.py",
        "refunds":     "test-suite/api-tests/test_refunds.py",
        "transfers":   "test-suite/api-tests/test_transfers.py",
        "accounts":    "test-suite/api-tests/test_accounts.py",
        "get_payment": "test-suite/api-tests/test_get_payment.py",
    }
    scored = []
    for module in affected_modules:
        if module in RISK_RULES:
            scored.append({
                "module":   module,
                "file":     test_files.get(module, ""),
                "priority": RISK_RULES[module]["priority"],
                "reason":   RISK_RULES[module]["reason"]
            })
    scored.sort(key=lambda x: x["priority"])
    return scored

def run_prioritised_tests(prioritised):
    print("\n📋 PRIORITISED TEST EXECUTION ORDER:")
    print("=" * 55)
    for i, item in enumerate(prioritised, 1):
        risk_label = ["🔴 HIGH", "🟡 MEDIUM", "🟢 LOW"][min(item["priority"]-1, 2)]
        print(f"{i}. {risk_label} — {item['module'].upper()}")
        print(f"   File:   {item['file']}")
        print(f"   Reason: {item['reason']}")
        print()
    print("=" * 55)
    files = " ".join([item["file"] for item in prioritised if item["file"]])
    print(f"\n▶️  Run prioritised tests:\n   pytest {files} -v\n")

if __name__ == "__main__":
    print("🤖 IntelliQA — AI Risk Prioritisation Engine")
    print("=" * 55)

    print("\n🔍 Step 1: Detecting changed files...")
    changed = get_changed_files()
    if changed and changed[0]:
        print(f"   Changed: {changed}")
    else:
        print("   No git changes — analysing all modules")
        changed = ["mock-api/server.js"]

    print("\n🗺️  Step 2: Mapping to test modules...")
    affected = map_files_to_modules(changed)
    print(f"   Affected: {affected}")

    print("\n🧠 Step 3: AI analysing risk...")
    ai_analysis = ai_risk_score(changed, affected)
    print("\n" + ai_analysis)

    print("\n⚡ Step 4: Generating prioritised test queue...")
    prioritised = prioritise_tests(affected)
    run_prioritised_tests(prioritised)

    results = {
        "changed_files":    changed,
        "affected_modules": affected,
        "prioritised_tests": prioritised,
        "ai_analysis":      ai_analysis
    }
    os.makedirs("execution-pipeline", exist_ok=True)
    with open("execution-pipeline/risk_report.json", "w") as f:
        json.dump(results, f, indent=2)
    print("💾 Risk report saved → execution-pipeline/risk_report.json")
