const sendBtn = document.getElementById("send");
const msgInput = document.getElementById("msg");
const chat = document.getElementById("chat");
const head = document.getElementById("ai-head");

let audio = null;

/* =========================
   PLAY ELEVENLABS AUDIO
   ========================= */
function playVoice() {
    // Stop previous audio if playing
    if (audio) {
        audio.pause();
        audio = null;
    }

    // Cache-busting so new audio loads every time
    audio = new Audio("/static/neura-core.mp3?t=" + Date.now());

    // Lip sync ON
    head.classList.add("talking");

    audio.play()
        .then(() => {
            // Lip sync OFF when audio ends
            audio.onended = () => {
                head.classList.remove("talking");
            };
        })
        .catch(err => {
            console.log("Audio play blocked:", err);
            head.classList.remove("talking");
        });
}

/* =========================
   SEND MESSAGE
   ========================= */
async function sendMessage() {
    const msg = msgInput.value.trim();
    if (!msg) return;

    // Show user message
    chat.innerHTML += `<p><b>You:</b> ${msg}</p>`;
    msgInput.value = "";
    chat.scrollTop = chat.scrollHeight;

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg })
        });

        const data = await res.json();

        // Show AI message with typing effect
        const aiMsg = document.createElement("p");
        aiMsg.innerHTML = "<b>AI:</b> ";
        chat.appendChild(aiMsg);

        await typeText(aiMsg, data.reply);

        // 🔊 Play ElevenLabs audio AFTER response
        playVoice();

    } catch (err) {
        chat.innerHTML += `<p style="color:red;"><b>System:</b> AI offline</p>`;
        console.error(err);
    }

    chat.scrollTop = chat.scrollHeight;
}

/* =========================
   EVENT LISTENERS
   ========================= */
sendBtn.addEventListener("click", sendMessage);

msgInput.addEventListener("keydown", e => {
    if (e.key === "Enter") sendMessage();
});

/* =========================
   TYPING EFFECT
   ========================= */
function typeText(element, text) {
    return new Promise(resolve => {
        let i = 0;
        const interval = setInterval(() => {
            element.innerHTML += text[i];
            i++;
            if (i >= text.length) {
                clearInterval(interval);
                resolve();
            }
        }, 30);
    });
}
