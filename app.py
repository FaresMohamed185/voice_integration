from flask import Flask, request, send_from_directory
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

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

    # اسم ملف فريد عشان الملفات متدخلش في بعضها
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(STATIC_DIR, filename)

    # توليد الصوت
    tts = gTTS(text=text, lang='en')
    tts.save(filepath)

    # بناء الرابط الكامل للملف
    audio_url = f"{request.host_url}static/{filename}"

    # الرد اللي هيروح لـ n8n ومنه للأبلكيشن
    return {
        "status": "success",
        "audio_url": audio_url
    }

# نود عشان تسمح للأبلكيشن إنه يفتح الرابط ويحمل الملف
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)

if __name__ == '__main__':
    # ريل واي بيستخدم بورت 3000 أو المتغير البيئي PORT
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
