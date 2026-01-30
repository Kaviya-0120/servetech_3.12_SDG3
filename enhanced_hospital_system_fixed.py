#!/usr/bin/env python3
"""
Enhanced Multilingual Telemedicine Queue Optimizer - Complete Implementation
Features: Background UI, Multilingual Support, Voice Assistant, Notifications, Responsive Design
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import sqlite3
import random
import string
from datetime import datetime, timedelta
import json
import hashlib

app = Flask(__name__)
app.secret_key = 'enhanced_hospital_secure_key_2024'

# Import enhanced templates
try:
    from enhanced_templates import (
        ENHANCED_PATIENT_REGISTER_TEMPLATE,
        ENHANCED_PATIENT_STATUS_TEMPLATE,
        ADMIN_LOGIN_TEMPLATE,
        ENHANCED_ADMIN_DASHBOARD_TEMPLATE
    )
    print("✅ Enhanced templates imported successfully")
except ImportError as e:
    print(f"⚠️ Template import warning: {e}")
    # Define minimal templates as fallback
    ENHANCED_PATIENT_REGISTER_TEMPLATE = "<!-- Template loading... -->"
    ENHANCED_PATIENT_STATUS_TEMPLATE = "<!-- Template loading... -->"
    ADMIN_LOGIN_TEMPLATE = "<!-- Template loading... -->"
    ENHANCED_ADMIN_DASHBOARD_TEMPLATE = "<!-- Template loading... -->"
# Multilingual translations
TRANSLATIONS = {
    'en': {
        'welcome': 'Welcome to MediCare Hospital',
        'select_language': 'Select Language',
        'patient_portal': 'Patient Portal',
        'book_appointment': 'Book New Appointment',
        'check_status': 'Check Appointment Status',
        'full_name': 'Full Name',
        'age': 'Age',
        'gender': 'Gender',
        'phone': 'Phone Number',
        'email': 'Email Address',
        'primary_symptom': 'Primary Symptom/Concern',
        'symptom_severity': 'Symptom Severity',
        'mild': 'Mild',
        'moderate': 'Moderate',
        'severe': 'Severe',
        'symptom_duration': 'Duration of Symptoms',
        'emergency': 'This is an Emergency',
        'submit': 'Book Appointment',
        'success': 'Appointment Booked Successfully!',
        'registration_id': 'Your Registration ID',
        'department': 'Recommended Department',
        'back': 'Back',
        'male': 'Male',
        'female': 'Female',
        'other': 'Other',
        'voice_help': 'Voice Assistant',
        'listening': 'Listening...',
        'speak_now': 'Speak now',
        'voice_not_supported': 'Voice recognition not supported in this browser',
        'patient_confirmed': 'Your appointment has been confirmed and you will be contacted shortly.',
        'status_waiting': 'Appointment Pending Review',
        'status_confirmed': 'Appointment Confirmed',
        'appointment_pending': 'Your appointment is being reviewed by our medical team.',
        'appointment_confirmed': 'Your appointment has been scheduled.',
        'enter_registration_id': 'Enter Registration ID (e.g., MED123456)',
        'check_status_btn': 'Check Status',
        'registration_not_found': 'Registration ID not found',
        'network_error': 'Network error occurred',
        'describe_symptoms': 'Please describe your symptoms in detail',
        'select_gender': 'Select Gender',
        'select_duration': 'Select Duration',
        'today': 'Today',
        'days_2': '2-3 days',
        'days_3': '3-7 days',
        'week': '1 week',
        'weeks_2': '2 weeks',
        'month': '1 month',
        'month_plus': 'More than 1 month',
        'manageable_discomfort': 'Manageable discomfort',
        'noticeable_impact': 'Noticeable impact on daily activities',
        'significant_distress': 'Significant distress or pain',
        'emergency_priority': 'Check this if you need immediate medical attention',
        'check_status': 'Check Appointment Status'
    },
    'hi': {
        'welcome': 'मेडिकेयर अस्पताल में आपका स्वागत है',
        'select_language': 'भाषा चुनें',
        'patient_portal': 'रोगी पोर्टल',
        'book_appointment': 'नई अपॉइंटमेंट बुक करें',
        'check_status': 'अपॉइंटमेंट स्थिति जांचें',
        'voice_help': 'आवाज सहायक',
        'success': 'अपॉइंटमेंट सफलतापूर्वक बुक हो गई!',
        'registration_id': 'आपकी पंजीकरण आईडी',
        'department': 'सुझाया गया विभाग',
        'back': 'वापस',
        'patient_confirmed': 'आपकी अपॉइंटमेंट की पुष्टि हो गई है और आपसे जल्द ही संपर्क किया जाएगा।',
        'enter_registration_id': 'पंजीकरण आईडी दर्ज करें (जैसे, MED123456)',
        'check_status_btn': 'स्थिति जांचें',
        'registration_not_found': 'पंजीकरण आईडी नहीं मिली',
        'network_error': 'नेटवर्क त्रुटि हुई',
        'full_name': 'पूरा नाम',
        'age': 'उम्र',
        'gender': 'लिंग',
        'phone': 'फोन नंबर',
        'email': 'ईमेल पता',
        'primary_symptom': 'मुख्य लक्षण/चिंता',
        'symptom_severity': 'लक्षण की गंभीरता',
        'mild': 'हल्का',
        'moderate': 'मध्यम',
        'severe': 'गंभीर',
        'emergency': 'यह एक आपातकाल है',
        'submit': 'अपॉइंटमेंट बुक करें',
        'describe_symptoms': 'कृपया अपने लक्षणों का विस्तार से वर्णन करें',
        'select_gender': 'लिंग चुनें',
        'male': 'पुरुष',
        'female': 'महिला',
        'other': 'अन्य',
        'listening': 'सुन रहा है...',
        'speak_now': 'अब बोलें'
    }
}

def get_translation(key, language='en'):
    """Get translation for given key and language"""
    return TRANSLATIONS.get(language, TRANSLATIONS['en']).get(key, key)

def init_hospital_db():
    """Initialize enhanced hospital database"""
    conn = sqlite3.connect('enhanced_hospital_system.db')
    cursor = conn.cursor()
    
    # Enhanced patients table with language preference and notification settings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            main_symptom TEXT NOT NULL,
            severity TEXT NOT NULL,
            symptom_days INTEGER NOT NULL,
            is_emergency BOOLEAN DEFAULT 0,
            department TEXT NOT NULL,
            risk_score INTEGER DEFAULT 0,
            status TEXT DEFAULT 'waiting',
            appointment_time TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            admin_notes TEXT,
            doctor_assigned TEXT,
            language_preference TEXT DEFAULT 'en',
            notification_frequency TEXT DEFAULT 'daily',
            last_notification_sent TIMESTAMP
        )
    ''')
    
    # Admin users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Emergency alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emergency_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            alert_type TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    # System settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key TEXT UNIQUE NOT NULL,
            setting_value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default admin
    admin_password = hashlib.sha256('hospital2024'.encode()).hexdigest()
    cursor.execute('''INSERT OR IGNORE INTO admin_users 
                     (username, email, password, full_name) 
                     VALUES (?, ?, ?, ?)''', 
                  ('admin', 'admin@hospital.com', admin_password, 'System Administrator'))
    
    conn.commit()
    conn.close()

def generate_registration_id():
    """Generate unique registration ID"""
    return 'MED' + ''.join(random.choices(string.digits, k=6))

def calculate_risk_score(patient_data):
    """Calculate patient risk score"""
    score = 0
    
    # Base severity score
    severity_scores = {'Mild': 20, 'Moderate': 50, 'Severe': 80}
    score += severity_scores.get(patient_data['severity'], 20)
    
    # Age factor
    age = patient_data['age']
    if age < 2 or age > 70:
        score += 30
    elif age < 12 or age > 60:
        score += 20
    
    # Symptom duration
    if patient_data['symptom_days'] > 7:
        score += 15
    elif patient_data['symptom_days'] > 3:
        score += 10
    
    # Emergency flag
    if patient_data.get('is_emergency'):
        score += 40
    
    return min(100, score)

def determine_department(symptom_text):
    """Advanced symptom-to-department mapping"""
    symptom_lower = symptom_text.lower()
    
    # Emergency keywords (highest priority)
    emergency_keywords = ['chest pain', 'heart attack', 'stroke', 'severe bleeding', 
                         'unconscious', 'difficulty breathing', 'severe pain']
    for keyword in emergency_keywords:
        if keyword in symptom_lower:
            return 'Emergency'
    
    # Cardiology
    cardio_keywords = ['chest', 'heart', 'palpitation', 'cardiac', 'blood pressure']
    if any(keyword in symptom_lower for keyword in cardio_keywords):
        return 'Cardiology'
    
    # Pulmonology
    pulmo_keywords = ['breathing', 'cough', 'lung', 'asthma', 'shortness of breath']
    if any(keyword in symptom_lower for keyword in pulmo_keywords):
        return 'Pulmonology'
    
    # Dermatology
    derma_keywords = ['skin', 'rash', 'acne', 'eczema', 'itching', 'allergy']
    if any(keyword in symptom_lower for keyword in derma_keywords):
        return 'Dermatology'
    
    return 'General Medicine'  # Default

def send_notification_email(patient_email, patient_name, message, language='en'):
    """Send notification email to patient"""
    try:
        # Mock implementation - in production, configure SMTP settings
        print(f"📧 Email Notification Sent:")
        print(f"   To: {patient_email}")
        print(f"   Patient: {patient_name}")
        print(f"   Language: {language}")
        print(f"   Message: {message}")
        return True
    except Exception as e:
        print(f"Email notification failed: {e}")
        return False
# ===== ROUTES =====

@app.route('/')
def home():
    """Enhanced hospital landing page with language selection"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MediCare Hospital - Enhanced Digital Healthcare Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: gradientShift 20s ease infinite;
        }
        
        @keyframes gradientShift {
            0%, 100% { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            25% { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
            50% { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
            75% { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
        }
        
        .hospital-container {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 60px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.15);
            text-align: center;
            max-width: 700px;
            width: 90%;
            position: relative;
            overflow: hidden;
        }
        
        .hospital-logo {
            font-size: 5rem;
            margin-bottom: 25px;
            background: linear-gradient(135deg, #1976d2, #42a5f5, #64b5f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .hospital-name {
            font-size: 3.2rem;
            color: #1565c0;
            margin-bottom: 20px;
            font-weight: 700;
            letter-spacing: -1px;
        }
        
        .hospital-tagline {
            color: #546e7a;
            margin-bottom: 50px;
            font-size: 1.3rem;
            font-weight: 300;
        }
        
        .language-selector {
            margin-bottom: 40px;
        }
        
        .language-selector h3 {
            color: #1565c0;
            margin-bottom: 20px;
            font-size: 1.2rem;
        }
        
        .language-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .lang-btn {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            color: #1565c0;
            border: 2px solid #e3f2fd;
            padding: 15px 30px;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .lang-btn:hover, .lang-btn.active {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(25, 118, 210, 0.3);
        }
        
        .access-buttons {
            display: flex;
            flex-direction: column;
            gap: 25px;
        }
        
        .access-btn {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
            border: none;
            padding: 25px 40px;
            border-radius: 15px;
            font-size: 1.4rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.4s ease;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            box-shadow: 0 8px 25px rgba(25, 118, 210, 0.3);
        }
        
        .access-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(25, 118, 210, 0.4);
        }
        
        .access-btn.admin {
            background: linear-gradient(135deg, #d32f2f, #c62828);
            box-shadow: 0 8px 25px rgba(211, 47, 47, 0.3);
        }
        
        .access-btn.admin:hover {
            box-shadow: 0 15px 35px rgba(211, 47, 47, 0.4);
        }
        
        .hospital-features {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid rgba(224, 224, 224, 0.5);
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .feature-item {
            color: #546e7a;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px;
            border-radius: 10px;
            background: rgba(25, 118, 210, 0.05);
            transition: all 0.3s ease;
        }
        
        .feature-item:hover {
            background: rgba(25, 118, 210, 0.1);
            transform: translateY(-2px);
        }
        
        @media (max-width: 768px) {
            .hospital-container { padding: 40px 30px; }
            .hospital-name { font-size: 2.5rem; }
            .language-buttons { flex-direction: column; align-items: center; }
        }
    </style>
</head>
<body>
    <div class="hospital-container">
        <div class="hospital-logo">🏥</div>
        <h1 class="hospital-name">MediCare Hospital</h1>
        <p class="hospital-tagline">Enhanced Digital Healthcare Platform</p>
        
        <div class="language-selector">
            <h3>🌐 Select Language / भाषा चुनें</h3>
            <div class="language-buttons">
                <a href="javascript:void(0)" class="lang-btn active" onclick="setLanguage('en')">
                    <span>🇺🇸</span>
                    <span>English</span>
                </a>
                <a href="javascript:void(0)" class="lang-btn" onclick="setLanguage('hi')">
                    <span>🇮🇳</span>
                    <span>हिंदी (Hindi)</span>
                </a>
            </div>
        </div>
        
        <div class="access-buttons">
            <a href="/patient" class="access-btn" id="patientBtn">
                <span>👤</span>
                <div>
                    <div id="patientPortalText">Patient Portal</div>
                    <div style="font-size: 0.9rem; font-weight: normal; margin-top: 5px;" id="patientSubtitleText">Book appointments & check status</div>
                </div>
            </a>
            
            <a href="/admin" class="access-btn admin">
                <span>🛡️</span>
                <div>
                    <div>Admin Dashboard</div>
                    <div style="font-size: 0.9rem; font-weight: normal; margin-top: 5px;">Hospital management system</div>
                </div>
            </a>
        </div>
        
        <div class="hospital-features">
            <div class="features-grid">
                <div class="feature-item">
                    <span style="color: #1976d2; font-size: 1.2rem;">🎤</span>
                    <span>Voice Assistant</span>
                </div>
                <div class="feature-item">
                    <span style="color: #1976d2; font-size: 1.2rem;">🌐</span>
                    <span>Multilingual Support</span>
                </div>
                <div class="feature-item">
                    <span style="color: #1976d2; font-size: 1.2rem;">⚡</span>
                    <span>Real-time Queue</span>
                </div>
                <div class="feature-item">
                    <span style="color: #1976d2; font-size: 1.2rem;">🚨</span>
                    <span>Emergency Priority</span>
                </div>
                <div class="feature-item">
                    <span style="color: #1976d2; font-size: 1.2rem;">📱</span>
                    <span>Mobile Responsive</span>
                </div>
                <div class="feature-item">
                    <span style="color: #1976d2; font-size: 1.2rem;">🔔</span>
                    <span>Smart Notifications</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        let selectedLanguage = 'en';
        
        const translations = {
            'en': {
                'patientPortal': 'Patient Portal',
                'patientSubtitle': 'Book appointments & check status'
            },
            'hi': {
                'patientPortal': 'रोगी पोर्टल',
                'patientSubtitle': 'अपॉइंटमेंट बुक करें और स्थिति जांचें'
            }
        };
        
        function setLanguage(lang) {
            selectedLanguage = lang;
            
            // Update language button states
            document.querySelectorAll('.lang-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.closest('.lang-btn').classList.add('active');
            
            // Update text content
            document.getElementById('patientPortalText').textContent = translations[lang]['patientPortal'];
            document.getElementById('patientSubtitleText').textContent = translations[lang]['patientSubtitle'];
            
            // Update patient portal link with language parameter
            document.getElementById('patientBtn').href = `/patient?lang=${lang}`;
        }
    </script>
</body>
</html>
    ''')

@app.route('/patient')
def patient_portal():
    """Enhanced patient portal with language support"""
    language = request.args.get('lang', 'en')
    session['language'] = language
    return render_template_string('''
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Patient Portal - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            animation: gradientShift 15s ease infinite;
        }
        
        @keyframes gradientShift {
            0%, 100% { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            50% { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
            animation: slideDown 1s ease-out;
        }
        
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .header h1 {
            font-size: 2.8rem;
            margin-bottom: 10px;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 50px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.15);
            animation: slideUp 1s ease-out;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .options-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .option-card {
            background: linear-gradient(135deg, #ffffff, #f8f9fa);
            border: 2px solid #e3f2fd;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.4s ease;
            text-decoration: none;
            color: inherit;
        }
        
        .option-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 25px 60px rgba(25, 118, 210, 0.25);
            border-color: #1976d2;
        }
        
        .option-icon {
            font-size: 4.5rem;
            margin-bottom: 25px;
            color: #1976d2;
        }
        
        .option-title {
            font-size: 1.8rem;
            font-weight: 600;
            color: #1565c0;
            margin-bottom: 15px;
        }
        
        .option-description {
            color: #546e7a;
            font-size: 1rem;
            line-height: 1.6;
        }
        
        .back-btn {
            background: linear-gradient(135deg, #90a4ae, #78909c);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 12px;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s ease;
        }
        
        .back-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(144, 164, 174, 0.3);
        }
        
        .voice-assistant-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 70px;
            height: 70px;
            background: linear-gradient(135deg, #4caf50, #45a049);
            border: none;
            border-radius: 50%;
            color: white;
            font-size: 1.8rem;
            cursor: pointer;
            box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
            transition: all 0.3s ease;
            z-index: 1000;
        }
        
        .voice-assistant-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 12px 35px rgba(76, 175, 80, 0.5);
        }
        
        @media (max-width: 768px) {
            .container { padding: 30px 20px; }
            .options-grid { grid-template-columns: 1fr; }
            .header h1 { font-size: 2.2rem; }
            .voice-assistant-btn { bottom: 20px; right: 20px; width: 60px; height: 60px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1 id="headerTitle">👤 Patient Portal</h1>
        <p id="headerSubtitle">Welcome to MediCare Hospital Digital Platform</p>
    </div>
    
    <div class="container">
        <div class="options-grid">
            <a href="/patient/register?lang={{ lang }}" class="option-card">
                <div class="option-icon">📝</div>
                <div class="option-title" id="bookAppointmentTitle">Book New Appointment</div>
                <div class="option-description" id="bookAppointmentDesc">Register for a new consultation with our medical experts</div>
            </a>
            
            <a href="/patient/status?lang={{ lang }}" class="option-card">
                <div class="option-icon">🔍</div>
                <div class="option-title" id="checkStatusTitle">Check Appointment Status</div>
                <div class="option-description" id="checkStatusDesc">View your appointment details and queue position</div>
            </a>
        </div>
        
        <a href="/?lang={{ lang }}" class="back-btn">
            ← <span id="backHomeText">Back to Home</span>
        </a>
    </div>
    
    <!-- Voice Assistant Button -->
    <button class="voice-assistant-btn" id="voiceBtn" onclick="toggleVoiceAssistant()" title="Voice Assistant">
        🎤
    </button>

    <script>
        const currentLang = '{{ lang }}';
        
        const translations = {
            'en': {
                'headerTitle': '👤 Patient Portal',
                'headerSubtitle': 'Welcome to MediCare Hospital Digital Platform',
                'bookAppointmentTitle': 'Book New Appointment',
                'bookAppointmentDesc': 'Register for a new consultation with our medical experts',
                'checkStatusTitle': 'Check Appointment Status',
                'checkStatusDesc': 'View your appointment details and queue position',
                'backHomeText': 'Back to Home'
            },
            'hi': {
                'headerTitle': '👤 रोगी पोर्टल',
                'headerSubtitle': 'मेडिकेयर अस्पताल डिजिटल प्लेटफॉर्म में आपका स्वागत है',
                'bookAppointmentTitle': 'नई अपॉइंटमेंट बुक करें',
                'bookAppointmentDesc': 'हमारे चिकित्सा विशेषज्ञों के साथ नए परामर्श के लिए पंजीकरण करें',
                'checkStatusTitle': 'अपॉइंटमेंट स्थिति जांचें',
                'checkStatusDesc': 'अपनी अपॉइंटमेंट विवरण और कतार स्थिति देखें',
                'backHomeText': 'होम पर वापस जाएं'
            }
        };
        
        // Update page content based on language
        function updatePageContent() {
            const t = translations[currentLang];
            if (t) {
                document.getElementById('headerTitle').textContent = t.headerTitle;
                document.getElementById('headerSubtitle').textContent = t.headerSubtitle;
                document.getElementById('bookAppointmentTitle').textContent = t.bookAppointmentTitle;
                document.getElementById('bookAppointmentDesc').textContent = t.bookAppointmentDesc;
                document.getElementById('checkStatusTitle').textContent = t.checkStatusTitle;
                document.getElementById('checkStatusDesc').textContent = t.checkStatusDesc;
                document.getElementById('backHomeText').textContent = t.backHomeText;
            }
        }
        
        function toggleVoiceAssistant() {
            if (window.voiceAssistant) {
                window.voiceAssistant.startListening();
            }
        }
        
        // Initialize page
        document.addEventListener('DOMContentLoaded', function() {
            updatePageContent();
        });
    </script>
</body>
</html>
    ''', lang=language)
@app.route('/patient/register')
def patient_register():
    """Enhanced patient registration with voice assistant"""
    language = session.get('language', 'en')
    
    # Create translation context for template
    t = type('obj', (object,), {})()
    for key, value in TRANSLATIONS[language].items():
        setattr(t, key, value)
    
    # Use enhanced template if available, otherwise use fallback
    if ENHANCED_PATIENT_REGISTER_TEMPLATE != "<!-- Template loading... -->":
        return render_template_string(ENHANCED_PATIENT_REGISTER_TEMPLATE, lang=language, t=t)
    else:
        # Fallback simple registration template
        return render_template_string('''
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t.book_appointment }} - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #1565c0;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #1565c0;
        }
        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none;
            border-color: #1976d2;
            box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
        }
        .submit-btn {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
            transition: all 0.3s ease;
        }
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(25, 118, 210, 0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 {{ t.book_appointment }}</h1>
            <p>{{ t.describe_symptoms }}</p>
        </div>
        
        <a href="/patient?lang={{ lang }}" style="color: #1976d2; text-decoration: none; margin-bottom: 20px; display: inline-block;">← {{ t.back }}</a>
        
        <form id="registrationForm">
            <div class="form-group">
                <label for="name">{{ t.full_name }} *</label>
                <input type="text" id="name" name="name" required>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                <div class="form-group">
                    <label for="age">{{ t.age }} *</label>
                    <input type="number" id="age" name="age" min="1" max="120" required>
                </div>
                
                <div class="form-group">
                    <label for="gender">{{ t.gender }} *</label>
                    <select id="gender" name="gender" required>
                        <option value="">{{ t.select_gender }}</option>
                        <option value="Male">{{ t.male }}</option>
                        <option value="Female">{{ t.female }}</option>
                        <option value="Other">{{ t.other }}</option>
                    </select>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                <div class="form-group">
                    <label for="phone">{{ t.phone }} *</label>
                    <input type="tel" id="phone" name="phone" required>
                </div>
                
                <div class="form-group">
                    <label for="email">{{ t.email }}</label>
                    <input type="email" id="email" name="email">
                </div>
            </div>
            
            <div class="form-group">
                <label for="main_symptom">{{ t.primary_symptom }} *</label>
                <textarea id="main_symptom" name="main_symptom" rows="4" 
                          placeholder="{{ t.describe_symptoms }}" required></textarea>
            </div>
            
            <div class="form-group">
                <label for="severity">{{ t.symptom_severity }} *</label>
                <select id="severity" name="severity" required>
                    <option value="">Select Severity</option>
                    <option value="Mild">{{ t.mild }}</option>
                    <option value="Moderate">{{ t.moderate }}</option>
                    <option value="Severe">{{ t.severe }}</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="symptom_days">{{ t.symptom_duration }} *</label>
                <select id="symptom_days" name="symptom_days" required>
                    <option value="">{{ t.select_duration }}</option>
                    <option value="1">{{ t.today }}</option>
                    <option value="2">{{ t.days_2 }}</option>
                    <option value="7">{{ t.week }}</option>
                    <option value="14">{{ t.weeks_2 }}</option>
                    <option value="30">{{ t.month }}</option>
                    <option value="90">{{ t.month_plus }}</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" id="is_emergency" name="is_emergency" value="true">
                    🚨 {{ t.emergency }}
                </label>
            </div>
            
            <button type="submit" class="submit-btn">
                📅 {{ t.submit }}
            </button>
        </form>
    </div>

    <script>
        document.getElementById('registrationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                name: document.getElementById('name').value,
                age: parseInt(document.getElementById('age').value),
                gender: document.getElementById('gender').value,
                phone: document.getElementById('phone').value,
                email: document.getElementById('email').value,
                main_symptom: document.getElementById('main_symptom').value,
                severity: document.getElementById('severity').value,
                symptom_days: parseInt(document.getElementById('symptom_days').value),
                is_emergency: document.getElementById('is_emergency').checked,
                language: '{{ lang }}'
            };
            
            try {
                const response = await fetch('/api/register_patient', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert(`{{ t.success }}\\nRegistration ID: ${result.registration_id}\\nDepartment: ${result.department}`);
                    window.location.href = '/patient?lang={{ lang }}';
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        });
    </script>
</body>
</html>
        ''', lang=language, t=t)

@app.route('/patient/status')
def patient_status():
    """Enhanced patient status check"""
    language = session.get('language', 'en')
    
    # Create translation context for template
    t = type('obj', (object,), {})()
    for key, value in TRANSLATIONS[language].items():
        setattr(t, key, value)
    
    # Use enhanced template if available, otherwise use fallback
    if ENHANCED_PATIENT_STATUS_TEMPLATE != "<!-- Template loading... -->":
        return render_template_string(ENHANCED_PATIENT_STATUS_TEMPLATE, lang=language, t=t)
    else:
        # Fallback simple status template
        return render_template_string('''
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t.check_status }} - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #1565c0;
        }
        .search-input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1.1rem;
            text-align: center;
            margin-bottom: 20px;
            text-transform: uppercase;
        }
        .search-btn {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1rem;
            cursor: pointer;
            width: 100%;
        }
        .status-card {
            display: none;
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            margin-top: 30px;
        }
        .error-message {
            background: #ffebee;
            color: #c62828;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 {{ t.check_status }}</h1>
            <p>{{ t.enter_registration_id }}</p>
        </div>
        
        <a href="/patient?lang={{ lang }}" style="color: #1976d2; text-decoration: none; margin-bottom: 20px; display: inline-block;">← {{ t.back }}</a>
        
        <div style="text-align: center;">
            <input type="text" id="registrationId" class="search-input" 
                   placeholder="{{ t.enter_registration_id }}">
            <button onclick="checkStatus()" class="search-btn">
                🔍 {{ t.check_status_btn }}
            </button>
        </div>
        
        <div id="errorMessage" class="error-message"></div>
        
        <div id="statusCard" class="status-card">
            <h2 id="patientName" style="color: #1565c0; margin-bottom: 20px;"></h2>
            <div id="statusInfo"></div>
        </div>
    </div>

    <script>
        async function checkStatus() {
            const registrationId = document.getElementById('registrationId').value.trim().toUpperCase();
            
            if (!registrationId) {
                showError('{{ t.enter_registration_id }}');
                return;
            }
            
            try {
                const response = await fetch('/api/check_patient_status', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        registration_id: registrationId,
                        language: '{{ lang }}'
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    displayPatientStatus(result.patient);
                    hideError();
                } else {
                    showError(result.error);
                    hideStatusCard();
                }
            } catch (error) {
                showError('{{ t.network_error }}');
                hideStatusCard();
            }
        }
        
        function displayPatientStatus(patient) {
            document.getElementById('patientName').textContent = patient.name;
            document.getElementById('statusInfo').innerHTML = `
                <p><strong>Registration ID:</strong> ${patient.registration_id}</p>
                <p><strong>Status:</strong> ${patient.status}</p>
                <p><strong>Department:</strong> ${patient.department}</p>
                <p><strong>Risk Score:</strong> ${patient.risk_score}/100</p>
                <p><strong>Severity:</strong> ${patient.severity}</p>
            `;
            document.getElementById('statusCard').style.display = 'block';
        }
        
        function showError(message) {
            document.getElementById('errorMessage').textContent = message;
            document.getElementById('errorMessage').style.display = 'block';
        }
        
        function hideError() {
            document.getElementById('errorMessage').style.display = 'none';
        }
        
        function hideStatusCard() {
            document.getElementById('statusCard').style.display = 'none';
        }
        
        // Enter key support
        document.getElementById('registrationId').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                checkStatus();
            }
        });
    </script>
