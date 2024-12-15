#!/usr/bin/env python3
import os
import sys
import json
import requests
import pytesseract
from PIL import Image

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/complete"
ANTHROPIC_MODEL = "claude-2"
MAX_TOKENS_TO_SAMPLE = 1024
TEMPERATURE = 0.7
STOP_SEQUENCES = ["\n\nHuman:"]
OCR_LANGUAGE = "eng"

def check_api_key():
    if not ANTHROPIC_API_KEY:
        print("ANTHROPIC_API_KEY not set.")
        sys.exit(1)

def extract_text_from_image(image_path: str) -> str:
    if not os.path.exists(image_path):
        print(f"Image file does not exist: {image_path}")
        sys.exit(1)
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Could not open image file: {image_path}")
        print(e)
        sys.exit(1)
    return pytesseract.image_to_string(image, lang=OCR_LANGUAGE)

def clean_ocr_text(text: str) -> str:
    cleaned = text.strip()
    cleaned = " ".join(cleaned.split())
    return cleaned

def build_prompt(extracted_text: str) -> str:
    prompt = f"""
Below is text extracted from an image of a generated report page. The report likely summarizes interviews, claims, or topics about challenges faced by formerly incarcerated individuals, community support, systemic issues, and success stories.

Text extracted from the image:
\"\"\"{extracted_text}\"\"\"

From this text:
1. Identify and list which topics or categories appear to be most commonly discussed.
2. Identify any topics that appear to be less mentioned or underexplored.
3. Generate a set of future interview questions:
   - 'deep_dive_questions': Questions for commonly discussed topics.
   - 'underexplored_questions': Questions for less mentioned or underexplored topics.
   - 'connecting_questions': Questions linking both sets.

Answer in JSON format:

{{
  "deep_dive_questions": [...],
  "underexplored_questions": [...],
  "connecting_questions": [...]
}}
"""
    return prompt.strip()

def query_anthropic_api(prompt: str) -> str:
    anthropic_prompt = f"\n\nHuman: {prompt}\n\nAssistant:"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": anthropic_prompt,
        "model": ANTHROPIC_MODEL,
        "max_tokens_to_sample": MAX_TOKENS_TO_SAMPLE,
        "temperature": TEMPERATURE,
        "stop_sequences": STOP_SEQUENCES
    }
    response = requests.post(ANTHROPIC_API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        print("Error querying Anthropic API:")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        sys.exit(1)
    data = response.json()
    return data.get("completion", "").strip()

def parse_model_response_to_json(response_text: str) -> dict:
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {"raw_response": response_text}

def main():
    check_api_key()
    if len(sys.argv) < 2:
        print("Usage: python generate_questions_from_image.py <image_path>")
        sys.exit(1)
    image_path = sys.argv[1]
    ocr_text = extract_text_from_image(image_path)
    cleaned_text = clean_ocr_text(ocr_text)
    prompt = build_prompt(cleaned_text)
    response_text = query_anthropic_api(prompt)
    questions = parse_model_response_to_json(response_text)
    print(json.dumps(questions, indent=2))

if __name__ == "__main__":
    main()
