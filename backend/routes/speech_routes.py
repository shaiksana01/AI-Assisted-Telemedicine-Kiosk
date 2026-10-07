import os
from flask import Blueprint, request, jsonify, make_response
from backend.speech.whisper_service import transcribe_audio
from backend.speech.tts_service import synthesize_speech

speech_bp = Blueprint("speech_bp", __name__, url_prefix="/api/speech")

@speech_bp.route("/status", methods=["GET"])
def speech_status():
    configured = bool(os.getenv("OPENAI_API_KEY", "").strip())
    return jsonify({
        "success": True,
        "configured": configured,
        "stt_configured": configured,
        "tts_configured": configured,
        "stt_model": "whisper-1",
        "tts_model": "tts-1"
    })


@speech_bp.route("/transcribe", methods=["POST"])
def transcribe():
    audio_file = request.files.get("audio")
    language = request.form.get("language", "en")
    
    if not audio_file:
        return jsonify({"success": False, "error": "No audio file provided in request."}), 400

    audio_bytes = audio_file.read()
    result = transcribe_audio(audio_bytes, filename=audio_file.filename or "audio.wav", language=language)
    status_code = 200 if result.get("success") else 400
    return jsonify(result), status_code

@speech_bp.route("/synthesize", methods=["POST"])
@speech_bp.route("/tts", methods=["POST"])
def synthesize():
    data = request.get_json() or {}
    text = data.get("text", "")
    voice = data.get("voice", "alloy")
    lang = data.get("language", "en")

    if not text.strip():
        return jsonify({"success": False, "error": "No text provided for synthesis."}), 400

    audio_bytes, err = synthesize_speech(text, voice=voice, language_code=lang)
    if err or not audio_bytes:
        return jsonify({"success": False, "error": err or "Speech synthesis unavailable."}), 503

    response = make_response(audio_bytes)
    response.headers["Content-Type"] = "audio/mpeg"
    return response
