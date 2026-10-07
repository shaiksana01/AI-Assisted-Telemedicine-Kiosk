#!/usr/bin/env python3
"""
AI-Assisted Telemedicine Kiosk
A Multilingual and Voice-Enabled Healthcare System for Rural India
================================================================================
Flask Web Application Entrypoint.
Serves responsive HTML/CSS/JS frontend alongside REST API endpoints.
"""

import os
import sys
import json
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
    make_response
)
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Database and ML modules
import database.database as db
from ml.predict import (
    predict_triage_priority,
    extract_symptoms_from_text,
    load_triage_model,
    SYMPTOM_DISPLAY_NAMES,
    SYMPTOM_COLUMNS
)
from utils.translations import get_text, get_available_languages, get_language_code
from backend.services.ehr_service import get_complete_patient_history
from backend.services.prescription_service import generate_prescription_html

# Flask Application Factory
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "telemedicine-kiosk-secret-key-2026")

# Enable CORS for API requests
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize Relational Database Schema
db.init_db()

# Register API Blueprints
from backend.routes.auth_routes import auth_bp
from backend.routes.patient_routes import patient_bp
from backend.routes.doctor_routes import doctor_bp
from backend.routes.triage_routes import triage_bp
from backend.routes.consultation_routes import consultation_bp
from backend.routes.prescription_routes import prescription_bp
from backend.routes.speech_routes import speech_bp
from backend.routes.webrtc_routes import webrtc_bp

app.register_blueprint(auth_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(triage_bp)
app.register_blueprint(consultation_bp)
app.register_blueprint(prescription_bp)
app.register_blueprint(speech_bp)
app.register_blueprint(webrtc_bp)

@app.route("/api/health", methods=["GET"])
def api_health():
    return jsonify({
        "status": "healthy",
        "service": "AI-Assisted Telemedicine Kiosk Flask Web Application",
        "version": "1.0.0",
        "database": "connected"
    }), 200

# Context processor for templates
@app.context_processor
def inject_global_template_vars():
    current_lang = session.get("language", "English")
    return {
        "current_lang": current_lang,
        "lang_code": get_language_code(current_lang),
        "available_languages": get_available_languages(),
        "get_text": get_text,
        "now": datetime.utcnow()
    }

# ------------------------------------------------------------------------------
# 1. CORE PUBLIC ROUTES (HOME, ABOUT, HELP, LANGUAGE)
# ------------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html", active_page="home")

@app.route("/set-language", methods=["POST"])
def set_language():
    lang = request.form.get("language", "English")
    if lang in get_available_languages():
        session["language"] = lang
    return redirect(request.referrer or url_for("index"))

@app.route("/about")
def about():
    return render_template("about.html", active_page="about")

@app.route("/help")
def help_page():
    return render_template("help.html", active_page="help")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("index"))

# ------------------------------------------------------------------------------
# 2. PATIENT FLOW (LOGIN, REGISTER, DASHBOARD, SYMPTOMS, TRIAGE, WAITING ROOM)
# ------------------------------------------------------------------------------

@app.route("/patient/login", methods=["GET", "POST"])
def patient_login():
    if request.method == "POST":
        phone = request.form.get("phone_number", "").strip()
        pwd = request.form.get("password", "")
        patient = db.authenticate_patient(phone, pwd)
        if patient:
            session["patient_id"] = patient["patient_id"]
            session["patient_name"] = patient["full_name"]
            session["language"] = patient.get("preferred_language", session.get("language", "English"))
            flash(f"Welcome back, {patient['full_name']}!", "success")
            return redirect(url_for("patient_dashboard"))
        else:
            flash("Invalid phone number or password. Please try again.", "error")
    return render_template("patient_login.html", active_page="patient_login")

@app.route("/patient/register", methods=["GET", "POST"])
def patient_register():
    if request.method == "POST":
        name = request.form.get("full_name", "").strip()
        age = request.form.get("age", 30)
        gender = request.form.get("gender", "Male")
        phone = request.form.get("phone_number", "").strip()
        location = request.form.get("location", "").strip()
        lang = request.form.get("preferred_language", "English")
        pwd = request.form.get("password", "")

        if not name or not phone:
            flash("Please enter full name and a valid phone number.", "error")
        else:
            pid = db.register_patient_account(
                full_name=name,
                age=int(age),
                gender=gender,
                phone_number=phone,
                preferred_language=lang,
                location=location,
                password=pwd
            )
            patient = db.get_patient_by_id(pid)
            session["patient_id"] = pid
            session["patient_name"] = name
            session["language"] = lang
            flash(f"Registration successful! Your Patient ID is {pid}.", "success")
            return redirect(url_for("patient_dashboard"))
            
    return render_template("patient_register.html", active_page="patient_register")

