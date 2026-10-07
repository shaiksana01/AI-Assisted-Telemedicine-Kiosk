# AI-Assisted Telemedicine Kiosk: A Multilingual and Voice-Enabled Healthcare System for Rural India

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Backend](https://img.shields.io/badge/Backend-Flask%20REST%20API-000000.svg)](https://flask.palletsprojects.com/)
[![ML Model](https://img.shields.io/badge/ML-Random%20Forest%20Classifier-green.svg)](https://scikit-learn.org/)
[![WebRTC](https://img.shields.io/badge/Video-Encrypted%20WebRTC-orange.svg)](https://webrtc.org/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%2F%20MySQL%20(EHR)-blue.svg)](https://www.sqlite.org/)

---

## 1. Problem Statement
Rural healthcare in India faces systemic challenges due to severe shortages of qualified medical practitioners in primary health centers (PHCs), acute language barriers across regional populations, geographic remoteness, and lack of systematic emergency triaging. Critical emergencies (such as acute myocardial events or severe respiratory distress) are frequently delayed, while routine ailments congest tertiary centers.

---

## 2. Project Objectives
* **Accessible Outpost Kiosk**: Provide an accessible, touchscreen-friendly telemedicine entry point for rural communities.
* **Multilingual Localization**: Full user interface and voice interaction across 4 Indian languages: **English**, **Hindi (हिंदी)**, **Kannada (ಕನ್ನಡ)**, and **Telugu (తెలుగు)**.
* **Speech-Enabled Input (Whisper STT)**: Enable illiterate, elderly, and rural patients to record symptoms through natural speech.
* **Clinical Decision-Support Triage (Random Forest)**: Categorize patient urgency (*Low Priority*, *Moderate Priority*, *High Priority*, *Urgent Attention*) with rule-based safety overrides for emergency conditions.
* **Encrypted WebRTC Video Consultations**: Real-time peer-to-peer audio/video calling between rural kiosks and attending doctors.
* **Structured Digital Prescriptions & Longitudinal EHR**: Generate printable prescriptions and maintain longitudinal Electronic Health Records.
* **Voice Audio Guidance (TTS)**: Read out critical prompts, token numbers, and triage results via synthesized speech.
* **AWS / Cloud Ready**: Modular architecture prepared for cloud deployment with MySQL database backend and RESTful APIs.

---

## 3. System Architecture & End-to-End Workflow

```
[ Rural Patient @ Kiosk ]
         │
         ├── 1. Language Selection (EN / HI / KN / TE)
         ├── 2. Patient Registration / Login (Secure Password Hash)
         ├── 3. Informed Clinical & Data Privacy Consent
         ├── 4. Symptom Entry: Text or Voice (OpenAI Whisper STT)
         ├── 5. Review & Confirm Transcribed Symptoms
         │
         ▼
[ ML Decision-Support Engine ]
         │
         ├── Supervised Random Forest Classifier (16 Clinical Indicators)
         ├── Emergency Red-Flag Safety Override (Chest pain, breathing distress, etc.)
         ├── Output: Triage Urgency + Confidence + Explanations + Voice TTS Output
         │
         ▼
[ Patient Waiting Room ] <──────────────┐
         │                               │
         ▼                               │ (Real-time Token & Queue State)
[ Doctor Telemedicine Dashboard ]        │
         │                               │
         ├── Urgency-Prioritized Queue ──┘
         ├── Patient Demographics & Complete EHR Trajectory
         ├── Review AI Triage Recommendations (Decision Support Only)
         ├── Initiate Encrypted WebRTC Video Call Room
         ├── Log Clinical Observations, Advice & Chief Complaints
         ├── Build Structured Multi-Item Digital Prescription
         │
         ▼
[ Electronic Health Record (EHR) & Printable Prescription Output ]
```

---

## 4. Technology Stack

| Layer | Technology | Function |
|---|---|---|
| **Frontend / Kiosk UI** | [Streamlit](https://streamlit.io/) | Responsive, accessible, touchscreen-optimized healthcare interface |
| **Backend REST API** | [Flask](https://flask.palletsprojects.com/) + [Flask-CORS](https://flask-cors.readthedocs.io/) | Modular RESTful API handling authentication, consultations, EHR, and signaling |
| **Machine Learning** | [Scikit-learn](https://scikit-learn.org/) (`RandomForestClassifier`) | Preliminary triage care-priority decision support |
| **Speech-to-Text (STT)** | [OpenAI Whisper](https://openai.com/research/whisper) | Multilingual audio transcription with text fallback |
| **Text-to-Speech (TTS)** | [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech) | Voice guidance and audio readouts with local caching |
| **Live Video Calling** | [WebRTC](https://webrtc.org/) + STUN Signaling | Real-time, peer-to-peer audio and video consultation rooms |
| **Database & EHR** | [SQLite3](https://www.sqlite.org/) / [MySQL](https://www.mysql.com/) + [SQLAlchemy](https://www.sqlalchemy.org/) | Relational database schema for patients, doctors, triage, prescriptions, and EHR |
| **Data Processing** | [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) | Clinical feature matrix extraction and dataset processing |
| **Containerization** | [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) | Production container packaging and cloud orchestration |

---

## 5. Machine Learning Approach & Transparency

### Model Architecture
* **Algorithm**: `RandomForestClassifier` (`n_estimators=100`, `max_depth=6`, `class_weight='balanced'`).
* **Input Features (16 Clinical Indicators)**: `fever`, `high_fever`, `cough`, `cold`, `headache`, `body_pain`, `fatigue`, `sore_throat`, `vomiting`, `diarrhea`, `abdominal_pain`, `dizziness`, `chest_pain`, `breathing_difficulty`, `loss_of_consciousness`, `severe_bleeding`.
* **Output Urgency Categories**:
  1. `Low Priority`: Mild, non-acute symptoms (cold, mild cough, slight fatigue).
  2. `Moderate Priority`: Acute primary care complaints (fever with headache, gastroenteritis symptoms).
  3. `High Priority`: Complex or high-temperature clusters requiring prompt review.
  4. `Urgent Attention`: Immediate cardiopulmonary, neurological, or trauma red flags.

### Performance Transparency & Evaluation Comparison
* **Research Paper Benchmark (Prototype Target)**:
  * Accuracy: 91.4%
  * Precision: 89.8%
  * Recall: 90.6%
  * F1-Score: 90.2%
* **Current Live Model Evaluation (Computed on `data/symptoms.csv`)**:
  * Holdout Test Accuracy: **100.0%**
  * Holdout Weighted F1-Score: **100.0%**
  * 3-Fold Stratified Cross-Validation Accuracy: **96.67% ± 4.71%**

> **Mandatory Clinical Disclaimer**: *The machine learning model functions strictly as an algorithmic decision-support tool to assist healthcare professionals in prioritizing consultation queues. It does NOT make formal medical diagnoses, prescribe medications, or replace certified medical practitioners.*

---

## 6. Database Schema & EHR Design

The database schema is normalized and supports both SQLite (local development) and MySQL (production/AWS RDS):

1. **`patients`**: Stores patient ID (`PAT-YYYY-XXXX`), name, demographics, contact number, preferred language, and SHA-256 hashed credentials.
2. **`doctors`**: Stores doctor ID (`DOC-YYYY-XXX`), specialization, medical license number, official email, phone, and hashed password.
3. **`consultations`**: Tracks consultation ID (`CNS-YYYY-XXXX`), patient ID, assigned doctor ID, symptom text, triage priority, status (`Waiting for doctor consultation`, `Under consultation`, `Completed`), chief complaints, doctor clinical observations, advice, and timestamps.
4. **`symptom_records`**: Archives raw patient inputs, input modality (`text` vs. `voice`), and detected clinical markers.
5. **`triage_results`**: Persists feature vectors, probability distributions, safety override triggers, and model explanations.
6. **`prescriptions`**: Header record for digital prescriptions (`RX-YYYY-XXXX`) linked to consultations, patients, and doctors.
7. **`prescription_items`**: Structured line-item medications containing medicine name, dosage, frequency, duration, and specific instructions.

---

## 7. Project Directory Structure

```
ai_telemedicine/
├── app.py                      # Main Streamlit kiosk & doctor application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── test_system.py              # Unified master automated test runner
├── telemedicine.db             # Local relational SQLite database
├── .env.example                # Environment variables template
├── .gitignore                  # Git exclusion rules
├── Dockerfile                  # Production container definition
├── docker-compose.yml          # Container orchestration configuration
│
├── backend/                    # Flask REST API Service Layer
│   ├── app.py                  # Flask application factory
│   ├── config.py               # Environment configuration loader
│   ├── auth/                   # Authentication & authorization service
│   ├── database/               # SQLAlchemy engine, session & schema models
│   ├── services/               # Consultation, prescription & EHR services
│   ├── speech/                 # Whisper STT & OpenAI TTS service wrappers
│   ├── webrtc/                 # WebRTC signaling session manager
│   └── routes/                 # REST API blueprints (auth, triage, ehr, webrtc, etc.)
│
├── translations/               # Central JSON localization dictionaries
│   ├── en.json                 # English
│   ├── hi.json                 # Hindi (हिंदी)
│   ├── kn.json                 # Kannada (ಕನ್ನಡ)
│   └── te.json                 # Telugu (తెలుగు)
│
├── utils/                      # UI helpers & components
│   ├── translations.py         # Dynamic translation loader & fallback
│   └── webrtc_component.py     # Interactive WebRTC video room component
│
├── ml/                         # Machine Learning Pipeline
│   ├── train_model.py          # Model training & metrics computation
│   └── predict.py              # NLP feature extraction & inference engine
│
├── models/                     # Serialized Model Artifacts
│   ├── triage_model.pkl        # Trained Random Forest classifier
│   └── model_metrics.json      # Evaluation metrics report
│
├── data/                       # Datasets
│   └── symptoms.csv            # Prototype clinical symptoms dataset
│
├── assets/                     # Visual & Audio Assets
│   ├── telemedicine_hero.jpg   # Rural kiosk visual asset
│   └── audio_cache/            # Local synthesized TTS audio cache
│
└── tests/                      # Automated Verification Test Suite
    ├── test_auth.py            # Authentication & role isolation tests
    ├── test_database.py        # Database CRUD, prescription & EHR tests
    ├── test_ml.py              # ML triage & safety override tests
    ├── test_speech.py          # Whisper & TTS fallback tests
    ├── test_webrtc.py          # WebRTC signaling session tests
    ├── test_api.py             # Flask REST API integration tests
    └── test_security.py        # Patient-Doctor & cross-EHR privacy tests
```

---

## 8. Installation & Setup Instructions

### Prerequisites
* Python 3.10+ (tested on Python 3.13)
* `pip` package manager
* Virtual environment tool (`venv`)

### Step 1: Clone Repository
```bash
git clone https://github.com/shaiksana01/AI-Assisted-Telemedicine-Kiosk.git
cd AI-Assisted-Telemedicine-Kiosk
```

### Step 2: Create Virtual Environment & Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables (Optional)
```bash
cp .env.example .env
# Edit .env to add your OPENAI_API_KEY (optional for Whisper/TTS)
```
*(Note: If `OPENAI_API_KEY` is not provided, the application runs with full text fallback.)*

### Step 4: Run System Verification Tests
```bash
python test_system.py
```

### Step 5: Start the Streamlit Kiosk Application
```bash
streamlit run app.py
```
Access the application at `http://localhost:8501`.

### Step 6: Start Flask REST API Server (Optional Backend Service)
```bash
python backend/app.py
```
Access the API endpoints at `http://localhost:5000/api/health`.

---

## 9. Pre-Seeded Demonstration Accounts

For ease of academic review and testing, a verified doctor account is pre-seeded in the database:

* **Doctor Portal Credentials**:
  * **Doctor ID / Email**: `doctor@kiosk.in` *(or `DOC-101`)*
  * **Password**: `doctor123`
  * **Doctor Name**: Dr. Arvind Sharma (General Medicine & Rural Health)

* **Patient Portal**:
  * Register any new patient with a 10-digit phone number or use an existing test account.

---

## 10. Cloud & AWS Deployment Architecture

For production deployment on Amazon Web Services (AWS):

1. **Frontend / Application Host**: AWS Elastic Container Service (ECS) with Fargate or AWS EC2 running the Docker container.
2. **Database**: Amazon RDS for MySQL (Multi-AZ) with automated backups and encryption at rest (KMS).
3. **Speech & AI**: OpenAI API endpoints via secure AWS Secrets Manager / Parameter Store.
4. **Video Signaling & Media**: AWS EC2 running WebRTC signaling server with STUN/TURN relays (e.g., coturn).
5. **Static Assets & Audio**: Amazon S3 + CloudFront CDN.

```
[ User Browser / Kiosk ]
         │ (HTTPS / WSS)
         ▼
[ AWS Application Load Balancer (ALB) ]
         ├──> [ Streamlit Web UI (ECS / EC2) ]
         ├──> [ Flask REST API (ECS / EC2) ]
         │
         ├──> [ Amazon RDS (MySQL Database) ]
         └──> [ OpenAI Whisper / TTS APIs ]
```

---

## 11. Ethical, Privacy, and Safety Guidelines

1. **Decision-Support Boundary**: The AI model is designed purely for preliminary decision support. It never renders diagnoses or autonomous treatment decisions.
2. **Data Privacy**: Patient records and EHR data are segregated with role-based access control. Plaintext passwords are never stored.
3. **Emergency Override**: Cardiopulmonary and critical neurological conditions bypass model thresholds to guarantee top queue priority.
4. **Rural Accessibility**: Multilingual voice readouts ensure that patients with low digital or textual literacy can understand all instructions.

---

## 12. License
Academic Mini-Project Prototype for Educational and Research Purposes.
