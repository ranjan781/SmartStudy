"""
modules/gemini_client.py
Shared API client with automatic retry and rate limit handling.
(Migrated from Gemini to Groq)
"""

from groq import Groq
import os
import time
import random
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_model(model_name="llama-3.3-70b-versatile"):
    """Returns the Groq model name to be used for completions."""
    return model_name

# Global variable to track last API call time
_last_call_time = 0
_MIN_CALL_GAP = 1.0  # minimum seconds between calls

def _rate_limit():
    """Ensure a minimum gap between consecutive API calls to avoid rate limits."""
    global _last_call_time
    now = time.time()
    elapsed = now - _last_call_time
    if elapsed < _MIN_CALL_GAP:
        sleep_time = _MIN_CALL_GAP - elapsed
        time.sleep(sleep_time)
    _last_call_time = time.time()

def generate_with_retry(prompt, max_tokens=2000, temperature=0.3, max_retries=5):
    """
    Calls Groq API with automatic retry on rate limit errors.
    Uses exponential backoff with jitter for retries.
    """
    model_name = get_model()
    
    for attempt in range(max_retries):
        try:
            # Apply rate limiting before each attempt
            _rate_limit()
            
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model_name,
                temperature=temperature,
                max_completion_tokens=max_tokens,
            )
            
            if response and response.choices and response.choices[0].message.content:
                return response.choices[0].message.content
                
            raise Exception("Empty response from Groq API")
            
        except Exception as e:
            error_str = str(e)
            # Check for rate limit / quota errors (429)
            if "429" in error_str or "rate limit" in error_str.lower() or "quota" in error_str.lower():
                # Exponential backoff with jitter: base 5s, max 60s
                base_wait = min(5 * (2 ** attempt), 60)
                jitter = random.uniform(0.8, 1.2)
                wait_time = int(base_wait * jitter)
                print(f"⏳ Rate limited — waiting {wait_time}s before retry {attempt + 1}/{max_retries}...")
                time.sleep(wait_time)
                # If this is the last retry, wait longer and give a suggestion
                if attempt == max_retries - 1:
                    print("💡 Tip: Check your Groq API quota and limits.")
            elif "Empty response" in error_str and attempt < max_retries - 1:
                print(f"⚠️ Empty response — retrying {attempt + 1}/{max_retries}...")
                time.sleep(2)
            else:
                print(f"❌ API error: {error_str[:200]}")
                raise e
    
    # If we exit the loop, all retries have been exhausted
    raise Exception(
        "Max retries exceeded due to persistent rate limiting. "
        "Please check your API key and quota. "
        "Wait a few minutes before trying again."
    )
