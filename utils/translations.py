"""
Translations module for AI-Assisted Telemedicine Kiosk.
Provides simple, natural UI text for English, Hindi, Kannada, and Telugu.
"""

TRANSLATIONS = {
    "English": {
        "lang_code": "en",
        "app_title": "AI-Assisted Telemedicine Kiosk",
        "app_subtitle": "Healthcare support for rural areas",
        "top_nav_home": "Home",
        "top_nav_doctor": "Doctor Portal",
        
        # Home Page
        "home_intro": "This system helps patients register their details, describe their symptoms and receive a preliminary priority assessment before consulting a doctor.",
        "btn_start_consultation": "Start Consultation",
        "how_it_works_heading": "How it works",
        "step_1": "1. Register",
        "step_2": "2. Describe symptoms",
        "step_3": "3. Get preliminary assessment",
        "step_4": "4. Consult a doctor",
        "home_disclaimer": "Note: This system provides preliminary decision support and does not replace a medical professional.",
        
        # Breadcrumb / Step Indicator
        "step_lang": "Language",
        "step_details": "Details",
        "step_symptoms": "Symptoms",
        "step_assessment": "Assessment",
        "step_consultation": "Consultation",
        
        # Language Selection Page
        "lang_heading": "Choose your language",
        "lang_subheading": "Select the language you are most comfortable using.",
        "lbl_language_select": "Preferred Language:",
        
        # Patient Details Page
        "reg_heading": "Patient Details",
        "reg_subheading": "Please enter your basic details to continue.",
        "lbl_full_name": "Full Name",
        "lbl_age": "Age",
        "lbl_gender": "Gender",
        "gender_select": "-- Select Gender --",
        "gender_male": "Male",
        "gender_female": "Female",
        "gender_other": "Other",
        "lbl_phone": "Mobile Number",
        "lbl_location": "Village / Town (Optional)",
        "lbl_pref_lang": "Selected Language",
        "val_name_empty": "Please enter the patient's full name.",
        "val_age_invalid": "Please enter a valid age between 1 and 120.",
        "val_gender_empty": "Please select a gender.",
        "val_phone_invalid": "Please enter a valid 10-digit mobile number.",
        
        # Registration Success Page
        "success_heading": "Registration completed",
        "success_patient_id_label": "Your Patient ID is:",
        "btn_continue_to_symptoms": "Continue to Symptoms",
        
        # Symptom Description Page
        "symp_heading": "Tell us about your symptoms",
        "symp_subheading": "Describe what you are currently experiencing. Please provide as much detail as possible.",
        "symp_textarea_label": "Describe your symptoms here:",
        "symp_textarea_placeholder": "Example: I have a high fever, dry cough, and headache since yesterday.",
        "symp_helper_title": "Common symptoms (optional):",
        "symp_empty_error": "Please describe at least one symptom before continuing.",
        
        # Assessment Processing
        "assessment_processing": "Assessing the information provided...",
        
        # Result Page
        "result_heading": "Preliminary Assessment",
        "lbl_patient_id": "Patient ID",
        "lbl_reported_symptoms": "Symptoms provided",
        "lbl_detected_symptoms": "Detected symptoms",
        "lbl_priority": "Priority",
        "lbl_confidence": "Confidence",
        "result_disclaimer": "This assessment is based on the symptoms provided and is intended only as preliminary decision support. It is not a medical diagnosis.",
        "btn_continue_to_doctor": "Continue to Doctor Consultation",
        
        # Doctor Waiting Page
        "waiting_heading": "Doctor Consultation",
        "waiting_subheading": "Your information has been added to the consultation queue.",
        "waiting_status": "Status: Waiting for doctor",
        "waiting_explanation": "A doctor can review the information provided before starting the consultation.",
        "btn_return_home": "Return to Home",
        
        # Doctor Portal
        "doc_heading": "Doctor Portal",
        "doc_subheading": "Registered patient queue and case review",
        "doc_queue_tab": "Patient Queue",
        "doc_case_tab": "Patient Case Details",
        "doc_metrics_tab": "Model Performance",
        "doc_filter_label": "Filter by status:",
        "doc_filter_all": "All",
        "doc_filter_waiting": "Waiting for doctor",
        "doc_filter_consultation": "Under consultation",
        "doc_filter_completed": "Completed",
        "doc_no_patients": "No registered patients found in the database.",
        "doc_select_patient": "Select a patient case to review:",
        "btn_open_case": "Open Case Details",
        "lbl_current_status": "Current Status:",
        "btn_mark_under_consultation": "Mark as Under Consultation",
        "btn_mark_completed": "Mark as Completed",
        "lbl_doctor_notes": "Doctor Consultation Notes:",
        "btn_save_notes": "Save Notes",
        "notes_saved_success": "Doctor notes saved successfully.",
        
        # Common Buttons
        "btn_continue": "Continue",
        "btn_back": "Back",
        "btn_refresh": "Refresh",
    },
    
    "Hindi": {
        "lang_code": "hi",
        "app_title": "एआई-सहायित टेलीमेडिसिन कियोस्क",
        "app_subtitle": "ग्रामीण क्षेत्रों के लिए स्वास्थ्य सहायता",
        "top_nav_home": "होम",
        "top_nav_doctor": "डॉक्टर पोर्टल",
        
        # Home Page
        "home_intro": "यह प्रणाली मरीजों को अपना विवरण दर्ज करने, अपने लक्षणों का वर्णन करने और डॉक्टर से परामर्श करने से पहले प्रारंभिक प्राथमिकता मूल्यांकन प्राप्त करने में मदद करती है।",
        "btn_start_consultation": "परामर्श शुरू करें",
        "how_it_works_heading": "यह कैसे कार्य करता है",
        "step_1": "1. पंजीकरण करें",
        "step_2": "2. लक्षण बताएं",
        "step_3": "3. प्रारंभिक मूल्यांकन प्राप्त करें",
        "step_4": "4. डॉक्टर से परामर्श करें",
        "home_disclaimer": "नोट: यह प्रणाली प्रारंभिक निर्णय सहायता प्रदान करती है और किसी चिकित्सा पेशेवर का विकल्प नहीं है।",
        
        # Breadcrumb / Step Indicator
        "step_lang": "भाषा",
        "step_details": "विवरण",
        "step_symptoms": "लक्षण",
        "step_assessment": "मूल्यांकन",
        "step_consultation": "परामर्श",
        
        # Language Selection Page
        "lang_heading": "अपनी भाषा चुनें",
        "lang_subheading": "वह भाषा चुनें जिसमें आप सबसे सहज हों।",
        "lbl_language_select": "पसंदीदा भाषा:",
        
        # Patient Details Page
        "reg_heading": "रोगी विवरण",
        "reg_subheading": "आगे बढ़ने के लिए कृपया अपना बुनियादी विवरण दर्ज करें।",
        "lbl_full_name": "पूरा नाम",
        "lbl_age": "आयु",
        "lbl_gender": "लिंग",
        "gender_select": "-- लिंग चुनें --",
        "gender_male": "पुरुष",
        "gender_female": "महिला",
        "gender_other": "अन्य",
        "lbl_phone": "मोबाइल नंबर",
        "lbl_location": "गांव / कस्बा (वैकल्पिक)",
        "lbl_pref_lang": "चुनी गई भाषा",
        "val_name_empty": "कृपया पूरा नाम दर्ज करें।",
        "val_age_invalid": "कृपया 1 से 120 के बीच मान्य आयु दर्ज करें।",
        "val_gender_empty": "कृपया लिंग चुनें।",
        "val_phone_invalid": "कृपया 10 अंकों का वैध मोबाइल नंबर दर्ज करें।",
        
        # Registration Success Page
        "success_heading": "पंजीकरण पूर्ण हुआ",
        "success_patient_id_label": "आपकी रोगी आईडी है:",
        "btn_continue_to_symptoms": "लक्षण दर्ज करने के लिए आगे बढ़ें",
        
        # Symptom Description Page
        "symp_heading": "अपने लक्षणों के बारे में बताएं",
        "symp_subheading": "आप वर्तमान में क्या अनुभव कर रहे हैं, उसका वर्णन करें। कृपया यथासंभव अधिक विवरण प्रदान करें।",
        "symp_textarea_label": "अपने लक्षणों का वर्णन यहां लिखें:",
        "symp_textarea_placeholder": "उदाहरण: मुझे कल से तेज बुखार, सूखी खांसी और सिरदर्द है।",
        "symp_helper_title": "सामान्य लक्षण (वैकल्पिक):",
        "symp_empty_error": "कृपया आगे बढ़ने से पहले कम से कम एक लक्षण का वर्णन करें।",
        
        # Assessment Processing
        "assessment_processing": "दी गई जानकारी का मूल्यांकन किया जा रहा है...",
        
        # Result Page
        "result_heading": "प्रारंभिक मूल्यांकन",
        "lbl_patient_id": "रोगी आईडी",
        "lbl_reported_symptoms": "प्रदान किए गए लक्षण",
        "lbl_detected_symptoms": "पहचाने गए लक्षण",
        "lbl_priority": "प्राथमिकता",
        "lbl_confidence": "सटीकता",
        "result_disclaimer": "यह मूल्यांकन प्रदान किए गए लक्षणों पर आधारित है और केवल प्रारंभिक निर्णय सहायता के रूप में है। यह चिकित्सीय निदान नहीं है।",
        "btn_continue_to_doctor": "डॉक्टर परामर्श के लिए आगे बढ़ें",
        
        # Doctor Waiting Page
        "waiting_heading": "डॉक्टर परामर्श",
        "waiting_subheading": "आपकी जानकारी परामर्श कतार में जोड़ दी गई है।",
        "waiting_status": "स्थिति: डॉक्टर की प्रतीक्षा में",
        "waiting_explanation": "परामर्श शुरू करने से पहले उपस्थित डॉक्टर आपकी जानकारी की समीक्षा करेंगे।",
        "btn_return_home": "मुख्य पृष्ठ पर लौटें",
        
        # Doctor Portal
        "doc_heading": "डॉक्टर पोर्टल",
        "doc_subheading": "पंजीकृत रोगी कतार और केस समीक्षा",
        "doc_queue_tab": "रोगी कतार",
        "doc_case_tab": "रोगी केस विवरण",
        "doc_metrics_tab": "मॉडल सटीकता",
        "doc_filter_label": "स्थिति अनुसार फ़िल्टर करें:",
        "doc_filter_all": "सभी",
        "doc_filter_waiting": "डॉक्टर की प्रतीक्षा में",
        "doc_filter_consultation": "परामर्श जारी",
        "doc_filter_completed": "पूर्ण",
        "doc_no_patients": "डेटाबेस में कोई पंजीकृत रोगी नहीं मिला।",
        "doc_select_patient": "समीक्षा के लिए रोगी केस चुनें:",
        "btn_open_case": "केस विवरण खोलें",
        "lbl_current_status": "वर्तमान स्थिति:",
        "btn_mark_under_consultation": "परामर्शधीन चिह्नित करें",
        "btn_mark_completed": "पूर्ण चिह्नित करें",
        "lbl_doctor_notes": "डॉक्टर परामर्श नोट्स:",
        "btn_save_notes": "नोट्स सहेजें",
        "notes_saved_success": "डॉक्टर नोट्स सफलतापूर्वक सहेजे गए।",
        
        # Common Buttons
        "btn_continue": "आगे बढ़ें",
        "btn_back": "पीछे जाएं",
        "btn_refresh": "रीफ़्रेश करें",
    },

    "Kannada": {
        "lang_code": "kn",
        "app_title": "AI-ನೆರವಿನ ಟೆಲಿಮೆಡಿಸಿನ್ ಕಿಯೋಸ್ಕ್",
        "app_subtitle": "ಗ್ರಾಮೀಣ ಪ್ರದೇಶಗಳಿಗಾಗಿ ಆರೋಗ್ಯ ಬೆಂಬಲ",
        "top_nav_home": "ಮುಖಪುಟ",
        "top_nav_doctor": "ವೈದ್ಯರ ಪೋರ್ಟಲ್",
        
        # Home Page
        "home_intro": "ಈ ವ್ಯವಸ್ಥೆಯು ರೋಗಿಗಳಿಗೆ ತಮ್ಮ ವಿವರಗಳನ್ನು ನೋಂದಾಯಿಸಲು, ಲಕ್ಷಣಗಳನ್ನು ವಿವರಿಸಲು ಮತ್ತು ವೈದ್ಯರ ಸಮಾಲೋಚನೆಗೆ ಮುನ್ನ ಪ್ರಾಥಮಿಕ ಆದ್ಯತೆಯ ಮೌಲ್ಯಮಾಪನವನ್ನು ಪಡೆಯಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ.",
        "btn_start_consultation": "ಸಮಾಲೋಚನೆ ಪ್ರಾರಂಭಿಸಿ",
        "how_it_works_heading": "ವ್ಯವಸ್ಥೆ ಹೇಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ",
        "step_1": "1. ನೋಂದಣಿ",
        "step_2": "2. ರೋಗಲಕ್ಷಣಗಳ ವಿವರಣೆ",
        "step_3": "3. ಪ್ರಾಥಮಿಕ ಮೌಲ್ಯಮಾಪನ",
        "step_4": "4. ವೈದ್ಯರ ಸಮಾಲೋಚನೆ",
        "home_disclaimer": "ಗಮನಿಸಿ: ಈ ವ್ಯವಸ್ಥೆಯು ಪ್ರಾಥಮಿಕ ನಿರ್ಧಾರ ಬೆಂಬಲವನ್ನು ನೀಡುತ್ತದೆ ಮತ್ತು ವೈದ್ಯರ ತಪಾಸಣೆಗೆ ಪರ್ಯಾಯವಲ್ಲ.",
        
        # Breadcrumb / Step Indicator
        "step_lang": "ಭಾಷೆ",
        "step_details": "ವಿವರಗಳು",
        "step_symptoms": "ಲಕ್ಷಣಗಳು",
        "step_assessment": "ಮೌಲ್ಯಮಾಪನ",
        "step_consultation": "ಸಮಾಲೋಚನೆ",
        
        # Language Selection Page
        "lang_heading": "ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "lang_subheading": "ನೀವು ಬಳಸಲು ಅನುಕೂಲಕರವಾದ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "lbl_language_select": "ಆದ್ಯತೆಯ ಭಾಷೆ:",
        
        # Patient Details Page
        "reg_heading": "ರೋಗಿಯ ವಿವರಗಳು",
        "reg_subheading": "ಮುಂದುವರಿಯಲು ದಯವಿಟ್ಟು ನಿಮ್ಮ ಮೂಲ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ.",
        "lbl_full_name": "ಪೂರ್ಣ ಹೆಸರು",
        "lbl_age": "ವಯಸ್ಸು",
        "lbl_gender": "ಲಿಂಗ",
        "gender_select": "-- ಲಿಂಗ ಆಯ್ಕೆಮಾಡಿ --",
        "gender_male": "ಪುರುಷ",
        "gender_female": "ಮಹಿಳೆ",
        "gender_other": "ಇತರ",
        "lbl_phone": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ",
        "lbl_location": "ಗ್ರಾಮ / ಪಟ್ಟಣ (ಐಚ್ಛಿಕ)",
        "lbl_pref_lang": "ಆಯ್ಕೆಮಾಡಿದ ಭಾಷೆ",
        "val_name_empty": "ದಯವಿಟ್ಟು ಪೂರ್ಣ ಹೆಸರನ್ನು ನಮೂದಿಸಿ.",
        "val_age_invalid": "ದಯವಿಟ್ಟು 1 ರಿಂದ 120 ರ ನಡುವೆ ಮಾನ್ಯವಾದ ವಯಸ್ಸನ್ನು ನಮೂದಿಸಿ.",
        "val_gender_empty": "ದಯವಿಟ್ಟು ಲಿಂಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "val_phone_invalid": "ದಯವಿಟ್ಟು 10 ಅಂಕಿಗಳ ಮಾನ್ಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.",
        
        # Registration Success Page
        "success_heading": "ನೋಂದಣಿ ಪೂರ್ಣಗೊಂಡಿದೆ",
        "success_patient_id_label": "ನಿಮ್ಮ ರೋಗಿ ಐಡಿ:",
        "btn_continue_to_symptoms": "ರೋಗಲಕ್ಷಣಗಳಿಗೆ ಮುಂದುವರಿಯಿರಿ",
        
        # Symptom Description Page
        "symp_heading": "ನಿಮ್ಮ ರೋಗಲಕ್ಷಣಗಳ ಬಗ್ಗೆ ತಿಳಿಸಿ",
        "symp_subheading": "ನೀವು ಪ್ರಸ್ತುತ ಏನನ್ನು ಅನುಭವಿಸುತ್ತಿದ್ದೀರಿ ಎಂಬುದನ್ನು ವಿವರಿಸಿ. ದಯವಿಟ್ಟು ಸಾಧ್ಯವಾದಷ್ಟು ವಿವರ ನೀಡಿ.",
        "symp_textarea_label": "ನಿಮ್ಮ ಲಕ್ಷಣಗಳನ್ನು ಇಲ್ಲಿ ವಿವರಿಸಿ:",
        "symp_textarea_placeholder": "ಉದಾಹರಣೆಗೆ: ನನಗೆ ನಿನ್ನೆಯಿಂದ ತೀವ್ರ ಜ್ವರ, ಒಣ ಕೆಮ್ಮು ಮತ್ತು ತಲೆನೋವು ಇದೆ.",
        "symp_helper_title": "ಸಾಮಾನ್ಯ ಲಕ್ಷಣಗಳು (ಐಚ್ಛಿಕ):",
        "symp_empty_error": "ಮುಂದುವರಿಯುವ ಮುನ್ನ ಕನಿಷ್ಠ ಒಂದು ಲಕ್ಷಣವನ್ನು ವಿವರಿಸಿ.",
        
        # Assessment Processing
        "assessment_processing": "ನೀಡಿದ ಮಾಹಿತಿಯನ್ನು ಮೌಲ್ಯಮಾಪನ ಮಾಡಲಾಗುತ್ತಿದೆ...",
        
        # Result Page
        "result_heading": "ಪ್ರಾಥಮಿಕ ಮೌಲ್ಯಮಾಪನ",
        "lbl_patient_id": "ರೋಗಿ ಐಡಿ",
        "lbl_reported_symptoms": "ವರದಿ ಮಾಡಿದ ಲಕ್ಷಣಗಳು",
        "lbl_detected_symptoms": "ಗುರುತಿಸಲಾದ ಲಕ್ಷಣಗಳು",
        "lbl_priority": "ಆದ್ಯತೆ",
        "lbl_confidence": "ವಿಶ್ವಾಸಾರ್ಹತೆ",
        "result_disclaimer": "ಈ ಮೌಲ್ಯಮಾಪನವು ನೀಡಿದ ರೋಗಲಕ್ಷಣಗಳನ್ನು ಆಧರಿಸಿದೆ ಮತ್ತು ಕೇವಲ ಪ್ರಾಥಮಿಕ ನಿರ್ಧಾರ ಬೆಂಬಲವಾಗಿದೆ. ಇದು ವೈದ್ಯಕೀಯ ರೋಗನಿರ್ಣಯವಲ್ಲ.",
        "btn_continue_to_doctor": "ವೈದ್ಯರ ಸಮಾಲೋಚನೆಗೆ ಮುಂದುವರಿಯಿರಿ",
        
        # Doctor Waiting Page
        "waiting_heading": "ವೈದ್ಯರ ಸಮಾಲೋಚನೆ",
        "waiting_subheading": "ನಿಮ್ಮ ಮಾಹಿತಿಯನ್ನು ಸಮಾಲೋಚನೆ ಸರದಿಗೆ ಸೇರಿಸಲಾಗಿದೆ.",
        "waiting_status": "ಸ್ಥಿತಿ: ವೈದ್ಯರಿಗಾಗಿ ಕಾಯಲಾಗುತ್ತಿದೆ",
        "waiting_explanation": "ಸಮಾಲೋಚನೆ ಪ್ರಾರಂಭಿಸುವ ಮುನ್ನ ವೈದ್ಯರು ನಿಮ್ಮ ವಿವರಗಳನ್ನು ಪರಿಶೀಲಿಸುತ್ತಾರೆ.",
        "btn_return_home": "ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ",
        
        # Doctor Portal
        "doc_heading": "ವೈದ್ಯರ ಪೋರ್ಟಲ್",
        "doc_subheading": "ರೋಗಿಗಳ ಸರದಿ ಮತ್ತು ಕೇಸ್ ಪರಿಶೀಲನೆ",
        "doc_queue_tab": "ರೋಗಿಗಳ ಸರದಿ",
        "doc_case_tab": "ಕೇಸ್ ವಿವರಗಳು",
        "doc_metrics_tab": "ಮಾದರಿ ಕಾರ್ಯಕ್ಷಮತೆ",
        "doc_filter_label": "ಸ್ಥಿತಿಯ ಪ್ರಕಾರ ಫಿಲ್ಟರ್ ಮಾಡಿ:",
        "doc_filter_all": "ಎಲ್ಲವೂ",
        "doc_filter_waiting": "ಕಾಯುತ್ತಿದ್ದಾರೆ",
        "doc_filter_consultation": "ಸಮಾಲೋಚನೆಯಲ್ಲಿದೆ",
        "doc_filter_completed": "ಪೂರ್ಣಗೊಂಡಿದೆ",
        "doc_no_patients": "ಡೇಟಾಬೇಸ್‌ನಲ್ಲಿ ಯಾವುದೇ ರೋಗಿಗಳು ಕಂಡುಬಂದಿಲ್ಲ.",
        "doc_select_patient": "ಪರಿಶೀಲಿಸಲು ರೋಗಿಯ ಕೇಸ್ ಆಯ್ಕೆಮಾಡಿ:",
        "btn_open_case": "ಕೇಸ್ ವಿವರಗಳನ್ನು ತೆರೆಯಿರಿ",
        "lbl_current_status": "ಪ್ರಸ್ತುತ ಸ್ಥಿತಿ:",
        "btn_mark_under_consultation": "ಸಮಾಲೋಚನೆಯಲ್ಲಿದೆ ಎಂದು ಗುರುತಿಸಿ",
        "btn_mark_completed": "ಪೂರ್ಣಗೊಂಡಿದೆ ಎಂದು ಗುರುತಿಸಿ",
        "lbl_doctor_notes": "ವೈದ್ಯರ ಟಿಪ್ಪಣಿಗಳು:",
        "btn_save_notes": "ಟಿಪ್ಪಣಿಗಳನ್ನು ಉಳಿಸಿ",
        "notes_saved_success": "ವೈದ್ಯರ ಟಿಪ್ಪಣಿಗಳನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ.",
        
        # Common Buttons
        "btn_continue": "ಮುಂದುವರಿಯಿರಿ",
        "btn_back": "ಹಿಂದಕ್ಕೆ",
        "btn_refresh": "ನವೀಕರಿಸಿ",
    },

    "Telugu": {
        "lang_code": "te",
        "app_title": "AI-సహాయక టెలిమెడిసిన్ కియోస్క్",
        "app_subtitle": "గ్రామీణ ప్రాంతాల కోసం ఆరోగ్య సంరక్షణ సహాయం",
        "top_nav_home": "హోమ్",
        "top_nav_doctor": "డాక్టర్ పోర్టల్",
        
        # Home Page
        "home_intro": "ఈ వ్యవస్థ రోగులకు తమ వివరాలను నమోదు చేసుకోవడానికి, లక్షణాలను వివరించడానికి మరియు డాక్టర్‌తో సంప్రదించడానికి ముందు ప్రాథమిక ప్రాధాన్యతా అంచనాను పొందడానికి సహాయపడుతుంది.",
        "btn_start_consultation": "సంప్రదింపు ప్రారంభించండి",
        "how_it_works_heading": "ఇది ఎలా పనిచేస్తుంది",
        "step_1": "1. నమోదు",
        "step_2": "2. లక్షణాల వివరణ",
        "step_3": "3. ప్రాథమిక అంచనా",
        "step_4": "4. డాక్టర్ సంప్రదింపు",
        "home_disclaimer": "గమనిక: ఈ వ్యవస్థ ప్రాథమిక నిర్ణయ మద్దతును మాత్రమే అందిస్తుంది మరియు డాక్టర్ పరీక్షకు ప్రత్యామ్నాయం కాదు.",
        
        # Breadcrumb / Step Indicator
        "step_lang": "భాష",
        "step_details": "వివరాలు",
        "step_symptoms": "లక్షణాలు",
        "step_assessment": "అంచనా",
        "step_consultation": "సంప్రదింపు",
        
        # Language Selection Page
        "lang_heading": "మీ భాషను ఎంచుకోండి",
        "lang_subheading": "మీకు సౌకర్యవంతమైన భాషను ఎంచుకోండి.",
        "lbl_language_select": "ప్రాధాన్య భాష:",
        
        # Patient Details Page
        "reg_heading": "రోగి వివరాలు",
        "reg_subheading": "కొనసాగడానికి దయచేసి ప్రాథమిక సమాచారాన్ని నమోదు చేయండి.",
        "lbl_full_name": "పూర్తి పేరు",
        "lbl_age": "వయస్సు",
        "lbl_gender": "లింగం",
        "gender_select": "-- లింగం ఎంచుకోండి --",
        "gender_male": "పురుషుడు",
        "gender_female": "మహిళ",
        "gender_other": "ఇతర",
        "lbl_phone": "మొబైల్ నంబర్",
        "lbl_location": "గ్రామం / ప్రాంతం (ఐచ్ఛికం)",
        "lbl_pref_lang": "ఎంచుకున్న భాష",
        "val_name_empty": "దయచేసి పూర్తి పేరును నమోదు చేయండి.",
        "val_age_invalid": "దయచేసి 1 నుండి 120 మధ్య చెల్లుబాటు అయ్యే వయస్సును నమోదు చేయండి.",
        "val_gender_empty": "దయచేసి లింగాన్ని ఎంచుకోండి.",
        "val_phone_invalid": "దయచేసి 10 అంకెల చెల్లుబాటు అయ్యే మొబైల్ నంబర్‌ను నమోదు చేయండి.",
        
        # Registration Success Page
        "success_heading": "నమోదు పూర్తయింది",
        "success_patient_id_label": "మీ రోగి ఐడి:",
        "btn_continue_to_symptoms": "లక్షణాల నమోదుకు కొనసాగండి",
        
        # Symptom Description Page
        "symp_heading": "మీ లక్షణాల గురించి చెప్పండి",
        "symp_subheading": "మీరు ప్రస్తుతం ఏమి ఎదుర్కొంటున్నారో వివరించండి. దయచేసి వీలైనంత ఎక్కువ సమాచారం అందించండి.",
        "symp_textarea_label": "మీ లక్షణాలను ఇక్కడ వివరించండి:",
        "symp_textarea_placeholder": "ఉదాహరణ: నాకు నిన్నటి నుండి తీవ్ర జ్వరం, పొడి దగ్గు మరియు తలనొప్పి ఉన్నాయి.",
        "symp_helper_title": "సాధారణ లక్షణాలు (ఐచ్ఛికం):",
        "symp_empty_error": "ముందుకు సాగడానికి కనీసం ఒక లక్షణాన్ని వివరించండి.",
        
        # Assessment Processing
        "assessment_processing": "అందించిన సమాచారం అంచనా వేయబడుతోంది...",
        
        # Result Page
        "result_heading": "ప్రాథమిక అంచనా",
        "lbl_patient_id": "రోగి ఐడి",
        "lbl_reported_symptoms": "అందించిన లక్షణాలు",
        "lbl_detected_symptoms": "గుర్తించిన లక్షణాలు",
        "lbl_priority": "ప్రాధాన్యత",
        "lbl_confidence": "విశ్వసనీయత",
        "result_disclaimer": "ఈ అంచనా అందించిన లక్షణాలపై ఆధారపడి ఉంటుంది మరియు ప్రాథమిక నిర్ణయ మద్దతుగా మాత్రమే ఉద్దేశించబడింది. ఇది వైద్య నిర్ధారణ కాదు.",
        "btn_continue_to_doctor": "డాక్టర్ సంప్రదింపులకు కొనసాగండి",
        
        # Doctor Waiting Page
        "waiting_heading": "డాక్టర్ సంప్రదింపు",
        "waiting_subheading": "మీ సమాచారం సంప్రదింపుల వరుసలో చేర్చబడింది.",
        "waiting_status": "స్థితి: డాక్టర్ కోసం వేచి ఉన్నారు",
        "waiting_explanation": "సంప్రదింపు ప్రారంభించడానికి ముందు డాక్టర్ మీ వివరాలను పరిశీలిస్తారు.",
        "btn_return_home": "హోమ్‌పేజీకి తిరిగి వెళ్ళండి",
        
        # Doctor Portal
        "doc_heading": "డాక్టర్ పోర్టల్",
        "doc_subheading": "నమోదైన రోగుల వరుస మరియు కేసు సమీక్ష",
        "doc_queue_tab": "రోగుల వరుస",
        "doc_case_tab": "రోగి కేసు వివరాలు",
        "doc_metrics_tab": "మోడల్ పనితీరు",
        "doc_filter_label": "స్థితి ప్రకారం ఫిల్టర్ చేయండి:",
        "doc_filter_all": "అన్నీ",
        "doc_filter_waiting": "వేచి ఉన్నవారు",
        "doc_filter_consultation": "సంప్రదింపులో ఉన్నారు",
        "doc_filter_completed": "పూర్తయినవి",
        "doc_no_patients": "డేటాబేస్‌లో నమోదైన రోగులు ఎవరూ లేరు.",
        "doc_select_patient": "సమీక్షించడానికి రోగి కేసును ఎంచుకోండి:",
        "btn_open_case": "కేసు వివరాలను తెరవండి",
        "lbl_current_status": "ప్రస్తుత స్థితి:",
        "btn_mark_under_consultation": "సంప్రదింపులో ఉన్నట్లు గుర్తించండి",
        "btn_mark_completed": "పూర్తయినట్లు గుర్తించండి",
        "lbl_doctor_notes": "డాక్టర్ సంప్రదింపు నోట్స్:",
        "btn_save_notes": "నోట్స్ సేవ్ చేయండి",
        "notes_saved_success": "డాక్టర్ నోట్స్ విజయవంతంగా సేవ్ చేయబడ్డాయి.",
        
        # Common Buttons
        "btn_continue": "కొనసాగించండి",
        "btn_back": "వెనుకకు",
        "btn_refresh": "రిఫ్రెష్ చేయండి",
    }
}

def get_text(key: str, lang: str = "English") -> str:
    """Get localized text string for a given key and language."""
    if lang not in TRANSLATIONS:
        lang = "English"
    return TRANSLATIONS[lang].get(key, TRANSLATIONS["English"].get(key, key))

def get_available_languages() -> list:
    """Return list of supported languages."""
    return list(TRANSLATIONS.keys())
