# EECS4312_W26_SpecChain

# Application
Application: Wysa: Mental Wellbeing AI
- Wysa is an AI mental health support chatbot

# Dataset
- reviews_raw.jsonl contains the collected reviews.
- reviews_clean.jsonl contains the cleaned dataset.
- The cleaned dataset contains 2437 reviews.

# Data Collection Method
Reviews were collected from app store sources and preprocessed using a cleaning script to remove noise, normalize text, and prepare the data for analysis.

# Repository Structure
- data/ contains datasets and review grouping files (manual, automated, hybrid)
- personas/ contains persona definitions for each pipeline
- spec/ contains generated system requirements
- tests/ contains validation test scenarios
- metrics/ contains computed metrics for all pipelines + summary
- src/ contains Python scripts for automation
- prompts/ contains stored prompts used for LLM generation
- reflection/ contains the final reflection

# Setup Requirements

This project uses the Groq API for automated generation.
You must first create an account on Groq and then generate an API key.  Next, you must set this API key as an environment variable using the following command: $env:GROQ_API_KEY="your_api_key"

Note that the model used in this project is a LLaMA-based model available through Groq, but it is not the version specified in the project instructions, meta-llama/llama-4-scout-17b-16e-instruct, as this seems to be an older version that was not working (the instructions also mentioned referring to the Prompt Engineering Lab completed in this course but that lab used GPT-3.5).  For this reason, llama-3.3-70b-versatile has been used as a substitute; it should produce the same functionality.

# How to Run

# Step 1: Validate repository structure
python src/00_validate_repo.py

# Step 2: Clean dataset
python src/02_clean_reviews.py

# Step 3: Run automated pipeline
python src/run_all.py

This will:
- Generate review groups: data/review_groups_auto.json
- Generate personas: personas/personas_auto.json
- Generate requirements: spec/spec_auto.md
- Generate tests: tests/tests_auto.json
- Compute metrics: metrics/metrics_auto.json

Keep in mind that since these are generated using Groq AI, the results it produces may vary.

# Step 4: View results
- metrics/metrics_manual.json
- metrics/metrics_auto.json
- metrics/metrics_hybrid.json
- metrics/metrics_summary.json

The summary file compares the metrics from all three pipelines.