</body>
</html>
        ''', lang=language, t=t)
@app.route('/api/register_patient', methods=['POST'])
def register_patient():
    """Enhanced patient registration with language and notification preferences"""
    try:
        data = request.get_json()
        
        # Generate registration ID
        registration_id = generate_registration_id()
        
        # Calculate risk score
        risk_score = calculate_risk_score(data)
        
        # Emergency handling - boost risk score and create alert
        if data.get('is_emergency'):
            risk_score = min(100, risk_score + 30)
        
        # Determine department
        department = determine_department(data['main_symptom'])
        
        # Get language and notification preferences
        language = data.get('language', session.get('language', 'en'))
        notification_frequency = data.get('notification_frequency', 'daily')
        
        # Save to database
        conn = sqlite3.connect('enhanced_hospital_system.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO patients (registration_id, name, age, gender, phone, email,
                                main_symptom, severity, symptom_days, is_emergency,
                                department, risk_score, language_preference, notification_frequency)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (registration_id, data['name'], data['age'], data['gender'], 
              data['phone'], data.get('email', ''), data['main_symptom'],
              data['severity'], data['symptom_days'], data.get('is_emergency', False),
              department, risk_score, language, notification_frequency))
        
        patient_id = cursor.lastrowid
        
        # Create emergency alert if needed
        if data.get('is_emergency') or risk_score >= 80:
            cursor.execute('''
                INSERT INTO emergency_alerts (patient_id, alert_type, message)
                VALUES (?, ?, ?)
            ''', (patient_id, 'high_risk', f'High-risk patient {data["name"]} requires immediate attention'))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'registration_id': registration_id,
            'department': department,
            'risk_score': risk_score,
            'is_emergency': data.get('is_emergency', False),
            'message': get_translation('success', language)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/check_patient_status', methods=['POST'])
def check_patient_status():
    """Enhanced patient status check with language support"""
    try:
        data = request.get_json()
        registration_id = data['registration_id']
        language = data.get('language', session.get('language', 'en'))
        
        conn = sqlite3.connect('enhanced_hospital_system.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT registration_id, name, status, appointment_time, created_at, 
                   severity, main_symptom, department, risk_score, language_preference
            FROM patients WHERE registration_id = ?
        ''', (registration_id,))
        
        patient = cursor.fetchone()
        conn.close()
        
        if patient:
            return jsonify({
                'success': True,
                'patient': {
                    'registration_id': patient[0],
                    'name': patient[1],
                    'status': patient[2],
                    'appointment_time': patient[3],
                    'registered_date': patient[4],
                    'severity': patient[5],
                    'symptom': patient[6],
                    'department': patient[7],
                    'risk_score': patient[8],
                    'language': patient[9]
                }
            })
        else:
            return jsonify({'success': False, 'error': get_translation('registration_not_found', language)})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ===== ADMIN ROUTES =====

