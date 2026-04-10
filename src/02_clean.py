"""cleans raw data & make clean dataset"""

import json
import re
import os
from num2words import num2words
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initialize tools
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    if not text:
        return ""

    # Lowercase
    text = text.lower()

    # Convert numbers to words
    def replace_numbers(match):
        try:
            return num2words(int(match.group()))
        except:
            return ""

    text = re.sub(r"\d+", replace_numbers, text)

    # Remove punctuation & special characters (keep letters and spaces)
    text = re.sub(r"[^a-z\s]", " ", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Tokenize
    words = text.split()

    # Remove stopwords + lemmatize
    cleaned_words = []
    for word in words:
        if word not in stop_words:
            lemma = lemmatizer.lemmatize(word)
            cleaned_words.append(lemma)

    return " ".join(cleaned_words)


def clean_dataset(input_file, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    seen_texts = set()
    cleaned_data = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            review = json.loads(line)
            raw_text = review.get("text", "").strip()

            # Skip empty
            if not raw_text:
                continue

            cleaned_text = clean_text(raw_text)

            # Skip very short reviews
            if len(cleaned_text.split()) < 3:
                continue

            # Remove duplicates
            if cleaned_text in seen_texts:
                continue

            seen_texts.add(cleaned_text)

            cleaned_data.append(
                {"review_id": review.get("review_id"), "text": cleaned_text}
            )

    # Save JSONL
    with open(output_file, "w", encoding="utf-8") as f:
        for item in cleaned_data:
            f.write(json.dumps(item) + "\n")

    print(f"Cleaned dataset size: {len(cleaned_data)}")


def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    input_path = os.path.join(BASE_DIR, "data", "reviews_raw.jsonl")
    output_path = os.path.join(BASE_DIR, "data", "reviews_clean.jsonl")

    clean_dataset(input_path, output_path)


if __name__ == "__main__":
    main()
