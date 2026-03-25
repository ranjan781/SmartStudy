"""
test_extractor.py
modules/extractor.py ko test karne ke liye quick script.
"""

from modules.extractor import extract_text

# --- Test 1: PDF file ---
print("=" * 50)
print("TEST 1: PDF Extract")
print("=" * 50)

try:
    text = extract_text("sample.pdf")
    print(f"Total characters extracted: {len(text)}")
    print("\nPehle 500 characters:")
    print("-" * 30)
    print(text[:500])
except FileNotFoundError as e:
    print(f"[ERROR] {e}")
    print("Tip: 'sample.pdf' project folder mein rakhna na bhoolen.")
except ImportError as e:
    print(f"[ERROR] {e}")
except Exception as e:
    print(f"[ERROR] Unexpected error: {e}")

# --- Test 2: TXT file (optional) ---
print("\n" + "=" * 50)
print("TEST 2: TXT Extract (sample.txt agar ho toh)")
print("=" * 50)

try:
    txt = extract_text("sample.txt")
    print(f"Total characters: {len(txt)}")
    print(txt[:500])
except FileNotFoundError:
    print("[SKIP] sample.txt nahi mili — skip kar rahe hain.")
except Exception as e:
    print(f"[ERROR] {e}")

# --- Test 3: Unsupported format ---
print("\n" + "=" * 50)
print("TEST 3: Unsupported Format (.docx)")
print("=" * 50)

try:
    extract_text("sample.docx")
except ValueError as e:
    print(f"[EXPECTED ERROR] {e}")
except FileNotFoundError as e:
    print(f"[EXPECTED ERROR] {e}")