@app.route("/patient/dashboard")
def patient_dashboard():
    pid = session.get("patient_id")
    if not pid:
        flash("Please log in to access your patient dashboard.", "error")
        return redirect(url_for("patient_login"))
    patient = db.get_patient_by_id(pid)
    return render_template("patient_dashboard.html", patient=patient, active_page="patient_dashboard")

@app.route("/symptoms", methods=["GET", "POST"])
def symptoms():
    pid = session.get("patient_id")
    if not pid:
        flash("Please log in or register before entering symptoms.", "error")
        return redirect(url_for("patient_login"))

    patient = db.get_patient_by_id(pid)

    if request.method == "POST":
        symptom_text = request.form.get("symptom_text", "").strip()
        if not symptom_text:
            flash("Please enter or record your symptoms to continue.", "error")
            return render_template("symptoms.html", patient=patient)

        # Run Random Forest preliminary triage prediction
        prediction = predict_triage_priority(symptom_text)
        detected_str = ", ".join(prediction.get("detected_symptoms", []))
        
        # Save consultation in relational database
        cid = db.create_consultation(
            patient_id=pid,
            symptoms_text=symptom_text,
            detected_symptoms=detected_str,
            triage_priority=prediction["predicted_priority"],
            triage_confidence=prediction["confidence_score"],
            input_method="text",
            triage_metadata=prediction
        )
        return redirect(url_for("triage_result", consultation_id=cid))

    return render_template("symptoms.html", patient=patient)

@app.route("/triage/<consultation_id>")
def triage_result(consultation_id):
    pid = session.get("patient_id")
    cns = db.get_consultation_by_id(consultation_id)
    if not cns:
        flash("Consultation record not found.", "error")
        return redirect(url_for("patient_dashboard"))

    # Re-evaluate structured triage metadata for display
    prediction = predict_triage_priority(cns["symptoms_text"])
    return render_template("triage_result.html", consultation_id=consultation_id, consultation=cns, triage=prediction)

@app.route("/waiting-room/<consultation_id>")
def waiting_room(consultation_id):
    cns = db.get_consultation_by_id(consultation_id)
    if not cns:
        flash("Consultation not found.", "error")
        return redirect(url_for("patient_dashboard"))
    
    rx = db.get_prescription_by_consultation_id(consultation_id)
    return render_template("waiting_room.html", consultation=cns, prescription=rx)

@app.route("/patient/<patient_id>/ehr")
def health_record(patient_id):
    ehr_data = get_complete_patient_history(patient_id)
    if not ehr_data or not ehr_data.get("patient"):
        flash("No health records found for this patient.", "error")
        return redirect(url_for("index"))
    return render_template("health_record.html", patient=ehr_data["patient"], consultations=ehr_data.get("consultations", []))

# ------------------------------------------------------------------------------
# 3. DOCTOR FLOW (LOGIN, REGISTER, DASHBOARD, CONSULTATION, PRESCRIPTION)
# ------------------------------------------------------------------------------

@app.route("/doctor/login", methods=["GET", "POST"])
def doctor_login():
    if request.method == "POST":
        d_id = request.form.get("id_or_email", "").strip()
        pwd = request.form.get("password", "")
        doctor = db.authenticate_doctor(d_id, pwd)
        if doctor:
            session["doctor_id"] = doctor["doctor_id"]
            session["doctor_name"] = doctor["full_name"]
            flash(f"Welcome back, Dr. {doctor['full_name']}!", "success")
            return redirect(url_for("doctor_dashboard"))
        else:
            flash("Invalid doctor credentials. Please check Doctor ID / Email and password.", "error")
    return render_template("doctor_login.html", active_page="doctor_login")

@app.route("/doctor/register", methods=["GET", "POST"])
def doctor_register():
    if request.method == "POST":
        name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        spec = request.form.get("specialization", "General Medicine").strip()
        lic = request.form.get("license_number", "").strip()
        phone = request.form.get("phone_number", "").strip()
        pwd = request.form.get("password", "")

        if not name or not email or not pwd:
            flash("Please fill all required registration fields.", "error")
        else:
            doc_id = db.register_doctor_account(
                full_name=name,
                email=email,
                doctor_id="",
                phone_number=phone,
                password=pwd,
                specialization=spec,
                license_number=lic
            )
            session["doctor_id"] = doc_id
            session["doctor_name"] = name
            flash(f"Doctor account created successfully! Doctor ID: {doc_id}", "success")
            return redirect(url_for("doctor_dashboard"))

    return render_template("doctor_register.html", active_page="doctor_register")

