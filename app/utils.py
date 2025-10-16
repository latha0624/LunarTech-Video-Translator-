import subprocess, os, yaml

def load_config(path="config.yaml"):
    try:
        with open(path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"⚠️ Error loading config: {e}")
        return None

def run_ffmpeg(cmd):
    process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print("FFmpeg Error:", process.stderr)
    return process

def split_video(input_path, chunk_dir, segment_time):
    os.makedirs(chunk_dir, exist_ok=True)
    cmd = f'ffmpeg -i "{input_path}" -f segment -segment_time {segment_time} -c copy "{chunk_dir}/chunk_%03d.mp4"'
    run_ffmpeg(cmd)

def get_duration(path):
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{path}"'
    process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return float(process.stdout.strip())

def sync_audio_to_video(audio, target_dur, output):
    current = get_duration(audio)
    ratio = target_dur / current if current > 0 else 1
    cmd = f'ffmpeg -i "{audio}" -filter:a "atempo={min(max(ratio,0.5),2.0)}" -y "{output}"'
    run_ffmpeg(cmd)