@app.route('/admin')
def admin_login():
    """Admin login page"""
    if ADMIN_LOGIN_TEMPLATE != "<!-- Template loading... -->":
        return render_template_string(ADMIN_LOGIN_TEMPLATE)
    else:
        # Fallback admin login template
        return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 90%;
        }
        .login-header {
            text-align: center;
            margin-bottom: 30px;
        }
        .admin-icon {
            font-size: 3rem;
            color: #d32f2f;
            margin-bottom: 15px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #1565c0;
        }
        input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
        }
        input:focus {
            outline: none;
            border-color: #d32f2f;
        }
        .login-btn {
            width: 100%;
            background: linear-gradient(135deg, #d32f2f, #c62828);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
        }
        .error-message {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
            display: none;
        }
        .demo-credentials {
            background: #f3e5f5;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <div class="admin-icon">🛡️</div>
            <h1 style="color: #1565c0; margin-bottom: 10px;">Admin Portal</h1>
            <p style="color: #546e7a;">Hospital Management System</p>
        </div>
        
        <div id="errorMessage" class="error-message"></div>
        
        <form id="loginForm">
            <div class="form-group">
                <label for="username">👤 Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">🔒 Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="login-btn">
                🔐 Secure Login
            </button>
        </form>
        
        <div class="demo-credentials">
            <h3 style="color: #1565c0; margin-bottom: 10px;">🔑 Demo Credentials</h3>
            <p><strong>Username:</strong> admin</p>
            <p><strong>Password:</strong> hospital2024</p>
        </div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                username: document.getElementById('username').value,
                password: document.getElementById('password').value
            };
            
            try {
                const response = await fetch('/admin/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    window.location.href = '/admin/dashboard';
                } else {
                    showError(result.error);
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            }
        });
        
        function showError(message) {
            document.getElementById('errorMessage').textContent = message;
            document.getElementById('errorMessage').style.display = 'block';
        }
    </script>
