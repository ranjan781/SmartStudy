"""
modules/quiz_gen.py
Summary se quiz questions generate karta hai using Google Gemini.
"""

import json
from modules.gemini_client import generate_with_retry

QUIZ_PROMPT = """
Generate 15 quiz questions from this study material.

Return ONLY a JSON array — no extra text, no markdown, no code fences:

[
  {{
    "type": "mcq",
    "question": "...",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "answer": "A"
  }},
  {{
    "type": "short_answer",
    "question": "...",
    "answer": "2-3 sentence answer"
  }},
  {{
    "type": "fill_blank",
    "question": "The ___ is responsible for...",
    "answer": "correct term"
  }},
  {{
    "type": "true_false",
    "question": "...",
    "answer": "True",
    "explanation": "Because..."
  }}
]

Generate: 6 MCQ + 3 Short Answer + 3 Fill in Blank + 3 True/False

Content: {summary}
"""

def generate_quiz(summary_text, _retries=0):
    """Summary se quiz questions banata hai"""
    MAX_RETRIES = 3
    try:
        raw = generate_with_retry(QUIZ_PROMPT.format(summary=summary_text), max_tokens=3000, temperature=0.4)
        raw = raw.strip()
        
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
            raw = raw.strip()
        
        questions = json.loads(raw)
        print(f"✅ {len(questions)} questions generate hue!")
        return questions
    except json.JSONDecodeError:
        if _retries < MAX_RETRIES:
            print(f"⚠️ JSON parse error — retry {_retries + 1}/{MAX_RETRIES}...")
            return generate_quiz(summary_text, _retries=_retries + 1)
        print("❌ Quiz generation failed after retries — returning empty list")
        return []
    except Exception as e:
        print(f"❌ Quiz generation error: {e}")
        return []