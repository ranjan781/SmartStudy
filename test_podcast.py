"""Test script to verify podcast audio generation."""
import os
import sys

# Change to the application directory if not already there
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from modules.podcast_gen import create_podcast

# Short dummy summary text to speed up processing
sample_summary = '''
The solar system consists of the Sun and the objects that orbit it. 
Key topics include:
- The Sun: A G-type main-sequence star.
- Inner Planets: Mercury, Venus, Earth, Mars (rocky planets).
- Outer Planets: Jupiter, Saturn, Uranus, Neptune (gas/ice giants).
'''

try:
    print("Testing podcast generation...")
    # This will trigger Gemini script generation first, then Kokoro audio gen, then Pydub merge.
    output_file = create_podcast(sample_summary)
    print(f"✅ Success! Podcast generated at: {output_file}")
    
    # Check if the file actually exists and is not empty
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        print(f"File verified. Size: {os.path.getsize(output_file)} bytes")
    else:
        print("❌ Error: Audio file is missing or empty.")
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
