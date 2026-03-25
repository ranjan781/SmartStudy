import argparse
from modules.extractor import extract_text
from modules.summarizer import summarize_pdf
from modules.quiz_gen import generate_quiz
from modules.podcast_gen import create_podcast
from modules.exporter import export_summary, export_quiz

def main():
    parser = argparse.ArgumentParser(description="StudyMind AI")
    parser.add_argument("pdf", help="PDF file ka path")
    parser.add_argument("--quiz", action="store_true", help="Quiz bhi generate karo")
    parser.add_argument("--podcast", action="store_true", help="Podcast bhi banao")
    args = parser.parse_args()
    
    print(f"\n🧠 StudyMind AI — {args.pdf}\n")
    
    # Step 1: Extract
    text = extract_text(args.pdf)
    
    # Step 2: Summarize
    summary = summarize_pdf(text)
    export_summary(summary)
    
    # Step 3: Quiz (optional)
    if args.quiz:
        questions = generate_quiz(summary)
        export_quiz(questions)
    
    # Step 4: Podcast (optional)
    if args.podcast:
        create_podcast(summary)
    
    print("\n✅ Sab kaam ho gaya! outputs/ folder dekho.\n")

if __name__ == "__main__":
    main()