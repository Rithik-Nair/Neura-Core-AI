from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import requests
from threading import Thread

app = Flask(__name__, static_folder="static")

# =========================
# NEURA-CORE SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = (
    "You are NEURA-CORE AI, an advanced artificial intelligence core. "
    "You know that your name is NEURA-CORE AI. "
    "You never deny your identity. "
    "You respond confidently, clearly, and concisely. "
    "If someone greets you, you greet them back as NEURA-CORE AI."
)

# =========================
# ELEVENLABS CONFIG
# =========================
API_KEY_FILE = "neura-core-ai-api.txt"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
AUDIO_PATH = "static/neura-core.mp3"

if os.path.exists(API_KEY_FILE):
    with open(API_KEY_FILE, "r") as f:
        ELEVEN_API_KEY = f.read().strip()
else:
    ELEVEN_API_KEY = None
    print("⚠️ ElevenLabs API key not found.")

# =========================
# ELEVENLABS TTS FUNCTION
# =========================
def speak_elevenlabs(text):
    """Generate and save ElevenLabs TTS audio with debug logs."""
    if not ELEVEN_API_KEY or not text:
        print("⚠️ API key missing or empty text. TTS skipped.")
        return

    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            "xi-api-key": ELEVEN_API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {
                "stability": 0.45,
                "similarity_boost": 0.8
            }
        }

        print("🔹 Sending request to ElevenLabs...")
        response = requests.post(url, json=data, headers=headers)

        print("🔹 Response status code:", response.status_code)
        if response.status_code != 200:
            print("❌ ElevenLabs error response:",response.content.decode("utf-8", errors="ignore"))
            return

        # Save MP3
        if not os.path.exists("static"):
            os.makedirs("static")
        audio_path = "static/neura-core.mp3"
        with open(audio_path, "wb") as f:
            f.write(response.content)
        print(f"✅ MP3 saved at {audio_path}")

    except Exception as e:
        print("❌ ElevenLabs exception:", e)


# =========================
# CHAT ROUTE
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please say something."})

    # -------- MEMORY STORE --------
    if user_message.lower().startswith("remember"):
        memory_text = user_message.replace("remember", "").strip()
        with open("memory.txt", "a", encoding="utf-8") as f:
            f.write(memory_text + "\n")
        return jsonify({"reply": "Memory stored successfully."})

    # -------- SAFETY FILTER --------
    forbidden_keywords = [
        "hack", "illegal", "kill", "bomb", "steal",
        "attack", "password", "real-time"
    ]

    if any(word in user_message.lower() for word in forbidden_keywords):
        return jsonify({
            "reply": "I cannot assist with this request due to safety and ethical reasons."
        })

    # -------- LOAD MEMORY --------
    memory = ""
    if os.path.exists("memory.txt"):
        with open("memory.txt", "r", encoding="utf-8") as f:
            memory = f.read().strip()

    # -------- BUILD PROMPT --------
    prompt = f"""
{SYSTEM_PROMPT}

SYSTEM MEMORY:
{memory}

User: {user_message}
AI:
"""

    # -------- RUN OLLAMA --------
    try:
        result = subprocess.run(
            ["ollama", "run", "neura-core"],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=160
        )

        reply = result.stdout.strip()
        if not reply:
            reply = "I did not receive a response."

    except Exception as e:
        reply = f"Error: {str(e)}"

    # -------- SPEAK IN BACKGROUND --------
    Thread(
        target=speak_elevenlabs,
        args=(reply,),
        daemon=True
    ).start()

    return jsonify({"reply": reply})

# =========================
# FRONTEND
# =========================
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(port=5000, debug=True)
