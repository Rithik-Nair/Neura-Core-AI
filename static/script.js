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
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg })
        });

        const data = await res.json();

        const aiMsg = document.createElement("p");
        aiMsg.innerHTML = "<b>AI:</b> ";
        chat.appendChild(aiMsg);
        await typeText(aiMsg, data.reply);

        speak(data.reply);

    } catch {
        chat.innerHTML += `<p style="color:red;"><b>System:</b> AI offline</p>`;
    }

    chat.scrollTop = chat.scrollHeight;
}

sendBtn.addEventListener("click", sendMessage);
msgInput.addEventListener("keydown", e => {
    if (e.key === "Enter") sendMessage();
});

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

function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;

    utterance.onstart = () => head.classList.add("talking");
    utterance.onend = () => head.classList.remove("talking");

    speechSynthesis.cancel(); // stop previous speech
    speechSynthesis.speak(utterance);
}
