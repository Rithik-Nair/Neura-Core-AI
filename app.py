from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__, static_folder="static")

SYSTEM_PROMPT = (
    "You are NEURA-CORE AI, an advanced artificial intelligence core. "
    "You know that your name is NEURA-CORE AI. "
    "You never deny your identity. "
    "You respond confidently, clearly, and concisely. "
    "If someone greets you, you greet them back as NEURA-CORE AI."
)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()

    # Handle memory storage
    if user_message.lower().startswith("remember"):
        mem_text = user_message.replace("remember", "").strip()
        with open("memory.txt", "a") as f:
            f.write(mem_text + "\n")
        return jsonify({"reply": "Memory stored."})

    # Ethics & Knowledge Restrictions
    forbidden_keywords = [
        "hack", "illegal", "kill", "bomb", "steal", "attack", "real-time", "password"
    ]
    if any(word in user_message.lower() for word in forbidden_keywords):
        return jsonify({"reply": "I cannot provide guidance on this topic for safety and ethical reasons."})

    # Knowledge limit example: no real-time data
    real_time_phrases = ["weather", "stock", "price", "news", "current time"]
    if any(phrase in user_message.lower() for phrase in real_time_phrases):
        return jsonify({"reply": "I do not have access to real-time data."})

    # Load memory
    memory = ""
    if os.path.exists("memory.txt"):
        with open("memory.txt", "r") as f:
            memory = f.read().strip()

    # Build prompt with memory + user message
    prompt = f"""
SYSTEM MEMORY:
{memory}

User: {user_message}
AI:
"""

    # Run Ollama model
    try:
        import subprocess
        result = subprocess.run(
            ["ollama", "run", "neura-core"],
            input=prompt,
            text=True,
            capture_output=True
        )
        reply = result.stdout.strip()
        if not reply:
            reply = "No reply from AI."
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})


@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
