"""
AI-Assisted Telemedicine Kiosk
A Multilingual and Voice-Enabled Healthcare System for Rural India
================================================================================
Comprehensive, full-featured telemedicine kiosk application providing:
- Multilingual UI (English, Hindi, Kannada, Telugu)
- Patient & Doctor Authentication with Role-Based Access Control
- Speech-to-Text Symptom Input (OpenAI Whisper) & Text Input
- Supervised Random Forest Preliminary Care-Priority Triage
- Live Encrypted WebRTC Video Consultation Room
- Structured Digital Prescription Builder with Printable View
- Complete Patient Electronic Health Record (EHR) & Consultation Trajectory
- Text-to-Speech (TTS) Voice Guidance for Rural Accessibility
"""

import streamlit as st
import os
import json
import io
import time
from datetime import datetime

# Database & Backend services
import database.database as db
from ml.predict import (
    predict_triage_priority,
    load_triage_model,
    SYMPTOM_DISPLAY_NAMES,
    SYMPTOM_COLUMNS
)
from utils.translations import get_text, get_available_languages, get_language_code
from utils.webrtc_component import render_webrtc_consultation
from backend.speech.whisper_service import transcribe_audio
from backend.speech.tts_service import synthesize_speech
from backend.services.prescription_service import generate_prescription_html
from backend.services.ehr_service import get_complete_patient_history

