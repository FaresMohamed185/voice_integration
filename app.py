from flask import Flask, request, send_from_directory
import edge_tts
import asyncio
import os
import uuid

app = Flask(__name__)

PUBLIC_URL = os.environ.get("PUBLIC_URL", "")

STATIC_DIR = 'static'
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get("text", "")
    
    if not text:
        return {"error": "No text provided"}, 400
    
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(STATIC_DIR, filename)
    
    # edge-tts أسرع بكتير
    async def generate():
        communicate = edge_tts.Communicate(text, "en-US-JennyNeural")
        await communicate.save(filepath)
    
    asyncio.run(generate())
    
    audio_url = f"{PUBLIC_URL}/static/{filename}"
    
    return {
        "status": "success",
        "audio_url": audio_url
    }

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)

@app.route('/health')
def health():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
