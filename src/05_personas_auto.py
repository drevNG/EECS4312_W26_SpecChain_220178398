# """automated persona generation pipeline"""
import json
import os
import random
from groq import Groq

# Initialize Groq client (set your API key in environment variables)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_PATH = os.path.join(BASE_DIR, "data", "reviews_clean.jsonl")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "review_groups_auto.json")
PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "prompt_auto.json")


def load_reviews(sample_size=120):
    reviews = []
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            reviews.append(json.loads(line))

    return random.sample(reviews, sample_size)


def build_prompt(reviews):
    review_texts = [r["text"] for r in reviews]

    prompt = f"""
You are an expert in software requirements analysis.

TASK:
Group the following user reviews into EXACTLY 5 groups based on common themes.

RULES:
- Each group must have a clear theme
- Each group must contain multiple reviews
- Groups must be distinct
- Do NOT include explanations
- Output ONLY valid JSON

FORMAT:
{{
  "groups": [
    {{
      "group_id": "G1",
      "theme": "short theme name",
      "reviews": ["review text 1", "review text 2"]
    }}
  ]
}}

REVIEWS:
{review_texts}
"""
    return prompt


def call_llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


def map_reviews_to_ids(groups, original_reviews):
    text_to_id = {r["text"]: i for i, r in enumerate(original_reviews)}

    for group in groups["groups"]:
        ids = []
        for text in group["reviews"]:
            if text in text_to_id:
                ids.append(text_to_id[text])
        group["review_ids"] = ids
        del group["reviews"]

    return groups

def build_persona_prompt(groups):
    prompt = f"""
You are an expert in software requirements engineering.

TASK:
Generate one persona for EACH review group.

RULES:
- One persona per group
- Use realistic names
- Base personas ONLY on the group themes
- Output ONLY valid JSON

FORMAT:
{{
  "personas": [
    {{
      "id": "P1",
      "name": "Name",
      "description": "Short description",
      "derived_from_group": "G1",
      "goals": ["goal1", "goal2"],
      "pain_points": ["pain1", "pain2"],
      "context": ["context1", "context2"],
      "constraints": ["constraint1", "constraint2"],
      "evidence_reviews": [1, 2, 3]
    }}
  ]
}}

GROUPS:
{json.dumps(groups, indent=2)}
"""
    return prompt

def main():
    print("Starting script...")

    reviews = load_reviews()
    print(f"Loaded {len(reviews)} reviews")

    prompt = build_prompt(reviews)
    print("Prompt built")

    # Save prompt
    os.makedirs(os.path.dirname(PROMPT_PATH), exist_ok=True)
    with open(PROMPT_PATH, "w", encoding="utf-8") as f:
        json.dump({"prompt": prompt}, f, indent=2)

    print("Prompt saved")

    response = call_llm(prompt)
    print("LLM response received")

    print(response[:500])  # preview response

    import re
    match = re.search(r'\{.*\}', response, re.DOTALL)

    if not match:
        print("ERROR: No JSON found in response")
        return

    json_text = match.group()
    groups = json.loads(json_text)

    print("Parsed JSON")

    groups = map_reviews_to_ids(groups, reviews)
    print("Mapped review IDs")

    # Save output
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(groups, f, indent=2)

    print("Auto review groups saved.")

        # ===== Generate Personas =====
    print("Generating personas...")

    persona_prompt = build_persona_prompt(groups)

    persona_response = call_llm(persona_prompt)
    print("LLM persona response received")

    match = re.search(r'\{.*\}', persona_response, re.DOTALL)

    if not match:
        print("ERROR: No JSON found in persona response")
        return

    personas_json = json.loads(match.group())

    PERSONA_OUTPUT = os.path.join(BASE_DIR, "personas", "personas_auto.json")

    os.makedirs(os.path.dirname(PERSONA_OUTPUT), exist_ok=True)

    with open(PERSONA_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(personas_json, f, indent=2)

    print("Auto personas saved.")

if __name__ == "__main__":
    main()