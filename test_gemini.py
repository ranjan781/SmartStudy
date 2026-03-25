"""Quick API key validation test using Groq."""
from dotenv import load_dotenv
load_dotenv()
import os
print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY", "NOT SET")[:15] + "...")

from modules.gemini_client import generate_with_retry

print("\nTesting Groq API with simple prompt...")
try:
    result = generate_with_retry("Say hello in 5 words.", max_tokens=50, temperature=0.1)
    print(f"API Response: {result}")
    print("\n✅ API IS VALID AND WORKING!")
except Exception as e:
    print(f"\n❌ API ERROR: {e}")
