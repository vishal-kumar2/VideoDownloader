from flask import Flask, request, send_file, jsonify, render_template
import yt_dlp
import uuid
import os
from flask import after_this_request
app = Flask(__name__)

DOWNLOAD_FOLDER=os.path.join(os.getcwd(),"downloads")
os.makedirs(DOWNLOAD_FOLDER,exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

# Video download route
@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get("url")
    quality = data.get("quality", "best")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    filename = f"video_{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    try:
        # Step 1: Extract info about formats
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])

        # Step 2: Pick format string
        if quality == "best":
            fmt = "bestvideo+bestaudio/best"
        else:
            # Find closest format <= requested height
            selected = None
            q = int(quality)
            for f in formats:
                if f.get("height") and f["height"] <= q and f.get("acodec") != "none":
                    selected = f["format_id"]
            fmt = selected if selected else "best"   # fallback

        # Step 3: Download
        ydl_opts = {
            'format': fmt,
            'outtmpl': filepath,
            'noplaylist': True,
            'merge_output_format': 'mp4'   # ensures audio+video merge
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        @after_this_request
        def remove_file(response):
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                print(f"Error deleting file: {e}")
            return response

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)