"""imports or reads your raw dataset; if you scraped, include scraper here"""

from google_play_scraper import reviews_all
import json
import os


def fetch_reviews(app_id):
    print("Fetching reviews...")
    reviews = reviews_all(app_id, lang="en", country="us")[
        :3000
    ]  # limit dataset, was previously getting 46230 reviews which is unnecessarily large for this project
    print(f"Fetched {len(reviews)} reviews")
    return reviews


def save_reviews_jsonl(reviews, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        for i, review in enumerate(reviews):
            record = {
                "review_id": i,
                "text": review.get("content", ""),
                "rating": review.get("score", None),
                "date": str(review.get("at", "")),
            }
            f.write(json.dumps(record) + "\n")


def main():
    app_id = "bot.touchkin"  # Wysa

    reviews = fetch_reviews(app_id)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(BASE_DIR, "data", "reviews_raw.jsonl")

    save_reviews_jsonl(reviews, output_path)

    print("Saved to data/reviews_raw.jsonl")


if __name__ == "__main__":
    main()
