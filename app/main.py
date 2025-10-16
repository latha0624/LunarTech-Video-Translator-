from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from app.pipeline import process_video

app = Flask(__name__)

# === Upload Directory ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    """Render main page"""
    success = request.args.get("success")
    output_file = request.args.get("file")
    return render_template("index.html", success=success, output_file=output_file)


@app.route("/translate", methods=["POST"])
def translate():
    """Handle upload and translation"""
    try:
        if "file" not in request.files:
            return "No file uploaded", 400

        file = request.files["file"]
        lang = request.form.get("language")

        if not file or file.filename == "":
            return "No file selected", 400

        video_path = os.path.join(UPLOAD_DIR, file.filename)
        file.save(video_path)
        print(f"🚀 Received file: {video_path}")

        # Run translation pipeline
        output_path = process_video(video_path, lang)

        if output_path and os.path.exists(output_path):
            print(f"✅ Translation complete: {output_path}")
            output_name = os.path.basename(output_path)
            return redirect(url_for("index", success=1, file=output_name))
        else:
            print("❌ Translation failed — output not found.")
            return redirect(url_for("index", success=0))

    except Exception as e:
        print("❌ Error during processing:", e)
        return f"Error: {e}", 500


@app.route("/download/<filename>")
def download(filename):
    """Serve translated video for download"""
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404


if __name__ == "__main__":
    app.run(debug=True)
