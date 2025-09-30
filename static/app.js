// Get elements
const fileInput = document.getElementById("fileUpload");
const uploadBtn = document.getElementById("upload-btn");
const uploadStatus = document.getElementById("upload-status");
const userInput = document.getElementById("question");
const sendBtn = document.getElementById("ask-btn");
const chatBox = document.getElementById("chat");

// Handle PDF upload
uploadBtn.addEventListener("click", async () => {
    if (!fileInput.files[0]) {
        uploadStatus.textContent = "Please select a PDF first.";
        return;
    }
    uploadBtn.disabled = true;
    uploadStatus.textContent = "Uploading...";

    const form = new FormData();
    form.append("file", fileInput.files[0]);

    try {
        const res = await fetch("/upload", { method: "POST", body: form });
        const data = await res.json();
        if (data.status === "uploaded") {
            uploadStatus.textContent = `Uploaded ✓ — ${data.chunks} chunk(s) stored.`;
        } else {
            uploadStatus.textContent = `Error: ${data.message || JSON.stringify(data)}`;
        }
    } catch (err) {
        uploadStatus.textContent = `Upload failed: ${err}`;
    }

    uploadBtn.disabled = false;
});

// Handle question ask
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    appendMsg(text, "user");
    userInput.value = "";
    sendBtn.disabled = true;

    const form = new FormData();
    form.append("question", text);

    try {
        const res = await fetch("/ask", { method: "POST", body: form });
        const data = await res.json();
        appendMsg(data.answer, "bot");
    } catch (err) {
        appendMsg(`Error: ${err}`, "bot");
    }

    sendBtn.disabled = false;
}

// Append messages in chat box
function appendMsg(text, cls) {
    const div = document.createElement("div");
    div.className = `message ${cls}`;
    div.textContent = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Event listeners
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});
