import os
import subprocess
from faster_whisper import WhisperModel
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS

# --- Model Initialization ---
print("🧠 Loading Whisper Model...")
model_stt = WhisperModel("base", device="cpu")

# Map of supported languages
LANG_MODELS = {
    "fr": "Helsinki-NLP/opus-mt-en-fr",  # French
    "es": "Helsinki-NLP/opus-mt-en-es",  # Spanish
    "de": "Helsinki-NLP/opus-mt-en-de",  # German
    "hi": "Helsinki-NLP/opus-mt-en-hi",  # Hindi
    "en": "Helsinki-NLP/opus-mt-en-en",  # English (identity)
}

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def run_ffmpeg(cmd):
    process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print("❌ FFmpeg error:", process.stderr)
    return process

def extract_audio(input_video, output_audio):
    cmd = f'ffmpeg -i "{input_video}" -q:a 0 -map a "{output_audio}" -y'
    run_ffmpeg(cmd)

def split_audio(audio_path, chunk_dir, chunk_length=300):
    os.makedirs(chunk_dir, exist_ok=True)
    cmd = f'ffmpeg -i "{audio_path}" -f segment -segment_time {chunk_length} -c copy "{chunk_dir}/chunk_%03d.wav" -y'
    run_ffmpeg(cmd)
    chunks = [os.path.join(chunk_dir, f) for f in os.listdir(chunk_dir) if f.endswith(".wav")]
    chunks.sort()
    return chunks

def transcribe_audio(audio_file):
    segments, _ = model_stt.transcribe(audio_file)
    text = " ".join([seg.text for seg in segments])
    return text.strip()

def translate_text(text, target_lang):
    """Translate dynamically based on target language"""
    if target_lang not in LANG_MODELS:
        raise ValueError(f"Unsupported language code: {target_lang}")

    model_name = LANG_MODELS[target_lang]
    print(f"🌐 Loading translation model: {model_name} ...")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    print(f"🈺 Translating text → {target_lang.upper()}...")
    inputs = tokenizer([text], return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**inputs)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text

def synthesize_speech(text, lang_code, output_file):
    """Generate translated voice using Google TTS"""
    print(f"🎤 Synthesizing voice in {lang_code} ...")
    tts = gTTS(text, lang=lang_code)
    tts.save(output_file)

def merge_audio_files(audio_files, output_path):
    txt_file = os.path.join(os.path.dirname(output_path), "concat_list.txt")
    with open(txt_file, "w") as f:
        for file in audio_files:
            f.write(f"file '{os.path.abspath(file)}'\n")
    cmd = f'ffmpeg -f concat -safe 0 -i "{txt_file}" -c copy "{output_path}" -y'
    run_ffmpeg(cmd)
    os.remove(txt_file)

def merge_audio_video(video, audio, output_video):
    cmd = f'ffmpeg -i "{video}" -i "{audio}" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 "{output_video}" -y'
    run_ffmpeg(cmd)

def process_video(input_video, target_lang="fr"):
    """Full translation pipeline"""
    try:
        print(f"🚀 Starting translation pipeline for {target_lang.upper()}...")
        audio_path = os.path.join(UPLOAD_DIR, "audio.wav")
        extract_audio(input_video, audio_path)

        chunk_dir = os.path.join(UPLOAD_DIR, "chunks")
        chunks = split_audio(audio_path, chunk_dir)

        translated_chunks = []
        for idx, chunk in enumerate(chunks):
            print(f"🎙️ Processing chunk {idx + 1}/{len(chunks)}...")
            text = transcribe_audio(chunk)
            if not text:
                continue
            translated_text = translate_text(text, target_lang)
            translated_audio = os.path.join(chunk_dir, f"translated_{idx:03d}.mp3")
            synthesize_speech(translated_text, target_lang, translated_audio)
            translated_chunks.append(translated_audio)

        merged_audio = os.path.join(UPLOAD_DIR, f"merged_translated_{target_lang}.mp3")
        merge_audio_files(translated_chunks, merged_audio)

        final_video = os.path.join(UPLOAD_DIR, f"final_translated_{target_lang}.mp4")
        merge_audio_video(input_video, merged_audio, final_video)

        print(f"✅ Translation complete! File ready at: {final_video}")
        return final_video

    except Exception as e:
        print("❌ Error during processing:", e)
        return None
