"""
modules/mindmap_gen.py
Summary se mind map data generate karta hai using Google Gemini.
"""

import json
from modules.gemini_client import generate_with_retry

MINDMAP_PROMPT = """
Generate a hierarchical mind map from this study material.

Return ONLY a valid JSON object — no markdown, no extra text, no code fences:

{{
  "title": "Main Topic",
  "children": [
    {{
      "title": "Subtopic 1",
      "children": [
        {{"title": "Detail 1a", "children": []}},
        {{"title": "Detail 1b", "children": []}}
      ]
    }},
    {{
      "title": "Subtopic 2",
      "children": [
        {{"title": "Detail 2a", "children": []}},
        {{"title": "Detail 2b", "children": []}}
      ]
    }}
  ]
}}

Rules:
- Maximum 3 levels deep
- 4-6 main subtopics
- 2-4 details per subtopic
- Keep titles concise (max 6 words each)

Content: {summary}
"""


def generate_mindmap(summary_text, _retries=0):
    """Summary se mind map hierarchy banata hai — returns dict"""
    MAX_RETRIES = 3
    try:
        raw = generate_with_retry(MINDMAP_PROMPT.format(summary=summary_text), max_tokens=2000, temperature=0.3)
        raw = raw.strip()

        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
            raw = raw.strip()

        mindmap = json.loads(raw)
        print(f"✅ Mind map ready — '{mindmap.get('title', 'Untitled')}'")
        return mindmap
    except json.JSONDecodeError:
        if _retries < MAX_RETRIES:
            print(f"⚠️ JSON parse error — retry {_retries + 1}/{MAX_RETRIES}...")
            return generate_mindmap(summary_text, _retries=_retries + 1)
        print("❌ Mind map generation failed after retries — returning default")
        return {"title": "Mind Map", "children": []}
    except Exception as e:
        print(f"❌ Mind map generation error: {e}")
        return {"title": "Mind Map", "children": []}