# Page Configuration
st.set_page_config(
    page_title="AI-Assisted Telemedicine Kiosk",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Database Schema
db.init_db()

# ------------------------------------------------------------------------------
# CLEAN HEALTHCARE THEME CSS
# ------------------------------------------------------------------------------
st.markdown("""
<style>
    /* Clean Streamlit Layout */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Base Healthcare Typography & Colors */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #1E293B;
        background-color: #F8FAFC;
    }
    .stApp { background-color: #F8FAFC; }
    
    .block-container {
        max-width: 1040px !important;
        padding-top: 1.25rem !important;
        padding-bottom: 2.5rem !important;
        background-color: #F8FAFC;
    }
    
    .brand-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.2px;
    }
    
    /* Navigation Link Buttons */
    div[class*="st-key-top_"] button {
        background: transparent !important;
        border: none !important;
        border-bottom: 2.5px solid transparent !important;
        box-shadow: none !important;
        color: #64748B !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        padding: 4px 8px !important;
        min-height: unset !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
    }
    div[class*="st-key-top_"] button:hover {
        color: #0284C7 !important;
        border-bottom: 2.5px solid #0284C7 !important;
    }
    div[class*="st-key-top_"] button[kind="primary"],
    div[class*="st-key-top_"] button[data-testid="baseButton-primary"] {
        color: #0284C7 !important;
        font-weight: 700 !important;
        border-bottom: 2.5px solid #0284C7 !important;
    }

    /* Hero Styling */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.15;
        margin-bottom: 0.4rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0284C7;
        margin-bottom: 0.8rem;
    }
    .hero-desc {
        font-size: 0.95rem;
        color: #475569;
        line-height: 1.5;
        margin-bottom: 1.2rem;
    }
    
    /* Cards & Containers */
    .section-label {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0F172A;
        margin: 1.5rem 0 0.8rem 0;
    }
    .choice-card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }
    .choice-icon-circle {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background-color: #E0F2FE;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .choice-card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
    }
    .choice-card-desc {
        font-size: 0.88rem;
        color: #64748B;
        line-height: 1.4;
    }

    /* Priority Badges */
    .badge-low {
        background-color: #F0FDF4;
        color: #166534;
        border: 1px solid #BBF7D0;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .badge-moderate {
        background-color: #FEFCE8;
        color: #854D0E;
        border: 1px solid #FEF08A;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .badge-high {
        background-color: #FFF7ED;
        color: #9A3412;
        border: 1px solid #FED7AA;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .badge-urgent {
        background-color: #FEF2F2;
        color: #991B1B;
        border: 1px solid #FECACA;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .disclaimer-box {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-left: 4px solid #0284C7;
        padding: 12px 16px;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #475569;
        line-height: 1.45;
        margin: 14px 0;
    }
    .emergency-banner {
        background-color: #FEF2F2;
        border: 1px solid #F87171;
        border-left: 5px solid #DC2626;
        padding: 12px 16px;
        border-radius: 4px;
        font-size: 0.92rem;
        color: #991B1B;
        font-weight: 600;
        margin: 14px 0;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# ------------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "language" not in st.session_state:
    st.session_state.language = "English"

# User authentication states
if "logged_patient" not in st.session_state:
    st.session_state.logged_patient = None
if "logged_doctor" not in st.session_state:
    st.session_state.logged_doctor = None

# Consultation workflow state
if "current_consultation_id" not in st.session_state:
    st.session_state.current_consultation_id = None
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None
if "symptom_input_text" not in st.session_state:
    st.session_state.symptom_input_text = ""
if "selected_symptom_chips" not in st.session_state:
    st.session_state.selected_symptom_chips = []
if "selected_doctor_case_id" not in st.session_state:
    st.session_state.selected_doctor_case_id = None
if "prescription_medicines" not in st.session_state:
    st.session_state.prescription_medicines = [
        {"medicine_name": "Paracetamol 500mg", "dosage": "1 tablet", "frequency": "Twice daily after food", "duration": "3 days", "instructions": "For fever & body ache"},
        {"medicine_name": "Cetirizine 10mg", "dosage": "1 tablet", "frequency": "Once daily at night", "duration": "3 days", "instructions": "For cold & congestion"}
    ]

def navigate_to(page_name: str):
    """Navigate to target page and trigger rerun."""
    st.session_state.page = page_name
    st.rerun()

def play_tts(text: str):
    """Synthesize and play audio prompt."""
    lang_code = get_language_code(st.session_state.language)
    audio_bytes, err = synthesize_speech(text, voice="alloy", language_code=lang_code)
    if audio_bytes:
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)

# ------------------------------------------------------------------------------
# TOP WEBSITE HEADER (AI-Assisted Telemedicine Kiosk | Home - About - Help)
# ------------------------------------------------------------------------------
h_col1, h_col2 = st.columns([5.5, 4.5], gap="medium")

with h_col1:
    st.markdown("<div class='brand-title'>🏥 AI-Assisted Telemedicine Kiosk</div>", unsafe_allow_html=True)

with h_col2:
    if st.session_state.logged_patient:
        n1, n2, n3, n4 = st.columns([1, 1, 1.4, 1.2], gap="small")
        with n1:
            if st.button("Home", key="top_home_btn", use_container_width=True, type="primary" if st.session_state.page == "home" else "secondary"):
                navigate_to("home")
        with n2:
            if st.button("Help", key="top_help_btn", use_container_width=True, type="primary" if st.session_state.page == "help" else "secondary"):
                navigate_to("help")
        with n3:
            if st.button("My Records (EHR)", key="top_ehr_btn", use_container_width=True, type="primary" if st.session_state.page == "patient_ehr" else "secondary"):
                navigate_to("patient_ehr")
        with n4:
            if st.button("Logout", key="top_logout_btn", use_container_width=True):
                st.session_state.logged_patient = None
                navigate_to("home")
    elif st.session_state.logged_doctor:
        n1, n2, n3, n4 = st.columns([1, 1, 1.4, 1.2], gap="small")
        with n1:
            if st.button("Home", key="top_home_btn", use_container_width=True, type="primary" if st.session_state.page == "home" else "secondary"):
                navigate_to("home")
        with n2:
            if st.button("Dashboard", key="top_doc_dash_btn", use_container_width=True, type="primary" if st.session_state.page == "doctor_dashboard" else "secondary"):
                navigate_to("doctor_dashboard")
        with n3:
            if st.button("About", key="top_about_btn", use_container_width=True, type="primary" if st.session_state.page == "about" else "secondary"):
                navigate_to("about")
        with n4:
            if st.button("Logout", key="top_logout_btn", use_container_width=True):
                st.session_state.logged_doctor = None
                navigate_to("home")
    else:
        n1, n2, n3 = st.columns([1, 1, 1], gap="small")
        with n1:
            if st.button("Home", key="top_home_btn", use_container_width=True, type="primary" if st.session_state.page == "home" else "secondary"):
                navigate_to("home")
        with n2:
            if st.button("About", key="top_about_btn", use_container_width=True, type="primary" if st.session_state.page == "about" else "secondary"):
                navigate_to("about")
        with n3:
            if st.button("Help", key="top_help_btn", use_container_width=True, type="primary" if st.session_state.page == "help" else "secondary"):
                navigate_to("help")

st.markdown("<hr style='margin: 4px 0 20px 0; border: 0; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)


# ==============================================================================
# 1. HOMEPAGE
# ==============================================================================
if st.session_state.page == "home":
    col_left, col_right = st.columns([5.5, 4.5], gap="large")
    
    with col_left:
        st.markdown(f"<div class='hero-title'>{get_text('hero_title', st.session_state.language)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='hero-subtitle'>{get_text('hero_subtitle', st.session_state.language)}</div>", unsafe_allow_html=True)
        st.markdown(f"<p class='hero-desc'>{get_text('hero_desc', st.session_state.language)}</p>", unsafe_allow_html=True)
        
        # Language Selector Bar
        st.markdown("<div style='font-weight: 600; font-size: 0.9rem; color: #475569; margin-bottom: 6px;'>🌐 Select Language / भाषा / ಭಾಷೆ / భాష</div>", unsafe_allow_html=True)
        langs = get_available_languages()
        selected_lang = st.selectbox(
            "Language",
            langs,
            index=langs.index(st.session_state.language) if st.session_state.language in langs else 0,
            label_visibility="collapsed",
            key="home_lang_select"
        )
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()

    with col_right:
        img_jpg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "telemedicine_hero.jpg")
        img_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "telemedicine_hero.png")
        if os.path.exists(img_jpg):
            st.image(img_jpg, use_container_width=True)
        elif os.path.exists(img_png):
            st.image(img_png, use_container_width=True)
        else:
            st.image("https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=600&q=80", use_container_width=True)
            
    st.markdown(f"<div class='section-label'>{get_text('choose_role', st.session_state.language)}</div>", unsafe_allow_html=True)
    
    card_p, card_d = st.columns(2, gap="medium")
    with card_p:
        with st.container(border=True):
            st.markdown(f"""
            <div class='choice-card-header'>
                <div class='choice-icon-circle'>
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                </div>
                <div class='choice-card-text'>
                    <div class='choice-card-title'>{get_text('card_patient_title', st.session_state.language)}</div>
                    <div class='choice-card-desc'>{get_text('card_patient_desc', st.session_state.language)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(get_text('card_patient_btn', st.session_state.language), key="home_patient_btn", type="primary", use_container_width=True):
                navigate_to("patient_portal")
            
    with card_d:
        with st.container(border=True):
            st.markdown(f"""
            <div class='choice-card-header'>
                <div class='choice-icon-circle'>
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"></path>
                        <path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4"></path>
                        <circle cx="20" cy="10" r="2"></circle>
                    </svg>
                </div>
                <div class='choice-card-text'>
                    <div class='choice-card-title'>{get_text('card_doctor_title', st.session_state.language)}</div>
                    <div class='choice-card-desc'>{get_text('card_doctor_desc', st.session_state.language)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(get_text('card_doctor_btn', st.session_state.language), key="home_doctor_btn", type="secondary", use_container_width=True):
                navigate_to("doctor_portal")
            
    st.markdown(f"""
    <hr style='margin: 36px 0 14px 0; border: 0; border-top: 1px solid #E2E8F0;'>
    <div style='font-size: 0.78rem; color: #94A3B8; text-align: center; margin-bottom: 4px;'>
        {get_text('footer_disclaimer', st.session_state.language)}
    </div>
    <div style='font-size: 0.78rem; color: #94A3B8; text-align: center;'>
        {get_text('footer_credit', st.session_state.language)}
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# 2. ABOUT PAGE
# ==============================================================================
elif st.session_state.page == "about":
    st.markdown(f"<div class='hero-title'>{get_text('about_title', st.session_state.language)}</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <p style='color: #475569; line-height: 1.6; font-size: 0.95rem; margin-top: 12px;'>
        {get_text('about_p1', st.session_state.language)}
    </p>
    <p style='color: #475569; line-height: 1.6; font-size: 0.95rem;'>
        {get_text('about_p2', st.session_state.language)}
    </p>
    <p style='color: #475569; line-height: 1.6; font-size: 0.95rem;'>
        {get_text('about_p3', st.session_state.language)}
    </p>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='disclaimer-box'>
        <strong>Clinical Decision-Support Notice:</strong> {get_text('about_disclaimer', st.session_state.language)}
    </div>
    """, unsafe_allow_html=True)

    if st.button(get_text('btn_back_home', st.session_state.language), key="about_back_btn"):
        navigate_to("home")


# ==============================================================================
# 3. HELP & INSTRUCTIONS PAGE
# ==============================================================================
elif st.session_state.page == "help":
    st.markdown(f"<div class='hero-title'>{get_text('help_title', st.session_state.language)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-label'>{get_text('help_steps_title', st.session_state.language)}</div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(f"""
        - **{get_text('help_step1', st.session_state.language)}**
        - **{get_text('help_step2', st.session_state.language)}**
        - **{get_text('help_step3', st.session_state.language)}**
        - **{get_text('help_step4', st.session_state.language)}**
        - **{get_text('help_step5', st.session_state.language)}**
        - **{get_text('help_step6', st.session_state.language)}**
        - **{get_text('help_step7', st.session_state.language)}**
        - **{get_text('help_step8', st.session_state.language)}**
        """)

    st.markdown(f"<div class='section-label'>{get_text('help_troubleshooting_title', st.session_state.language)}</div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"""
        * **Microphone Permissions**: {get_text('help_mic_issue', st.session_state.language)}
        * **Camera Access**: {get_text('help_cam_issue', st.session_state.language)}
        """)

    if st.button(get_text('btn_back_home', st.session_state.language), key="help_back_btn"):
        navigate_to("home")


# ==============================================================================
# 4. PATIENT PORTAL (LOGIN & REGISTRATION)
# ==============================================================================
elif st.session_state.page == "patient_portal":
    st.markdown(f"<div class='hero-title'>{get_text('auth_patient_title', st.session_state.language)}</div>", unsafe_allow_html=True)
    
    # If already logged in, show quick actions
    if st.session_state.logged_patient:
        pat = st.session_state.logged_patient
        st.success(f"{get_text('msg_login_success', st.session_state.language)} **{pat.get('full_name')}** (ID: {pat.get('patient_id')})")
        
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            if st.button("🩺 Start New Consultation", type="primary", use_container_width=True):
                navigate_to("patient_consent")
        with c2:
            if st.button("📋 View My Health Records (EHR)", use_container_width=True):
                navigate_to("patient_ehr")
        with c3:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_patient = None
                navigate_to("home")
    else:
        tab_login, tab_reg = st.tabs([
            get_text("auth_patient_login_tab", st.session_state.language),
            get_text("auth_patient_reg_tab", st.session_state.language)
        ])

        with tab_login:
            with st.form("patient_login_form"):
                p_phone = st.text_input(get_text("lbl_phone", st.session_state.language), placeholder="9876543210")
                p_pass = st.text_input(get_text("lbl_password", st.session_state.language), type="password")
                submit_login = st.form_submit_button(get_text("btn_login", st.session_state.language), type="primary")

                if submit_login:
                    if not p_phone:
                        st.error(get_text("lbl_phone_help", st.session_state.language))
                    else:
                        patient = db.authenticate_patient(p_phone, p_pass)
                        if patient:
                            st.session_state.logged_patient = patient
                            st.session_state.language = patient.get("preferred_language", st.session_state.language)
                            st.success(f"{get_text('msg_login_success', st.session_state.language)} {patient.get('full_name')}")
                            time.sleep(0.5)
                            navigate_to("patient_consent")
                        else:
                            st.error(get_text("msg_login_failed", st.session_state.language))

        with tab_reg:
            with st.form("patient_reg_form"):
                r_name = st.text_input(get_text("lbl_full_name", st.session_state.language), placeholder="e.g. Ramesh Gowda")
                c_a, c_g = st.columns(2)
                with c_a:
                    r_age = st.number_input(get_text("lbl_age", st.session_state.language), min_value=1, max_value=120, value=30)
                with c_g:
                    r_gender = st.selectbox(get_text("lbl_gender", st.session_state.language), ["Male", "Female", "Other"])
                
                r_phone = st.text_input(get_text("lbl_phone", st.session_state.language), placeholder="10-digit mobile number")
                r_loc = st.text_input(get_text("lbl_location", st.session_state.language), placeholder="Village / Town")
                
                langs = get_available_languages()
                r_lang = st.selectbox(get_text("lbl_pref_lang", st.session_state.language), langs, index=langs.index(st.session_state.language) if st.session_state.language in langs else 0)
                r_pass = st.text_input(get_text("lbl_password", st.session_state.language), type="password", help="Create a password for your health records.")

                submit_reg = st.form_submit_button(get_text("btn_register", st.session_state.language), type="primary")

                if submit_reg:
                    if not r_name.strip():
                        st.error("Please enter patient's full name.")
                    elif not r_phone.strip() or len(r_phone.strip()) < 10:
                        st.error("Please enter a valid 10-digit mobile number.")
                    else:
                        pid = db.register_patient_account(
                            full_name=r_name,
                            age=r_age,
                            gender=r_gender,
                            phone_number=r_phone,
                            preferred_language=r_lang,
                            location=r_loc,
                            password=r_pass
                        )
                        st.session_state.logged_patient = db.get_patient_by_id(pid)
                        st.session_state.language = r_lang
                        st.success(f"{get_text('msg_reg_success', st.session_state.language)} **{pid}**")
                        time.sleep(0.8)
                        navigate_to("patient_consent")

    if st.button("← " + get_text('btn_back_home', st.session_state.language), key="pat_portal_back"):
        navigate_to("home")


# ==============================================================================
# 5. PATIENT PRIVACY & INFORMED CONSENT
# ==============================================================================
elif st.session_state.page == "patient_consent":
    if not st.session_state.logged_patient:
        navigate_to("patient_portal")

    pat = st.session_state.logged_patient
    st.markdown(f"<div class='hero-title'>{get_text('consent_title', st.session_state.language)}</div>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f"""
        <p style='color: #475569; font-size: 0.95rem;'>
            {get_text('consent_p1', st.session_state.language)}
        </p>
        <ul style='color: #334155; line-height: 1.7; font-size: 0.92rem;'>
            <li>{get_text('consent_bullet1', st.session_state.language)}</li>
            <li>{get_text('consent_bullet2', st.session_state.language)}</li>
            <li>{get_text('consent_bullet3', st.session_state.language)}</li>
        </ul>
        """, unsafe_allow_html=True)

        consent_check = st.checkbox(get_text("consent_checkbox", st.session_state.language), value=True)
        
        if st.button(get_text("consent_btn_agree", st.session_state.language), type="primary", disabled=not consent_check):
            navigate_to("symptom_entry")


# ==============================================================================
# 6. SYMPTOM ENTRY (TEXT & VOICE VIA OPENAI WHISPER)
# ==============================================================================
elif st.session_state.page == "symptom_entry":
    if not st.session_state.logged_patient:
        navigate_to("patient_portal")

    pat = st.session_state.logged_patient
    st.markdown(f"<div class='hero-title'>{get_text('symptom_title', st.session_state.language)}</div>", unsafe_allow_html=True)
    st.markdown(f"<p class='hero-desc'>{get_text('symptom_desc', st.session_state.language)}</p>", unsafe_allow_html=True)

    tab_txt, tab_voice = st.tabs([
        get_text("tab_text_input", st.session_state.language),
        get_text("tab_voice_input", st.session_state.language)
    ])

    with tab_voice:
        st.markdown("#### 🎙️ Multilingual Voice Input (OpenAI Whisper)")
        st.info("Speak clearly into your microphone in your preferred language (English, Hindi, Kannada, Telugu). Whisper will transcribe your voice into text.")
        
        audio_file = st.file_uploader("Upload audio recording (WAV/MP3/M4A/WebM) or use microphone:", type=["wav", "mp3", "m4a", "webm", "ogg"], key="audio_uploader")
        
        if audio_file is not None:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/wav")
            
            if st.button("✨ Transcribe Audio with Whisper", type="primary", key="btn_whisper_transcribe"):
                with st.spinner("Processing speech with OpenAI Whisper..."):
                    res = transcribe_audio(audio_bytes, filename=audio_file.name, language=get_language_code(st.session_state.language))
                    if res.get("success"):
                        transcription = res.get("text", "")
                        st.session_state.symptom_input_text = transcription
                        st.success("✅ Voice transcribed successfully! You can review and edit below:")
                    else:
                        st.error(res.get("error"))

    with tab_txt:
        # Quick symptom helper chips
        st.markdown(f"**{get_text('quick_symptoms_label', st.session_state.language)}**")
        chip_cols = st.columns(4)
        common_chips = [
            ("fever", "Fever / बुखार / ಜ್ವರ"),
            ("cough", "Cough / खांसी / ಕೆಮ್ಮು"),
            ("headache", "Headache / सिरदर्द / ತಲೆನೋವು"),
            ("cold", "Cold / सर्दी / ಶೀತ"),
            ("body_pain", "Body Pain / बदन दर्द / ಮೈಕೈ ನೋವು"),
            ("vomiting", "Vomiting / उल्टी / ವಾಂತಿ"),
            ("abdominal_pain", "Stomach Pain / पेट दर्द / ಹೊಟ್ಟೆ ನೋವು"),
            ("breathing_difficulty", "Breathing Issue / सांस तकलीफ / ಉಸಿರಾಟದ ತೊಂದರೆ")
        ]
        
        for idx, (sym_key, sym_label) in enumerate(common_chips):
            col = chip_cols[idx % 4]
            with col:
                is_selected = sym_key in st.session_state.selected_symptom_chips
                if st.button(f"{'✅ ' if is_selected else '+ '}{sym_label}", key=f"chip_{sym_key}", use_container_width=True):
                    if is_selected:
                        st.session_state.selected_symptom_chips.remove(sym_key)
                    else:
                        st.session_state.selected_symptom_chips.append(sym_key)
                    st.rerun()

    # Shared Symptom Description Textarea
    st.markdown("---")
    symptom_text_val = st.text_area(
        get_text("transcribed_heading", st.session_state.language),
        value=st.session_state.symptom_input_text,
        height=130,
        placeholder=get_text("lbl_text_placeholder", st.session_state.language),
        key="symptom_text_area_input"
    )
    st.session_state.symptom_input_text = symptom_text_val

    col_sub1, col_sub2 = st.columns([6, 4])
    with col_sub1:
        if st.button(get_text("btn_submit_triage", st.session_state.language), type="primary", use_container_width=True):
            if not st.session_state.symptom_input_text.strip() and not st.session_state.selected_symptom_chips:
                st.error("Please describe or select at least one symptom to proceed.")
            else:
                with st.spinner("Analyzing symptoms using Random Forest classifier..."):
                    pred = predict_triage_priority(
                        st.session_state.symptom_input_text,
                        st.session_state.selected_symptom_chips
                    )
                    st.session_state.last_prediction = pred
                    
                    # Create consultation in database
                    detected_str = ", ".join(pred.get("detected_symptoms", []))
                    cid = db.create_consultation(
                        patient_id=pat["patient_id"],
                        symptoms_text=st.session_state.symptom_input_text,
                        detected_symptoms=detected_str,
                        triage_priority=pred["predicted_priority"],
                        triage_confidence=pred["confidence_score"],
                        input_method="voice" if audio_file else "text",
                        triage_metadata=pred
                    )
                    st.session_state.current_consultation_id = cid
                    navigate_to("triage_assessment")


# ==============================================================================
# 7. AI PRELIMINARY TRIAGE ASSESSMENT RESULT
# ==============================================================================
elif st.session_state.page == "triage_assessment":
    if not st.session_state.last_prediction or not st.session_state.current_consultation_id:
        navigate_to("symptom_entry")

    pred = st.session_state.last_prediction
    priority = pred["predicted_priority"]
    conf = pred["confidence_score"]

    st.markdown(f"<div class='hero-title'>{get_text('triage_title', st.session_state.language)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='hero-subtitle'>{get_text('triage_subtitle', st.session_state.language)}</div>", unsafe_allow_html=True)

    if pred.get("is_emergency"):
        st.markdown(f"""
        <div class='emergency-banner'>
            🚨 {get_text('triage_emergency_alert', st.session_state.language)}
        </div>
        """, unsafe_allow_html=True)

    with st.container(border=True):
        badge_class = {
            "Low Priority": "badge-low",
            "Moderate Priority": "badge-moderate",
            "High Priority": "badge-high",
            "Urgent Attention": "badge-urgent"
        }.get(priority, "badge-moderate")

        st.markdown(f"""
        <div style='margin-bottom: 12px;'>
            <span style='font-size: 1.05rem; font-weight: 700;'>{get_text('triage_priority_label', st.session_state.language)}</span>
            <span class='{badge_class}' style='font-size: 1.05rem; margin-left: 8px;'>{priority}</span>
        </div>
        <div style='font-size: 0.92rem; color: #475569; margin-bottom: 8px;'>
            <strong>{get_text('triage_confidence_label', st.session_state.language)}</strong> {int(conf * 100)}%
        </div>
        <div style='font-size: 0.92rem; color: #475569; margin-bottom: 8px;'>
            <strong>{get_text('triage_detected_label', st.session_state.language)}</strong> {', '.join(pred.get('detected_symptoms', []))}
        </div>
        <div style='font-size: 0.92rem; color: #475569; margin-bottom: 8px;'>
            <strong>{get_text('triage_explanation_label', st.session_state.language)}</strong> {pred.get('explanation', '')}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='disclaimer-box'>
        <strong>Clinical Safety Notice:</strong> {get_text('triage_disclaimer', st.session_state.language)}
    </div>
    """, unsafe_allow_html=True)

    col_t1, col_t2 = st.columns([6, 4])
    with col_t1:
        if st.button(get_text("btn_proceed_waiting", st.session_state.language), type="primary", use_container_width=True):
            navigate_to("waiting_room")
    with col_t2:
        if st.button("🔊 Read Out Results (Voice)", use_container_width=True):
            tts_text = f"Your preliminary triage assessment is {priority}. An attending physician will consult with you shortly."
            play_tts(tts_text)


# ==============================================================================
# 8. PATIENT WAITING ROOM & LIVE WEBRTC CALL
# ==============================================================================
elif st.session_state.page == "waiting_room":
    if not st.session_state.current_consultation_id:
        navigate_to("patient_portal")

    cid = st.session_state.current_consultation_id
    cns = db.get_consultation_by_id(cid)
    pat = st.session_state.logged_patient or {}

    st.markdown(f"<div class='hero-title'>{get_text('waiting_title', st.session_state.language)}</div>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
            <div>
                <span style='font-size: 1.1rem; font-weight: 700;'>{get_text('waiting_token', st.session_state.language)}</span>
                <span style='font-size: 1.2rem; font-weight: 800; color: #0284C7; margin-left: 8px;'>{cid}</span>
            </div>
            <div>
                <span style='font-size: 0.9rem; color: #64748B;'>{get_text('waiting_status', st.session_state.language)}</span>
                <span style='font-size: 0.95rem; font-weight: 700; color: #0F172A; margin-left: 6px;'>{cns.get('consultation_status', 'Waiting for doctor')}</span>
            </div>
        </div>
        <p style='color: #475569; font-size: 0.92rem;'>
            {get_text('waiting_instructions', st.session_state.language)}
        </p>
        """, unsafe_allow_html=True)

    # Check if prescription was completed
    rx = db.get_prescription_by_consultation_id(cid)
    if rx:
        st.success("🎉 Consultation completed! Your digital prescription is ready below.")
        with st.expander("📄 View My Digital Prescription", expanded=True):
            html_doc = generate_prescription_html(rx, pat, {"full_name": rx.get("doctor_name", "Doctor"), "specialization": rx.get("specialization", "General Medicine"), "license_number": rx.get("license_number", "")})
            st.components.v1.html(html_doc, height=520, scrolling=True)
            st.download_button("📥 Download Prescription (HTML)", data=html_doc, file_name=f"Prescription_{cid}.html", mime="text/html")
    else:
        st.markdown("### 🎥 Live Video Consultation Room")
        webrtc_html = render_webrtc_consultation(
            room_id=cid,
            user_role="patient",
            user_name=pat.get("full_name", "Patient")
        )
        st.components.v1.html(webrtc_html, height=520)

    col_w1, col_w2 = st.columns([1, 1])
    with col_w1:
        if st.button("🔄 " + get_text("btn_refresh_status", st.session_state.language), use_container_width=True):
            st.rerun()
    with col_w2:
        if st.button("📋 " + get_text("nav_ehr", st.session_state.language), use_container_width=True):
            navigate_to("patient_ehr")


# ==============================================================================
# 9. PATIENT ELECTRONIC HEALTH RECORD (EHR) HISTORY
# ==============================================================================
elif st.session_state.page == "patient_ehr":
    if not st.session_state.logged_patient:
        navigate_to("patient_portal")

    pat = st.session_state.logged_patient
    pid = pat["patient_id"]
    ehr_data = get_complete_patient_history(pid)

    st.markdown(f"<div class='hero-title'>{get_text('ehr_title', st.session_state.language)}</div>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f"""
        **Patient Name:** {pat.get('full_name')} &nbsp;|&nbsp; 
        **Patient ID:** `{pid}` &nbsp;|&nbsp; 
        **Age / Gender:** {pat.get('age')} Yrs / {pat.get('gender')} &nbsp;|&nbsp; 
        **Location:** {pat.get('location') or 'Not specified'}
        """)

    st.markdown(f"<div class='section-label'>{get_text('ehr_past_consultations', st.session_state.language)}</div>", unsafe_allow_html=True)
    consultations = ehr_data.get("consultations", [])

    if not consultations:
        st.info(get_text("ehr_no_records", st.session_state.language))
    else:
        for idx, cns in enumerate(consultations, 1):
            with st.expander(f"Consultation {cns.get('consultation_id')} - {cns.get('created_at')} ({cns.get('triage_priority')})", expanded=(idx == 1)):
                st.markdown(f"""
                - **Symptoms Reported:** {cns.get('symptoms_text')}
                - **Detected Clinical Markers:** {cns.get('detected_symptoms')}
                - **Triage Urgency:** `{cns.get('triage_priority')}` (Confidence: {int(float(cns.get('triage_confidence', 0.8)) * 100)}%)
                - **Attending Doctor:** {cns.get('doctor_name') or 'Pending Assignment'}
                - **Doctor Observations:** {cns.get('doctor_observations') or cns.get('doctor_notes') or 'No notes logged.'}
                """)
                
                if cns.get("prescription"):
                    rx = cns["prescription"]
                    st.markdown("**Prescribed Medications:**")
                    for med in rx.get("items", []):
                        st.markdown(f"• **{med.get('medicine_name')}** - {med.get('dosage')}, {med.get('frequency')} for {med.get('duration')} *({med.get('instructions')})*")

    if st.button("← " + get_text("btn_back_home", st.session_state.language)):
        navigate_to("home")


# ==============================================================================
# 10. DOCTOR PORTAL (LOGIN & REGISTRATION)
# ==============================================================================
elif st.session_state.page == "doctor_portal":
    st.markdown(f"<div class='hero-title'>{get_text('doctor_auth_title', st.session_state.language)}</div>", unsafe_allow_html=True)
    
    if st.session_state.logged_doctor:
        doc = st.session_state.logged_doctor
        st.success(f"Logged in as **{doc.get('full_name')}** ({doc.get('specialization')})")
        if st.button("Go to Doctor Dashboard →", type="primary"):
            navigate_to("doctor_dashboard")
    else:
        tab_d_login, tab_d_reg = st.tabs([
            get_text("doctor_login_tab", st.session_state.language),
            get_text("doctor_reg_tab", st.session_state.language)
        ])

        with tab_d_login:
            with st.form("doctor_login_form"):
                d_id = st.text_input(get_text("lbl_doctor_id", st.session_state.language), value="doctor@kiosk.in")
                d_pass = st.text_input(get_text("lbl_password", st.session_state.language), type="password", value="doctor123")
                submit_doc_login = st.form_submit_button(get_text("btn_login", st.session_state.language), type="primary")

                if submit_doc_login:
                    doctor = db.authenticate_doctor(d_id, d_pass)
                    if doctor:
                        st.session_state.logged_doctor = doctor
                        st.success(f"Welcome back, {doctor.get('full_name')}!")
                        time.sleep(0.5)
                        navigate_to("doctor_dashboard")
                    else:
                        st.error("Invalid Doctor credentials. Please check ID/Email and password.")

        with tab_d_reg:
            with st.form("doctor_reg_form"):
                dr_name = st.text_input(get_text("lbl_full_name", st.session_state.language), placeholder="Dr. Firstname Lastname")
                dr_email = st.text_input(get_text("lbl_email", st.session_state.language), placeholder="doctor@health.gov.in")
                dr_spec = st.text_input(get_text("lbl_specialization", st.session_state.language), placeholder="General Medicine / Primary Care")
                dr_lic = st.text_input(get_text("lbl_license_no", st.session_state.language), placeholder="MCI-123456")
                dr_phone = st.text_input(get_text("lbl_phone", st.session_state.language), placeholder="10-digit mobile number")
                dr_pass = st.text_input(get_text("lbl_password", st.session_state.language), type="password")

                submit_doc_reg = st.form_submit_button(get_text("btn_register", st.session_state.language), type="primary")

                if submit_doc_reg:
                    if not dr_name.strip() or not dr_email.strip():
                        st.error("Please fill all required doctor registration fields.")
                    else:
                        new_doc_id = db.register_doctor_account(
                            full_name=dr_name,
                            email=dr_email,
                            doctor_id="",
                            phone_number=dr_phone,
                            password=dr_pass,
                            specialization=dr_spec,
                            license_number=dr_lic
                        )
                        st.session_state.logged_doctor = db.get_doctor_by_id(new_doc_id)
                        st.success(f"Doctor registration successful! Doctor ID: **{new_doc_id}**")
                        time.sleep(0.8)
                        navigate_to("doctor_dashboard")

    if st.button("← " + get_text('btn_back_home', st.session_state.language), key="doc_portal_back"):
        navigate_to("home")


# ==============================================================================
# 11. DOCTOR TELEMEDICINE DASHBOARD & QUEUE
# ==============================================================================
elif st.session_state.page == "doctor_dashboard":
    if not st.session_state.logged_doctor:
        navigate_to("doctor_portal")

    doc = st.session_state.logged_doctor
    st.markdown(f"<div class='hero-title'>{get_text('doc_dash_title', st.session_state.language)}</div>", unsafe_allow_html=True)
    st.markdown(f"**Attending Physician:** {doc.get('full_name')} &nbsp;|&nbsp; **Specialization:** {doc.get('specialization')} &nbsp;|&nbsp; **ID:** `{doc.get('doctor_id')}`")

    # Metrics Row
    stats = db.get_queue_summary_stats()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Patients", stats.get("total_patients", 0))
    m2.metric("Waiting in Queue", stats.get("waiting", 0))
    m3.metric("Under Consultation", stats.get("in_progress", 0))
    m4.metric("Completed", stats.get("completed", 0))

    tab_q, tab_comp, tab_metrics = st.tabs([
        get_text("doc_queue_tab", st.session_state.language),
        get_text("doc_completed_tab", st.session_state.language),
        get_text("doc_model_tab", st.session_state.language)
    ])

    with tab_q:
        all_cases = db.get_all_consultations()
        waiting_cases = [c for c in all_cases if c.get("consultation_status") != "Completed"]
        
        if not waiting_cases:
            st.info("No patients currently waiting in the queue.")
        else:
            for cns in waiting_cases:
                cid = cns.get("consultation_id")
                priority = cns.get("triage_priority", "Moderate Priority")
                
                badge_class = {
                    "Low Priority": "badge-low",
                    "Moderate Priority": "badge-moderate",
                    "High Priority": "badge-high",
                    "Urgent Attention": "badge-urgent"
                }.get(priority, "badge-moderate")

                with st.container(border=True):
                    c_h1, c_h2 = st.columns([7, 3])
                    with c_h1:
                        st.markdown(f"""
                        <div style='display: flex; align-items: center; gap: 8px;'>
                            <span style='font-size: 1.05rem; font-weight: 700;'>{cns.get('patient_name')}</span>
                            <span style='color: #64748B; font-size: 0.88rem;'>({cns.get('age')} Y, {cns.get('gender')})</span>
                            <span class='{badge_class}'>{priority}</span>
                        </div>
                        <div style='font-size: 0.88rem; color: #475569; margin-top: 4px;'>
                            <strong>Token:</strong> <code>{cid}</code> | <strong>Location:</strong> {cns.get('location') or 'Rural Outpost'} | <strong>Time:</strong> {cns.get('created_at')}
                        </div>
                        <div style='font-size: 0.9rem; color: #334155; margin-top: 4px;'>
                            <strong>Symptoms:</strong> {cns.get('symptoms_text')}
                        </div>
                        """, unsafe_allow_html=True)
                    with c_h2:
                        if st.button("Consult Patient 🩺", key=f"btn_consult_{cid}", type="primary", use_container_width=True):
                            st.session_state.selected_doctor_case_id = cid
                            db.update_consultation_status(cid, "Under consultation", doctor_id=doc.get("doctor_id"))
                            navigate_to("doctor_consultation_room")

    with tab_comp:
        all_cases = db.get_all_consultations()
        completed_cases = [c for c in all_cases if c.get("consultation_status") == "Completed"]
        
        if not completed_cases:
            st.info("No completed consultations yet.")
        else:
            for cns in completed_cases:
                cid = cns.get("consultation_id")
                with st.expander(f"Case {cid} - {cns.get('patient_name')} ({cns.get('triage_priority')})"):
                    st.markdown(f"""
                    - **Patient:** {cns.get('patient_name')} (ID: {cns.get('patient_id')})
                    - **Symptoms:** {cns.get('symptoms_text')}
                    - **Doctor Observations:** {cns.get('doctor_observations') or cns.get('doctor_notes')}
                    - **Completed Date:** {cns.get('completed_at') or cns.get('updated_at')}
                    """)
                    rx = db.get_prescription_by_consultation_id(cid)
                    if rx:
                        st.markdown("**Prescription Medicines:**")
                        for m in rx.get("items", []):
                            st.markdown(f"• {m.get('medicine_name')} - {m.get('dosage')} ({m.get('frequency')})")

    with tab_metrics:
        st.markdown("#### 📊 Supervised Random Forest Classifier Transparency Report")
        metrics_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "model_metrics.json")
        if os.path.exists(metrics_file):
            with open(metrics_file, "r") as f:
                metrics_data = json.load(f)
            
            c_m1, c_m2, c_m3 = st.columns(3)
            c_m1.metric("Holdout Test Accuracy", f"{metrics_data.get('holdout_test_accuracy')}%")
            c_m2.metric("Cross-Validation Accuracy", f"{metrics_data.get('cross_val_accuracy_mean')}% ± {metrics_data.get('cross_val_accuracy_std')}%")
            c_m3.metric("Weighted F1-Score", f"{metrics_data.get('holdout_weighted_f1')}%")

            st.json(metrics_data)
        else:
            st.warning("Model metrics file not found. Run `python ml/train_model.py` to regenerate.")


# ==============================================================================
# 12. DOCTOR CONSULTATION WORKSPACE (WEBRTC + NOTES + PRESCRIPTION BUILDER)
# ==============================================================================
elif st.session_state.page == "doctor_consultation_room":
    if not st.session_state.logged_doctor or not st.session_state.selected_doctor_case_id:
        navigate_to("doctor_dashboard")

    doc = st.session_state.logged_doctor
    cid = st.session_state.selected_doctor_case_id
    cns = db.get_consultation_by_id(cid)
    pat = db.get_patient_by_id(cns["patient_id"])

    st.markdown(f"<div class='hero-title'>{get_text('doc_consultation_title', st.session_state.language)}: {cns.get('patient_name')}</div>", unsafe_allow_html=True)
    
    # Patient Summary Card
    with st.container(border=True):
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between;'>
            <div>
                <strong>Patient:</strong> {pat.get('full_name')} (ID: <code>{pat.get('patient_id')}</code>) | 
                <strong>Age/Gender:</strong> {pat.get('age')}Y / {pat.get('gender')} | 
                <strong>Location:</strong> {pat.get('location')}
            </div>
            <div>
                <strong>AI Triage:</strong> <span class='badge-urgent' style='padding: 2px 6px;'>{cns.get('triage_priority')}</span>
            </div>
        </div>
        <div style='margin-top: 6px; font-size: 0.9rem; color: #334155;'>
            <strong>Patient Symptoms:</strong> {cns.get('symptoms_text')}
        </div>
        """, unsafe_allow_html=True)

    # 1. Live WebRTC Call Window
    st.markdown("### 🎥 Live Video Consultation Feed")
    webrtc_html = render_webrtc_consultation(
        room_id=cid,
        user_role="doctor",
        user_name=doc.get("full_name", "Doctor")
    )
    st.components.v1.html(webrtc_html, height=520)

    # 2. Clinical Notes & Observations
    st.markdown("### 📝 Clinical Observations & Advice")
    with st.form("doc_notes_form"):
        c_comp = st.text_input(get_text("doc_complaint_lbl", st.session_state.language), value=cns.get("symptoms_text", ""))
        c_obs = st.text_area(get_text("doc_notes_lbl", st.session_state.language), placeholder="Enter clinical observations, vital signs check, examination notes...")
        c_adv = st.text_area(get_text("doc_advice_lbl", st.session_state.language), placeholder="Rest, hydration, dietary precautions...")
        c_fol = st.text_input(get_text("doc_followup_lbl", st.session_state.language), placeholder="Follow up in 3 days if fever persists.")
        save_notes_btn = st.form_submit_button("💾 Save Clinical Notes")
        
        if save_notes_btn:
            db.update_doctor_notes(
                consultation_id=cid,
                notes=c_obs,
                chief_complaint=c_comp,
                observations=c_obs,
                advice=c_adv,
                followup=c_fol
            )
            st.success("Clinical notes saved successfully.")

    # 3. Digital Prescription Builder
    st.markdown(f"### 💊 {get_text('rx_builder_title', st.session_state.language)}")
    
    with st.container(border=True):
        st.markdown("**Current Prescription Items:**")
        for idx, med in enumerate(st.session_state.prescription_medicines):
            st.markdown(f"{idx+1}. **{med.get('medicine_name')}** | {med.get('dosage')} | {med.get('frequency')} | {med.get('duration')} | *{med.get('instructions')}*")

        # Form to add new medicine
        with st.form("add_medicine_form"):
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                m_name = st.text_input(get_text("rx_medicine_name", st.session_state.language), placeholder="e.g. Amoxicillin 500mg")
                m_dose = st.text_input(get_text("rx_dosage", st.session_state.language), value="1 tab")
            with c_m2:
                m_freq = st.text_input(get_text("rx_frequency", st.session_state.language), value="Twice daily after food")
                m_dur = st.text_input(get_text("rx_duration", st.session_state.language), value="5 days")
            m_inst = st.text_input(get_text("rx_instructions", st.session_state.language), placeholder="Take after meals")
            
            if st.form_submit_button(get_text("btn_add_medicine", st.session_state.language)):
                if m_name.strip():
                    st.session_state.prescription_medicines.append({
                        "medicine_name": m_name,
                        "dosage": m_dose,
                        "frequency": m_freq,
                        "duration": m_dur,
                        "instructions": m_inst
                    })
                    st.success(f"Added {m_name} to prescription.")
                    st.rerun()

        # Complete consultation button
        if st.button(get_text("btn_save_consultation", st.session_state.language), type="primary", use_container_width=True):
            rx_id = db.create_prescription(
                consultation_id=cid,
                patient_id=pat["patient_id"],
                doctor_id=doc["doctor_id"],
                medicines=st.session_state.prescription_medicines,
                general_notes=f"Chief Complaint: {c_comp}. Advice: {c_adv}. Followup: {c_fol}"
            )
            st.success(f"Prescription issued successfully! Rx ID: **{rx_id}**. Consultation marked as Completed.")
            time.sleep(1.2)
            navigate_to("doctor_dashboard")

    if st.button("← " + get_text("btn_back_dashboard", st.session_state.language)):
        navigate_to("doctor_dashboard")
