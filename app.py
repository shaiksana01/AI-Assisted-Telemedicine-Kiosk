"""
AI-Assisted Telemedicine Kiosk
Healthcare support for rural communities
================================================================================
A clean, student-built healthcare website with separate Patient and Doctor portals,
step-by-step consultation flow, and ML triage support.
"""

import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime

# Database and ML modules
from database.database import (
    init_db,
    register_patient_account,
    authenticate_patient,
    register_doctor_account,
    authenticate_doctor,
    create_consultation,
    get_patient_by_id,
    get_consultation_by_id,
    get_all_consultations,
    update_consultation_status,
    update_doctor_notes,
    get_queue_summary_stats
)
from ml.predict import (
    predict_triage_priority,
    load_triage_model,
    SYMPTOM_DISPLAY_NAMES,
    SYMPTOM_COLUMNS
)
from utils.translations import get_text, get_available_languages

# Page Config
st.set_page_config(
    page_title="AI-Assisted Telemedicine Kiosk",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize database
init_db()

# Clean, Light Healthcare Website CSS
st.markdown("""
<style>
    /* Hide Streamlit default sidebar and header */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Base Typography & Light Healthcare Background */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #263238;
        background-color: #F8FAFC;
    }
    
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Central Content Constraints */
    .block-container {
        max-width: 1040px !important;
        padding-top: 1.25rem !important;
        padding-bottom: 2.5rem !important;
        background-color: #F8FAFC;
    }
    
    /* Top Website Header */
    .brand-title {
        font-size: 1.12rem;
        font-weight: 700;
        color: #1E3A5F;
        padding-top: 4px;
        letter-spacing: -0.2px;
    }
    
    /* Header Navigation Links */
    .st-key-top_home_btn button,
    .st-key-top_about_btn button,
    .st-key-top_help_btn button,
    div[class*="st-key-top_"] button {
        background: transparent !important;
        border: none !important;
        border-bottom: 2.5px solid transparent !important;
        box-shadow: none !important;
        color: #64748B !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        padding: 4px 10px 6px 10px !important;
        min-height: unset !important;
        height: auto !important;
        border-radius: 0 !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
        width: 100% !important;
        text-align: center !important;
        transition: color 0.15s ease, border-color 0.15s ease !important;
    }
    
    .st-key-top_home_btn button p,
    .st-key-top_about_btn button p,
    .st-key-top_help_btn button p,
    div[class*="st-key-top_"] button p,
    div[class*="st-key-top_"] button span {
        font-size: 0.95rem !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .st-key-top_home_btn button:hover,
    .st-key-top_about_btn button:hover,
    .st-key-top_help_btn button:hover,
    div[class*="st-key-top_"] button:hover {
        background: transparent !important;
        color: #1E3A5F !important;
        border: none !important;
        border-bottom: 2.5px solid #CBD5E1 !important;
    }
    
    /* Active Link State */
    .st-key-top_home_btn button[kind="primary"],
    .st-key-top_about_btn button[kind="primary"],
    .st-key-top_help_btn button[kind="primary"],
    .st-key-top_home_btn button[data-testid="baseButton-primary"],
    .st-key-top_about_btn button[data-testid="baseButton-primary"],
    .st-key-top_help_btn button[data-testid="baseButton-primary"],
    div[class*="st-key-top_"] button[kind="primary"],
    div[class*="st-key-top_"] button[data-testid="baseButton-primary"] {
        background: transparent !important;
        color: #1E3A5F !important;
        font-weight: 700 !important;
        border: none !important;
        border-bottom: 2.5px solid #237099 !important;
    }
    
    /* Hero Section */
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #1E3A5F;
        line-height: 1.2;
        margin-bottom: 12px;
        letter-spacing: -0.4px;
    }
    
    .hero-subtitle {
        font-size: 1.12rem;
        font-weight: 600;
        color: #237099;
        margin-bottom: 12px;
    }
    
    .hero-desc {
        font-size: 0.95rem;
        color: #64748B;
        line-height: 1.55;
        margin-bottom: 20px;
    }
    
    .section-label {
        font-size: 1.12rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-top: 26px;
        margin-bottom: 14px;
    }
    
    /* Choice Cards Container */
    div[data-testid="column"]:has(button[key="home_patient_btn"]) [data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="column"]:has(button[key="home_doctor_btn"]) [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 24px 24px 22px 24px !important;
        min-height: 180px !important;
        height: 100% !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        box-sizing: border-box !important;
    }
    
    div[data-testid="column"]:has(button[key="home_patient_btn"]) [data-testid="stVerticalBlockBorderWrapper"] > div,
    div[data-testid="column"]:has(button[key="home_doctor_btn"]) [data-testid="stVerticalBlockBorderWrapper"] > div {
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        gap: 20px !important;
    }
    
    .choice-card-header {
        display: flex;
        align-items: flex-start;
        gap: 16px;
    }
    
    .choice-icon-circle {
        width: 44px;
        height: 44px;
        min-width: 44px;
        border-radius: 50%;
        background-color: #E0F2FE;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 2px;
    }
    
    .choice-card-text {
        flex: 1;
    }
    
    .choice-card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 4px;
    }
    
    .choice-card-desc {
        font-size: 0.88rem;
        color: #64748B;
        line-height: 1.45;
    }
    
    .page-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 6px;
    }
    
    .page-subtitle {
        font-size: 0.9rem;
        color: #64748B;
        margin-bottom: 18px;
    }
    
    /* Action Buttons Styling */
    .st-key-home_patient_btn button,
    button[data-testid="baseButton-primary"]:not([key^="top_"]) {
        background-color: #237099 !important;
        color: #FFFFFF !important;
        border: 1px solid #237099 !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 0.92rem !important;
        padding: 9px 18px !important;
        min-height: 40px !important;
        height: 40px !important;
        width: 100% !important;
        margin-top: auto !important;
        transition: background-color 0.15s ease, border-color 0.15s ease !important;
    }
    .st-key-home_patient_btn button:hover,
    button[data-testid="baseButton-primary"]:not([key^="top_"]):hover {
        background-color: #1A5676 !important;
        border-color: #1A5676 !important;
        color: #FFFFFF !important;
    }
    
    .st-key-home_doctor_btn button,
    button[data-testid="baseButton-secondary"]:not([key^="top_"]) {
        background-color: #FFFFFF !important;
        color: #237099 !important;
        border: 1.5px solid #237099 !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 0.92rem !important;
        padding: 9px 18px !important;
        min-height: 40px !important;
        height: 40px !important;
        width: 100% !important;
        margin-top: auto !important;
        transition: background-color 0.15s ease, border-color 0.15s ease !important;
    }
    .st-key-home_doctor_btn button:hover,
    button[data-testid="baseButton-secondary"]:not([key^="top_"]):hover {
        background-color: #F0F9FF !important;
        color: #1A5676 !important;
        border-color: #1A5676 !important;
    }
    
    /* Form inputs and textareas */
    input, textarea, select {
        background-color: #FFFFFF !important;
        border: 1px solid #D9E3EA !important;
        color: #263238 !important;
        border-radius: 4px !important;
    }
    input:focus, textarea:focus, select:focus {
        border-color: #237099 !important;
        box-shadow: 0 0 0 1px #237099 !important;
    }
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
        background-color: #FFFFFF !important;
        border-color: #D9E3EA !important;
        color: #263238 !important;
    }
    [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label {
        color: #263238 !important;
    }
    
    /* Hero Image */
    .stImage img {
        border-radius: 8px;
        max-height: 250px !important;
        width: 100% !important;
        object-fit: cover;
    }
    
    /* Consultation Stepper Bar */
    .consultation-stepper {
        display: flex;
        justify-content: center;
        gap: 8px;
        font-size: 0.82rem;
        color: #607080;
        padding-bottom: 12px;
        margin-bottom: 20px;
        border-bottom: 1px solid #D9E3EA;
    }
    
    .step-current {
        color: #2F6F95;
        font-weight: 700;
    }
    
    .step-past {
        color: #607080;
    }
    
    /* Footer Disclaimer Note */
    .footer-disclaimer {
        font-size: 0.78rem;
        color: #8A9BA8;
        text-align: center;
        margin-top: 36px;
        padding-top: 14px;
        border-top: 1px solid #E4ECF2;
    }
    
    /* Priority Badges */
    .badge-low {
        background-color: #EAF3F8;
        color: #1E3A5F;
        border: 1px solid #D9E3EA;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .badge-moderate {
        background-color: #FFFBEB;
        color: #92400E;
        border: 1px solid #FDE68A;
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
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "page" not in st.session_state:
    st.session_state.page = "home"
if "language" not in st.session_state:
    st.session_state.language = "English"

# Active user sessions
if "logged_patient" not in st.session_state:
    st.session_state.logged_patient = None
if "logged_doctor" not in st.session_state:
    st.session_state.logged_doctor = None

# Active consultation session
if "current_consultation" not in st.session_state:
    st.session_state.current_consultation = None
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None
if "selected_doctor_case" not in st.session_state:
    st.session_state.selected_doctor_case = None

# Transient form fields
if "symptom_input_text" not in st.session_state:
    st.session_state.symptom_input_text = ""

def navigate_to(page_name: str):
    """Navigate to a target page and rerun."""
    st.session_state.page = page_name
    st.rerun()

# ------------------------------------------------------------------------------
# 1. TOP HEADER (AI-Assisted Telemedicine Kiosk | Home - About - Help)
# ------------------------------------------------------------------------------
h_col1, h_col2 = st.columns([6, 3], gap="medium")

with h_col1:
    st.markdown("<div class='brand-title'>AI-Assisted Telemedicine Kiosk</div>", unsafe_allow_html=True)

with h_col2:
    nav_c1, nav_c2, nav_c3 = st.columns([1, 1, 1], gap="small")
    with nav_c1:
        if st.button("Home", key="top_home_btn", use_container_width=True, type="primary" if st.session_state.page == "home" else "secondary"):
            navigate_to("home")
    with nav_c2:
        if st.button("About", key="top_about_btn", use_container_width=True, type="primary" if st.session_state.page == "about" else "secondary"):
            navigate_to("about")
    with nav_c3:
        if st.button("Help", key="top_help_btn", use_container_width=True, type="primary" if st.session_state.page == "help" else "secondary"):
            navigate_to("help")

st.markdown("<hr style='margin: 4px 0 24px 0; border: 0; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)


# ==============================================================================
# 2. HOMEPAGE
# ==============================================================================
if st.session_state.page == "home":
    col_left, col_right = st.columns([5.5, 4.5], gap="large")
    
    with col_left:
        st.markdown("<div class='hero-title'>AI-Assisted Telemedicine<br>Kiosk</div>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle'>Healthcare support for rural communities</div>", unsafe_allow_html=True)
        st.markdown("<p class='hero-desc'>Register as a patient or access the doctor portal to continue.</p>", unsafe_allow_html=True)
        
    with col_right:
        img_jpg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "telemedicine_hero.jpg")
        img_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "telemedicine_hero.png")
        if os.path.exists(img_jpg):
            st.image(img_jpg, use_container_width=True)
        elif os.path.exists(img_png):
            st.image(img_png, use_container_width=True)
        else:
            st.image("https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=600&q=80", use_container_width=True)
            
    st.markdown("<div class='section-label'>Choose how you want to continue</div>", unsafe_allow_html=True)
    
    card_p, card_d = st.columns(2, gap="medium")
    with card_p:
        with st.container(border=True):
            st.markdown("""
            <div class='choice-card-header'>
                <div class='choice-icon-circle'>
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                </div>
                <div class='choice-card-text'>
                    <div class='choice-card-title'>Patient</div>
                    <div class='choice-card-desc'>For registering, describing symptoms and receiving preliminary assessment.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Continue as Patient →", key="home_patient_btn", type="primary", use_container_width=True):
                navigate_to("patient_landing")
            
    with card_d:
        with st.container(border=True):
            st.markdown("""
            <div class='choice-card-header'>
                <div class='choice-icon-circle'>
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"></path>
                        <path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4"></path>
                        <circle cx="20" cy="10" r="2"></circle>
                    </svg>
                </div>
                <div class='choice-card-text'>
                    <div class='choice-card-title'>Doctor</div>
                    <div class='choice-card-desc'>For viewing submitted patient cases and continuing consultation.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Continue as Doctor →", key="home_doctor_btn", type="secondary", use_container_width=True):
                navigate_to("doctor_landing")
            
    st.markdown("""
    <hr style='margin: 40px 0 16px 0; border: 0; border-top: 1px solid #E2E8F0;'>
    <div style='font-size: 0.76rem; color: #94A3B8; text-align: center; margin-bottom: 6px;'>
        Preliminary assessment only. This system does not replace professional medical advice.
    </div>
    <div style='font-size: 0.76rem; color: #94A3B8; text-align: center;'>
        AI-Assisted Telemedicine Kiosk &nbsp;|&nbsp; College Mini Project
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# ABOUT PAGE
# ==============================================================================
elif st.session_state.page == "about":
    st.markdown("<div class='page-title'>About the Project</div>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color: #5F6F7F; line-height: 1.6; font-size: 0.95rem;'>
        The <strong>AI-Assisted Telemedicine Kiosk</strong> is designed to support healthcare access in rural areas. Patients can register their basic details, describe their symptoms in their preferred regional language, and receive a preliminary priority assessment before consulting a doctor.
    </p>
    <p style='color: #5F6F7F; line-height: 1.6; font-size: 0.95rem;'>
        The system helps streamline doctor consultations by prioritizing patient queues based on clinical urgency, allowing healthcare workers and attending doctors to review cases systematically.
    </p>
    """, unsafe_allow_html=True)
    
    if st.button("Back to Home", key="about_back_btn"):
        navigate_to("home")


# ==============================================================================
# HELP PAGE
# ==============================================================================
elif st.session_state.page == "help":
    st.markdown("<div class='page-title'>Help & FAQ</div>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color: #5F6F7F; line-height: 1.6; font-size: 0.95rem;'>
        <strong>For Patients:</strong><br>
        Click 'Continue as Patient' on the homepage. If you are a new patient, choose 'Create Account' to register your details. Once registered or logged in, you will be guided through entering your symptoms and receiving a preliminary assessment before the doctor reviews your case.
    </p>
    <p style='color: #5F6F7F; line-height: 1.6; font-size: 0.95rem;'>
        <strong>For Doctors:</strong><br>
        Click 'Continue as Doctor' on the homepage. Log in using your Doctor ID / Email and password to access the patient queue, review patient symptoms, update consultation status, and save clinical notes.
    </p>
    """, unsafe_allow_html=True)
    
    if st.button("Back to Home", key="help_back_btn"):
        navigate_to("home")


# ==============================================================================
# 3. PATIENT LANDING (Login or Create Account)
# ==============================================================================
elif st.session_state.page == "patient_landing":
    st.markdown("<div class='page-title'>Patient</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Please choose an option to continue</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", key="p_land_login", type="primary", use_container_width=True):
            navigate_to("patient_login")
    with col2:
        if st.button("Create Account", key="p_land_create", type="secondary", use_container_width=True):
            navigate_to("patient_register")
            
    st.markdown("<br><hr style='border: 0; border-top: 1px solid #D9E5EA;'>", unsafe_allow_html=True)
    if st.button("Back to Home", key="p_land_back"):
        navigate_to("home")


# ==============================================================================
# 4. PATIENT LOGIN
# ==============================================================================
elif st.session_state.page == "patient_login":
    st.markdown("<div class='page-title'>Patient Login</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Enter your mobile number and password</div>", unsafe_allow_html=True)
    
    with st.form("p_login_form"):
        p_phone = st.text_input("Mobile Number", placeholder="")
        p_pass = st.text_input("Password", type="password", placeholder="")
        
        st.markdown("<br>", unsafe_allow_html=True)
        login_btn = st.form_submit_button("Login", type="primary", use_container_width=True)
        
    if login_btn:
        if not p_phone.strip():
            st.error("Please enter your mobile number.")
        elif not p_pass.strip():
            st.error("Please enter your password.")
        else:
            patient_record = authenticate_patient(p_phone.strip(), p_pass.strip())
            if patient_record:
                st.session_state.logged_patient = patient_record
                navigate_to("consultation_details")
            else:
                st.error("Invalid mobile number or password. If you are new, please create an account.")
                
    st.markdown("<hr style='border: 0; border-top: 1px solid #D9E5EA; margin: 16px 0;'>", unsafe_allow_html=True)
    st.write("Don't have an account?")
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("Create Account", key="p_login_to_create"):
            navigate_to("patient_register")
    with c_btn2:
        if st.button("Back", key="p_login_back"):
            navigate_to("patient_landing")


# ==============================================================================
# 5. PATIENT REGISTRATION (Create Patient Account)
# ==============================================================================
elif st.session_state.page == "patient_register":
    st.markdown("<div class='page-title'>Create Patient Account</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Please enter your details below</div>", unsafe_allow_html=True)
    
    with st.form("p_register_form"):
        r_name = st.text_input("Full Name", placeholder="")
        
        col_a, col_g = st.columns(2)
        with col_a:
            r_age = st.text_input("Age", placeholder="")
        with col_g:
            r_gender = st.selectbox("Gender", options=["-- Select Gender --", "Male", "Female", "Other"])
            
        r_phone = st.text_input("Mobile Number", placeholder="")
        r_loc = st.text_input("Village / Town", placeholder="")
        r_lang = st.selectbox("Preferred Language", options=["English", "Hindi", "Kannada", "Telugu"])
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            r_pass = st.text_input("Password", type="password", placeholder="")
        with col_p2:
            r_pass_conf = st.text_input("Confirm Password", type="password", placeholder="")
            
        st.markdown("<br>", unsafe_allow_html=True)
        reg_btn = st.form_submit_button("Create Account", type="primary", use_container_width=True)
        
    if reg_btn:
        if not r_name.strip():
            st.error("Please enter your full name.")
        elif not r_age.strip().isdigit() or not (1 <= int(r_age.strip()) <= 120):
            st.error("Please enter a valid age between 1 and 120.")
        elif r_gender == "-- Select Gender --":
            st.error("Please select a gender.")
        elif not r_phone.strip().isdigit() or len(r_phone.strip()) != 10:
            st.error("Please enter a valid 10-digit mobile number.")
        elif not r_pass.strip():
            st.error("Please enter a password.")
        elif r_pass != r_pass_conf:
            st.error("Passwords do not match.")
        else:
            patient_id = register_patient_account(
                full_name=r_name.strip(),
                age=int(r_age.strip()),
                gender=r_gender,
                phone_number=r_phone.strip(),
                preferred_language=r_lang,
                location=r_loc.strip(),
                password=r_pass.strip()
            )
            st.session_state.logged_patient = get_patient_by_id(patient_id)
            navigate_to("patient_register_success")
            
    if st.button("Back", key="p_reg_back"):
        navigate_to("patient_landing")


# ==============================================================================
# 6. PATIENT REGISTRATION SUCCESS
# ==============================================================================
elif st.session_state.page == "patient_register_success":
    patient = st.session_state.logged_patient
    if not patient:
        navigate_to("patient_register")
        st.stop()
        
    st.markdown("<div class='page-title'>Account created successfully.</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <p style='color: #5F6F7F; font-size: 0.95rem; margin-top: 10px;'>
        Your Patient ID is: <strong style='color: #1E3A5F; font-size: 1.15rem;'>{patient['patient_id']}</strong>
    </p>
    <div style='background-color: #FFFFFF; border: 1px solid #D9E5EA; border-radius: 4px; padding: 12px 16px; margin: 16px 0; font-size: 0.9rem; line-height: 1.5;'>
        <strong>Name:</strong> {patient['full_name']}<br>
        <strong>Age / Gender:</strong> {patient['age']} yrs / {patient['gender']}<br>
        <strong>Contact:</strong> {patient['phone_number']}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Continue", key="p_succ_cont", type="primary", use_container_width=True):
        navigate_to("consultation_details")


# ==============================================================================
# 7. PATIENT CONSULTATION - SCREEN 1: PATIENT DETAILS
# ==============================================================================
elif st.session_state.page == "consultation_details":
    patient = st.session_state.logged_patient
    if not patient:
        navigate_to("patient_login")
        st.stop()
        
    st.markdown("""
    <div class='consultation-stepper'>
        <span class='step-current'>1. Patient Details</span> → <span>2. Symptoms</span> → <span>3. Preliminary Assessment</span> → <span>4. Doctor Consultation</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='page-title'>Patient Details</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Confirm your details to proceed with the consultation</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background-color: #FFFFFF; border: 1px solid #D9E5EA; border-radius: 4px; padding: 16px; margin-bottom: 20px; font-size: 0.9rem; line-height: 1.6;'>
        <strong>Patient ID:</strong> {patient['patient_id']}<br>
        <strong>Full Name:</strong> {patient['full_name']}<br>
        <strong>Age / Gender:</strong> {patient['age']} yrs / {patient['gender']}<br>
        <strong>Mobile Number:</strong> {patient['phone_number']}<br>
        <strong>Village / Town:</strong> {patient['location'] or 'Not specified'}<br>
        <strong>Preferred Language:</strong> {patient['preferred_language']}
    </div>
    """, unsafe_allow_html=True)
    
    col_b, col_c = st.columns([1, 2])
    with col_b:
        if st.button("Back", key="c_det_back"):
            navigate_to("patient_landing")
    with col_c:
        if st.button("Continue", key="c_det_cont", type="primary", use_container_width=True):
            navigate_to("consultation_symptoms")


# ==============================================================================
# 8. PATIENT CONSULTATION - SCREEN 2: SYMPTOMS
# ==============================================================================
elif st.session_state.page == "consultation_symptoms":
    patient = st.session_state.logged_patient
    if not patient:
        navigate_to("patient_login")
        st.stop()
        
    st.markdown("""
    <div class='consultation-stepper'>
        <span class='step-past'>1. Patient Details</span> → <span class='step-current'>2. Symptoms</span> → <span>3. Preliminary Assessment</span> → <span>4. Doctor Consultation</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='page-title'>Symptoms</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Please describe the symptoms you are currently experiencing.</div>", unsafe_allow_html=True)
    
    st.caption(f"Patient: **{patient['full_name']}** (ID: {patient['patient_id']})")
    
    symptom_text = st.text_area(
        "Describe your symptoms:",
        value=st.session_state.symptom_input_text,
        placeholder="Example: I have a high fever, dry cough, and headache since yesterday.",
        height=140
    )
    st.session_state.symptom_input_text = symptom_text
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_b, col_c = st.columns([1, 2])
    with col_b:
        if st.button("Back", key="c_sym_back"):
            navigate_to("consultation_details")
    with col_c:
        if st.button("Continue", key="c_sym_cont", type="primary", use_container_width=True):
            if not symptom_text.strip():
                st.error("Please enter your symptoms before continuing.")
            else:
                with st.spinner("Reviewing the information provided..."):
                    # ML Inference
                    prediction = predict_triage_priority(symptom_text=symptom_text.strip())
                    
                    # Store in SQLite
                    consultation_id = create_consultation(
                        patient_id=patient["patient_id"],
                        symptoms_text=symptom_text.strip(),
                        detected_symptoms=", ".join(prediction["detected_symptoms"]),
                        triage_priority=prediction["predicted_priority"],
                        triage_confidence=prediction["confidence_score"]
                    )
                    
                    st.session_state.last_prediction = prediction
                    st.session_state.current_consultation = get_consultation_by_id(consultation_id)
                    navigate_to("consultation_assessment")


# ==============================================================================
# 9. PATIENT CONSULTATION - SCREEN 3: PRELIMINARY ASSESSMENT
# ==============================================================================
elif st.session_state.page == "consultation_assessment":
    prediction = st.session_state.last_prediction
    consultation = st.session_state.current_consultation
    patient = st.session_state.logged_patient
    
    if not prediction or not consultation or not patient:
        navigate_to("home")
        st.stop()
        
    st.markdown("""
    <div class='consultation-stepper'>
        <span class='step-past'>1. Patient Details</span> → <span class='step-past'>2. Symptoms</span> → <span class='step-current'>3. Preliminary Assessment</span> → <span>4. Doctor Consultation</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='page-title'>Preliminary Assessment</div>", unsafe_allow_html=True)
    
    priority_level = prediction["predicted_priority"]
    badge_cls = {
        "Low Priority": "badge-low",
        "Moderate Priority": "badge-moderate",
        "High Priority": "badge-high",
        "Urgent Attention": "badge-urgent"
    }.get(priority_level, "badge-moderate")
    
    st.markdown(f"""
    <div style='background-color: #FFFFFF; border: 1px solid #D9E5EA; border-radius: 4px; padding: 16px; margin: 16px 0;'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
            <div><strong>Patient ID:</strong> {patient['patient_id']}</div>
            <div><span class='{badge_cls}'>{priority_level}</span></div>
        </div>
        <div style='margin-bottom: 8px; font-size: 0.9rem;'>
            <strong>Symptoms:</strong> {consultation['symptoms_text']}
        </div>
        <div style='margin-bottom: 8px; font-size: 0.9rem;'>
            <strong>Detected Symptoms:</strong> {', '.join(prediction['detected_symptoms'])}
        </div>
        <div style='font-size: 0.9rem;'>
            <strong>Confidence:</strong> {prediction['confidence_score']*100:.0f}%
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #EAF3F8; border: 1px solid #D9E3EA; border-left: 3px solid #2F6F95; border-radius: 4px; padding: 10px 14px; font-size: 0.85rem; color: #1E3A5F; margin-bottom: 20px;'>
        This assessment is intended for preliminary decision support only and is not a medical diagnosis.
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Continue to Consultation", key="c_ass_cont", type="primary", use_container_width=True):
        navigate_to("consultation_waiting")


# ==============================================================================
# 10. PATIENT CONSULTATION - SCREEN 4: DOCTOR CONSULTATION / WAITING
# ==============================================================================
elif st.session_state.page == "consultation_waiting":
    consultation = st.session_state.current_consultation
    patient = st.session_state.logged_patient
    
    if not consultation or not patient:
        navigate_to("home")
        st.stop()
        
    latest_record = get_consultation_by_id(consultation["consultation_id"])
    
    st.markdown("""
    <div class='consultation-stepper'>
        <span class='step-past'>1. Patient Details</span> → <span class='step-past'>2. Symptoms</span> → <span class='step-past'>3. Preliminary Assessment</span> → <span class='step-current'>4. Doctor Consultation</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='page-title'>Doctor Consultation</div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #607080; font-size: 0.95rem; margin-bottom: 14px;'>Your information has been submitted for doctor review.</p>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background-color: #FFFFFF; border: 1px solid #D9E3EA; border-radius: 4px; padding: 20px; margin: 16px 0; text-align: left; font-size: 0.92rem; line-height: 1.6;'>
        <strong>Patient ID:</strong> {patient['patient_id']}<br>
        <strong>Patient Name:</strong> {patient['full_name']}<br>
        <strong>Priority:</strong> {latest_record['triage_priority']}<br>
        <strong>Status:</strong> <span style='color: #1E3A5F; font-weight: 600;'>{latest_record['consultation_status']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        if st.button("Refresh Status", key="c_wait_ref", use_container_width=True):
            st.rerun()
    with col_w2:
        if st.button("Return to Home", key="c_wait_home", type="primary", use_container_width=True):
            st.session_state.symptom_input_text = ""
            st.session_state.current_consultation = None
            st.session_state.last_prediction = None
            navigate_to("home")


# ==============================================================================
# 11. DOCTOR LANDING (Login or Create Account)
# ==============================================================================
elif st.session_state.page == "doctor_landing":
    st.markdown("<div class='page-title'>Doctor</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Please choose an option to access the Doctor Portal</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", key="d_land_login", type="primary", use_container_width=True):
            navigate_to("doctor_login")
    with col2:
        if st.button("Create Account", key="d_land_create", type="secondary", use_container_width=True):
            navigate_to("doctor_register")
            
    st.markdown("<br><hr style='border: 0; border-top: 1px solid #D9E5EA;'>", unsafe_allow_html=True)
    if st.button("Back to Home", key="d_land_back"):
        navigate_to("home")


# ==============================================================================
# 12. DOCTOR LOGIN
# ==============================================================================
elif st.session_state.page == "doctor_login":
    st.markdown("<div class='page-title'>Doctor Login</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Enter your Doctor ID / Email and password</div>", unsafe_allow_html=True)
    
    with st.form("d_login_form"):
        d_id = st.text_input("Doctor ID / Email", placeholder="")
        d_pass = st.text_input("Password", type="password", placeholder="")
        
        st.markdown("<br>", unsafe_allow_html=True)
        doc_login_btn = st.form_submit_button("Login", type="primary", use_container_width=True)
        
    if doc_login_btn:
        if not d_id.strip():
            st.error("Please enter your Doctor ID or Email.")
        elif not d_pass.strip():
            st.error("Please enter your password.")
        else:
            doctor_record = authenticate_doctor(d_id.strip(), d_pass.strip())
            if doctor_record:
                st.session_state.logged_doctor = doctor_record
                navigate_to("doctor_portal")
            else:
                st.error("Invalid credentials. Please verify your Doctor ID/Email and password.")
                
    st.markdown("<hr style='border: 0; border-top: 1px solid #D9E5EA; margin: 16px 0;'>", unsafe_allow_html=True)
    st.write("Don't have an account?")
    d_btn1, d_btn2 = st.columns(2)
    with d_btn1:
        if st.button("Create Account", key="d_login_to_create"):
            navigate_to("doctor_register")
    with d_btn2:
        if st.button("Back", key="d_login_back"):
            navigate_to("doctor_landing")


# ==============================================================================
# 13. DOCTOR REGISTRATION (Create Doctor Account)
# ==============================================================================
elif st.session_state.page == "doctor_register":
    st.markdown("<div class='page-title'>Create Doctor Account</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Please enter your professional details below</div>", unsafe_allow_html=True)
    
    with st.form("d_register_form"):
        dr_name = st.text_input("Full Name", placeholder="")
        dr_email = st.text_input("Email", placeholder="")
        dr_id = st.text_input("Doctor ID (Optional)", placeholder="e.g. DOC-102")
        dr_phone = st.text_input("Phone Number", placeholder="")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            dr_pass = st.text_input("Password", type="password", placeholder="")
        with col_p2:
            dr_pass_conf = st.text_input("Confirm Password", type="password", placeholder="")
            
        st.markdown("<br>", unsafe_allow_html=True)
        dr_reg_btn = st.form_submit_button("Create Doctor Account", type="primary", use_container_width=True)
        
    if dr_reg_btn:
        if not dr_name.strip():
            st.error("Please enter your full name.")
        elif not dr_email.strip() or "@" not in dr_email:
            st.error("Please enter a valid email address.")
        elif not dr_phone.strip().isdigit() or len(dr_phone.strip()) != 10:
            st.error("Please enter a valid 10-digit phone number.")
        elif not dr_pass.strip():
            st.error("Please enter a password.")
        elif dr_pass != dr_pass_conf:
            st.error("Passwords do not match.")
        else:
            doc_id_val = register_doctor_account(
                full_name=dr_name.strip(),
                email=dr_email.strip(),
                doctor_id=dr_id.strip(),
                phone_number=dr_phone.strip(),
                password=dr_pass.strip()
            )
            st.session_state.logged_doctor = {"doctor_id": doc_id_val, "full_name": dr_name.strip(), "email": dr_email.strip()}
            navigate_to("doctor_register_success")
            
    if st.button("Back", key="dr_reg_back"):
        navigate_to("doctor_landing")


# ==============================================================================
# 14. DOCTOR REGISTRATION SUCCESS
# ==============================================================================
elif st.session_state.page == "doctor_register_success":
    doctor = st.session_state.logged_doctor
    if not doctor:
        navigate_to("doctor_register")
        st.stop()
        
    st.markdown("<div class='page-title'>Doctor account created successfully.</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <p style='color: #607080; font-size: 0.95rem; margin-top: 10px;'>
        Doctor ID: <strong style='color: #1E3A5F;'>{doctor['doctor_id']}</strong> ({doctor['full_name']})
    </p>
    """, unsafe_allow_html=True)
    
    if st.button("Continue to Doctor Portal", key="d_succ_cont", type="primary", use_container_width=True):
        navigate_to("doctor_portal")


# ==============================================================================
# 15. DOCTOR PORTAL (Dedicated View After Login)
# ==============================================================================
elif st.session_state.page == "doctor_portal":
    doctor = st.session_state.logged_doctor
    if not doctor:
        st.info("Doctor authentication required.")
        col_l1, col_l2 = st.columns([1, 4])
        with col_l1:
            if st.button("Go to Doctor Login", type="primary"):
                navigate_to("doctor_login")
        st.stop()
        
    col_d_title, col_d_logout = st.columns([4, 1])
    with col_d_title:
        st.markdown(f"<div class='page-title'>Doctor Portal</div>", unsafe_allow_html=True)
        st.caption(f"Logged in as: **{doctor['full_name']}** (ID: {doctor['doctor_id']})")
    with col_d_logout:
        if st.button("Logout", key="doc_logout_btn"):
            st.session_state.logged_doctor = None
            navigate_to("home")
            
    all_cases = get_all_consultations()
    
    tab_queue, tab_case, tab_metrics = st.tabs([
        "Patient Queue",
        "Patient Case Details",
        "Model Performance"
    ])
    
    # --- TAB 1: PATIENT QUEUE ---
    with tab_queue:
        if not all_cases:
            st.info("No registered patients found in the database.")
        else:
            col_f, col_r = st.columns([3, 1])
            with col_f:
                filter_choice = st.selectbox(
                    "Filter by status:",
                    options=["All", "Waiting for doctor consultation", "Under consultation", "Completed"]
                )
            with col_r:
                st.write("")
                st.write("")
                if st.button("Refresh Queue", key="doc_portal_ref", use_container_width=True):
                    st.rerun()
                    
            filtered_cases = all_cases if filter_choice == "All" else [c for c in all_cases if c["consultation_status"] == filter_choice]
            
            queue_records = []
            for c in filtered_cases:
                queue_records.append({
                    "Patient ID": c["patient_id"],
                    "Name": c["full_name"],
                    "Age/Sex": f"{c['age']}/{c['gender']}",
                    "Language": c["preferred_language"],
                    "Priority": c["triage_priority"],
                    "Confidence": f"{c['triage_confidence']*100:.0f}%",
                    "Status": c["consultation_status"],
                    "Registered Time": c["created_at"]
                })
                
            df_table = pd.DataFrame(queue_records)
            st.dataframe(df_table, use_container_width=True, hide_index=True)
            
            st.markdown("<hr style='border: 0; border-top: 1px solid #D9E5EA; margin: 16px 0;'>", unsafe_allow_html=True)
            
            st.write("**Select a patient case to review:**")
            case_mapping = {f"{c['patient_id']} - {c['full_name']} ({c['triage_priority']}) [{c['consultation_status']}]": c["consultation_id"] for c in all_cases}
            selected_label = st.selectbox("Select patient:", options=list(case_mapping.keys()), label_visibility="collapsed")
            
            if st.button("Open Case Details", key="doc_open_case", type="primary"):
                st.session_state.selected_doctor_case = case_mapping[selected_label]
                st.rerun()

    # --- TAB 2: PATIENT CASE DETAILS ---
    with tab_case:
        selected_cid = st.session_state.selected_doctor_case
        if not selected_cid and all_cases:
            selected_cid = all_cases[0]["consultation_id"]
            
        if not selected_cid:
            st.info("Select a patient from the Queue tab to view case details.")
        else:
            case_data = get_consultation_by_id(selected_cid)
            if not case_data:
                st.error("Patient record not found.")
            else:
                st.subheader(f"Patient: {case_data['full_name']} ({case_data['patient_id']})")
                
                c_info1, c_info2 = st.columns([3, 2])
                with c_info1:
                    st.markdown(f"""
                    <div style="border: 1px solid #D9E5EA; border-radius: 4px; padding: 14px; background-color: #FFFFFF; margin-bottom: 14px;">
                        <div><strong>Age:</strong> {case_data['age']} | <strong>Gender:</strong> {case_data['gender']} | <strong>Phone:</strong> {case_data['phone_number']}</div>
                        <div><strong>Language:</strong> {case_data['preferred_language']} | <strong>Location:</strong> {case_data['location'] or 'Not specified'}</div>
                        <hr style='border: 0; border-top: 1px solid #D9E5EA; margin: 8px 0;'>
                        <div><strong>Reported Symptoms:</strong><br><span style="color: #5F6F7F;">{case_data['symptoms_text']}</span></div>
                        <div style="margin-top: 6px;"><strong>Detected Symptoms:</strong><br><code>{case_data['detected_symptoms']}</code></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with c_info2:
                    triage_tag = {
                        "Low Priority": "badge-low",
                        "Moderate Priority": "badge-moderate",
                        "High Priority": "badge-high",
                        "Urgent Attention": "badge-urgent"
                    }.get(case_data["triage_priority"], "badge-moderate")
                    
                    st.markdown(f"""
                    <div style="border: 1px solid #D9E5EA; border-radius: 4px; padding: 14px; background-color: #FFFFFF; margin-bottom: 14px;">
                        <div><strong>Triage Priority:</strong></div>
                        <div class="{triage_tag}" style="margin: 6px 0 10px 0;">{case_data['triage_priority']}</div>
                        <div><strong>Confidence:</strong> {case_data['triage_confidence']*100:.0f}%</div>
                        <div style="margin-top: 6px;"><strong>Status:</strong> <code>{case_data['consultation_status']}</code></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if case_data["consultation_status"] != "Under consultation":
                        if st.button("Mark as Under Consultation", key="btn_under_cons", type="primary", use_container_width=True):
                            update_consultation_status(case_data["consultation_id"], "Under consultation")
                            st.rerun()
                            
                    if case_data["consultation_status"] != "Completed":
                        if st.button("Mark as Completed", key="btn_mark_comp", use_container_width=True):
                            update_consultation_status(case_data["consultation_id"], "Completed")
                            st.rerun()

                st.write("**Doctor Consultation Notes:**")
                clinical_notes = st.text_area(
                    "Doctor notes:",
                    value=case_data.get("doctor_notes", ""),
                    height=90,
                    key=f"doc_notes_{case_data['consultation_id']}",
                    label_visibility="collapsed"
                )
                if st.button("Save Notes", key="save_notes_btn", type="primary"):
                    update_doctor_notes(case_data["consultation_id"], clinical_notes)
                    st.success("Doctor notes saved successfully.")

    # --- TAB 3: MODEL PERFORMANCE ---
    with tab_metrics:
        st.write("### Model Training & Evaluation Metrics")
        st.caption("Random Forest Classifier trained on symptom dataset (data/symptoms.csv)")
        
        metrics_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "model_metrics.json")
        if os.path.exists(metrics_file):
            with open(metrics_file, "r") as f:
                metrics_dict = json.load(f)
                
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Accuracy", f"{metrics_dict.get('holdout_test_accuracy', 'N/A')}%")
            with m2:
                st.metric("F1 Score", f"{metrics_dict.get('holdout_weighted_f1', 'N/A')}%")
            with m3:
                st.metric("Precision", f"{metrics_dict.get('holdout_weighted_precision', 'N/A')}%")
            with m4:
                st.metric("Recall", f"{metrics_dict.get('holdout_weighted_recall', 'N/A')}%")
                
            st.markdown(f"""
            - **Cross-Validation Accuracy**: {metrics_dict.get('cross_val_accuracy_mean', 'N/A')}% ± {metrics_dict.get('cross_val_accuracy_std', 'N/A')}%
            - **Dataset Samples**: {metrics_dict.get('dataset_samples', 'N/A')}
            - **Evaluated Symptoms**: {', '.join(metrics_dict.get('features', []))}
            - **Triage Classes**: {', '.join(metrics_dict.get('classes', []))}
            """)
        else:
            st.info("Metrics file not found. Run python ml/train_model.py to generate.")
