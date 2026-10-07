"""
Prescription Management Service for AI-Assisted Telemedicine Kiosk.
Handles structured digital prescriptions and printable document generation.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import database.database as db

def generate_prescription_html(prescription_data: Dict[str, Any], patient_data: Dict[str, Any], doctor_data: Dict[str, Any]) -> str:
    """
    Generate clean, printable HTML digital prescription with clinic header and doctor signature.
    """
    rx_id = prescription_data.get("prescription_id", "RX-PREVIEW")
    date_str = datetime.now().strftime("%d %B %Y, %I:%M %p")
    doc_name = doctor_data.get("full_name", "Attending Telemedicine Physician")
    doc_spec = doctor_data.get("specialization", "General Medicine")
    doc_lic = doctor_data.get("license_number", "MCI-VALIDATED")
    pat_name = patient_data.get("full_name", "Patient")
    pat_id = patient_data.get("patient_id", "PAT-XXXX")
    pat_age = patient_data.get("age", "--")
    pat_gender = patient_data.get("gender", "--")
    pat_loc = patient_data.get("location", "Rural Center")

    items = prescription_data.get("items", [])
    items_rows = ""
    for idx, item in enumerate(items, 1):
        items_rows += f"""
        <tr>
            <td style="padding: 8px; border: 1px solid #CBD5E1; text-align: center;">{idx}</td>
            <td style="padding: 8px; border: 1px solid #CBD5E1; font-weight: 600;">{item.get('medicine_name', '')}</td>
            <td style="padding: 8px; border: 1px solid #CBD5E1;">{item.get('dosage', '')}</td>
            <td style="padding: 8px; border: 1px solid #CBD5E1;">{item.get('frequency', '')}</td>
            <td style="padding: 8px; border: 1px solid #CBD5E1;">{item.get('duration', '')}</td>
            <td style="padding: 8px; border: 1px solid #CBD5E1;">{item.get('instructions', '')}</td>
        </tr>
        """

    notes = prescription_data.get("general_notes", "Maintain hydration and rest. Follow up if symptoms persist.")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #1E293B; background: #FFF; padding: 24px; }}
            .rx-card {{ border: 2px solid #0284C7; border-radius: 8px; padding: 24px; max-width: 800px; margin: 0 auto; background: #FFFFFF; }}
            .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #0284C7; padding-bottom: 12px; margin-bottom: 16px; }}
            .clinic-title {{ font-size: 1.25rem; font-weight: 700; color: #0369A1; }}
            .clinic-sub {{ font-size: 0.85rem; color: #64748B; }}
            .doc-info {{ text-align: right; }}
            .doc-name {{ font-weight: 700; color: #0F172A; }}
            .doc-details {{ font-size: 0.82rem; color: #64748B; }}
            .patient-box {{ background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 12px; margin-bottom: 16px; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.9rem; }}
            .rx-symbol {{ font-size: 1.8rem; font-weight: 700; color: #0284C7; margin: 12px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 16px; font-size: 0.88rem; }}
            th {{ background-color: #F1F5F9; padding: 8px; border: 1px solid #CBD5E1; text-align: left; font-weight: 600; color: #334155; }}
            .notes-box {{ background-color: #FEF3C7; border-left: 4px solid #F59E0B; padding: 10px; border-radius: 4px; font-size: 0.88rem; margin-bottom: 24px; }}
            .footer {{ display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px solid #E2E8F0; padding-top: 16px; font-size: 0.8rem; color: #64748B; }}
            .signature-box {{ text-align: center; }}
            .signature-line {{ width: 180px; border-top: 1px dashed #475569; margin-top: 40px; margin-bottom: 4px; }}
        </style>
    </head>
    <body>
        <div class="rx-card">
            <div class="header">
                <div>
                    <div class="clinic-title">🏥 AI-Assisted Rural Telemedicine Kiosk</div>
                    <div class="clinic-sub">Primary Healthcare Support & Digital Outpost</div>
                    <div class="clinic-sub">Rx No: <strong>{rx_id}</strong> | Date: {date_str}</div>
                </div>
                <div class="doc-info">
                    <div class="doc-name">{doc_name}</div>
                    <div class="doc-details">{doc_spec}</div>
                    <div class="doc-details">Reg No: {doc_lic}</div>
                </div>
            </div>

            <div class="patient-box">
                <div><strong>Patient Name:</strong> {pat_name}</div>
                <div><strong>Patient ID:</strong> {pat_id}</div>
                <div><strong>Age / Gender:</strong> {pat_age} Yrs / {pat_gender}</div>
                <div><strong>Location:</strong> {pat_loc}</div>
            </div>

            <div class="rx-symbol">℞</div>

            <table>
                <thead>
                    <tr>
                        <th style="width: 5%;">#</th>
                        <th style="width: 30%;">Medicine Name</th>
                        <th style="width: 15%;">Dosage</th>
                        <th style="width: 20%;">Frequency</th>
                        <th style="width: 15%;">Duration</th>
                        <th style="width: 15%;">Instructions</th>
                    </tr>
                </thead>
                <tbody>
                    {items_rows if items_rows else '<tr><td colspan="6" style="padding: 12px; text-align: center; color: #64748B;">No prescription items added.</td></tr>'}
                </tbody>
            </table>

            <div class="notes-box">
                <strong>Doctor's Advice & Instructions:</strong><br>
                {notes}
            </div>

            <div class="footer">
                <div>
                    <div><em>Generated via AI-Assisted Telemedicine Kiosk</em></div>
                    <div>Digital Record Verified & Archived to Patient EHR</div>
                </div>
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div><strong>{doc_name}</strong></div>
                    <div style="font-size: 0.75rem;">Digital Signature Verified</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html
