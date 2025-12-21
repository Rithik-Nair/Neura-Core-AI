const sendBtn = document.getElementById("send");
const msgInput = document.getElementById("msg");
const chat = document.getElementById("chat");
const head = document.getElementById("ai-head");

async function sendMessage() {
    const msg = msgInput.value.trim();
    if (!msg) return;

    chat.innerHTML += `<p><b>You:</b> ${msg}</p>`;
    
    msgInput.value = "";
    chat.scrollTop = chat.scrollHeight;

    try {
        // MODEL THINKING (NO LIP MOVEMENT)
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg })
        });

        const data = await res.json();

        // START SPEAKING
        head.classList.add("talking");

        const aiMsg = document.createElement("p");
        aiMsg.innerHTML = "<b>AI:</b> ";
        chat.appendChild(aiMsg);

        await typeText(aiMsg, data.reply);

        // STOP SPEAKING
        head.classList.remove("talking");

    } catch {
        chat.innerHTML += `<p style="color:red;"><b>System:</b> AI offline</p>`;
    }

    chat.scrollTop = chat.scrollHeight;
}

sendBtn.addEventListener("click", sendMessage);
msgInput.addEventListener("keydown", e => {
    if (e.key === "Enter") sendMessage();
});

// Typing effect synced with lip movement
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
        }, 30); // speaking speed
    });
}

function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);

    // Voice settings
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.volume = 1;

    // Select a good voice if available
    const voices = speechSynthesis.getVoices();
    const preferred = voices.find(v => v.name.includes("Male") || v.name.includes("David"));
    if (preferred) utterance.voice = preferred;

    // Lip sync ON
    utterance.onstart = () => {
        mouth.classList.add("talking");
        mouth.style.opacity = "1";
    };

    // Lip sync OFF
    utterance.onend = () => {
        mouth.classList.remove("talking");
        mouth.style.opacity = "0";
    };

    speechSynthesis.speak(utterance);
}
