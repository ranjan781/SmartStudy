# StudyMind AI – Comprehensive System Response After Document Submission

## Overview
StudyMind AI is an intelligent study assistant that processes educational documents (PDF, TXT, MD) and generates multiple AI‑powered learning resources. The system leverages Google Gemini for content understanding and generation, with a modular architecture that supports summarization, quiz creation, flashcards, mind maps, podcast scripts, and more.

## Core Modules & Feature Specifications

### 1. Document Extraction (`modules/extractor.py`)
**Intended Behavior:** Extract text from PDF, TXT, and MD files while preserving structure and page boundaries.
- **Parameters:**
  - `file_path` (str): Path to the input file.
- **Returns:** Raw extracted text as a single string.
- **Integrations:** Used by summarizer, quiz generator, flashcard generator, etc.
- **Validation:** Implements PyMuPDF for PDFs, UTF‑8 reading for text files; includes chunking utility (`chunk_text`) for large documents.

### 2. Structured Summarization (`modules/summarizer.py`)
**Intended Behavior:** Convert extracted text into a structured JSON summary with overview, key topics, definitions, formulas, and takeaways.
- **Parameters:**
  - `extracted_text` (str): Raw text from the extractor.
- **Returns:** Dictionary with keys: `overview`, `key_topics`, `definitions`, `formulas`, `takeaway`.
- **Integrations:** Uses Gemini API via `gemini_client`; supports chunk‑and‑merge for long documents.
- **Validation:** Prompt enforces JSON‑only output; fallback parsing ensures graceful degradation.

### 3. Quiz Generation (`modules/quiz_gen.py`)
**Intended Behavior:** Produce 15 exam‑style questions (MCQ, short answer, fill‑in‑blank, true/false) from the summary.
- **Parameters:**
  - `summary_text` (str): Structured summary (or raw text).
- **Returns:** List of question objects, each with `type`, `question`, `options` (if MCQ), `answer`, and optional `explanation`.
- **Integrations:** Depends on Gemini API; exported via `exporter.export_quiz`.
- **Validation:** Retry logic for JSON parsing errors; output matches specified distribution (6 MCQ + 3 short answer + 3 fill blank + 3 true/false).

### 4. Flashcard Generation (`modules/flashcard_gen.py`)
**Intended Behavior:** Create 15 concise flashcards covering key terms, concepts, and facts.
- **Parameters:**
  - `summary_text` (str): Summary or raw content.
- **Returns:** List of `{"front": "...", "back": "..."}` dictionaries.
- **Integrations:** Gemini API; designed for integration with spaced‑repeatition systems.
- **Validation:** Mix of term definitions (6), concept questions (5), and important facts/formulas (4).

### 5. Mind Map Generation (`modules/mindmap_gen.py`)
**Intended Behavior:** Build a hierarchical mind‑map representation of the material.
- **Parameters:**
  - `summary_text` (str): Summary or raw content.
- **Returns:** Nested JSON object with `title` and `children` arrays (max 3 levels, 4–6 main subtopics, 2–4 details each).
- **Integrations:** Can be visualized with Graphviz (in Streamlit UI) or exported as JSON.
- **Validation:** Structure adheres to prompt constraints; fallback returns a default empty map.

### 6. Podcast Generation (`modules/podcast_gen.py`)
**Intended Behavior:** Generate a 5‑minute educational podcast script and convert it to audio.
- **Parameters:**
  - `summary_text` (str): Summary or raw content.
- **Returns:** Final MP3 file path.
- **Process:**
  1. **Script Generation:** Creates a dialogue between two hosts (Priya & Arjun) as a JSON array of speaker turns.
  2. **Audio Synthesis:** Uses Kokoro TTS to generate voice clips for each line.
  3. **Audio Merging:** Combines clips with silences into a single MP3.
- **Integrations:** Gemini API, Kokoro TTS, pydub, soundfile.
- **Validation:** Script contains 20–25 turns; audio files are produced and merged correctly.

### 7. YouTube Ingestion (`modules/youtube_ingestr.py`)
**Intended Behavior:** (Placeholder) Ingest YouTube video transcripts for processing.
- **Current Status:** Module file exists but is empty; specification indicates future integration with YouTube Data API.

