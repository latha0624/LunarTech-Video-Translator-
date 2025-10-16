# LunarTech Standard Video Translator (Octavia — Beyond Nations)

An end-to-end AI video translation and dubbing system built as part of the **LunarTech Software Engineering Apprenticeship – Fall 2025**.  
It automatically translates and dubs marketing videos while maintaining perfect timing, natural voice quality, and synchronization fidelity.

---

## 🚀 Overview

This project demonstrates the full engineering workflow of a **Standard Video Translator** — from media ingestion to AI dubbing and synchronized output.  
It uses open-source AI models for Speech-to-Text (STT), Translation, and Text-to-Speech (TTS), orchestrated through a modular Python + Flask pipeline.

### ✨ Key Features
- Upload any video (MP4, MOV, AVI)
- Automatic transcription using **Whisper**
- Neural translation via **Hugging Face MarianMT**
- Voice synthesis with **gTTS**
- Seamless dubbing and export with **FFmpeg**
- Real-time progress UI and download link

---

## 📁 Project Structure

| File | Description |
|------|--------------|
| `run.py` | Launches the Flask web application |
| `app/main.py` | Defines routes, handles uploads, triggers the translation pipeline |
| `app/pipeline.py` | Core AI workflow (FFmpeg + Whisper + Translation + TTS + Muxing) |
| `app/templates/index.html` | Front-end upload and processing UI |
| `uploads/` | Temporary input/output storage for videos and audio chunks |

---

## ⚙️ Installation & Setup

### 1️⃣ Prerequisites
- Python **3.10+**
- **FFmpeg** installed (`ffmpeg --version`)
- Virtual environment recommended
- Optional GPU for faster transcription

---

### 2️⃣ Clone the Repository
```bash
git clone <your-private-repo-url>
cd lunartech-video-translator
```
---

### 3️⃣ Create & Activate Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Verify FFmpeg Installation

```bash
ffmpeg -version
```

If not found, install FFmpeg:

**Windows**

```bash
winget install Gyan.FFmpeg
```

**macOS**

```bash
brew install ffmpeg
```

**Linux**

```bash
sudo apt install ffmpeg
```

---

### 6️⃣ Run the Application

```bash
python run.py
```

Then open your browser at:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧩 How It Works

1. User uploads a video file (.mp4).
2. FFmpeg extracts the original audio.
3. Whisper (STT) transcribes speech to text.
4. MarianMT translates the text into the target language.
5. gTTS generates natural speech from the translation.
6. FFmpeg merges the dubbed audio with the original video.
7. The app exports a synchronized, translated MP4 ready for download.

---

## 🌍 Supported Languages

| Code | Language |
| ---- | -------- |
| en   | English  |
| fr   | French   |
| es   | Spanish  |
| de   | German   |
| hi   | Hindi    |

---

## 🧠 Usage Guide

1. Launch the app (`python run.py`)
2. Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)**
3. Upload a video file (MP4 format)
4. Select your target translation language
5. Click **Translate Video**
6. Wait for processing — the UI shows “Processing your video...”
7. Once completed, a **Download Translated Video** link appears

---

## 🧾 Example Output

| Input            | Output                                     |
| ---------------- | ------------------------------------------ |
| `promo_clip.mp4` | `translated_fr.mp4`                        |
| `uploads/`       | Directory where processed files are stored |

---

## 🛠️ Troubleshooting

| Issue                        | Cause / Fix                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| `ffmpeg not found`           | Install FFmpeg and ensure it’s in PATH                       |
| `googletrans/httpx error`    | Run `pip install httpx==0.13.3` to fix dependency mismatch   |
| No sound in output           | Ensure input video has audio; re-run process                 |
| Translation still in English | Confirm correct language code (e.g., `fr`, `es`, `de`, `hi`) |
| Long videos truncated        | Increase chunk length or verify disk space                   |

---

## 🔮 Future Enhancements

* Multi-threaded STT/TTS for faster long-video processing
* Replace **gTTS** with **Edge-TTS** or **Coqui-TTS** for richer voice tone
* Integrate **Wav2Lip** for accurate lip-sync
* Docker packaging for one-command deployment
* Add structured JSON logging and checkpoint resume system

---

## 🧱 Engineering Notes

* Modular design with clearly separated STT, Translation, TTS, and Sync stages
* Safe temp-file handling inside `uploads/`
* Handles long videos by chunking and merging results
* Automatic cleanup of intermediate files
* Supports resumability and error recovery
* Logs progress and errors in the console

---

## 🧮 Evaluation Rubric Reference (Mentor Use)

| Category                     | Points      |
| ---------------------------- | ----------- |
| Voice Quality                | 25          |
| Translation Fidelity         | 20          |
| Lip-Sync & Duration Accuracy | 20          |
| Functionality & Stability    | 15          |
| UX & Visual Design           | 10          |
| Code Quality & Modularity    | 10          |
| **Total**                    | **100 pts** |

### ✅ Pass Conditions

* Output duration matches input (± 1 frame)
* Full pipeline runs end-to-end without crashes
* Demo video ≥ 10 minutes showing upload → process → export

---

## 🎥 Demo Video Guide (For Submission)

When recording your **10-minute demo** (Unlisted YouTube or Private Drive):

**Show:**

* Launching the Flask app
* Uploading the **LunarTech PR video**
* Selecting a target language (e.g., French)
* Console showing pipeline progress
* The “Processing...” UI updating to “Download Translated Video”
* Downloading and previewing a short dubbed clip (10–30 seconds)
* Demonstrating duration match

**Explain:**

* Tools and models chosen (Whisper, MarianMT, gTTS, FFmpeg)
* Trade-offs between quality and speed
* Logs and metrics (timing, sync, errors)
* Known limitations and improvements

---

## 🔒 Confidentiality & Ethics

* This project and all media assets are **confidential LunarTech materials**.
* **Do not** publish the video, code, or results publicly.
* Delete local copies within **7 days** of review unless instructed otherwise.
* Only private submission to mentors is permitted.

---

## 🙏 Acknowledgements

* **Mentor:** Dr. Kevin Matthews
* **Program:** LunarTech Software Engineering Apprenticeship – Fall 2025
* **Project:** Octavia — Beyond Nations
* **Author:** *Your Name*

---

## 📜 License

This project is licensed under **LunarTech Private Educational License**.
Redistribution or public sharing of code, media, or outputs is strictly prohibited.

```









