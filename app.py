from flask import Flask, request, send_from_directory
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

# Public URL من Railway Variables
PUBLIC_URL = os.environ.get("PUBLIC_URL", "")

# إنشاء فولدر للملفات لو مش موجود
STATIC_DIR = 'static'
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get("text", "")
    
    if not text:
        return {"error": "No text provided"}, 400
    
    # اسم ملف فريد
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(STATIC_DIR, filename)
    
    # توليد الصوت
    tts = gTTS(text=text, lang='en')
    tts.save(filepath)
    
    # بناء الرابط الكامل
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
