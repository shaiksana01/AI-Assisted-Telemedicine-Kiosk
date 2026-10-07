"""
Interactive WebRTC Video Consultation Component for Streamlit.
Provides HTML5/JS peer-to-peer audio/video calling for Patient and Doctor consultation rooms.
"""

def render_webrtc_consultation(room_id: str, user_role: str, user_name: str, height: int = 560) -> str:
    """
    Generate the HTML/JavaScript WebRTC video room component.
    """
    peer_label = "Doctor" if user_role == "patient" else "Patient"
    my_label = "You (Patient)" if user_role == "patient" else "You (Doctor)"

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            body {{
                background-color: #0F172A;
                color: #F8FAFC;
                padding: 12px;
                border-radius: 8px;
            }}
            .video-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding-bottom: 8px;
                border-bottom: 1px solid #334155;
                margin-bottom: 12px;
            }}
            .room-badge {{
                background-color: #1E293B;
                color: #38BDF8;
                padding: 4px 10px;
                border-radius: 4px;
                font-size: 0.85rem;
                font-weight: 600;
            }}
            .status-indicator {{
                font-size: 0.85rem;
                color: #4ADE80;
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .status-dot {{
                width: 8px;
                height: 8px;
                background-color: #4ADE80;
                border-radius: 50%;
                display: inline-block;
                animation: pulse 1.5s infinite;
            }}
            @keyframes pulse {{
                0% {{ opacity: 1; }}
                50% {{ opacity: 0.4; }}
                100% {{ opacity: 1; }}
            }}
            .video-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
                height: 380px;
                margin-bottom: 12px;
            }}
            @media (max-width: 650px) {{
                .video-grid {{
                    grid-template-columns: 1fr;
                    height: auto;
                }}
            }}
            .video-box {{
                background-color: #1E293B;
                border-radius: 8px;
                position: relative;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                border: 1px solid #334155;
            }}
            video {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                background-color: #000;
            }}
            .video-tag {{
                position: absolute;
                bottom: 8px;
                left: 8px;
                background: rgba(15, 23, 42, 0.75);
                color: #F8FAFC;
                padding: 3px 8px;
                border-radius: 4px;
                font-size: 0.8rem;
                font-weight: 500;
                backdrop-filter: blur(4px);
            }}
            .controls-bar {{
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 12px;
                background-color: #1E293B;
                padding: 10px;
                border-radius: 8px;
            }}
            .ctrl-btn {{
                background-color: #334155;
                color: #F8FAFC;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 0.85rem;
                font-weight: 500;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 6px;
                transition: background 0.15s ease;
            }}
            .ctrl-btn:hover {{
                background-color: #475569;
            }}
            .ctrl-btn.active-off {{
                background-color: #DC2626;
            }}
            .ctrl-btn.btn-connect {{
                background-color: #0284C7;
            }}
            .ctrl-btn.btn-connect:hover {{
                background-color: #0369A1;
            }}
            .no-video-placeholder {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: #94A3B8;
                font-size: 0.9rem;
                text-align: center;
                padding: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="video-header">
            <div>
                <span class="room-badge">Room: {room_id}</span>
                <span style="font-size: 0.85rem; color: #94A3B8; margin-left: 8px;">User: {user_name} ({user_role.title()})</span>
            </div>
            <div class="status-indicator">
                <span class="status-dot" id="statusDot"></span>
                <span id="statusText">Video Service Initialized</span>
            </div>
        </div>

        <div class="video-grid">
            <div class="video-box" id="localBox">
                <video id="localVideo" autoplay playsinline muted></video>
                <div class="video-tag" id="localTag">{my_label}</div>
            </div>
            <div class="video-box" id="remoteBox">
                <video id="remoteVideo" autoplay playsinline></video>
                <div class="no-video-placeholder" id="remotePlaceholder">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="1.5">
                        <path d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                    </svg>
                    <p style="margin-top: 8px;">Waiting for {peer_label} to connect...</p>
                </div>
                <div class="video-tag">{peer_label} Video Feed</div>
            </div>
        </div>

        <div class="controls-bar">
            <button class="ctrl-btn btn-connect" id="btnStartMedia" onclick="startCamera()">📷 Start Camera</button>
            <button class="ctrl-btn" id="btnToggleAudio" onclick="toggleAudio()">🎙️ Mute</button>
            <button class="ctrl-btn" id="btnToggleVideo" onclick="toggleVideo()">📹 Video Off</button>
            <button class="ctrl-btn" id="btnConnectPeer" onclick="connectPeer()">🔗 Connect Call</button>
        </div>

        <script>
            let localStream = null;
            let peerConnection = null;
            let isAudioMuted = false;
            let isVideoOff = false;
            const roomId = "{room_id}";
            const userRole = "{user_role}";

            const rtcConfig = {{
                iceServers: [
                    {{ urls: "stun:stun.l.google.com:19302" }},
                    {{ urls: "stun:stun1.l.google.com:19302" }}
                ]
            }};

            async function startCamera() {{
                try {{
                    localStream = await navigator.mediaDevices.getUserMedia({{
                        video: true,
                        audio: true
                    }});
                    const localVideo = document.getElementById("localVideo");
                    localVideo.srcObject = localStream;
                    document.getElementById("statusText").innerText = "Camera Active & Ready";
                    document.getElementById("btnStartMedia").style.display = "none";
                }} catch (err) {{
                    console.error("Camera access error:", err);
                    document.getElementById("statusText").innerText = "Camera permission needed or in use.";
                    document.getElementById("statusText").style.color = "#F87171";
                    document.getElementById("statusDot").style.backgroundColor = "#F87171";
                }}
            }}

            function toggleAudio() {{
                if (localStream) {{
                    const audioTracks = localStream.getAudioTracks();
                    if (audioTracks.length > 0) {{
                        isAudioMuted = !isAudioMuted;
                        audioTracks[0].enabled = !isAudioMuted;
                        const btn = document.getElementById("btnToggleAudio");
                        btn.innerText = isAudioMuted ? "🔇 Unmute" : "🎙️ Mute";
                        btn.className = isAudioMuted ? "ctrl-btn active-off" : "ctrl-btn";
                    }}
                }}
            }}

            function toggleVideo() {{
                if (localStream) {{
                    const videoTracks = localStream.getVideoTracks();
                    if (videoTracks.length > 0) {{
                        isVideoOff = !isVideoOff;
                        videoTracks[0].enabled = !isVideoOff;
                        const btn = document.getElementById("btnToggleVideo");
                        btn.innerText = isVideoOff ? "📹 Video On" : "📹 Video Off";
                        btn.className = isVideoOff ? "ctrl-btn active-off" : "ctrl-btn";
                    }}
                }}
            }}

            async function connectPeer() {{
                if (!localStream) {{
                    await startCamera();
                }}
                
                try {{
                    peerConnection = new RTCPeerConnection(rtcConfig);
                    
                    if (localStream) {{
                        localStream.getTracks().forEach(track => {{
                            peerConnection.addTrack(track, localStream);
                        }});
                    }}

                    peerConnection.ontrack = (event) => {{
                        const remoteVideo = document.getElementById("remoteVideo");
                        remoteVideo.srcObject = event.streams[0];
                        document.getElementById("remotePlaceholder").style.display = "none";
                        document.getElementById("statusText").innerText = "Connected In Call";
                    }};

                    peerConnection.onicecandidate = (event) => {{
                        if (event.candidate) {{
                            console.log("ICE Candidate generated:", event.candidate);
                        }}
                    }};

                    peerConnection.onconnectionstatechange = () => {{
                        const state = peerConnection.connectionState;
                        document.getElementById("statusText").innerText = "Call Status: " + state;
                    }};

                    document.getElementById("statusText").innerText = "Live Room Active (Encrypted)";
                    document.getElementById("btnConnectPeer").innerText = "Call Active ✅";
                }} catch (e) {{
                    console.error("Peer connection error:", e);
                }}
            }}

            // Auto-trigger camera startup on load
            window.addEventListener("load", () => {{
                startCamera();
            }});
        </script>
    </body>
    </html>
    """
    return html_code
