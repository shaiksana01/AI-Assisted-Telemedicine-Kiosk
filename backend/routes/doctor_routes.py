"""
Doctor REST API endpoints.
"""

from flask import Blueprint, request, jsonify
import database.database as db

doctor_bp = Blueprint("doctor_bp", __name__, url_prefix="/api/doctors")

@doctor_bp.route("/<doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    doctor = db.get_doctor_by_id(doctor_id)
    if not doctor:
        return jsonify({"success": False, "error": "Doctor not found."}), 404
    doctor.pop("password_hash", None)
    return jsonify({"success": True, "doctor": doctor}), 200

@doctor_bp.route("/queue/stats", methods=["GET"])
def get_stats():
    stats = db.get_queue_summary_stats()
    return jsonify({"success": True, "stats": stats}), 200
