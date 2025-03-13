const startRecordingBtn = document.getElementById('start-recording');
const statusText = document.getElementById('status');
const resultDiv = document.getElementById('result');

let mediaRecorder;
let audioChunks = [];
const socket = new WebSocket("ws://localhost:8000/audio");

// WebSocket message handler
socket.onmessage = (event) => {
    resultDiv.innerHTML = `Result: ${event.data}`;
};

// Start Recording
startRecordingBtn.addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            audioChunks = [];

            const reader = new FileReader();
            reader.readAsArrayBuffer(audioBlob);
            reader.onloadend = () => {
                socket.send(reader.result);
            };
        };

        mediaRecorder.start();
        statusText.innerText = "Status: Recording...";

        setTimeout(() => {
            mediaRecorder.stop();
            statusText.innerText = "Status: Processing...";
        }, 10000); // Auto-stop after 5 seconds for demo purposes

    } catch (error) {
        console.error("Error accessing microphone:", error);
        statusText.innerText = "Status: Error accessing microphone.";
    }
});