</body>
</html>
        ''')

@app.route('/admin/login', methods=['POST'])
def admin_authenticate():
    """Admin authentication"""
    try:
        data = request.get_json()
        username = data['username']
        password = hashlib.sha256(data['password'].encode()).hexdigest()
        
        conn = sqlite3.connect('enhanced_hospital_system.db')
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, full_name FROM admin_users 
                         WHERE username = ? AND password = ?''', (username, password))
        admin = cursor.fetchone()
        conn.close()
        
        if admin:
            session['admin_logged_in'] = True
            session['admin_id'] = admin[0]
            session['admin_name'] = admin[1]
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/dashboard')
def admin_dashboard():
    """Enhanced admin dashboard"""
    if not session.get('admin_logged_in'):
        return redirect('/admin')
    
    if ENHANCED_ADMIN_DASHBOARD_TEMPLATE != "<!-- Template loading... -->":
        return render_template_string(ENHANCED_ADMIN_DASHBOARD_TEMPLATE)
    else:
        # Fallback admin dashboard template
        return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
        }
        .admin-navbar {
            background: linear-gradient(135deg, #1565c0, #0d47a1);
            color: white;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        .navbar-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .main-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        .dashboard-title {
            font-size: 2.5rem;
            color: #1565c0;
            margin-bottom: 30px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        .patients-section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        .patients-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .patients-table th, .patients-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        .patients-table th {
            background: #f8f9fa;
            font-weight: 600;
        }
        .action-btn {
            background: #2ecc71;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
            margin: 2px;
        }
        .logout-btn {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <nav class="admin-navbar">
        <div class="navbar-content">
            <div>
                <h1>🏥 MediCare Hospital</h1>
                <p>Enhanced Admin Dashboard</p>
            </div>
            <div>
                <span>Welcome, {{ session.admin_name or 'Administrator' }}</span>
                <a href="/admin/logout" class="logout-btn">Logout</a>
            </div>
        </div>
    </nav>
    
    <div class="main-content">
        <h1 class="dashboard-title">🏥 Enhanced Hospital Dashboard</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>👥 Patients Today</h3>
                <div style="font-size: 2rem; font-weight: bold; color: #1976d2;" id="totalToday">0</div>
            </div>
            
            <div class="stat-card">
                <h3>🚨 Critical Cases</h3>
                <div style="font-size: 2rem; font-weight: bold; color: #d32f2f;" id="criticalCases">0</div>
            </div>
            
            <div class="stat-card">
                <h3>⏱️ Avg Wait Time</h3>
                <div style="font-size: 2rem; font-weight: bold; color: #388e3c;" id="avgWaiting">0</div>
            </div>
            
            <div class="stat-card">
                <h3>👨‍⚕️ Doctors Online</h3>
                <div style="font-size: 2rem; font-weight: bold; color: #f57c00;" id="doctorsOnline">0</div>
            </div>
        </div>
        
        <div class="patients-section">
            <h3>👥 Enhanced Patient Management</h3>
            <table class="patients-table">
                <thead>
                    <tr>
                        <th>Patient Info</th>
                        <th>Age</th>
                        <th>Symptoms</th>
                        <th>Risk Level</th>
                        <th>Department</th>
                        <th>Language</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="patientsTableBody">
                    <!-- Patients will be loaded here -->
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Load dashboard data on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadDashboardStats();
            loadPatients();
            
            // Auto-refresh every 30 seconds
            setInterval(() => {
                loadDashboardStats();
                loadPatients();
            }, 30000);
        });
        
        async function loadDashboardStats() {
            try {
                const response = await fetch('/api/admin/dashboard_stats');
                const stats = await response.json();
                
                document.getElementById('totalToday').textContent = stats.total_today;
                document.getElementById('criticalCases').textContent = stats.critical_cases;
                document.getElementById('avgWaiting').textContent = stats.avg_waiting;
                document.getElementById('doctorsOnline').textContent = stats.doctors_online;
                
            } catch (error) {
                console.error('Error loading dashboard stats:', error);
            }
        }
        
        async function loadPatients() {
            try {
                const response = await fetch('/api/admin/patients');
                const patients = await response.json();
                
                const tbody = document.getElementById('patientsTableBody');
                tbody.innerHTML = '';
                
                patients.forEach(patient => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>
                            <div style="font-weight: 600;">${patient.name}</div>
                            <div style="font-size: 0.8rem; color: #666;">${patient.registration_id}</div>
                        </td>
                        <td>${patient.age}</td>
                        <td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis;">
                            ${patient.symptom}
                        </td>
                        <td>
                            <span style="padding: 4px 8px; border-radius: 10px; font-size: 0.8rem; background: ${getRiskColor(patient.risk_score)};">
                                ${getRiskLevel(patient.risk_score)} (${patient.risk_score})
                            </span>
                        </td>
                        <td>${patient.department}</td>
                        <td>
                            <span style="padding: 4px 8px; background: #e3f2fd; color: #1976d2; border-radius: 10px; font-size: 0.8rem;">
                                ${getLanguageFlag(patient.language)} ${patient.language.toUpperCase()}
                            </span>
                        </td>
                        <td>
                            <span style="padding: 4px 8px; border-radius: 10px; font-size: 0.8rem; background: ${getStatusColor(patient.status)};">
                                ${patient.status.charAt(0).toUpperCase() + patient.status.slice(1)}
                            </span>
                        </td>
                        <td>
                            ${patient.status === 'waiting' ? 
                                `<button onclick="confirmPatient(${patient.id})" class="action-btn">✅ Confirm</button>` :
                                `<button onclick="generateReport(${patient.id})" class="action-btn">📋 Report</button>`
                            }
                        </td>
                    `;
                    tbody.appendChild(row);
                });
                
            } catch (error) {
                console.error('Error loading patients:', error);
            }
        }
        
        function getRiskLevel(score) {
            if (score >= 80) return 'High';
            if (score >= 50) return 'Medium';
            return 'Low';
        }
        
        function getRiskColor(score) {
            if (score >= 80) return '#ffebee';
            if (score >= 50) return '#fff3e0';
            return '#e8f5e8';
        }
        
        function getStatusColor(status) {
            const colors = {
                'waiting': '#fff3e0',
                'confirmed': '#e8f5e8',
                'in-consultation': '#e3f2fd',
                'completed': '#f3e5f5'
            };
            return colors[status] || '#f5f5f5';
        }
        
        function getLanguageFlag(lang) {
            const flags = { 'en': '🇺🇸', 'hi': '🇮🇳' };
            return flags[lang] || '🌐';
        }
        
        async function confirmPatient(patientId) {
            try {
                const response = await fetch('/api/admin/confirm_patient', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        patient_id: patientId,
                        appointment_time: new Date().toISOString().slice(0, 16)
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert('Patient confirmed successfully!');
                    loadPatients(); // Refresh the table
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        }
        
        function generateReport(patientId) {
            alert('Report generation feature coming soon!');
        }
    </script>
</body>
</html>
        ''')

@app.route('/api/admin/dashboard_stats')
def get_dashboard_stats():
    """Get dashboard statistics"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('enhanced_hospital_system.db')
    cursor = conn.cursor()
    
    # Today's stats
    today = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute("SELECT COUNT(*) FROM patients WHERE DATE(created_at) = ?", (today,))
    total_today = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM patients WHERE risk_score >= 80")
    critical_cases = cursor.fetchone()[0]
    
    # Mock data for demo
    doctors_online = 8
    avg_waiting = 25
    
    # Department distribution
    cursor.execute('''SELECT department, COUNT(*) FROM patients 
                     WHERE DATE(created_at) = ? GROUP BY department''', (today,))
    dept_data = cursor.fetchall()
    
    # Common symptoms
    cursor.execute('''SELECT main_symptom, COUNT(*) as count FROM patients 
                     WHERE DATE(created_at) = ? GROUP BY main_symptom 
                     ORDER BY count DESC LIMIT 5''', (today,))
    symptom_data = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'total_today': total_today,
        'critical_cases': critical_cases,
        'avg_waiting': avg_waiting,
        'doctors_online': doctors_online,
        'department_distribution': dict(dept_data),
        'common_symptoms': dict(symptom_data)
    })

@app.route('/api/admin/patients')
def get_all_patients():
    """Get all patients for admin (enhanced with language info)"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('enhanced_hospital_system.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, registration_id, name, age, gender, phone, main_symptom, 
               severity, department, risk_score, status, created_at, is_emergency, 
               appointment_time, language_preference, notification_frequency
        FROM patients ORDER BY risk_score DESC, created_at ASC
    ''')
    
    patients = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': p[0], 'registration_id': p[1], 'name': p[2], 'age': p[3], 'gender': p[4],
        'phone': p[5], 'symptom': p[6], 'severity': p[7], 'department': p[8],
        'risk_score': p[9], 'status': p[10], 'created_at': p[11], 'is_emergency': p[12],
        'appointment_time': p[13], 'language': p[14], 'notification_frequency': p[15]
    } for p in patients])

@app.route('/api/admin/confirm_patient', methods=['POST'])
def confirm_patient():
    """Enhanced patient confirmation with notifications"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        patient_id = data['patient_id']
        appointment_time = data.get('appointment_time', datetime.now().strftime('%Y-%m-%d %H:%M'))
        
        conn = sqlite3.connect('enhanced_hospital_system.db')
        cursor = conn.cursor()
        
        # Get patient details for notification
        cursor.execute('''
            SELECT name, email, language_preference FROM patients WHERE id = ?
        ''', (patient_id,))
        patient_info = cursor.fetchone()
        
        # Update patient status
        cursor.execute('''
            UPDATE patients 
            SET status = 'confirmed', appointment_time = ?, updated_at = ?
            WHERE id = ?
        ''', (appointment_time, datetime.now().isoformat(), patient_id))
        
        conn.commit()
        conn.close()
        
        # Send notification to patient
        if patient_info and patient_info[1]:  # If email exists
            patient_name, patient_email, language = patient_info
            message = get_translation('patient_confirmed', language or 'en')
            send_notification_email(patient_email, patient_name, message, language or 'en')
        
        return jsonify({'success': True, 'message': 'Patient confirmed and notified successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/admin/generate_report/<int:patient_id>')
def generate_patient_report(patient_id):
    """Generate patient report"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        conn = sqlite3.connect('enhanced_hospital_system.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patients WHERE id = ?
        ''', (patient_id,))
        
        patient = cursor.fetchone()
        conn.close()
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Generate report data
        report_data = {
            'patient_name': patient[2],
            'registration_id': patient[1],
            'age': patient[3],
            'gender': patient[4],
            'phone': patient[5],
            'symptom': patient[7],
            'severity': patient[8],
            'department': patient[10],
            'risk_score': patient[11],
            'status': patient[12],
            'created_at': patient[15],
            'appointment_time': patient[13],
            'is_emergency': patient[9]
        }
        
        return jsonify({
            'success': True,
            'report_data': report_data,
            'download_url': f'/api/admin/download_report/{patient_id}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/analytics')
def admin_analytics():
    """Admin analytics page"""
    if not session.get('admin_logged_in'):
        return redirect('/admin')
    
    # Import analytics template from enhanced_templates.py
    from enhanced_templates import ADMIN_ANALYTICS_TEMPLATE
    return render_template_string(ADMIN_ANALYTICS_TEMPLATE)

@app.route('/admin/reports')
def admin_reports():
    """Admin reports page"""
    if not session.get('admin_logged_in'):
        return redirect('/admin')
    
    # Import reports template from enhanced_templates.py
    from enhanced_templates import ADMIN_REPORTS_TEMPLATE
    return render_template_string(ADMIN_REPORTS_TEMPLATE)

@app.route('/admin/settings')
def admin_settings():
    """Admin settings page"""
    if not session.get('admin_logged_in'):
        return redirect('/admin')
    
    # Import settings template from enhanced_templates.py
    from enhanced_templates import ADMIN_SETTINGS_TEMPLATE
    return render_template_string(ADMIN_SETTINGS_TEMPLATE)

@app.route('/api/admin/analytics_data')
def get_analytics_data():
    """Get analytics data"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('enhanced_hospital_system.db')
    cursor = conn.cursor()
    
    # Weekly patient trends
    cursor.execute('''
        SELECT DATE(created_at) as date, COUNT(*) as count 
        FROM patients 
        WHERE created_at >= date('now', '-7 days')
        GROUP BY DATE(created_at)
        ORDER BY date
    ''')
    weekly_trends = cursor.fetchall()
    
    # Department performance
    cursor.execute('''
        SELECT department, 
               COUNT(*) as total_patients,
               AVG(risk_score) as avg_risk,
               COUNT(CASE WHEN status = 'confirmed' THEN 1 END) as confirmed
        FROM patients 
        GROUP BY department
    ''')
    dept_performance = cursor.fetchall()
    
    # Risk distribution
    cursor.execute('''
        SELECT 
            CASE 
                WHEN risk_score >= 80 THEN 'High Risk'
                WHEN risk_score >= 50 THEN 'Medium Risk'
                ELSE 'Low Risk'
            END as risk_level,
            COUNT(*) as count
        FROM patients
        GROUP BY risk_level
    ''')
    risk_distribution = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'weekly_trends': [{'date': row[0], 'count': row[1]} for row in weekly_trends],
        'department_performance': [{'department': row[0], 'total': row[1], 'avg_risk': round(row[2], 1), 'confirmed': row[3]} for row in dept_performance],
        'risk_distribution': [{'level': row[0], 'count': row[1]} for row in risk_distribution]
    })

@app.route('/api/admin/generate_daily_report')
def generate_daily_report():
    """Generate daily report"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('enhanced_hospital_system.db')
    cursor = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Daily statistics
    cursor.execute("SELECT COUNT(*) FROM patients WHERE DATE(created_at) = ?", (today,))
    total_patients = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM patients WHERE DATE(created_at) = ? AND risk_score >= 80", (today,))
    high_risk = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM patients WHERE DATE(created_at) = ? AND status = 'confirmed'", (today,))
    confirmed = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT department, COUNT(*) 
        FROM patients 
        WHERE DATE(created_at) = ? 
        GROUP BY department
    ''', (today,))
    dept_breakdown = cursor.fetchall()
    
    conn.close()
    
    report_data = {
        'date': today,
        'total_patients': total_patients,
        'high_risk_patients': high_risk,
        'confirmed_appointments': confirmed,
        'department_breakdown': dict(dept_breakdown),
        'generated_at': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'report_data': report_data,
        'filename': f'daily_report_{today}.json'
    })

@app.route('/api/admin/update_settings', methods=['POST'])
def update_admin_settings():
    """Update admin settings"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        
        conn = sqlite3.connect('enhanced_hospital_system.db')
        cursor = conn.cursor()
        
        # Update admin profile
        if 'admin_name' in data:
            cursor.execute('''
                UPDATE admin_users 
                SET full_name = ?, updated_at = ?
                WHERE id = ?
            ''', (data['admin_name'], datetime.now().isoformat(), session['admin_id']))
            session['admin_name'] = data['admin_name']
        
        # Update system settings
        settings_to_update = ['clinic_name', 'working_hours_start', 'working_hours_end', 'emergency_threshold']
        for setting in settings_to_update:
            if setting in data:
                cursor.execute('''
                    INSERT OR REPLACE INTO system_settings (setting_key, setting_value, updated_at)
                    VALUES (?, ?, ?)
                ''', (setting, data[setting], datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Settings updated successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/admin/get_settings')
def get_admin_settings():
    """Get current admin settings"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('enhanced_hospital_system.db')
    cursor = conn.cursor()
    
    # Get admin info
    cursor.execute('SELECT full_name, email FROM admin_users WHERE id = ?', (session['admin_id'],))
    admin_info = cursor.fetchone()
    
    # Get system settings
    cursor.execute('SELECT setting_key, setting_value FROM system_settings')
    system_settings = dict(cursor.fetchall())
    
    conn.close()
    
    return jsonify({
        'admin_name': admin_info[0] if admin_info else 'Administrator',
        'admin_email': admin_info[1] if admin_info else 'admin@hospital.com',
        'clinic_name': system_settings.get('clinic_name', 'MediCare Hospital'),
        'working_hours_start': system_settings.get('working_hours_start', '08:00'),
        'working_hours_end': system_settings.get('working_hours_end', '20:00'),
        'emergency_threshold': system_settings.get('emergency_threshold', '80')
    })

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    init_hospital_db()
    app.run(debug=True, host='127.0.0.1', port=5000)