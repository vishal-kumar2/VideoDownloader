from flask import Flask, request, send_file, jsonify, render_template_string
import yt_dlp
import uuid
import os

app = Flask(__name__)

# Serve HTML with UTF-8 encoding
@app.route('/')
def index():
    with open("index.html", encoding="utf-8") as f:
        return render_template_string(f.read())

# Video download route
@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get("url")
    quality = data.get("quality", "best")  # default to best

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    filename = f"video_{uuid.uuid4()}.mp4"

    # Build yt-dlp format string based on selected quality
    if quality == "best":
        fmt = "best"
    else:
        fmt = f"bestvideo[height<={quality}]+bestaudio/best"

    ydl_opts = {
        'format': fmt,
        'outtmpl': filename,
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        @after_this_request
        def remove_file(response):
            try:
                if os.path.exists(filename):
                    os.remove(filename)
            except Exception as e:
                print(f"Error deleting file: {e}")
            return response

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
