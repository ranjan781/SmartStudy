"""
modules/podcast_gen.py
Summary se podcast script generate karta hai using Google Gemini
and converts to audio using Kokoro TTS.
"""

import os
import json
from modules.gemini_client import generate_with_retry

PODCAST_PROMPT = """
Create a 5-minute educational podcast discussing this study material.

Host A (Priya): curious, asks probing questions
Host B (Arjun): knowledgeable, explains clearly with real examples

Return ONLY a JSON array — no markdown, no extra text, no code fences:
[
  {{"speaker": "A", "line": "..."}},
  {{"speaker": "B", "line": "..."}}
]

Aim for 20-25 turns. Cover all key topics naturally.

Content: {summary}
"""

def generate_script(summary_text):
    """Gemini se podcast script banata hai"""
    raw = generate_with_retry(PODCAST_PROMPT.format(summary=summary_text), max_tokens=3000, temperature=0.7)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()
    
    script = json.loads(raw)
    print(f"✅ Script ready — {len(script)} turns")
    return script

def generate_audio(script, output_dir="outputs/audio_clips"):
    """Har dialogue turn ke liye audio file banata hai"""
    try:
        import soundfile as sf
        from kokoro import KPipeline
    except ImportError:
        raise ImportError(
            "Kokoro TTS and soundfile are required for podcast audio. "
            "Install with: pip install kokoro soundfile"
        )
    
    os.makedirs(output_dir, exist_ok=True)
    pipeline_a = KPipeline(lang_code='a')
    
    audio_files = []
    for i, turn in enumerate(script):
        speaker = turn["speaker"]
        line = turn["line"]
        filename = f"{output_dir}/turn_{i:03d}_{speaker}.wav"
        voice = "af_heart" if speaker == "A" else "am_fenrir"
        
        generator = pipeline_a(line, voice=voice)
        for _, _, audio in generator:
            sf.write(filename, audio, 24000)
            break
        
        audio_files.append(filename)
        print(f"  🎙️ Turn {i+1}: Speaker {speaker} — done")
    
    return audio_files

def merge_audio(audio_files, output_path="outputs/podcast.mp3"):
    """Sab audio clips ko merge karta hai"""
    try:
        from pydub import AudioSegment
        import imageio_ffmpeg
        AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        raise ImportError("pydub and imageio-ffmpeg are required. Install with: pip install pydub imageio-ffmpeg")
    
    combined = AudioSegment.empty()
    silence = AudioSegment.silent(duration=400)
    
    for wav_file in audio_files:
        clip = AudioSegment.from_wav(wav_file)
        combined += clip + silence
    
    combined.export(output_path, format="mp3")
    print(f"✅ Podcast ready: {output_path}")
    return output_path

def create_podcast(summary_text):
    """Full podcast pipeline"""
    print("📝 Script generate kar raha hoon...")
    script = generate_script(summary_text)
    
    print("🎙️ Audio clips bana raha hoon...")
    audio_files = generate_audio(script)
    
    print("🎵 Sab clips merge kar raha hoon...")
    final_mp3 = merge_audio(audio_files)
    
    return final_mp3