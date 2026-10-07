// Voice Input & Whisper Speech-to-Text Handling

let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;

async function toggleVoiceRecording(lang = "en") {
    const recordBtn = document.getElementById("recordVoiceBtn");
    const statusText = document.getElementById("voiceStatusText");
    const symptomArea = document.getElementById("symptom_text");

    if (!isRecording) {
        // Start Recording
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioChunks = [];
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                if (statusText) statusText.innerText = "Transcribing speech with OpenAI Whisper...";
                
                const formData = new FormData();
                formData.append("audio", audioBlob, "voice_input.wav");
                formData.append("language", lang);

                try {
                    const res = await fetch("/api/speech/transcribe", {
                        method: "POST",
                        body: formData
                    });
                    const data = await res.json();
                    if (data.success && data.text) {
                        if (symptomArea) {
                            symptomArea.value = data.text;
                        }
                        if (statusText) statusText.innerText = "✅ Speech transcribed successfully! Please review and submit.";
                    } else {
                        if (statusText) statusText.innerText = "⚠️ " + (data.error || "Could not transcribe audio. Please type symptoms.");
                    }
                } catch (err) {
                    console.error("Transcription error:", err);
                    if (statusText) statusText.innerText = "Voice service unavailable. Please use text input.";
                }
            };

            mediaRecorder.start();
            isRecording = true;
            if (recordBtn) {
                recordBtn.innerText = "⏹️ Stop Recording";
                recordBtn.classList.add("btn-danger");
                recordBtn.classList.remove("btn-primary");
            }
            if (statusText) statusText.innerText = "🔴 Listening... Speak clearly in your selected language.";
        } catch (err) {
            console.error("Microphone access error:", err);
            if (statusText) statusText.innerText = "Microphone access denied. Please type your symptoms.";
        }
    } else {
        // Stop Recording
        if (mediaRecorder && mediaRecorder.state !== "inactive") {
            mediaRecorder.stop();
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
        isRecording = false;
        if (recordBtn) {
            recordBtn.innerText = "🎙️ Record Voice";
            recordBtn.classList.remove("btn-danger");
            recordBtn.classList.add("btn-primary");
        }
    }
}
