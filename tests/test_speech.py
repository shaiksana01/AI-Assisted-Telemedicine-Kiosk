"""
Unit Tests for Speech Services (Whisper STT and OpenAI TTS) and WebRTC Signaling.
"""

from backend.speech.whisper_service import transcribe_audio
from backend.speech.tts_service import synthesize_speech
from backend.webrtc.signaling import WebRTCSignalingManager

def test_speech_fallbacks():
    # Empty audio handling
    res_empty = transcribe_audio(b"")
    assert res_empty["success"] is False
    assert "No valid audio" in res_empty["error"] or "API key" in res_empty["error"]

    # TTS empty text handling
    audio_bytes, err = synthesize_speech("")
    assert audio_bytes is None
    assert "Empty text" in err

def test_webrtc_signaling():
    mgr = WebRTCSignalingManager()
    room_id = "TEST-ROOM-101"

    # Join room as patient
    p_room = mgr.join_room(room_id, "patient", "PAT-1")
    assert p_room["patient"]["user_id"] == "PAT-1"

    # Join room as doctor
    d_room = mgr.join_room(room_id, "doctor", "DOC-1")
    assert d_room["doctor"]["user_id"] == "DOC-1"
    assert d_room["status"] == "ready_to_connect"

    # Send SDP Offer
    offer_sdp = {"type": "offer", "sdp": "v=0\r\no=doctor..."}
    mgr.set_offer(room_id, offer_sdp)
    assert mgr.get_offer(room_id) == offer_sdp

    # Send SDP Answer
    answer_sdp = {"type": "answer", "sdp": "v=0\r\no=patient..."}
    mgr.set_answer(room_id, answer_sdp)
    assert mgr.get_answer(room_id) == answer_sdp
    assert mgr.get_room_state(room_id)["status"] == "in_call"

    # ICE candidate exchange
    candidate = {"candidate": "candidate:1 1 UDP ...", "sdpMid": "0"}
    mgr.add_ice_candidate(room_id, "doctor", candidate)
    peer_candidates = mgr.get_peer_ice_candidates(room_id, "patient")
    assert len(peer_candidates) == 1
    assert peer_candidates[0]["candidate"] == candidate["candidate"]

    # Leave room
    mgr.leave_room(room_id, "patient")
    assert mgr.get_room_state(room_id)["patient"] is None

if __name__ == "__main__":
    test_speech_fallbacks()
    test_webrtc_signaling()
    print("✅ All speech & WebRTC tests passed!")
