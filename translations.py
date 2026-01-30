#!/usr/bin/env python3
"""
Multilingual Support for MediCare Hospital System
Supports English, Hindi, and Tamil for patient-facing pages only
"""

TRANSLATIONS = {
    'en': {
        # Landing Page
        'hospital_name': 'MediCare Hospital',
        'hospital_tagline': 'Advanced Digital Healthcare Platform',
        'patient_portal': 'Patient Portal',
        'patient_portal_desc': 'Book appointments & check status',
        'admin_dashboard': 'Admin Dashboard',
        'admin_dashboard_desc': 'Hospital management system',
        
        # Patient Portal
        'patient_portal_title': 'Patient Portal',
        'patient_portal_welcome': 'Welcome to MediCare Hospital Digital Platform',
        'book_appointment': 'Book New Appointment',
        'book_appointment_desc': 'Register for a new consultation with our medical experts',
        'check_status': 'Check Appointment Status',
        'check_status_desc': 'View your appointment details and queue position',
        'back_to_home': 'Back to Home',
        
        # Patient Registration
        'book_appointment_title': 'Book New Appointment',
        'registration_subtitle': 'Please provide your details for consultation',
        'back_to_patient_portal': 'Back to Patient Portal',
        'personal_information': 'Personal Information',
        'medical_information': 'Medical Information',
        'full_name': 'Full Name',
        'age': 'Age',
        'gender': 'Gender',
        'select_gender': 'Select Gender',
        'male': 'Male',
        'female': 'Female',
        'other': 'Other',
        'phone_number': 'Phone Number',
        'email_address': 'Email Address',
        'primary_symptom': 'Primary Symptom/Concern',
        'symptom_placeholder': 'Please describe your main health concern in detail...',
        'symptom_severity': 'Symptom Severity',
        'mild': 'Mild',
        'mild_desc': 'Manageable discomfort',
        'moderate': 'Moderate',
        'moderate_desc': 'Noticeable impact',
        'severe': 'Severe',
        'severe_desc': 'Significant distress',
        'symptom_duration': 'Duration of Symptoms',
        'select_duration': 'Select duration',
        'today': 'Today (1 day)',
        '2_days': '2 days',
        '3_days': '3 days',
        'week': 'About a week',
        '2_weeks': 'About 2 weeks',
        'month': 'About a month',
        'more_month': 'More than a month',
        'emergency': 'This is an Emergency',
        'emergency_desc': 'Selecting this option will prioritize your case and attempt to schedule you for immediate consultation.',
        'book_appointment_btn': 'Book Appointment',
        
        # Success Modal
        'success_title': 'Appointment Booked Successfully!',
        'registration_id': 'Your Registration ID:',
        'recommended_dept': 'Recommended Department',
        'emergency_priority': 'Emergency Priority Activated',
        'emergency_msg': 'Your emergency request is being prioritized. You will be contacted shortly.',
        'back_to_portal': 'Back to Patient Portal',
        
        # Status Check
        'check_status_title': 'Check Appointment Status',
        'status_subtitle': 'Enter your Registration ID to view appointment details',
        'registration_id_placeholder': 'Enter Registration ID (e.g., MED123456)',
        'check_status_btn': 'Check Status',
        'appointment_pending': 'Appointment Pending Review',
        'pending_msg': 'Your appointment is being reviewed by our medical team.',
        'appointment_confirmed': 'Appointment Confirmed',
        'confirmed_msg': 'Your appointment has been scheduled.',
        'department': 'Department',
        'risk_score': 'Risk Score',
        'severity': 'Severity',
        'appointment_time': 'Appointment Time',
        'not_scheduled': 'Not Scheduled',
        
        # Common
        'required': '*',
        'close': 'Close',
        'cancel': 'Cancel',
        'confirm': 'Confirm',
        'loading': 'Loading...',
        'error': 'Error',
        'success': 'Success',
        'language': 'Language',
        'select_language': 'Select Language'
    },
    
    'hi': {
        # Landing Page
        'hospital_name': 'मेडिकेयर अस्पताल',
        'hospital_tagline': 'उन्नत डिजिटल स्वास्थ्य सेवा प्लेटफॉर्म',
        'patient_portal': 'रोगी पोर्टल',
        'patient_portal_desc': 'अपॉइंटमेंट बुक करें और स्थिति जांचें',
        'admin_dashboard': 'एडमिन डैशबोर्ड',
        'admin_dashboard_desc': 'अस्पताल प्रबंधन प्रणाली',
        
        # Patient Portal
        'patient_portal_title': 'रोगी पोर्टल',
        'patient_portal_welcome': 'मेडिकेयर अस्पताल डिजिटल प्लेटफॉर्म में आपका स्वागत है',
        'book_appointment': 'नई अपॉइंटमेंट बुक करें',
        'book_appointment_desc': 'हमारे चिकित्सा विशेषज्ञों के साथ नए परामर्श के लिए पंजीकरण करें',
        'check_status': 'अपॉइंटमेंट स्थिति जांचें',
        'check_status_desc': 'अपनी अपॉइंटमेंट का विवरण और कतार की स्थिति देखें',
        'back_to_home': 'होम पर वापस जाएं',
        
        # Patient Registration
        'book_appointment_title': 'नई अपॉइंटमेंट बुक करें',
        'registration_subtitle': 'कृपया परामर्श के लिए अपना विवरण प्रदान करें',
        'back_to_patient_portal': 'रोगी पोर्टल पर वापस जाएं',
        'personal_information': 'व्यक्तिगत जानकारी',
        'medical_information': 'चिकित्सा जानकारी',
        'full_name': 'पूरा नाम',
        'age': 'आयु',
        'gender': 'लिंग',
        'select_gender': 'लिंग चुनें',
        'male': 'पुरुष',
        'female': 'महिला',
        'other': 'अन्य',
        'phone_number': 'फोन नंबर',
        'email_address': 'ईमेल पता',
        'primary_symptom': 'मुख्य लक्षण/चिंता',
        'symptom_placeholder': 'कृपया अपनी मुख्य स्वास्थ्य चिंता का विस्तार से वर्णन करें...',
        'symptom_severity': 'लक्षण की गंभीरता',
        'mild': 'हल्का',
        'mild_desc': 'प्रबंधनीय असुविधा',
        'moderate': 'मध्यम',
        'moderate_desc': 'ध्यान देने योग्य प्रभाव',
        'severe': 'गंभीर',
        'severe_desc': 'महत्वपूर्ण परेशानी',
        'symptom_duration': 'लक्षणों की अवधि',
        'select_duration': 'अवधि चुनें',
        'today': 'आज (1 दिन)',
        '2_days': '2 दिन',
        '3_days': '3 दिन',
        'week': 'लगभग एक सप्ताह',
        '2_weeks': 'लगभग 2 सप्ताह',
        'month': 'लगभग एक महीना',
        'more_month': 'एक महीने से अधिक',
        'emergency': 'यह एक आपातकाल है',
        'emergency_desc': 'इस विकल्प का चयन करने से आपके मामले को प्राथमिकता मिलेगी और तत्काल परामर्श के लिए शेड्यूल करने का प्रयास किया जाएगा।',
        'book_appointment_btn': 'अपॉइंटमेंट बुक करें',
        
        # Success Modal
        'success_title': 'अपॉइंटमेंट सफलतापूर्वक बुक हो गई!',
        'registration_id': 'आपकी पंजीकरण आईडी:',
        'recommended_dept': 'अनुशंसित विभाग',
        'emergency_priority': 'आपातकालीन प्राथमिकता सक्रिय',
        'emergency_msg': 'आपके आपातकालीन अनुरोध को प्राथमिकता दी जा रही है। आपसे जल्द ही संपर्क किया जाएगा।',
        'back_to_portal': 'रोगी पोर्टल पर वापस जाएं',
        
        # Status Check
        'check_status_title': 'अपॉइंटमेंट स्थिति जांचें',
        'status_subtitle': 'अपॉइंटमेंट का विवरण देखने के लिए अपनी पंजीकरण आईडी दर्ज करें',
        'registration_id_placeholder': 'पंजीकरण आईडी दर्ज करें (जैसे, MED123456)',
        'check_status_btn': 'स्थिति जांचें',
        'appointment_pending': 'अपॉइंटमेंट समीक्षा में',
        'pending_msg': 'आपकी अपॉइंटमेंट हमारी चिकित्सा टीम द्वारा समीक्षा की जा रही है।',
        'appointment_confirmed': 'अपॉइंटमेंट पुष्ट',
        'confirmed_msg': 'आपकी अपॉइंटमेंट निर्धारित कर दी गई है।',
        'department': 'विभाग',
        'risk_score': 'जोखिम स्कोर',
        'severity': 'गंभीरता',
        'appointment_time': 'अपॉइंटमेंट का समय',
        'not_scheduled': 'निर्धारित नहीं',
        
        # Common
        'required': '*',
        'close': 'बंद करें',
        'cancel': 'रद्द करें',
        'confirm': 'पुष्टि करें',
        'loading': 'लोड हो रहा है...',
        'error': 'त्रुटि',
        'success': 'सफलता',
        'language': 'भाषा',
        'select_language': 'भाषा चुनें'
    },
    
    'ta': {
        # Landing Page
        'hospital_name': 'மெடிகேர் மருத்துவமனை',
        'hospital_tagline': 'மேம்பட்ட டிஜிட்டல் சுகாதார தளம்',
        'patient_portal': 'நோயாளி போர்ட்டல்',
        'patient_portal_desc': 'சந்திப்பு முன்பதிவு மற்றும் நிலை சரிபார்ப்பு',
        'admin_dashboard': 'நிர்வாக டாஷ்போர்ட்',
        'admin_dashboard_desc': 'மருத்துவமனை மேலாண்மை அமைப்பு',
        
        # Patient Portal
        'patient_portal_title': 'நோயாளி போர்ட்டல்',
        'patient_portal_welcome': 'மெடிகேர் மருத்துவமனை டிஜிட்டல் தளத்திற்கு வரவேற்கிறோம்',
        'book_appointment': 'புதிய சந்திப்பு முன்பதிவு',
        'book_appointment_desc': 'எங்கள் மருத்துவ நிபுணர்களுடன் புதிய ஆலோசனைக்கு பதிவு செய்யுங்கள்',
        'check_status': 'சந்திப்பு நிலை சரிபார்ப்பு',
        'check_status_desc': 'உங்கள் சந்திப்பு விவரங்கள் மற்றும் வரிசை நிலையைப் பார்க்கவும்',
        'back_to_home': 'முகப்புக்கு திரும்பு',
        
        # Patient Registration
        'book_appointment_title': 'புதிய சந்திப்பு முன்பதிவு',
        'registration_subtitle': 'ஆலோசனைக்கு உங்கள் விவரங்களை வழங்கவும்',
        'back_to_patient_portal': 'நோயாளி போர்ட்டலுக்கு திரும்பு',
        'personal_information': 'தனிப்பட்ட தகவல்',
        'medical_information': 'மருத்துவ தகவல்',
        'full_name': 'முழு பெயர்',
        'age': 'வயது',
        'gender': 'பாலினம்',
        'select_gender': 'பாலினம் தேர்ந்தெடுக்கவும்',
        'male': 'ஆண்',
        'female': 'பெண்',
        'other': 'மற்றவை',
        'phone_number': 'தொலைபேசி எண்',
        'email_address': 'மின்னஞ்சல் முகவரி',
        'primary_symptom': 'முதன்மை அறிகுறி/கவலை',
        'symptom_placeholder': 'உங்கள் முக்கிய சுகாதார கவலையை விரிவாக விவரிக்கவும்...',
        'symptom_severity': 'அறிகுறியின் தீவிரம்',
        'mild': 'லேசான',
        'mild_desc': 'நிர்வகிக்கக்கூடிய அசௌகரியம்',
        'moderate': 'மிதமான',
        'moderate_desc': 'கவனிக்கத்தக்க தாக்கம்',
        'severe': 'கடுமையான',
        'severe_desc': 'குறிப்பிடத்தக்க துன்பம்',
        'symptom_duration': 'அறிகுறிகளின் காலம்',
        'select_duration': 'காலம் தேர்ந்தெடுக்கவும்',
        'today': 'இன்று (1 நாள்)',
        '2_days': '2 நாட்கள்',
        '3_days': '3 நாட்கள்',
        'week': 'சுமார் ஒரு வாரம்',
        '2_weeks': 'சுமார் 2 வாரங்கள்',
        'month': 'சுமார் ஒரு மாதம்',
        'more_month': 'ஒரு மாதத்திற்கு மேல்',
        'emergency': 'இது ஒரு அவசரநிலை',
        'emergency_desc': 'இந்த விருப்பத்தைத் தேர்ந்தெடுப்பது உங்கள் வழக்கிற்கு முன்னுரிமை அளித்து உடனடி ஆலோசனைக்கு திட்டமிட முயற்சிக்கும்.',
        'book_appointment_btn': 'சந்திப்பு முன்பதிவு',
        
        # Success Modal
        'success_title': 'சந்திப்பு வெற்றிகரமாக முன்பதிவு செய்யப்பட்டது!',
        'registration_id': 'உங்கள் பதிவு ஐடி:',
        'recommended_dept': 'பரிந்துரைக்கப்பட்ட துறை',
        'emergency_priority': 'அவசர முன்னுரிமை செயல்படுத்தப்பட்டது',
        'emergency_msg': 'உங்கள் அவசர கோரிக்கைக்கு முன்னுரிமை அளிக்கப்படுகிறது. விரைவில் உங்களைத் தொடர்பு கொள்வோம்.',
        'back_to_portal': 'நோயாளி போர்ட்டலுக்கு திரும்பு',
        
        # Status Check
        'check_status_title': 'சந்திப்பு நிலை சரிபார்ப்பு',
        'status_subtitle': 'சந்திப்பு விவரங்களைப் பார்க்க உங்கள் பதிவு ஐடியை உள்ளிடவும்',
        'registration_id_placeholder': 'பதிவு ஐடியை உள்ளிடவும் (எ.கா., MED123456)',
        'check_status_btn': 'நிலை சரிபார்க்கவும்',
        'appointment_pending': 'சந்திப்பு மதிப்பாய்வில்',
        'pending_msg': 'உங்கள் சந்திப்பு எங்கள் மருத்துவ குழுவால் மதிப்பாய்வு செய்யப்படுகிறது.',
        'appointment_confirmed': 'சந்திப்பு உறுதிப்படுத்தப்பட்டது',
        'confirmed_msg': 'உங்கள் சந்திப்பு திட்டமிடப்பட்டுள்ளது.',
        'department': 'துறை',
        'risk_score': 'ஆபத்து மதிப்பெண்',
        'severity': 'தீவிரம்',
        'appointment_time': 'சந்திப்பு நேரம்',
        'not_scheduled': 'திட்டமிடப்படவில்லை',
        
        # Common
        'required': '*',
        'close': 'மூடு',
        'cancel': 'ரத்து செய்',
        'confirm': 'உறுதிப்படுத்து',
        'loading': 'ஏற்றுகிறது...',
        'error': 'பிழை',
        'success': 'வெற்றி',
        'language': 'மொழி',
        'select_language': 'மொழி தேர்ந்தெடுக்கவும்'
    }
}

def get_translation(lang_code, key, default=None):
    """Get translation for a specific key and language"""
    if lang_code not in TRANSLATIONS:
        lang_code = 'en'  # Default to English
    
    return TRANSLATIONS[lang_code].get(key, default or key)

def get_supported_languages():
    """Get list of supported languages"""
    return {
        'en': 'English',
        'hi': 'हिन्दी',
        'ta': 'தமிழ்'
    }