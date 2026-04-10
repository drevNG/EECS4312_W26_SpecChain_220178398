# """generates structured specs from personas"""
import json
import os
import re
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PERSONA_PATH = os.path.join(BASE_DIR, "personas", "personas_auto.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "spec", "spec_auto.md")


def load_personas():
    with open(PERSONA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_prompt(personas):
    prompt = f"""
You are an expert in software requirements engineering.

TASK:
Generate software requirements based on the following personas.

RULES:
- Generate at least 2 requirements per persona
- Each requirement must follow the exact format below
- Use unique IDs like FR_auto_1, FR_auto_2, etc.
- Do NOT include explanations
- Output ONLY the requirements in plain text

FORMAT:

# Requirement ID: FR_auto_1
- Description: [The system shall ...]

- Source Persona: [Persona Name]
- Traceability: [Derived from review group G#]
- Acceptance Criteria: [Given ..., When ..., Then ...]

PERSONAS:
{json.dumps(personas, indent=2)}
"""
    return prompt


def call_llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content


def main():
    print("Loading personas...")
    personas = load_personas()

    prompt = build_prompt(personas)
    print("Prompt built")

    response = call_llm(prompt)
    print("LLM response received")

    # Clean response (remove anything before first requirement)
    match = re.search(r"# Requirement ID:.*", response, re.DOTALL)

    if not match:
        print("ERROR: No valid requirements found")
        return

    cleaned_output = match.group()

    # Save to file
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(cleaned_output)

    print("Auto specifications saved.")


if __name__ == "__main__":
    main()