@app.route("/doctor/dashboard")
def doctor_dashboard():
    doc_id = session.get("doctor_id")
    if not doc_id:
        flash("Please log in to access the doctor dashboard.", "error")
        return redirect(url_for("doctor_login"))

    doctor = db.get_doctor_by_id(doc_id)
    stats = db.get_queue_summary_stats()
    all_consultations = db.get_all_consultations()
    waiting_cns = [c for c in all_consultations if c.get("consultation_status") != "Completed"]
    completed_cns = [c for c in all_consultations if c.get("consultation_status") == "Completed"]

    return render_template(
        "doctor_dashboard.html",
        doctor=doctor,
        stats=stats,
        waiting_consultations=waiting_cns,
        completed_consultations=completed_cns,
        active_page="doctor_dashboard"
    )

@app.route("/consultation/<consultation_id>")
def consultation_room(consultation_id):
    doc_id = session.get("doctor_id")
    if not doc_id:
        flash("Please log in as a doctor to open patient consultations.", "error")
        return redirect(url_for("doctor_login"))

    cns = db.get_consultation_by_id(consultation_id)
    if not cns:
        flash("Consultation case not found.", "error")
        return redirect(url_for("doctor_dashboard"))

    # Update status to Under consultation
    db.update_consultation_status(consultation_id, "Under consultation", doctor_id=doc_id)
    patient = db.get_patient_by_id(cns["patient_id"])
    doctor = db.get_doctor_by_id(doc_id)

    return render_template(
        "consultation.html",
        consultation=cns,
        patient=patient,
        doctor=doctor
    )

@app.route("/consultation/<consultation_id>/notes", methods=["POST"])
def save_consultation_notes(consultation_id):
    doc_id = session.get("doctor_id")
    if not doc_id:
        return redirect(url_for("doctor_login"))

    chief_complaint = request.form.get("chief_complaint", "")
    obs = request.form.get("doctor_observations", "")
    advice = request.form.get("doctor_advice", "")
    followup = request.form.get("followup", "")

    db.update_doctor_notes(
        consultation_id=consultation_id,
        notes=obs,
        chief_complaint=chief_complaint,
        observations=obs,
        advice=advice,
        followup=followup
    )
    flash("Clinical notes saved successfully.", "success")
    return redirect(url_for("consultation_room", consultation_id=consultation_id))

@app.route("/consultation/<consultation_id>/prescription", methods=["POST"])
def save_prescription(consultation_id):
    doc_id = session.get("doctor_id")
    if not doc_id:
        return redirect(url_for("doctor_login"))

    cns = db.get_consultation_by_id(consultation_id)
    med_names = request.form.getlist("medicine_name[]")
    dosages = request.form.getlist("dosage[]")
    frequencies = request.form.getlist("frequency[]")
    durations = request.form.getlist("duration[]")
    notes = request.form.get("general_notes", "")

    medicines = []
    for i in range(len(med_names)):
        if med_names[i].strip():
            medicines.append({
                "medicine_name": med_names[i].strip(),
                "dosage": dosages[i].strip() if i < len(dosages) else "1 tab",
                "frequency": frequencies[i].strip() if i < len(frequencies) else "Twice daily",
                "duration": durations[i].strip() if i < len(durations) else "3 days",
                "instructions": "As advised"
            })

    rx_id = db.create_prescription(
        consultation_id=consultation_id,
        patient_id=cns["patient_id"],
        doctor_id=doc_id,
        medicines=medicines,
        general_notes=notes
    )

    flash(f"Prescription {rx_id} issued successfully and archived to patient EHR!", "success")
    return redirect(url_for("view_prescription", consultation_id=consultation_id))

@app.route("/prescription/<consultation_id>")
def view_prescription(consultation_id):
    rx = db.get_prescription_by_consultation_id(consultation_id)
    if not rx:
        flash("No prescription found for this consultation.", "error")
        return redirect(url_for("index"))

    cns = db.get_consultation_by_id(consultation_id)
    patient = db.get_patient_by_id(rx["patient_id"])
    return render_template("prescription.html", prescription=rx, consultation=cns, patient=patient)

# ------------------------------------------------------------------------------
# APPLICATION RUNNER
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    target_port = int(os.getenv("PORT", 5000))
    print(f"\n==================================================")
    print(f"🏥 AI-Assisted Telemedicine Kiosk Web Application")
    print(f"==================================================")
    print(f"Starting server on http://127.0.0.1:{target_port}")
    print(f"==================================================\n")
    
    try:
        app.run(host="0.0.0.0", port=target_port, debug=False)
    except OSError as e:
        if "Address already in use" in str(e):
            fallback_port = 5001 if target_port == 5000 else target_port + 1
            print(f"Port {target_port} is in use, falling back to http://127.0.0.1:{fallback_port}")
            app.run(host="0.0.0.0", port=fallback_port, debug=False)
        else:
            raise e