### 8. Progress Tracking (`modules/tracker.py`)
**Intended Behavior:** (Placeholder) Track user study progress and quiz performance.
- **Current Status:** Module file exists but is empty; intended for future analytics.

### 9. Export & Output (`modules/exporter.py`)
**Intended Behavior:** Save generated resources (summary, quiz) to disk in human‑readable formats.
- **Functions:**
  - `export_summary`: Writes summary as JSON or plain text to `outputs/summary.txt`.
  - `export_quiz`: Formats questions and answer key into `outputs/quiz.txt`.
- **Integrations:** Called by main pipeline and Streamlit UI.

### 10. Gemini Client (`modules/gemini_client.py`)
**Intended Behavior:** Centralized API client with automatic retry and rate‑limit handling.
- **Parameters:**
  - `prompt` (str): Input prompt.
  - `max_tokens`, `temperature`, `max_retries` (optional).
- **Returns:** Generated text from Gemini‑2.0‑flash model.
- **Validation:** Exponential backoff on 429/quota errors; raises exception after max retries.

## System Integration & Data Flow
1. **Submission:** User uploads a PDF (or text file) via CLI (`main.py`) or Streamlit UI (`app.py`).
2. **Extraction:** `extractor.py` converts the document to plain text.
3. **Summarization:** `summarizer.py` produces a structured JSON summary.
4. **Optional Resources:** Based on user flags, the system generates:
   - Quiz (`--quiz`)
   - Flashcards (UI only)
   - Mind map (UI only)
   - Podcast (`--podcast`)
5. **Export:** All outputs are saved to the `outputs/` directory.
6. **UI Presentation:** Streamlit app provides a dark‑themed interface with sidebar navigation, real‑time generation, and visualizations.

## Validation of Implementation Against Specifications
| Feature | Specified Behavior | Implemented | Notes |
|---------|-------------------|-------------|-------|
| PDF/Text Extraction | Support .pdf, .txt, .md | ✅ | Uses PyMuPDF & plain text reading |
| Structured Summary | JSON with overview, topics, definitions, formulas, takeaway | ✅ | Chunk‑and‑merge for long docs |
| Quiz Generation | 15 questions (6 MCQ, 3 short answer, 3 fill blank, 3 true/false) | ✅ | Retry logic for JSON parsing |
| Flashcards | 15 cards (6 term definitions, 5 concept questions, 4 facts/formulas) | ✅ | Returns front/back pairs |
| Mind Map | Hierarchical JSON, max 3 levels, 4–6 main subtopics | ✅ | Graphviz visualization in UI |
| Podcast | 5‑minute script with two hosts, audio synthesis | ✅ | Kokoro TTS + pydub merging |
| YouTube Ingestion | (Planned) | ⚠️ | Module placeholder |
| Progress Tracking | (Planned) | ⚠️ | Module placeholder |
| Export | Summary and quiz saved to `outputs/` | ✅ | Plain‑text and JSON formats |
| API Client | Retry on rate limits, exponential backoff | ✅ | Uses Gemini‑2.0‑flash |

## Example Output After Document Submission
Assuming a PDF on “Machine Learning Basics” is submitted with `--quiz` and `--podcast` flags:

```
🧠 StudyMind AI — ml_basics.pdf

📄 Single chunk — direct summarize kar raha hoon...
✅ Summary saved: outputs/summary.txt
📝 Script generate kar raha hoon...
✅ Script ready — 24 turns
🎙️ Audio clips bana raha hoon...
  🎙️ Turn 1: Speaker A — done
  ...
🎵 Sab clips merge kar raha hoon...
✅ Podcast ready: outputs/podcast.mp3
✅ 15 questions generate hue!
✅ Quiz saved: outputs/quiz.txt

✅ Sab kaam ho gaya! outputs/ folder dekho.
```

## Conclusion
StudyMind AI fully implements the documented feature set for document processing, summarization, quiz generation, flashcard creation, mind‑map building, and podcast production. The system is modular, extensible, and ready for integration with additional data sources (YouTube, tracking) as specified. All core functionalities behave as intended, with robust error handling and user‑friendly outputs.