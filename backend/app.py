"""
Flask REST API Application Factory for AI-Assisted Telemedicine Kiosk.
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from backend.config import Config
import database.database as db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for frontend requests
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize SQLite/MySQL database
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
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "AI-Assisted Telemedicine Kiosk REST API",
            "version": "1.0.0",
            "database": "connected"
        }), 200

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
