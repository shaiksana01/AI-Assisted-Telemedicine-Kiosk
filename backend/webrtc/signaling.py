"""
WebRTC Signaling Service for AI-Assisted Telemedicine Kiosk.
Manages peer-to-peer room state, SDP offers, answers, and ICE candidate exchange
between patient and doctor consultation rooms.
"""

import time
from typing import Dict, Any, List, Optional

class WebRTCSignalingManager:
    def __init__(self):
        # Format: {room_id: {"patient": {...}, "doctor": {...}, "offer": None, "answer": None, "candidates": {"patient": [], "doctor": []}, "updated_at": timestamp}}
        self.rooms: Dict[str, Dict[str, Any]] = {}

    def get_or_create_room(self, room_id: str) -> Dict[str, Any]:
        if room_id not in self.rooms:
            self.rooms[room_id] = {
                "room_id": room_id,
                "patient": None,
                "doctor": None,
                "offer": None,
                "answer": None,
                "candidates": {"patient": [], "doctor": []},
                "status": "waiting",
                "created_at": time.time(),
                "updated_at": time.time()
            }
        return self.rooms[room_id]

    def join_room(self, room_id: str, role: str, user_id: str) -> Dict[str, Any]:
        room = self.get_or_create_room(room_id)
        if role in ["patient", "doctor"]:
            room[role] = {"user_id": user_id, "joined_at": time.time()}
            room["updated_at"] = time.time()
            if room["patient"] and room["doctor"]:
                room["status"] = "ready_to_connect"
        return room

    def set_offer(self, room_id: str, offer_sdp: Dict[str, Any]) -> bool:
        room = self.get_or_create_room(room_id)
        room["offer"] = offer_sdp
        room["updated_at"] = time.time()
        room["status"] = "offer_sent"
        return True

    def get_offer(self, room_id: str) -> Optional[Dict[str, Any]]:
        room = self.get_or_create_room(room_id)
        return room.get("offer")

    def set_answer(self, room_id: str, answer_sdp: Dict[str, Any]) -> bool:
        room = self.get_or_create_room(room_id)
        room["answer"] = answer_sdp
        room["updated_at"] = time.time()
        room["status"] = "in_call"
        return True

    def get_answer(self, room_id: str) -> Optional[Dict[str, Any]]:
        room = self.get_or_create_room(room_id)
        return room.get("answer")

    def add_ice_candidate(self, room_id: str, role: str, candidate: Dict[str, Any]) -> bool:
        room = self.get_or_create_room(room_id)
        if role in ["patient", "doctor"]:
            room["candidates"][role].append(candidate)
            room["updated_at"] = time.time()
            return True
        return False

    def get_peer_ice_candidates(self, room_id: str, current_role: str) -> List[Dict[str, Any]]:
        room = self.get_or_create_room(room_id)
        peer_role = "doctor" if current_role == "patient" else "patient"
        return room["candidates"].get(peer_role, [])

    def leave_room(self, room_id: str, role: str) -> bool:
        if room_id in self.rooms:
            room = self.rooms[room_id]
            room[role] = None
            room["status"] = "peer_disconnected"
            room["updated_at"] = time.time()
            return True
        return False

    def get_room_state(self, room_id: str) -> Dict[str, Any]:
        return self.get_or_create_room(room_id)

# Global signaling singleton
signaling_manager = WebRTCSignalingManager()
