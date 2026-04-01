<div align="center">

# 🧠 SmartStudy AI

### AI-Powered Study Tool — Turn Any PDF into Summary, Quiz, Flashcards, Mind Map & Podcast

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-Free_API-F55036?style=flat-square&logo=groq&logoColor=white)](https://console.groq.com)
[![Llama](https://img.shields.io/badge/Llama_3.3-70B-blueviolet?style=flat-square)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-22c55e?style=flat-square)]()

**Upload any PDF — AI instantly generates a structured summary, quiz questions, flashcards, a visual mind map, and an audio podcast.**

[Features](#-features) · [Installation](#-installation) · [Usage](#-usage) · [Project Structure](#-project-structure) · [Tech Stack](#-tech-stack) · [Roadmap](#-roadmap)

</div>

---

## 🎯 What is SmartStudy AI?

**SmartStudy AI** is a free, open-source Python application built for students. Upload any academic PDF — a textbook chapter, lecture notes, or research paper — and the AI automatically produces five types of study content:

| Output | What You Get |
|---|---|
| 📋 **Smart Summary** | Structured notes with overview, key topics, definitions, and formulas |
| ❓ **Quiz & Q&A** | 15 auto-generated questions — MCQ, Short Answer, Fill in Blank, True/False |
| 🗂️ **Flashcards** | 15 revision cards with the question on the front and the answer on the back |
| 🧩 **Mind Map** | Visual topic hierarchy rendered with Graphviz |
| 🎙️ **Podcast** | Two-host conversational audio in NotebookLM style |

> **100% Free** — Powered by the **Groq API free tier** running **Llama 3.3 70B**. No credit card required.

---

## ✨ Features

### 📋 Module 1 — AI Summarization
- Extracts text from any text-based PDF using **PyMuPDF (fitz)**
- Sends extracted text to **Groq API (Llama 3.3 70B)** for summarization
- Returns a structured JSON summary containing:
  - **Overview** — 3 to 5 sentence introduction to the topic
  - **Key Topics** — hierarchical bullet list with descriptions
  - **Definitions** — important terms explained concisely
  - **Formulas** — preserved exactly as written, never simplified
  - **Takeaway** — 2 to 3 sentence study conclusion
- Automatic chunking for large documents — handles 200+ page PDFs
- Chunk-then-merge strategy for coherent final output

### ❓ Module 2 — Quiz & Q&A Generation
- Generates 15 questions across 4 types:
  - **MCQ** — 4 options per question, correct answer marked with explanation
  - **Short Answer** — question paired with a model answer
  - **Fill in the Blank** — key term removed from a statement + answer key
  - **True / False** — statement with correct verdict and one-line reasoning
- Interactive mode in the UI — select answers and reveal correct ones
- Progress bar tracking how many questions you have answered
- JSON validation and auto-retry on malformed API output
- Export the full quiz with answer key as a `.txt` file

### 🗂️ Module 3 — Flashcards
- Generates 15 study flashcards from the document summary
- **Front side** — question or key term to recall
- **Back side** — detailed answer or definition
- Card flip interaction in the Streamlit UI
- Navigate with Previous and Next buttons

### 🧩 Module 4 — Mind Map
- Generates a structured topic hierarchy using **Graphviz**
- Root node = main document topic
- Branch nodes = major subtopics
- Leaf nodes = supporting details and facts
- Exports as a downloadable PNG image

### 🎙️ Module 5 — Podcast Generation
- Generates a natural **two-host dialogue script** (NotebookLM style)
- **Host A** — a curious student asking probing questions
- **Host B** — a knowledgeable expert explaining with examples
- Script produced by Groq API (Llama 3.3 70B for natural conversation quality)
- Targets 25 to 30 dialogue turns covering all key topics

### 🖥️ Streamlit Web UI
- Premium dark-themed interface built with custom CSS
- Sidebar navigation — Summary, Quiz, Flashcards, Mind Map, Podcast
- Accepts PDF, TXT, and MD file uploads
- Live progress indicator during AI processing
- Download buttons for every generated output
- On-demand generation — each tool generates only when you click

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or newer
- Groq API key — [Get your free key here](https://console.groq.com)
- Graphviz installed at the system level (required for mind map)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/ranjan781/SmartStudy.git
cd SmartStudy
```

### Step 2 — Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` contents:

```
pymupdf>=1.24.0
streamlit>=1.30.0
groq>=0.9.0
python-dotenv>=1.0.0
graphviz>=0.20.0
reportlab>=4.0.0
```

### Step 4 — Install Graphviz at System Level

```bash
# Windows (using Chocolatey)
choco install graphviz

# macOS
brew install graphviz

# Ubuntu / Debian
sudo apt install graphviz
```

> **Why system-level?** The Python `graphviz` package is just a wrapper — the actual rendering engine must be installed separately.

### Step 5 — Configure Your API Key

Create a `.env` file in the project root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

> **How to get a Groq API key:**
> 1. Go to [console.groq.com](https://console.groq.com)
> 2. Sign up with Google or email
> 3. Navigate to **API Keys** → **Create New Key**
> 4. Copy and paste it into your `.env` file
>
> Free tier gives you **14,400 requests/day** and **30 requests/minute** — more than enough for any student.

---

## 💻 Usage

### Option A — Streamlit Web UI (Recommended)

```bash
streamlit run app.py
```

Your browser will open at `http://localhost:8501`.

1. Upload a PDF from the left sidebar
2. Click **"Process Document"**
3. Wait for the AI to generate the summary (10 to 30 seconds)
4. Navigate to Quiz, Flashcards, Mind Map, or Podcast from the sidebar
5. Click **"Generate"** on each page to produce that content on demand
6. Use the download buttons to save your outputs

### Option B — Command Line (CLI)

```bash
# Summary only
python main.py "path/to/your/chapter.pdf"

# Summary + Quiz
python main.py "path/to/your/chapter.pdf" --quiz

# Summary + Quiz + Podcast
python main.py "path/to/your/chapter.pdf" --quiz --podcast
```

All output files are saved automatically to the `outputs/` folder.

---

## 🗂️ Project Structure

```
SmartStudy/
│
├── app.py                    # Main Streamlit web application
├── main.py                   # CLI entry point
│
├── modules/
│   ├── extractor.py          # PDF text extraction — PyMuPDF
│   ├── summarizer.py         # AI summarization — Groq API
│   ├── quiz_gen.py           # Quiz generation — Groq API
│   ├── flashcard_gen.py      # Flashcard generation — Groq API
│   ├── mindmap_gen.py        # Mind map generation — Graphviz
│   ├── podcast_gen.py        # Podcast script — Groq API
│   └── exporter.py           # File export — TXT, JSON, PDF via ReportLab
│
├── prompts/
│   ├── summary_prompt.txt    # System prompt for summarization
│   ├── quiz_prompt.txt       # System prompt for quiz questions
│   ├── flashcard_prompt.txt  # System prompt for flashcards
│   ├── mindmap_prompt.txt    # System prompt for mind map hierarchy
│   └── podcast_prompt.txt    # System prompt for podcast dialogue
│
├── outputs/                  # All generated files land here
│   ├── summary.json
│   ├── quiz.txt
│   └── podcast script
│
├── test_extractor.py         # Test — PDF text extraction
├── test_gemini.py            # Test — Groq API connection
├── test_podcast.py           # Test — Podcast script generation
│
├── system_response.md        # Sample AI responses for development reference
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔧 Tech Stack

| Layer | Tool | Version | Purpose |
|---|---|---|---|
| **PDF Extraction** | PyMuPDF (fitz) | 1.24+ | Extract and clean text from PDF pages |
| **AI / LLM** | Groq API | 0.9+ | Fast inference for all AI features |
| **LLM Models** | Llama 3.3 70B + Llama 3.1 8B | — | Groq-hosted open-source models |
| **UI Framework** | Streamlit | 1.30+ | Web interface with custom dark theme |
| **Mind Map** | Graphviz | 0.20+ | Topic hierarchy diagram rendering |
| **PDF Export** | ReportLab | 4.0+ | Generate downloadable quiz PDFs |
| **Environment** | python-dotenv | 1.0+ | Secure API key loading from `.env` |
| **Language** | Python | 3.10+ | Core application runtime |

### Model Selection Strategy

| Module | Groq Model | Why This Model |
|---|---|---|
| Summarization | `llama-3.3-70b-versatile` | Best at structured extraction and reasoning |
| Quiz Generation | `llama-3.1-8b-instant` | Fast enough, good at formatted JSON output |
| Flashcards | `llama-3.1-8b-instant` | Simple Q&A pairs, speed is the priority |
| Mind Map | `llama-3.3-70b-versatile` | Better hierarchical reasoning |
| Podcast Script | `llama-3.3-70b-versatile` | Natural and engaging conversational dialogue |

### Why Groq Over Other Providers?

| Factor | Groq | OpenAI | Google Gemini |
|---|---|---|---|
| Cost | Free tier | Paid only | Free tier |
| Speed | Fastest (LPU) | Medium | Medium |
| Daily limit | 14,400 req/day | — | 1,500 req/day |
| Card required | No | Yes | No |
| Model quality | Llama 3.3 70B | GPT-4o | Gemini 1.5 |

---

## 📊 End-to-End Data Flow

```
User uploads PDF
        │
        ▼
[extractor.py]
  PyMuPDF reads all pages
  Cleans headers, footers, page numbers, whitespace
  Chunks text if > 3000 tokens
        │
        ▼
[summarizer.py]
  Each chunk → Groq API (Llama 3.3 70B)
  Partial summaries → final merge prompt
  Returns structured JSON: overview, topics, definitions, formulas, takeaway
        │
        ├─────────────────────┬─────────────────────┬─────────────────────┐
        ▼                     ▼                     ▼                     ▼
[quiz_gen.py]         [flashcard_gen.py]    [mindmap_gen.py]     [podcast_gen.py]
Groq → 15 questions   Groq → 15 cards       Groq → hierarchy     Groq → dialogue JSON
JSON with answers     front + back pairs    Graphviz → PNG       script → audio
        │                     │                     │                     │
        └─────────────────────┴─────────────────────┴─────────────────────┘
                                        │
                                        ▼
                              [exporter.py]
                   Saves summary.json, quiz.txt, mind_map.png
                   to the outputs/ folder
```

---

## 🧪 Running Tests

Three test scripts verify that each core component is working:

```bash
# Verify PDF text extraction is working
python test_extractor.py

# Verify Groq API key and connection
python test_gemini.py

# Verify podcast script generation
python test_podcast.py
```

Run these first whenever you set up on a new machine or debug an API issue.

---

## ⚙️ Configuration Guide

### Switch Between Groq Models

In any module file, change the model string:

```python
from groq import Groq
client = Groq()

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",  # Change this line
    # model="llama-3.1-8b-instant",   # Faster but slightly lower quality
    messages=[{"role": "user", "content": your_prompt}]
)
```

### Adjust Chunk Size for Large PDFs

In `modules/extractor.py`:

```python
MAX_CHARS = 12000  # Roughly 3000 tokens — increase if your PDFs are very long
```

### Change the Number of Questions or Cards

Edit `prompts/quiz_prompt.txt` or `prompts/flashcard_prompt.txt` directly — no Python code change required.

### Add Rate Limit Protection

If you hit Groq rate limits, add this between API calls:

```python
import time
time.sleep(2)  # 2 second pause between calls
```

---

## 🐛 Common Errors and Fixes

| Error | Likely Cause | Fix |
|---|---|---|
| `GROQ_API_KEY not found` | `.env` file missing or misnamed | Create `.env` in the project root with your key |
| `AuthenticationError` | Invalid or expired API key | Generate a new key at console.groq.com |
| `RateLimitError` | Too many requests per minute | Add `time.sleep(2)` between Groq calls |
| `graphviz.backend.execute.ExecutableNotFound` | Graphviz not installed at system level | Run `brew install graphviz` or `apt install graphviz` |
| `ModuleNotFoundError: fitz` | PyMuPDF not installed | Run `pip install pymupdf` |
| `JSONDecodeError` on quiz output | LLM returned text with markdown fences | The retry logic in `quiz_gen.py` handles this automatically |
| Empty extraction from PDF | Scanned or image-only PDF | OCR is not supported in v1 — use text-based PDFs only |
| Streamlit port already in use | Another process on port 8501 | Run `streamlit run app.py --server.port 8502` |
| `ModuleNotFoundError: groq` | Groq package not installed | Run `pip install groq` |

---

## 🗺️ Roadmap

### v1.0 — Current Release ✅
- [x] PDF text extraction with PyMuPDF
- [x] AI summarization via Groq + Llama 3.3
- [x] Quiz generation — 4 question types
- [x] Flashcard generation with flip interaction
- [x] Mind map visualization with Graphviz
- [x] Podcast script generation
- [x] Dark-themed Streamlit UI with custom CSS
- [x] CLI support with feature flags
- [x] File export — TXT, JSON, PDF

### v2.0 — Planned 🚧
- [ ] **OCR support** — handle scanned and image-only PDFs using pytesseract
- [ ] **Multi-PDF RAG** — build a personal knowledge base across multiple documents and ask questions across all of them
- [ ] **Interactive quiz mode** — live scoring, countdown timer, wrong answer explanations with links back to the summary
- [ ] **Anki export** — generate `.apkg` flashcard files compatible with the Anki spaced repetition system
- [ ] **Hindi voice support** — multilingual podcast output using regional TTS voices
- [ ] **YouTube transcript ingestion** — study from video lectures, not just PDFs
- [ ] **Progress dashboard** — track quiz scores over time, identify weak topics, visualize improvement
- [ ] **Telegram bot interface** — send a PDF, receive summary and quiz directly on mobile

---

## 🤝 Contributing

Contributions are welcome. To add a feature or report a bug:

1. Fork this repository
2. Create a feature branch — `git checkout -b feature/your-feature`
3. Make your changes and commit — `git commit -m "Add: description of change"`
4. Push your branch — `git push origin feature/your-feature`
5. Open a Pull Request with a clear description

Please write clean, commented code and test your changes before submitting.

---

## 👨‍💻 Author

**Ranjan Yadav** — Solo student project

- GitHub: [@ranjan781](https://github.com/ranjan781)
- Repository: [SmartStudy](https://github.com/ranjan781/SmartStudy)

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

<div align="center">

**Found this useful? Give it a ⭐ star on GitHub!**

Built with ❤️ for students everywhere

</div>
