"""
WebRTC Signaling REST API endpoints for peer-to-peer audio/video consultations.
"""

from flask import Blueprint, request, jsonify
from backend.webrtc.signaling import signaling_manager

webrtc_bp = Blueprint("webrtc_bp", __name__, url_prefix="/api/webrtc")

@webrtc_bp.route("/room/<room_id>", methods=["GET"])
def get_room_state(room_id):
    state = signaling_manager.get_room_state(room_id)
    return jsonify({"success": True, "room": state}), 200

@webrtc_bp.route("/room/<room_id>/join", methods=["POST"])
def join_room(room_id):
    data = request.get_json() or {}
    role = data.get("role", "patient")
    user_id = data.get("user_id", "user")
    state = signaling_manager.join_room(room_id, role, user_id)
    return jsonify({"success": True, "room": state}), 200

@webrtc_bp.route("/room/<room_id>/offer", methods=["POST"])
def post_offer(room_id):
    data = request.get_json() or {}
    offer = data.get("offer")
    if not offer:
        return jsonify({"success": False, "error": "offer SDP is required."}), 400
    signaling_manager.set_offer(room_id, offer)
    return jsonify({"success": True, "message": "Offer stored."}), 200

@webrtc_bp.route("/room/<room_id>/offer", methods=["GET"])
def get_offer(room_id):
    offer = signaling_manager.get_offer(room_id)
    return jsonify({"success": True, "offer": offer}), 200

@webrtc_bp.route("/room/<room_id>/answer", methods=["POST"])
def post_answer(room_id):
    data = request.get_json() or {}
    answer = data.get("answer")
    if not answer:
        return jsonify({"success": False, "error": "answer SDP is required."}), 400
    signaling_manager.set_answer(room_id, answer)
    return jsonify({"success": True, "message": "Answer stored."}), 200

@webrtc_bp.route("/room/<room_id>/answer", methods=["GET"])
def get_answer(room_id):
    answer = signaling_manager.get_answer(room_id)
    return jsonify({"success": True, "answer": answer}), 200

@webrtc_bp.route("/room/<room_id>/ice-candidate", methods=["POST"])
def add_ice_candidate(room_id):
    data = request.get_json() or {}
    role = data.get("role", "patient")
    candidate = data.get("candidate")
    if not candidate:
        return jsonify({"success": False, "error": "candidate is required."}), 400
    signaling_manager.add_ice_candidate(room_id, role, candidate)
    return jsonify({"success": True, "message": "ICE candidate added."}), 200

@webrtc_bp.route("/room/<room_id>/ice-candidates", methods=["GET"])
def get_ice_candidates(room_id):
    role = request.args.get("role", "patient")
    candidates = signaling_manager.get_peer_ice_candidates(room_id, role)
    return jsonify({"success": True, "candidates": candidates}), 200

@webrtc_bp.route("/room/<room_id>/leave", methods=["POST"])
def leave_room(room_id):
    data = request.get_json() or {}
    role = data.get("role", "patient")
    signaling_manager.leave_room(room_id, role)
    return jsonify({"success": True, "message": "Left room."}), 200
