// Voice Input & Whisper Speech-to-Text State Machine Handling

let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;
let recordedMimeType = "audio/webm";
let fileExtension = "webm";

// Helper to set Voice UI state cleanly
function setVoiceUIState(state, message = "", errorMsg = "") {
    const recordBtn = document.getElementById("recordVoiceBtn");
    const statusText = document.getElementById("voiceStatusText");

    if (!recordBtn) return;

    switch (state) {
        case "idle":
            recordBtn.disabled = false;
            recordBtn.innerText = "🎙️ Record Voice";
            recordBtn.className = "btn btn-primary btn-sm";
            if (statusText && message) statusText.innerText = message;
            break;

        case "recording":
            recordBtn.disabled = false;
            recordBtn.innerText = "🔴 Stop Recording";
            recordBtn.className = "btn btn-danger btn-sm";
            if (statusText) statusText.innerText = message || "🔴 Recording your symptoms... Speak clearly in your selected language.";
            break;

        case "processing":
            recordBtn.disabled = true;
            recordBtn.innerText = "⏳ Transcribing...";
            recordBtn.className = "btn btn-primary btn-sm";
            if (statusText) statusText.innerText = "⏳ Transcribing speech with OpenAI Whisper...";
            break;

        case "success":
            recordBtn.disabled = false;
            recordBtn.innerText = "🎙️ Record Again";
            recordBtn.className = "btn btn-primary btn-sm";
            if (statusText) statusText.innerText = message || "✓ Transcription complete. Please review and edit your symptoms below before proceeding.";
            break;

        case "error":
            recordBtn.disabled = false;
            recordBtn.innerText = "🎙️ Try Again";
            recordBtn.className = "btn btn-primary btn-sm";
            if (statusText) statusText.innerText = errorMsg || "⚠️ Unable to transcribe audio. Please try again or enter symptoms using text.";
            break;
    }
}

// Detect best supported MIME type for browser
function getSupportedMimeType() {
    if (typeof MediaRecorder === "undefined") {
        return null;
    }
    const types = [
        { mime: "audio/webm;codecs=opus", ext: "webm" },
        { mime: "audio/webm", ext: "webm" },
        { mime: "audio/mp4", ext: "mp4" },
        { mime: "audio/ogg;codecs=opus", ext: "ogg" },
        { mime: "audio/wav", ext: "wav" }
    ];
    for (const t of types) {
        if (MediaRecorder.isTypeSupported(t.mime)) {
            return t;
        }
    }
    return { mime: "", ext: "wav" };
}

async function toggleVoiceRecording(lang = "en") {
    const symptomArea = document.getElementById("symptom_text");

    if (!isRecording) {
        // 1. Check browser support
        const supported = getSupportedMimeType();
        if (!supported) {
            setVoiceUIState("error", "", "Voice recording is not supported in this browser. Please use a modern browser or enter symptoms using text.");
            return;
        }
        recordedMimeType = supported.mime;
        fileExtension = supported.ext;

        // 2. Request microphone permission & start recording
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioChunks = [];
            const options = recordedMimeType ? { mimeType: recordedMimeType } : {};
            mediaRecorder = new MediaRecorder(stream, options);

            mediaRecorder.ondataavailable = (event) => {
                if (event.data && event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = async () => {
                const blobType = recordedMimeType || "audio/wav";
                const audioBlob = new Blob(audioChunks, { type: blobType });

                if (!audioBlob || audioBlob.size === 0) {
                    setVoiceUIState("error", "", "⚠️ Recording failed. No audio was captured. Please check your microphone and try again.");
                    return;
                }

                setVoiceUIState("processing");

                const formData = new FormData();
                const filename = `voice_symptoms.${fileExtension}`;
                formData.append("audio", audioBlob, filename);
                formData.append("language", lang);

                try {
                    const res = await fetch("/api/speech/transcribe", {
                        method: "POST",
                        body: formData
                    });
                    const data = await res.json();
                    
                    const transcript = data.transcript || data.text;
                    if (data.success && transcript) {
                        if (symptomArea) {
                            symptomArea.value = transcript;
                            symptomArea.focus();
                        }
                        setVoiceUIState("success", "✓ Transcription complete. Please review and edit your symptoms below before proceeding.");
                    } else {
                        const errMsg = data.error || "Unable to transcribe audio. Please try again or enter symptoms using text.";
                        setVoiceUIState("error", "", "⚠️ " + errMsg);
                    }
                } catch (err) {
                    console.error("Transcription network error:", err);
                    setVoiceUIState("error", "", "⚠️ Audio transcription service is currently unavailable. Please enter symptoms using text.");
                }
            };

            mediaRecorder.start();
            isRecording = true;
            setVoiceUIState("recording");
        } catch (err) {
            console.error("Microphone access error:", err);
            isRecording = false;
            if (err.name === "NotAllowedError" || err.name === "PermissionDeniedError") {
                setVoiceUIState("error", "", "⚠️ Microphone permission was denied. Please allow microphone access in your browser settings and try again.");
            } else if (err.name === "NotFoundError" || err.name === "DevicesNotFoundError") {
                setVoiceUIState("error", "", "⚠️ Microphone is unavailable. Please check your microphone connection.");
            } else {
                setVoiceUIState("error", "", "⚠️ Microphone access error. Please check your browser audio settings or type your symptoms.");
            }
        }
    } else {
        // Stop recording
        if (mediaRecorder && mediaRecorder.state !== "inactive") {
            mediaRecorder.stop();
            if (mediaRecorder.stream) {
                mediaRecorder.stream.getTracks().forEach(track => track.stop());
            }
        }
        isRecording = false;
    }
}


