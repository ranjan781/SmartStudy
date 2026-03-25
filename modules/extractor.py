"""
modules/extractor.py
PDF aur text files se content extract karne ke liye.
"""

import os

def extract_text(file_path: str) -> str:
    """
    Given file path se text extract karta hai.
    Supports: .pdf, .txt, .md

    Args:
        file_path: File ka path (relative ya absolute)

    Returns:
        Extracted text as string

    Raises:
        FileNotFoundError: Agar file exist nahi karti
        ValueError: Agar file format supported nahi hai
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File nahi mili: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _extract_from_pdf(file_path)
    elif ext in (".txt", ".md"):
        return _extract_from_text(file_path)
    else:
        raise ValueError(f"Unsupported file format: '{ext}'. Supported: .pdf, .txt, .md")


def _extract_from_pdf(file_path: str) -> str:
    """PyMuPDF (fitz) se PDF text extract karta hai."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise ImportError(
            "PyMuPDF install nahi hai. Run karo: pip install pymupdf"
        )

    text_parts = []
    with fitz.open(file_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text("text")
            if page_text.strip():
                text_parts.append(f"--- Page {page_num} ---\n{page_text}")

    return "\n\n".join(text_parts)


def _extract_from_text(file_path: str) -> str:
    """Plain text / markdown file ko read karta hai."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text: str, max_tokens: int = 3000) -> list[str]:
    """Text ko chunks mein divide karta hai."""
    # Simple chunking logic based on characters (roughly 4 chars per token)
    chunk_size = max_tokens * 4
    if len(text) <= chunk_size:
        return [text]
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
