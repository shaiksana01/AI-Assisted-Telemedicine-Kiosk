// Voice Input & Whisper Speech-to-Text Handling

let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;
let recordedMimeType = "audio/webm";
let fileExtension = "webm";

// Detect best supported MIME type for the browser
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
    const recordBtn = document.getElementById("recordVoiceBtn");
    const statusText = document.getElementById("voiceStatusText");
    const symptomArea = document.getElementById("symptom_text");

    if (!isRecording) {
        // 1. Check browser support
        const supported = getSupportedMimeType();
        if (!supported) {
            if (statusText) {
                statusText.innerText = "Voice recording is not supported in this browser. Please use a modern browser or enter symptoms using text.";
            }
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
                
                if (statusText) {
                    statusText.innerText = "⏳ Transcribing speech with OpenAI Whisper...";
                }
                if (recordBtn) {
                    recordBtn.disabled = true;
                    recordBtn.innerText = "⏳ Processing...";
                }

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
                        if (statusText) {
                            statusText.innerText = "✓ Voice transcription complete. Please review and edit your symptoms below before proceeding.";
                        }
                    } else {
                        const errMsg = data.error || "Unable to transcribe audio. Please try again or enter symptoms using text.";
                        if (statusText) {
                            statusText.innerText = "⚠️ " + errMsg;
                        }
                    }
                } catch (err) {
                    console.error("Transcription network error:", err);
                    if (statusText) {
                        statusText.innerText = "⚠️ Audio transcription service is currently unavailable. Please enter symptoms using text.";
                    }
                } finally {
                    if (recordBtn) {
                        recordBtn.disabled = false;
                        recordBtn.innerText = "🎙️ Record Again";
                        recordBtn.classList.remove("btn-danger");
                        recordBtn.classList.add("btn-primary");
                    }
                }
            };

            mediaRecorder.start();
            isRecording = true;
            if (recordBtn) {
                recordBtn.innerText = "🔴 Stop Recording";
                recordBtn.classList.add("btn-danger");
                recordBtn.classList.remove("btn-primary");
            }
            if (statusText) {
                statusText.innerText = "🔴 Recording your symptoms... Speak clearly in your selected language.";
            }
        } catch (err) {
            console.error("Microphone access error:", err);
            if (err.name === "NotAllowedError" || err.name === "PermissionDeniedError") {
                if (statusText) {
                    statusText.innerText = "Microphone permission was denied. Please allow microphone access in your browser settings and try again.";
                }
            } else if (err.name === "NotFoundError" || err.name === "DevicesNotFoundError") {
                if (statusText) {
                    statusText.innerText = "Microphone is unavailable. Please check your microphone connection.";
                }
            } else {
                if (statusText) {
                    statusText.innerText = "Microphone access error. Please check your browser audio settings or type your symptoms.";
                }
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

