import json
import os

def export_summary(summary_data, path="outputs/summary.txt"):
    """Summary data ko file mein save karta hai — handles both dict and string"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        if isinstance(summary_data, dict):
            f.write(json.dumps(summary_data, indent=2, ensure_ascii=False))
        else:
            f.write(str(summary_data))
    print(f"✅ Summary saved: {path}")

def export_quiz(questions, path="outputs/quiz.txt"):
    """Quiz questions ko file mein save karta hai"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("QUIZ QUESTIONS\n")
        f.write("=" * 50 + "\n\n")
        
        # Questions pehle
        for i, q in enumerate(questions, 1):
            f.write(f"Q{i}. [{q.get('type', 'unknown').upper()}] {q.get('question', '')}\n")
            if q.get('type') == 'mcq':
                for opt in q.get('options', []):
                    f.write(f"   {opt}\n")
            f.write("\n")
        
        # Answer key baad mein
        f.write("\n" + "=" * 50 + "\n")
        f.write("ANSWER KEY\n")
        f.write("=" * 50 + "\n\n")
        
        for i, q in enumerate(questions, 1):
            f.write(f"Q{i}: {q.get('answer', 'N/A')}\n")
            if 'explanation' in q:
                f.write(f"   → {q['explanation']}\n")
    
    print(f"✅ Quiz saved: {path}")