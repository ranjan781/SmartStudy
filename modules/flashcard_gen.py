"""
modules/flashcard_gen.py
Summary se flashcards generate karta hai using Google Gemini.
"""

import json
from modules.gemini_client import generate_with_retry

FLASHCARD_PROMPT = """
Generate 15 study flashcards from this material.

Return ONLY a valid JSON array — no markdown, no extra text, no code fences:

[
  {{"front": "Question or term", "back": "Answer or definition"}},
  ...
]

Mix of:
- Key term definitions (6 cards)
- Concept questions (5 cards)
- Important facts/formulas (4 cards)

Make them concise and exam-focused.

Content: {summary}
"""


def generate_flashcards(summary_text, _retries=0):
    """Summary se flashcards banata hai — returns list of dicts"""
    MAX_RETRIES = 3
    try:
        raw = generate_with_retry(FLASHCARD_PROMPT.format(summary=summary_text), max_tokens=2000, temperature=0.4)
        raw = raw.strip()

        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
            raw = raw.strip()

        flashcards = json.loads(raw)
        print(f"✅ {len(flashcards)} flashcards generate hue!")
        return flashcards
    except json.JSONDecodeError:
        if _retries < MAX_RETRIES:
            print(f"⚠️ JSON parse error — retry {_retries + 1}/{MAX_RETRIES}...")
            return generate_flashcards(summary_text, _retries=_retries + 1)
        print("❌ Flashcard generation failed after retries — returning empty list")
        return []
    except Exception as e:
        print(f"❌ Flashcard generation error: {e}")
        return []
