# AI-Assisted Telemedicine Kiosk: A Multilingual and Voice-Enabled Healthcare System for Rural India

> **Project Status: Current 50% Working Implementation (Phase 1 Milestone)**  
> *Note: This repository contains the working Phase 1 (~50%) implementation of the college mini project. Core kiosk workflows, multilingual UI, patient/doctor authentication, triage ML pipeline, and queue management are fully implemented and functional. Advanced Phase 2 features (Voice STT, WebRTC video calling, IoT sensors, cloud sync) are planned for the subsequent development phase.*

---

## 1. Problem Statement
Rural healthcare in India faces severe challenges due to the acute shortage of qualified doctors, language barriers, remote geographic locations, and delayed emergency identification. Patients often travel long distances for primary health consultations, while critical emergency cases (e.g., cardiopulmonary events or acute respiratory distress) remain untriaged until serious complications arise.

## 2. Project Objectives
* Provide an accessible, kiosk-based telemedicine entry point for rural populations.
* Offer a multilingual interface supporting regional Indian languages (English, Hindi, Kannada, Telugu).
* Implement machine learning-based preliminary triage to categorize patient urgency (Low Priority, Moderate Priority, High Priority, Urgent Attention) for doctor decision support.
* Streamline doctor tele-consultations by organizing patient queues dynamically based on clinical priority.
* Maintain modular design to allow scalable future integrations of speech recognition, encrypted video calls, and cloud synchronization.

---

## 3. Technology Stack (Phase 1 Prototype)

