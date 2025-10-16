import subprocess
from faster_whisper import WhisperModel
from transformers import pipeline
import asyncio
from edge_tts import Communicate

# <-- ADD THIS LINE BELOW -->
ffmpeg_path = r"C:\Users\latha\Downloads\ffmpeg-8.0-essentials_build\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe"

# 1. Extract first 10 s of audio from a video
subprocess.run([ffmpeg_path, "-y", "-i", "input.mp4", "-t", "10", "-ar", "16000", "-ac", "1", "sample.wav"])

# 2. Speech-to-text
model = WhisperModel("tiny", device="cpu")
segments, _ = model.transcribe("sample.wav")
text = " ".join([s.text for s in segments])
print("Original text:", text)

# 3. Translate to French
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")
translated = translator(text)[0]["translation_text"]
print("Translated:", translated)

# 4. Text-to-speech
async def speak(text):
    c = Communicate(text, voice="fr-FR-DeniseNeural")
    await c.save("tts.wav")

asyncio.run(speak(translated))
print("✅  tts.wav generated")