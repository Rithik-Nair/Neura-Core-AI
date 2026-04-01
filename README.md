## *🧠 Neura Core AI*
Neura Core AI is a ChatGPT-like conversational AI system built using a locally hosted LLM (Ollama).
It enables intelligent, context-aware conversations with a lightweight and modular architecture.

```
🚀 Features
💬 ChatGPT-style chat interface
🧠 Context-aware responses using memory
⚡ Runs locally using Ollama (no API cost)
💾 Persistent chat storage (memory.txt)
🎯 Custom AI personality via Modelfile
🖥️ Simple and clean UI

🏗️ Project Structure
Neura-Core-AI/
│
├── static/
│   ├── avatar/
│   │   └── head.png
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── logo.png
│
├── app.py          # Backend server
├── memory.txt      # Stores chat history
├── Modelfile       # Ollama model configuration
└── README.md

```

## *⚙️ Tech Stack*
```
Frontend: HTML, CSS, JavaScript
Backend: Python (Flask)
LLM: Ollama (Local Large Language Model)
Storage: Text-based memory (memory.txt)
```

## *🧠 How It Works*
User enters a message in the UI
script.js sends the request to backend (app.py)
Backend reads previous conversation from memory.txt
Context + user input is sent to Ollama
AI generates a response
Response is saved and displayed
## *🔧 Setup Instructions*
1. Clone the Repository
git clone https://github.com/your-username/neura-core-ai.git
cd neura-core-ai
2. Install Dependencies
pip install flask requests
3. Install Ollama

Download and install from: https://ollama.com

4. Create Custom Model

After editing the Modelfile, run:

ollama create neura-core-ai -f Modelfile
5. Run Ollama Model
ollama run neura-core-ai
6. Run the Backend Server
python app.py
7. Open the Application
Open static/index.html in your browser
OR
Go to: http://127.0.0.1:5000 (if served via Flask)
📂 Memory System
Conversations are stored in memory.txt
Enables basic context awareness
Can be extended to advanced memory systems
🧠 Custom Model (Modelfile)

```

You can customize:

AI personality
Tone and style
Behavior and responses

After changes:

ollama create neura-core-ai -f Modelfile
ollama run neura-core-ai

```

## 👨‍💻 Author

Rithik Nair
AI Developer

```
```

## *⭐ Acknowledgements*
Ollama for local LLM support
Open-source AI community