| Component | Technology | Description |
|---|---|---|
| **Frontend / Web UI** | [Streamlit](https://streamlit.io/) | Interactive, accessible healthcare kiosk web application |
| **Machine Learning** | [Scikit-learn](https://scikit-learn.org/) (`RandomForestClassifier`) | Decision-support preliminary urgency classification |
| **Data Processing** | [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) | Dataset preparation, feature extraction, and matrix handling |
| **Database** | [SQLite3](https://www.sqlite.org/) | Relational database for patients, doctors, and consultations |
| **Model Serialization** | [Joblib](https://joblib.readthedocs.io/) | Model persistence and loading |
| **Multilingual Engine** | Custom Python dictionary (`utils/translations.py`) | Extensible localization engine (English, Hindi, Kannada, Telugu) |

---

## 4. Scope Breakdown: Current Phase 1 vs. Planned Phase 2

### ✅ Implemented in Current 50% Version (Phase 1)
* **Kiosk Landing Page**: Multilingual portal, academic disclaimers, language selector, and dual authentication routing for Patients and Doctors.
* **Multilingual Localization**: Complete interface localization across 4 regional languages: **English**, **Hindi (हिंदी)**, **Kannada (ಕನ್ನಡ)**, and **Telugu (తెలుగు)** with session persistence.
* **Patient Registration & Login**: Registration capturing Name, Age, Gender, Phone Number, Preferred Language, and Location, stored securely in SQLite with unique Patient IDs (`PAT-YYYY-XXXX`).
* **Symptom Input**: Free-form natural language text symptom entry with multilingual keyword feature extraction and interactive quick-symptom helper chips.
* **Machine Learning Triage Model**:
  - Supervised `RandomForestClassifier` trained on `data/symptoms.csv`.
  - Binary feature extraction across 16 clinical symptom indicators.
  - Returns classification into 4 triage levels (*Low Priority*, *Moderate Priority*, *High Priority*, *Urgent Attention*) with decision rationale.
  - Quantitative evaluation metrics recorded in `models/model_metrics.json`.
* **Clinical Safety Override Layer**: Rule-based emergency detection for critical conditions (chest pain, breathing difficulty, loss of consciousness, severe trauma) to ensure urgent cases receive top priority.
* **Triage Result & Decision-Support Page**: Color-coded urgency badges, extracted clinical markers, confidence scores, and mandatory medical disclaimers.
* **Patient Waiting Room**: Token display, live consultation status tracking, and queue guidance.
* **Doctor Telemedicine Dashboard**:
  - Live patient queue dynamically prioritized by clinical urgency (Urgent cases displayed first).
  - Status filters (*All*, *Waiting for Doctor*, *Under Consultation*, *Completed*).
  - Detailed patient case review and clinical symptom breakdown.
  - Real-time consultation status updates (`Under Consultation`, `Completed`).
  - Doctor clinical notes and prescription observation logging.
  - Transparent ML model metrics and validation report viewer.

---

### ⏳ Planned for Future Phase 2 (Remaining 50% Scope)
* **Speech-to-Text (STT) Voice Pipeline**: Multilingual voice input (Whisper / Vosk) for illiterate and elderly rural patients.
* **Real-time WebRTC Video Consultation**: Encrypted, low-bandwidth peer-to-peer audio/video calling between kiosk and attending doctor.
* **Digital Prescription & SMS Dispatch**: Automated PDF prescription generation with doctor's digital signature and SMS delivery.
* **Cloud Database Migration**: Migration from local SQLite to AWS RDS / MySQL with cloud synchronization across multiple rural kiosks.
* **IoT Health Sensor Integration**: Hardware integration for pulse oximeter (SpO2), non-contact infrared thermometer, and automated blood pressure monitor.
* **Electronic Health Records (EHR)**: Longitudinal medical history tracking with Aadhaar/ABHA health ID integration.

---

## 5. Machine Learning Approach & Transparency

* **Dataset**: `data/symptoms.csv` — An educational prototype dataset with clinical symptom vectors across common primary care and emergency scenarios.
* **Model**: `RandomForestClassifier` with balanced class weights and stratified evaluation.
* **Clinical Safety Override**: High-risk emergency red flags (e.g., severe breathing difficulty, chest pain, loss of consciousness, severe bleeding) are passed through an algorithmic safety layer ensuring emergency cases receive top priority.
* **Important Academic Disclaimer**: *The ML model provides algorithmic preliminary triage and decision-support only. It does NOT constitute a clinical diagnosis or replace a qualified medical practitioner.*

---

## 6. Project Directory Structure

```
ai_telemedicine/
├── .gitignore                  # Git ignore rules for virtualenvs, cache, etc.
├── .streamlit/
│   └── config.toml             # Streamlit theme & UI styling configuration
├── assets/
│   ├── telemedicine_hero.png   # Kiosk hero visual asset
│   └── telemedicine_hero.jpg   # Image asset fallback
├── app.py                      # Main Streamlit kiosk & doctor application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── test_system.py              # Automated test suite for database, ML & auth
├── telemedicine.db             # SQLite database
├── data/
│   └── symptoms.csv            # Symptom dataset for triage model
├── models/
│   ├── triage_model.pkl        # Trained Random Forest classifier
│   └── model_metrics.json      # Performance evaluation metrics
├── ml/
│   ├── __init__.py
│   ├── train_model.py          # ML training and evaluation script
│   └── predict.py              # Symptom NLP extraction & inference pipeline
├── database/
│   ├── __init__.py
│   └── database.py             # SQLite database schema, auth, and CRUD operations
└── utils/
    ├── __init__.py
    └── translations.py         # Multilingual UI localization dictionary
```

---

## 7. How to Run the Project

### Prerequisites
* Python 3.10+ (tested on Python 3.13)
* `pip` package manager

### Step 1: Set Up Virtual Environment & Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Run Verification Test Suite
```bash
python test_system.py
```

### Step 3: Train the ML Model (Optional - pre-trained model included)
```bash
python ml/train_model.py
```

### Step 4: Run the Streamlit Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

---

## 8. Verification & Test Plan
The system includes an automated test suite (`test_system.py`) covering:
1. Multi-language switching and string retrieval (English, Hindi, Kannada, Telugu).
2. Registration of new patient and doctor accounts with password hashing.
3. Patient and doctor credential authentication.
4. Natural text symptom input and keyword extraction.
5. Real-time ML triage prediction and safety override tests.
6. Doctor queue prioritization, consultation creation, and clinical note updates.
