"""
Triage and Symptom REST API endpoints for AI-Assisted Telemedicine Kiosk.
"""

from flask import Blueprint, request, jsonify
from ml.predict import predict_triage_priority, extract_symptoms_from_text

triage_bp = Blueprint("triage_bp", __name__, url_prefix="/api/triage")

@triage_bp.route("/extract", methods=["POST"])
def extract_symptoms():
    data = request.get_json() or {}
    text = data.get("text", "")
    if not text.strip():
        return jsonify({"success": False, "error": "No symptom text provided."}), 400

    features, detected_keys = extract_symptoms_from_text(text)
    return jsonify({
        "success": True,
        "features": features,
        "detected_keys": detected_keys
    }), 200

@triage_bp.route("/predict", methods=["POST"])
def predict_triage():
    data = request.get_json() or {}
    text = data.get("symptoms_text", "")
    additional_chips = data.get("additional_symptoms", [])

    if not text.strip() and not additional_chips:
        return jsonify({"success": False, "error": "Please provide symptom text or select symptoms."}), 400

    prediction_result = predict_triage_priority(text, additional_chips)
    return jsonify({
        "success": True,
        "triage": prediction_result
    }), 200
