// Main Interactive JS for AI-Assisted Telemedicine Kiosk

document.addEventListener("DOMContentLoaded", () => {
    // Language dropdown synchronization & persistence
    const langSelect = document.querySelector('select[name="language"]');
    if (langSelect) {
        // Save on change
        langSelect.addEventListener("change", (e) => {
            if (e.target.value) {
                try {
                    localStorage.setItem("kiosk_preferred_language", e.target.value);
                } catch (err) {
                    console.log("LocalStorage not available:", err);
                }
            }
        });
    }

    // Tabs Functionality
    const tabBtns = document.querySelectorAll(".tab-btn");
    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const target = btn.getAttribute("data-tab");
            const parent = btn.closest(".tabs-wrapper") || document;
            
            parent.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
            parent.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
            
            btn.classList.add("active");
            const targetEl = parent.querySelector(`#${target}`);
            if (targetEl) targetEl.classList.add("active");
        });
    });

    // Symptom Chips
    const chips = document.querySelectorAll(".chip-btn");
    const symptomArea = document.getElementById("symptom_text");
    chips.forEach(chip => {
        chip.addEventListener("click", () => {
            chip.classList.toggle("selected");
            const val = chip.getAttribute("data-val");
            if (symptomArea && val) {
                if (chip.classList.contains("selected")) {
                    if (symptomArea.value.trim().length > 0) {
                        symptomArea.value += ", " + val;
                    } else {
                        symptomArea.value = val;
                    }
                }
            }
        });
    });
});

// TTS Voice Synthesis Playback with Multi-Language Support
async function playTTS(text, lang = "en") {
    if (!text || text.trim() === "") return;
    try {
        const res = await fetch("/api/speech/tts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text, language: lang })
        });
        if (res.ok) {
            const blob = await res.blob();
            const audioUrl = URL.createObjectURL(blob);
            const audio = new Audio(audioUrl);
            audio.play().catch(err => {
                console.log("Autoplay prevented or audio playback issue:", err);
            });
        } else {
            console.log("TTS audio synthesis unavailable, text display active.");
        }
    } catch (e) {
        console.error("TTS playback error:", e);
    }
}

