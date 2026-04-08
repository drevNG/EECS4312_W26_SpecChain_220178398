# """generates tests from specs"""
import json
import os
import re
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SPEC_PATH = os.path.join(BASE_DIR, "spec", "spec_auto.md")
OUTPUT_PATH = os.path.join(BASE_DIR, "tests", "tests_auto.json")


def load_spec():
    with open(SPEC_PATH, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(spec_text):
    prompt = f"""
You are an expert in software testing.

TASK:
Generate validation test cases for each requirement below.

RULES:
- Each requirement must have at least ONE test
- Use the exact JSON format below
- Use requirement IDs exactly as given
- Output ONLY valid JSON

FORMAT:
{{
  "tests": [
    {{
      "test_id": "T_auto_1",
      "requirement_id": "FR_auto_1",
      "scenario": "Short scenario name",
      "steps": ["Step 1", "Step 2"],
      "expected_result": "Expected outcome"
    }}
  ]
}}

REQUIREMENTS:
{spec_text}
"""
    return prompt


def call_llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content


def main():
    print("Loading specifications...")
    spec_text = load_spec()

    prompt = build_prompt(spec_text)
    print("Prompt built")

    response = call_llm(prompt)
    print("LLM response received")

    match = re.search(r'\{.*\}', response, re.DOTALL)

    if not match:
        print("ERROR: No JSON found")
        return

    tests_json = json.loads(match.group())

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(tests_json, f, indent=2)

    print("Auto tests saved.")


if __name__ == "__main__":
    main()