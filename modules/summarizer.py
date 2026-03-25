"""
modules/summarizer.py
PDF text ko structured JSON summary mein convert karta hai using Google Gemini.
"""

import json
from modules.extractor import chunk_text
from modules.gemini_client import generate_with_retry

SUMMARY_PROMPT = """
Summarize this content. Return ONLY a valid JSON object — no markdown, no extra text, no code fences.

{{
  "overview": "3-5 sentence introduction paragraph about the topic",
  "key_topics": [
    {{"title": "Topic Name", "description": "Brief explanation"}},
    ...
  ],
  "definitions": [
    {{"term": "Term Name", "definition": "Clear explanation"}},
    ...
  ],
  "formulas": [
    {{"name": "Formula Name", "formula": "The exact formula", "description": "What it represents"}},
    ...
  ],
  "takeaway": "2-3 sentence conclusion"
}}

If there are no formulas, return an empty array for "formulas".
If there are no specific definitions, return an empty array for "definitions".
Always include at least 3-5 key topics.

Content: {text}
"""

MERGE_PROMPT = """
Merge these partial summaries into one cohesive structured summary.
Return ONLY a valid JSON object — no markdown, no extra text, no code fences.

{{
  "overview": "3-5 sentence introduction paragraph about the topic",
  "key_topics": [
    {{"title": "Topic Name", "description": "Brief explanation"}},
    ...
  ],
  "definitions": [
    {{"term": "Term Name", "definition": "Clear explanation"}},
    ...
  ],
  "formulas": [
    {{"name": "Formula Name", "formula": "The exact formula", "description": "What it represents"}},
    ...
  ],
  "takeaway": "2-3 sentence conclusion"
}}

Partial summaries:
{text}
"""


def summarize_chunk(text, is_merge=False):
    """Ek chunk ko summarize karta hai — returns JSON string"""
    prompt = MERGE_PROMPT.format(text=text) if is_merge else SUMMARY_PROMPT.format(text=text)
    return generate_with_retry(prompt, max_tokens=2000, temperature=0.3)


def parse_summary(raw_text):
    """Raw response ko parse karke structured dict return karta hai"""
    raw = raw_text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "overview": raw,
            "key_topics": [],
            "definitions": [],
            "formulas": [],
            "takeaway": ""
        }


def summarize_pdf(extracted_text):
    """Full PDF summarize karta hai, chunking ke saath — returns structured dict"""
    chunks = chunk_text(extracted_text, max_tokens=3000)

    if len(chunks) == 1:
        print("📄 Single chunk — direct summarize kar raha hoon...")
        raw = summarize_chunk(chunks[0])
        return parse_summary(raw)

    print(f"📚 {len(chunks)} chunks mein toda — har ek summarize kar raha hoon...")

    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}/{len(chunks)} processing...")
        summary = summarize_chunk(chunk)
        chunk_summaries.append(summary)

    print("🔗 Sab summaries merge kar raha hoon...")
    merged_text = "\n\n---\n\n".join(chunk_summaries)

    final_raw = summarize_chunk(merged_text, is_merge=True)
    return parse_summary(final_raw)