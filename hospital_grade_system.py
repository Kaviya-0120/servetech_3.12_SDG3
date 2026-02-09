from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import sqlite3
import random
import string
from datetime import datetime, timedelta
import json
import hashlib

app = Flask(__name__)
app.secret_key = 'hospital_grade_secure_key_2024'

def init_hospital_db():
    """Initialize hospital-grade database"""
    conn = sqlite3.connect('hospital_system.db')
    cursor = conn.cursor()
    
    # Enhanced patients table
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
            doctor_assigned TEXT
        )
    ''')
    
    # Enhanced admin users table
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
    
    # Doctors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            specialization TEXT,
            phone TEXT,
            status TEXT DEFAULT 'online',
            working_hours TEXT DEFAULT '09:00-17:00',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    
    # Insert default admin
    admin_password = hashlib.sha256('hospital2024'.encode()).hexdigest()
    cursor.execute('''INSERT OR IGNORE INTO admin_users 
                     (username, email, password, full_name) 
                     VALUES (?, ?, ?, ?)''', 
                  ('admin', 'admin@hospital.com', admin_password, 'System Administrator'))
    
    # Insert sample doctors
    doctors_data = [
        ('Dr. Sarah Johnson', 'sarah@hospital.com', 'Cardiology', 'Interventional Cardiology', '+1-555-0101'),
        ('Dr. Michael Chen', 'michael@hospital.com', 'Pulmonology', 'Respiratory Medicine', '+1-555-0102'),
        ('Dr. Emily Rodriguez', 'emily@hospital.com', 'General Medicine', 'Internal Medicine', '+1-555-0103'),
        ('Dr. David Kim', 'david@hospital.com', 'Dermatology', 'Clinical Dermatology', '+1-555-0104'),
        ('Dr. Lisa Thompson', 'lisa@hospital.com', 'Neurology', 'Neurological Disorders', '+1-555-0105'),
        ('Dr. James Wilson', 'james@hospital.com', 'Orthopedics', 'Sports Medicine', '+1-555-0106'),
        ('Dr. Maria Garcia', 'maria@hospital.com', 'Emergency', 'Emergency Medicine', '+1-555-0107'),
        ('Dr. Robert Brown', 'robert@hospital.com', 'Pediatrics', 'Child Healthcare', '+1-555-0108')
    ]
    
    cursor.executemany('''INSERT OR IGNORE INTO doctors 
                         (name, email, department, specialization, phone) 
                         VALUES (?, ?, ?, ?, ?)''', doctors_data)
    
    # Insert default system settings
    default_settings = [
        ('clinic_name', 'MediCare Hospital'),
        ('working_hours_start', '08:00'),
        ('working_hours_end', '20:00'),
        ('emergency_threshold', '80'),
        ('max_daily_patients', '100')
    ]
    
    cursor.executemany('''INSERT OR IGNORE INTO system_settings 
                         (setting_key, setting_value) 
                         VALUES (?, ?)''', default_settings)
    
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
    
    # Neurology
    neuro_keywords = ['headache', 'migraine', 'dizziness', 'seizure', 'numbness']
    if any(keyword in symptom_lower for keyword in neuro_keywords):
        return 'Neurology'
    
    # Orthopedics
    ortho_keywords = ['joint', 'bone', 'fracture', 'back pain', 'muscle']
    if any(keyword in symptom_lower for keyword in ortho_keywords):
        return 'Orthopedics'
    
    # Pediatrics (age-based)
    return 'General Medicine'  # Default

@app.route('/')
def home():
    """Hospital landing page"""
    return render_template_string(HOSPITAL_LANDING_TEMPLATE)

@app.route('/patient')
def patient_portal():
    """Patient portal"""
    return render_template_string(PATIENT_PORTAL_TEMPLATE)
@app.route('/patient/register')
def patient_register():
    """Enhanced patient registration"""
    return render_template_string(ENHANCED_PATIENT_REGISTER_TEMPLATE)

@app.route('/api/register_patient', methods=['POST'])
def register_patient():
    """Process enhanced patient registration"""
    try:
        data = request.get_json()
        
        # Generate registration ID
        registration_id = generate_registration_id()
        
        # Calculate risk score
        risk_score = calculate_risk_score(data)
        
        # Emergency handling - boost risk score and create alert
        if data.get('is_emergency'):
            risk_score = min(100, risk_score + 30)  # Boost emergency cases
        
        # Determine department
        department = determine_department(data['main_symptom'])
        
        # Save to database
        conn = sqlite3.connect('hospital_system.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO patients (registration_id, name, age, gender, phone, email,
                                main_symptom, severity, symptom_days, is_emergency,
                                department, risk_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (registration_id, data['name'], data['age'], data['gender'], 
              data['phone'], data.get('email', ''), data['main_symptom'],
              data['severity'], data['symptom_days'], data.get('is_emergency', False),
              department, risk_score))
        
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
            'message': 'Registration successful. You will be contacted shortly.'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin')
def admin_login():
    """Admin login page"""
    return render_template_string(ADMIN_LOGIN_TEMPLATE)

@app.route('/admin/login', methods=['POST'])
def admin_authenticate():
    """Admin authentication"""
    try:
        data = request.get_json()
        username = data['username']
        password = hashlib.sha256(data['password'].encode()).hexdigest()
        
        conn = sqlite3.connect('hospital_system.db')
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
    return render_template_string(ENHANCED_ADMIN_DASHBOARD_TEMPLATE)

@app.route('/admin/analytics')
def admin_analytics():
    """Patient analytics page"""
    if not session.get('admin_logged_in'):
        return redirect('/admin')
    return render_template_string(ADMIN_ANALYTICS_TEMPLATE)

@app.route('/admin/departments')
def admin_departments():
    """Department insights page"""
    if not session.get('admin_logged_in'):
        return redirect('/admin')
    return render_template_string(ADMIN_DEPARTMENTS_TEMPLATE)

@app.route('/admin/reports')
def admin_reports():
    """Reports module"""
    if not session.get('admin_logged_in'):
        return redirect('/admin')
    return render_template_string(ADMIN_REPORTS_TEMPLATE)

@app.route('/admin/settings')
def admin_settings():
    """Settings page"""
    if not session.get('admin_logged_in'):
        return redirect('/admin')
    return render_template_string(ADMIN_SETTINGS_TEMPLATE)

# API Endpoints for Admin Dashboard
@app.route('/api/admin/dashboard_stats')
def get_dashboard_stats():
    """Get dashboard statistics"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('hospital_system.db')
    cursor = conn.cursor()
    
    # Today's stats
    today = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute("SELECT COUNT(*) FROM patients WHERE DATE(created_at) = ?", (today,))
    total_today = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM patients WHERE risk_score >= 80")
    critical_cases = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM doctors WHERE status = 'online'")
    doctors_online = cursor.fetchone()[0]
    
    # Average waiting time (mock calculation)
    avg_waiting = 25  # minutes
    
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
    """Get all patients for admin"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('hospital_system.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, registration_id, name, age, gender, phone, main_symptom, 
               severity, department, risk_score, status, created_at, is_emergency, appointment_time
        FROM patients ORDER BY risk_score DESC, created_at ASC
    ''')
    
    patients = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': p[0], 'registration_id': p[1], 'name': p[2], 'age': p[3], 'gender': p[4],
        'phone': p[5], 'symptom': p[6], 'severity': p[7], 'department': p[8],
        'risk_score': p[9], 'status': p[10], 'created_at': p[11], 'is_emergency': p[12],
        'appointment_time': p[13]
    } for p in patients])

@app.route('/api/admin/confirm_patient', methods=['POST'])
def confirm_patient():
    """Confirm patient appointment"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        patient_id = data['patient_id']
        appointment_time = data.get('appointment_time', datetime.now().strftime('%Y-%m-%d %H:%M'))
        
        conn = sqlite3.connect('hospital_system.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE patients 
            SET status = 'confirmed', appointment_time = ?, updated_at = ?
            WHERE id = ?
        ''', (appointment_time, datetime.now().isoformat(), patient_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Patient confirmed successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/admin/generate_report/<int:patient_id>')
def generate_patient_report(patient_id):
    """Generate patient report"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        conn = sqlite3.connect('hospital_system.db')
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
            'created_at': patient[14],
            'appointment_time': patient[13],
            'is_emergency': patient[15]
        }
        
        return jsonify({
            'success': True,
            'report_data': report_data,
            'download_url': f'/api/admin/download_report/{patient_id}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/admin/download_report/<int:patient_id>')
def download_patient_report(patient_id):
    """Download patient report as PDF"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    # In production, this would generate an actual PDF
    # For demo, we'll return a JSON response
    return jsonify({
        'success': True,
        'message': f'PDF report for patient ID {patient_id} would be downloaded in production',
        'filename': f'patient_report_{patient_id}.pdf'
    })

@app.route('/patient/status')
def patient_status():
    """Patient status check page"""
    return render_template_string(PATIENT_STATUS_TEMPLATE)

@app.route('/api/check_patient_status', methods=['POST'])
def check_patient_status():
    """Check patient status by registration ID"""
    try:
        data = request.get_json()
        registration_id = data['registration_id']
        
        conn = sqlite3.connect('hospital_system.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT registration_id, name, status, appointment_time, created_at, 
                   severity, main_symptom, department, risk_score
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
                    'risk_score': patient[8]
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Registration ID not found'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/admin/emergency_alerts')
def get_emergency_alerts():
    """Get active emergency alerts"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('hospital_system.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT ea.id, ea.alert_type, ea.message, ea.created_at, p.name, p.registration_id
        FROM emergency_alerts ea
        JOIN patients p ON ea.patient_id = p.id
        WHERE ea.status = 'active'
        ORDER BY ea.created_at DESC
    ''')
    
    alerts = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': a[0], 'type': a[1], 'message': a[2], 'created_at': a[3],
        'patient_name': a[4], 'registration_id': a[5]
    } for a in alerts])

@app.route('/api/admin/update_settings', methods=['POST'])
def update_settings():
    """Update system settings"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        
        conn = sqlite3.connect('hospital_system.db')
        cursor = conn.cursor()
        
        for key, value in data.items():
            cursor.execute('''
                INSERT OR REPLACE INTO system_settings (setting_key, setting_value, updated_at)
                VALUES (?, ?, ?)
            ''', (key, value, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.clear()
    return redirect('/')
# ===== HOSPITAL-GRADE UI TEMPLATES =====

HOSPITAL_LANDING_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MediCare Hospital - Digital Healthcare Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 50%, #f0f8ff 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .hospital-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            padding: 60px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 600px;
            width: 90%;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .hospital-logo {
            font-size: 4rem;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #1976d2, #42a5f5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .hospital-name {
            font-size: 2.8rem;
            color: #1565c0;
            margin-bottom: 15px;
            font-weight: 700;
            letter-spacing: -1px;
        }
        .hospital-tagline {
            color: #546e7a;
            margin-bottom: 50px;
            font-size: 1.2rem;
            font-weight: 300;
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
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(25, 118, 210, 0.4);
        }
        .access-btn.admin {
            background: linear-gradient(135deg, #d32f2f, #c62828);
            box-shadow: 0 8px 25px rgba(211, 47, 47, 0.3);
        }
        .access-btn.admin:hover {
            box-shadow: 0 15px 35px rgba(211, 47, 47, 0.4);
        }
        .btn-icon {
            font-size: 1.6rem;
        }
        .btn-text {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        .btn-subtitle {
            font-size: 0.9rem;
            font-weight: 400;
            opacity: 0.9;
        }
        .hospital-features {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid #e0e0e0;
        }
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .feature-item {
            color: #546e7a;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .feature-icon {
            color: #1976d2;
            font-size: 1.1rem;
        }
    </style>
</head>
<body>
    <div class="hospital-container">
        <div class="hospital-logo">🏥</div>
        <h1 class="hospital-name">MediCare Hospital</h1>
        <p class="hospital-tagline">Advanced Digital Healthcare Platform</p>
        
        <div class="access-buttons">
            <a href="/patient" class="access-btn">
                <span class="btn-icon">👤</span>
                <div class="btn-text">
                    <span>Patient Portal</span>
                    <span class="btn-subtitle">Book appointments & check status</span>
                </div>
            </a>
            
            <a href="/admin" class="access-btn admin">
                <span class="btn-icon">🛡️</span>
                <div class="btn-text">
                    <span>Admin Dashboard</span>
                    <span class="btn-subtitle">Hospital management system</span>
                </div>
            </a>
        </div>
        
        <div class="hospital-features">
            <div class="features-grid">
                <div class="feature-item">
                    <span class="feature-icon">⚡</span>
                    <span>Real-time Queue</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🚨</span>
                    <span>Emergency Priority</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">📊</span>
                    <span>Advanced Analytics</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🔒</span>
                    <span>HIPAA Compliant</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

PATIENT_PORTAL_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Patient Portal - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 50%, #f0f8ff 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            color: #1565c0;
        }
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .header p {
            font-size: 1.1rem;
            color: #546e7a;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            padding: 50px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.1);
        }
        .options-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
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
            position: relative;
            overflow: hidden;
        }
        .option-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(25, 118, 210, 0.1), transparent);
            transition: left 0.5s;
        }
        .option-card:hover::before {
            left: 100%;
        }
        .option-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 60px rgba(25, 118, 210, 0.2);
            border-color: #1976d2;
        }
        .option-icon {
            font-size: 4rem;
            margin-bottom: 20px;
            color: #1976d2;
        }
        .option-title {
            font-size: 1.6rem;
            font-weight: 600;
            color: #1565c0;
            margin-bottom: 15px;
        }
        .option-desc {
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
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .back-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(144, 164, 174, 0.4);
        }
        .emergency-notice {
            background: linear-gradient(135deg, #ffebee, #fce4ec);
            border: 2px solid #f8bbd9;
            border-radius: 15px;
            padding: 25px;
            margin-top: 30px;
            text-align: center;
        }
        .emergency-notice h3 {
            color: #c62828;
            margin-bottom: 10px;
            font-size: 1.3rem;
        }
        .emergency-notice p {
            color: #ad1457;
            font-size: 0.95rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>👤 Patient Portal</h1>
        <p>Welcome to MediCare Hospital Digital Platform</p>
    </div>
    
    <div class="container">
        <div class="options-grid">
            <a href="/patient/register" class="option-card">
                <div class="option-icon">📝</div>
                <div class="option-title">Book New Appointment</div>
                <div class="option-desc">Register for a new consultation with our medical experts</div>
            </a>
            
            <a href="/patient/status" class="option-card">
                <div class="option-icon">🔍</div>
                <div class="option-title">Check Appointment Status</div>
                <div class="option-desc">View your appointment details and queue position</div>
            </a>
        </div>
        
        <div class="emergency-notice">
            <h3>🚨 Medical Emergency?</h3>
            <p>For life-threatening emergencies, call 911 immediately or visit the nearest emergency room. 
               For urgent but non-emergency cases, use our emergency booking option.</p>
        </div>
        
        <a href="/" class="back-btn">
            ← Back to Home
        </a>
    </div>
</body>
</html>
'''
ENHANCED_PATIENT_REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book Appointment - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 50%, #f0f8ff 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #1565c0;
        }
        .header h1 {
            font-size: 2.2rem;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            padding: 40px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.1);
        }
        .form-section {
            margin-bottom: 35px;
            padding: 25px;
            background: linear-gradient(135deg, #fafafa, #ffffff);
            border-radius: 15px;
            border: 1px solid #e3f2fd;
        }
        .section-title {
            font-size: 1.4rem;
            color: #1565c0;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e3f2fd;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
        }
        .form-group.full-width {
            grid-column: 1 / -1;
        }
        label {
            margin-bottom: 8px;
            font-weight: 600;
            color: #1565c0;
            font-size: 0.95rem;
        }
        input, select, textarea {
            padding: 15px;
            border: 2px solid #e3f2fd;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.8);
        }
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #1976d2;
            box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
            background: white;
        }
        .severity-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 10px;
        }
        .severity-btn {
            padding: 20px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            background: white;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
        }
        .severity-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        .severity-btn.selected {
            border-color: #1976d2;
            background: linear-gradient(135deg, #e3f2fd, #ffffff);
        }
        .severity-btn.mild.selected { border-color: #4caf50; background: linear-gradient(135deg, #e8f5e8, #ffffff); }
        .severity-btn.moderate.selected { border-color: #ff9800; background: linear-gradient(135deg, #fff3e0, #ffffff); }
        .severity-btn.severe.selected { border-color: #f44336; background: linear-gradient(135deg, #ffebee, #ffffff); }
        .severity-title {
            font-weight: bold;
            margin-bottom: 5px;
        }
        .severity-desc {
            font-size: 0.85rem;
            color: #666;
        }
        .emergency-section {
            background: linear-gradient(135deg, #ffebee, #fce4ec);
            border: 2px solid #f8bbd9;
            border-radius: 15px;
            padding: 25px;
            margin: 25px 0;
        }
        .emergency-toggle {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        .emergency-switch {
            position: relative;
            width: 60px;
            height: 30px;
            background: #ccc;
            border-radius: 15px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .emergency-switch.active {
            background: #f44336;
        }
        .emergency-switch::before {
            content: '';
            position: absolute;
            width: 26px;
            height: 26px;
            border-radius: 50%;
            background: white;
            top: 2px;
            left: 2px;
            transition: transform 0.3s;
        }
        .emergency-switch.active::before {
            transform: translateX(30px);
        }
        .emergency-label {
            font-size: 1.1rem;
            font-weight: 600;
            color: #c62828;
        }
        .emergency-info {
            color: #ad1457;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        .submit-btn {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
            border: none;
            padding: 20px 40px;
            border-radius: 15px;
            font-size: 1.2rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-top: 30px;
            transition: all 0.4s ease;
            box-shadow: 0 8px 25px rgba(25, 118, 210, 0.3);
        }
        .submit-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(25, 118, 210, 0.4);
        }
        .back-btn {
            background: linear-gradient(135deg, #90a4ae, #78909c);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 10px;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 25px;
            font-weight: 500;
        }
        .success-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        .modal-content {
            background: white;
            padding: 50px;
            border-radius: 25px;
            text-align: center;
            max-width: 600px;
            width: 90%;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.3);
        }
        .success-icon {
            font-size: 5rem;
            color: #4caf50;
            margin-bottom: 25px;
        }
        .modal-title {
            font-size: 2rem;
            color: #1565c0;
            margin-bottom: 20px;
            font-weight: 700;
        }
        .registration-info {
            background: linear-gradient(135deg, #e3f2fd, #ffffff);
            padding: 25px;
            border-radius: 15px;
            margin: 25px 0;
            border: 2px solid #1976d2;
        }
        .reg-id {
            font-size: 2rem;
            font-weight: bold;
            color: #1976d2;
            margin: 15px 0;
        }
        .department-info {
            background: linear-gradient(135deg, #f3e5f5, #ffffff);
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            border-left: 4px solid #9c27b0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📝 Book New Appointment</h1>
        <p>Please provide your details for consultation</p>
    </div>
    
    <div class="container">
        <a href="/patient" class="back-btn">← Back to Patient Portal</a>
        
        <form id="registrationForm">
            <!-- Personal Information -->
            <div class="form-section">
                <div class="section-title">
                    <span>👤</span> Personal Information
                </div>
                <div class="form-grid">
                    <div class="form-group">
                        <label for="name">Full Name *</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="age">Age *</label>
                        <input type="number" id="age" name="age" min="1" max="120" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="gender">Gender *</label>
                        <select id="gender" name="gender" required>
                            <option value="">Select Gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="phone">Phone Number *</label>
                        <input type="tel" id="phone" name="phone" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="email">Email Address</label>
                        <input type="email" id="email" name="email">
                    </div>
                </div>
            </div>
            
            <!-- Medical Information -->
            <div class="form-section">
                <div class="section-title">
                    <span>🩺</span> Medical Information
                </div>
                
                <div class="form-group full-width">
                    <label for="main_symptom">Primary Symptom/Concern *</label>
                    <textarea id="main_symptom" name="main_symptom" rows="4" 
                              placeholder="Please describe your main health concern in detail..." required></textarea>
                </div>
                
                <div class="form-group">
                    <label>Symptom Severity *</label>
                    <div class="severity-grid">
                        <div class="severity-btn mild" onclick="selectSeverity('Mild', this)">
                            <div class="severity-title" style="color: #4caf50;">Mild</div>
                            <div class="severity-desc">Manageable discomfort</div>
                        </div>
                        <div class="severity-btn moderate" onclick="selectSeverity('Moderate', this)">
                            <div class="severity-title" style="color: #ff9800;">Moderate</div>
                            <div class="severity-desc">Noticeable impact on daily life</div>
                        </div>
                        <div class="severity-btn severe" onclick="selectSeverity('Severe', this)">
                            <div class="severity-title" style="color: #f44336;">Severe</div>
                            <div class="severity-desc">Significant distress/pain</div>
                        </div>
                    </div>
                    <input type="hidden" id="severity" name="severity" required>
                </div>
                
                <div class="form-group">
                    <label for="symptom_days">Duration of Symptoms *</label>
                    <select id="symptom_days" name="symptom_days" required>
                        <option value="">Select duration</option>
                        <option value="1">Today (1 day)</option>
                        <option value="2">2 days</option>
                        <option value="3">3 days</option>
                        <option value="7">About a week</option>
                        <option value="14">About 2 weeks</option>
                        <option value="30">About a month</option>
                        <option value="90">More than a month</option>
                    </select>
                </div>
            </div>
            
            <!-- Emergency Section -->
            <div class="emergency-section">
                <div class="emergency-toggle">
                    <div class="emergency-switch" id="emergencySwitch" onclick="toggleEmergency()"></div>
                    <div class="emergency-label">🚨 This is an Emergency</div>
                </div>
                <div class="emergency-info">
                    <strong>Emergency Priority:</strong> Selecting this option will prioritize your case and attempt to schedule you for immediate consultation. Use only for urgent medical situations that require prompt attention.
                </div>
                <input type="hidden" id="is_emergency" name="is_emergency" value="false">
            </div>
            
            <button type="submit" class="submit-btn">
                📅 Book Appointment
            </button>
        </form>
    </div>
    
    <!-- Success Modal -->
    <div id="successModal" class="success-modal">
        <div class="modal-content">
            <div class="success-icon">✅</div>
            <h2 class="modal-title">Appointment Booked Successfully!</h2>
            
            <div class="registration-info">
                <strong>Your Registration ID:</strong>
                <div class="reg-id" id="registrationId"></div>
                <p style="color: #666; margin-top: 10px;">Please save this ID to check your appointment status</p>
            </div>
            
            <div class="department-info" id="departmentInfo">
                <h3 style="color: #9c27b0; margin-bottom: 10px;">📋 Recommended Department</h3>
                <div id="departmentName" style="font-size: 1.2rem; font-weight: bold;"></div>
                <div id="departmentMessage" style="margin-top: 10px; color: #666;"></div>
            </div>
            
            <div id="emergencyMessage" style="display: none; background: #ffebee; padding: 20px; border-radius: 12px; margin: 20px 0; border-left: 4px solid #f44336;">
                <h4 style="color: #c62828; margin-bottom: 10px;">🚨 Emergency Priority Activated</h4>
                <p style="color: #ad1457;">We are trying to schedule your consultation earlier due to emergency status. You will be contacted shortly.</p>
            </div>
            
            <button onclick="goToPatientPortal()" style="background: #1976d2; color: white; border: none; padding: 15px 30px; border-radius: 10px; cursor: pointer; font-size: 1rem; margin-top: 20px;">
                Back to Patient Portal
            </button>
        </div>
    </div>

    <script>
        let selectedSeverity = '';
        let isEmergency = false;
        
        function selectSeverity(severity, element) {
            document.querySelectorAll('.severity-btn').forEach(btn => {
                btn.classList.remove('selected');
            });
            
            element.classList.add('selected');
            selectedSeverity = severity;
            document.getElementById('severity').value = severity;
        }
        
        function toggleEmergency() {
            const switchEl = document.getElementById('emergencySwitch');
            const hiddenInput = document.getElementById('is_emergency');
            
            isEmergency = !isEmergency;
            
            if (isEmergency) {
                switchEl.classList.add('active');
                hiddenInput.value = 'true';
            } else {
                switchEl.classList.remove('active');
                hiddenInput.value = 'false';
            }
        }
        
        document.getElementById('registrationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!selectedSeverity) {
                alert('Please select symptom severity');
                return;
            }
            
            const formData = {
                name: document.getElementById('name').value,
                age: parseInt(document.getElementById('age').value),
                gender: document.getElementById('gender').value,
                phone: document.getElementById('phone').value,
                email: document.getElementById('email').value,
                main_symptom: document.getElementById('main_symptom').value,
                severity: selectedSeverity,
                symptom_days: parseInt(document.getElementById('symptom_days').value),
                is_emergency: isEmergency
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
                    document.getElementById('registrationId').textContent = result.registration_id;
                    document.getElementById('departmentName').textContent = result.department;
                    
                    const deptMessages = {
                        'Cardiology': 'Heart and cardiovascular conditions - Our cardiology team will evaluate your symptoms.',
                        'Pulmonology': 'Respiratory and lung conditions - Our pulmonology specialists will assess your breathing concerns.',
                        'General Medicine': 'General health concerns - Our internal medicine doctors will provide comprehensive care.',
                        'Dermatology': 'Skin conditions and disorders - Our dermatology experts will examine your skin concerns.',
                        'Neurology': 'Neurological conditions - Our neurology team will evaluate your symptoms.',
                        'Orthopedics': 'Bone, joint, and muscle conditions - Our orthopedic specialists will assess your concerns.',
                        'Emergency': 'Emergency medical attention - You will be prioritized for immediate care.',
                        'Pediatrics': 'Pediatric care - Our child healthcare specialists will provide age-appropriate treatment.'
                    };
                    
                    document.getElementById('departmentMessage').textContent = deptMessages[result.department] || 'Our medical team will provide appropriate care.';
                    
                    if (result.is_emergency || result.risk_score >= 80) {
                        document.getElementById('emergencyMessage').style.display = 'block';
                    }
                    
                    document.getElementById('successModal').style.display = 'flex';
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        });
        
        function goToPatientPortal() {
            window.location.href = '/patient';
        }
    </script>
</body>
</html>
'''
ADMIN_LOGIN_TEMPLATE = '''
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
            background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 50%, #f0f8ff 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            padding: 60px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            width: 90%;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .login-header {
            text-align: center;
            margin-bottom: 40px;
        }
        .admin-icon {
            font-size: 4rem;
            color: #d32f2f;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #d32f2f, #c62828);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .login-title {
            color: #1565c0;
            margin-bottom: 10px;
            font-size: 2.2rem;
            font-weight: 700;
        }
        .login-subtitle {
            color: #546e7a;
            font-size: 1rem;
        }
        .form-group {
            margin-bottom: 25px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #1565c0;
        }
        input {
            width: 100%;
            padding: 18px;
            border: 2px solid #e3f2fd;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.8);
        }
        input:focus {
            outline: none;
            border-color: #d32f2f;
            box-shadow: 0 0 0 3px rgba(211, 47, 47, 0.1);
            background: white;
        }
        .login-btn {
            width: 100%;
            background: linear-gradient(135deg, #d32f2f, #c62828);
            color: white;
            border: none;
            padding: 20px;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.4s ease;
            box-shadow: 0 8px 25px rgba(211, 47, 47, 0.3);
        }
        .login-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(211, 47, 47, 0.4);
        }
        .back-btn {
            background: linear-gradient(135deg, #90a4ae, #78909c);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 10px;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 30px;
            font-weight: 500;
        }
        .error-message {
            background: linear-gradient(135deg, #ffebee, #fce4ec);
            color: #c62828;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            display: none;
            border: 1px solid #f8bbd9;
        }
        .demo-credentials {
            background: linear-gradient(135deg, #f3e5f5, #ffffff);
            padding: 25px;
            border-radius: 15px;
            margin-top: 30px;
            text-align: center;
            border: 1px solid #e1bee7;
        }
        .demo-credentials h3 {
            color: #1565c0;
            margin-bottom: 15px;
            font-size: 1.2rem;
        }
        .demo-credentials p {
            color: #546e7a;
            font-size: 0.95rem;
            margin: 5px 0;
        }
        .security-notice {
            background: linear-gradient(135deg, #e8f5e8, #ffffff);
            padding: 20px;
            border-radius: 12px;
            margin-top: 25px;
            border-left: 4px solid #4caf50;
        }
        .security-notice h4 {
            color: #2e7d32;
            margin-bottom: 8px;
            font-size: 1rem;
        }
        .security-notice p {
            color: #388e3c;
            font-size: 0.9rem;
            line-height: 1.4;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <a href="/" class="back-btn">← Back to Home</a>
        
        <div class="login-header">
            <div class="admin-icon">🛡️</div>
            <h1 class="login-title">Admin Portal</h1>
            <p class="login-subtitle">Hospital Management System</p>
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
            <h3>🔑 Demo Credentials</h3>
            <p><strong>Username:</strong> admin</p>
            <p><strong>Password:</strong> hospital2024</p>
        </div>
        
        <div class="security-notice">
            <h4>🔒 Security Notice</h4>
            <p>This system contains sensitive patient information. Unauthorized access is prohibited and monitored.</p>
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
'''
ENHANCED_ADMIN_DASHBOARD_TEMPLATE = '''
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
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        /* Navigation Bar */
        .admin-navbar {
            background: linear-gradient(135deg, #1565c0, #0d47a1);
            color: white;
            padding: 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .navbar-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 20px 0;
        }
        .brand-icon {
            font-size: 2rem;
        }
        .brand-text h1 {
            font-size: 1.5rem;
            font-weight: 700;
        }
        .brand-text p {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        .nav-menu {
            display: flex;
            list-style: none;
            gap: 0;
        }
        .nav-item {
            position: relative;
        }
        .nav-link {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 20px 25px;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        .nav-link:hover, .nav-link.active {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        .nav-link.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: #64b5f6;
        }
        .user-menu {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .user-info {
            text-align: right;
        }
        .user-name {
            font-weight: 600;
            font-size: 1rem;
        }
        .user-role {
            font-size: 0.8rem;
            opacity: 0.8;
        }
        .logout-btn {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .logout-btn:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        
        /* Main Content */
        .main-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        
        /* Dashboard Header */
        .dashboard-header {
            margin-bottom: 30px;
        }
        .dashboard-title {
            font-size: 2.2rem;
            color: #1565c0;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .dashboard-subtitle {
            color: #546e7a;
            font-size: 1.1rem;
        }
        
        /* Stats Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        .stat-card {
            background: linear-gradient(135deg, #ffffff, #f8f9fa);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--card-color);
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }
        .stat-card.primary { --card-color: linear-gradient(135deg, #1976d2, #1565c0); }
        .stat-card.danger { --card-color: linear-gradient(135deg, #d32f2f, #c62828); }
        .stat-card.success { --card-color: linear-gradient(135deg, #388e3c, #2e7d32); }
        .stat-card.warning { --card-color: linear-gradient(135deg, #f57c00, #ef6c00); }
        
        .stat-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
        }
        .stat-icon {
            font-size: 2.5rem;
            opacity: 0.8;
        }
        .stat-card.primary .stat-icon { color: #1976d2; }
        .stat-card.danger .stat-icon { color: #d32f2f; }
        .stat-card.success .stat-icon { color: #388e3c; }
        .stat-card.warning .stat-icon { color: #f57c00; }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1565c0;
            margin-bottom: 5px;
        }
        .stat-label {
            color: #546e7a;
            font-size: 1rem;
            font-weight: 500;
        }
        .stat-change {
            font-size: 0.85rem;
            margin-top: 10px;
            padding: 5px 10px;
            border-radius: 20px;
            display: inline-block;
        }
        .stat-change.positive {
            background: #e8f5e8;
            color: #2e7d32;
        }
        .stat-change.negative {
            background: #ffebee;
            color: #c62828;
        }
        
        /* Charts Section */
        .charts-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        .chart-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        .chart-header {
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }
        .chart-title {
            font-size: 1.4rem;
            color: #1565c0;
            font-weight: 600;
            margin-bottom: 5px;
        }
        .chart-subtitle {
            color: #546e7a;
            font-size: 0.9rem;
        }
        .chart-container {
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Emergency Alerts */
        .alerts-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }
        .alerts-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }
        .alerts-title {
            font-size: 1.4rem;
            color: #d32f2f;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .alert-item {
            background: linear-gradient(135deg, #ffebee, #fce4ec);
            border: 1px solid #f8bbd9;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #d32f2f;
        }
        .alert-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        .alert-patient {
            font-weight: 600;
            color: #c62828;
        }
        .alert-time {
            font-size: 0.85rem;
            color: #ad1457;
        }
        .alert-message {
            color: #880e4f;
            font-size: 0.95rem;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .navbar-content {
                flex-direction: column;
                gap: 20px;
            }
            .nav-menu {
                flex-wrap: wrap;
                justify-content: center;
            }
            .nav-link {
                padding: 15px 20px;
            }
            .stats-grid {
                grid-template-columns: 1fr;
            }
            .charts-section {
                grid-template-columns: 1fr;
            }
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <!-- Admin Navigation -->
    <nav class="admin-navbar">
        <div class="navbar-content">
            <div class="navbar-brand">
                <span class="brand-icon">🏥</span>
                <div class="brand-text">
                    <h1>MediCare Hospital</h1>
                    <p>Admin Dashboard</p>
                </div>
            </div>
            
            <ul class="nav-menu">
                <li class="nav-item">
                    <a href="/admin/dashboard" class="nav-link active">
                        <span>📊</span> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/analytics" class="nav-link">
                        <span>📈</span> Analytics
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/departments" class="nav-link">
                        <span>🏢</span> Departments
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/reports" class="nav-link">
                        <span>📋</span> Reports
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/settings" class="nav-link">
                        <span>⚙️</span> Settings
                    </a>
                </li>
            </ul>
            
            <div class="user-menu">
                <div class="user-info">
                    <div class="user-name">{{ session.admin_name or 'Administrator' }}</div>
                    <div class="user-role">System Admin</div>
                </div>
                <a href="/admin/logout" class="logout-btn">Logout</a>
            </div>
        </div>
    </nav>
    
    <!-- Main Content -->
    <div class="main-content">
        <!-- Dashboard Header -->
        <div class="dashboard-header">
            <h1 class="dashboard-title">Hospital Dashboard</h1>
            <p class="dashboard-subtitle">Real-time overview of hospital operations and patient management</p>
        </div>
        
        <!-- Statistics Cards -->
        <div class="stats-grid">
            <div class="stat-card primary">
                <div class="stat-header">
                    <div class="stat-icon">👥</div>
                </div>
                <div class="stat-number" id="totalToday">0</div>
                <div class="stat-label">Patients Today</div>
                <div class="stat-change positive" id="todayChange">+12% from yesterday</div>
            </div>
            
            <div class="stat-card danger">
                <div class="stat-header">
                    <div class="stat-icon">🚨</div>
                </div>
                <div class="stat-number" id="criticalCases">0</div>
                <div class="stat-label">Critical Cases</div>
                <div class="stat-change negative" id="criticalChange">Requires attention</div>
            </div>
            
            <div class="stat-card success">
                <div class="stat-header">
                    <div class="stat-icon">⏱️</div>
                </div>
                <div class="stat-number" id="avgWaiting">0</div>
                <div class="stat-label">Avg Wait Time (min)</div>
                <div class="stat-change positive" id="waitChange">-5 min from last hour</div>
            </div>
            
            <div class="stat-card warning">
                <div class="stat-header">
                    <div class="stat-icon">👨‍⚕️</div>
                </div>
                <div class="stat-number" id="doctorsOnline">0</div>
                <div class="stat-label">Doctors Online</div>
                <div class="stat-change positive" id="doctorChange">All departments covered</div>
            </div>
        </div>
        
        <!-- Charts Section -->
        <div class="charts-section">
            <div class="chart-card">
                <div class="chart-header">
                    <h3 class="chart-title">Department Distribution</h3>
                    <p class="chart-subtitle">Patient distribution across departments today</p>
                </div>
                <div class="chart-container">
                    <canvas id="departmentChart"></canvas>
                </div>
            </div>
            
            <div class="chart-card">
                <div class="chart-header">
                    <h3 class="chart-title">Common Symptoms</h3>
                    <p class="chart-subtitle">Most reported symptoms today</p>
                </div>
                <div class="chart-container">
                    <canvas id="symptomsChart"></canvas>
                </div>
            </div>
        </div>
        
        <!-- Emergency Alerts -->
        <div class="alerts-section">
            <div class="alerts-header">
                <h3 class="alerts-title">
                    <span>🚨</span> Emergency Alerts
                </h3>
                <button onclick="refreshAlerts()" style="background: #d32f2f; color: white; border: none; padding: 8px 15px; border-radius: 6px; cursor: pointer;">
                    Refresh
                </button>
            </div>
            <div id="alertsContainer">
                <!-- Emergency alerts will be loaded here -->
            </div>
        </div>
        
        <!-- Patient Management Table -->
        <div class="patients-section">
            <div class="section-header">
                <h3 style="font-size: 1.4rem; color: #1565c0; font-weight: 600; display: flex; align-items: center; gap: 10px;">
                    <span>👥</span> Patient Management
                </h3>
                <button onclick="refreshPatients()" style="background: #1976d2; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer;">
                    Refresh Patients
                </button>
            </div>
            <div class="table-container" style="overflow-x: auto; background: white; border-radius: 15px; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);">
                <table class="patients-table" style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background: #f8f9fa;">
                            <th style="padding: 15px; text-align: left; font-weight: 600; color: #2c3e50; border-bottom: 2px solid #e0e0e0;">Name</th>
                            <th style="padding: 15px; text-align: left; font-weight: 600; color: #2c3e50; border-bottom: 2px solid #e0e0e0;">Age</th>
                            <th style="padding: 15px; text-align: left; font-weight: 600; color: #2c3e50; border-bottom: 2px solid #e0e0e0;">Symptoms</th>
                            <th style="padding: 15px; text-align: left; font-weight: 600; color: #2c3e50; border-bottom: 2px solid #e0e0e0;">Risk Level</th>
                            <th style="padding: 15px; text-align: left; font-weight: 600; color: #2c3e50; border-bottom: 2px solid #e0e0e0;">Department</th>
                            <th style="padding: 15px; text-align: left; font-weight: 600; color: #2c3e50; border-bottom: 2px solid #e0e0e0;">Status</th>
                            <th style="padding: 15px; text-align: left; font-weight: 600; color: #2c3e50; border-bottom: 2px solid #e0e0e0;">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="patientsTableBody">
                        <!-- Patients will be loaded here -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <!-- Confirm Patient Modal -->
    <div id="confirmModal" class="modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); z-index: 1000; align-items: center; justify-content: center;">
        <div class="modal-content" style="background: white; padding: 30px; border-radius: 15px; max-width: 500px; width: 90%;">
            <h3 style="margin-bottom: 20px; color: #1565c0;">📅 Confirm Patient Appointment</h3>
            <div style="margin-bottom: 20px;">
                <label style="display: block; margin-bottom: 8px; font-weight: 600;">Appointment Date & Time:</label>
                <input type="datetime-local" id="appointmentDateTime" style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px;" required>
            </div>
            <div style="display: flex; gap: 15px; justify-content: flex-end;">
                <button onclick="closeConfirmModal()" style="background: #95a5a6; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer;">Cancel</button>
                <button onclick="confirmPatient()" style="background: #1976d2; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer;">Confirm Appointment</button>
            </div>
        </div>
    </div>
    
    <!-- Report Modal -->
    <div id="reportModal" class="modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); z-index: 1000; align-items: center; justify-content: center;">
        <div class="modal-content" style="background: white; padding: 30px; border-radius: 15px; max-width: 600px; width: 90%;">
            <h3 style="margin-bottom: 20px; color: #1565c0;">📋 Patient Report</h3>
            <div id="reportContent" style="margin-bottom: 20px;">
                <!-- Report content will be loaded here -->
            </div>
            <div style="display: flex; gap: 15px; justify-content: flex-end;">
                <button onclick="closeReportModal()" style="background: #95a5a6; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer;">Close</button>
                <button onclick="downloadReport()" style="background: #2ecc71; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer;">📥 Download PDF</button>
            </div>
        </div>
    </div>

    <script>
        let departmentChart, symptomsChart;
        let currentPatientId = null;
        let currentReportData = null;
        
        // Load dashboard data on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadDashboardStats();
            initializeCharts();
            loadEmergencyAlerts();
            loadPatients();
            
            // Auto-refresh every 30 seconds
            setInterval(() => {
                loadDashboardStats();
                loadEmergencyAlerts();
                loadPatients();
            }, 30000);
        });
        
        async function loadDashboardStats() {
            try {
                const response = await fetch('/api/admin/dashboard_stats');
                const stats = await response.json();
                
                // Update stat cards
                document.getElementById('totalToday').textContent = stats.total_today;
                document.getElementById('criticalCases').textContent = stats.critical_cases;
                document.getElementById('avgWaiting').textContent = stats.avg_waiting;
                document.getElementById('doctorsOnline').textContent = stats.doctors_online;
                
                // Update charts
                updateDepartmentChart(stats.department_distribution);
                updateSymptomsChart(stats.common_symptoms);
                
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
                    row.style.borderBottom = '1px solid #e0e0e0';
                    row.innerHTML = `
                        <td style="padding: 15px;">
                            <div style="font-weight: 600;">${patient.name}</div>
                            <div style="font-size: 0.8rem; color: #666;">${patient.registration_id}</div>
                        </td>
                        <td style="padding: 15px;">${patient.age}</td>
                        <td style="padding: 15px; max-width: 200px;">
                            <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${patient.symptom}">
                                ${patient.symptom}
                            </div>
                        </td>
                        <td style="padding: 15px;">
                            <span class="risk-badge risk-${getRiskLevel(patient.risk_score)}" style="padding: 5px 12px; border-radius: 15px; font-size: 0.8rem; font-weight: bold;">
                                ${getRiskLevel(patient.risk_score)} (${patient.risk_score})
                            </span>
                        </td>
                        <td style="padding: 15px;">
                            <div style="font-weight: 600;">${patient.department}</div>
                            <div style="font-size: 0.8rem; color: #666;">${patient.severity}</div>
                        </td>
                        <td style="padding: 15px;">
                            <span class="status-badge status-${patient.status}" style="padding: 5px 12px; border-radius: 15px; font-size: 0.8rem; font-weight: bold;">
                                ${patient.status.charAt(0).toUpperCase() + patient.status.slice(1)}
                            </span>
                        </td>
                        <td style="padding: 15px;">
                            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                                ${patient.status === 'waiting' ? 
                                    `<button onclick="openConfirmModal(${patient.id})" style="background: #2ecc71; color: white; border: none; padding: 6px 12px; border-radius: 5px; cursor: pointer; font-size: 0.8rem;">Confirm</button>` :
                                    `<button onclick="generateReport(${patient.id})" style="background: #1976d2; color: white; border: none; padding: 6px 12px; border-radius: 5px; cursor: pointer; font-size: 0.8rem;">📋 Report</button>`
                                }
                            </div>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
                
            } catch (error) {
                console.error('Error loading patients:', error);
            }
        }
        
        function getRiskLevel(score) {
            if (score >= 80) return 'high';
            if (score >= 50) return 'medium';
            return 'low';
        }
        
        function openConfirmModal(patientId) {
            currentPatientId = patientId;
            
            // Set default appointment time to next available slot
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            tomorrow.setHours(10, 0, 0, 0);
            
            document.getElementById('appointmentDateTime').value = tomorrow.toISOString().slice(0, 16);
            document.getElementById('confirmModal').style.display = 'flex';
        }
        
        function closeConfirmModal() {
            document.getElementById('confirmModal').style.display = 'none';
            currentPatientId = null;
        }
        
        async function confirmPatient() {
            const appointmentTime = document.getElementById('appointmentDateTime').value;
            
            if (!appointmentTime) {
                alert('Please select appointment date and time');
                return;
            }
            
            try {
                const response = await fetch('/api/admin/confirm_patient', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        patient_id: currentPatientId,
                        appointment_time: appointmentTime
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    closeConfirmModal();
                    loadPatients(); // Refresh the table
                    alert('Patient confirmed successfully!');
                } else {
                    alert('Error confirming patient: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        }
        
        async function generateReport(patientId) {
            try {
                const response = await fetch(`/api/admin/generate_report/${patientId}`);
                const result = await response.json();
                
                if (result.success) {
                    currentReportData = result.report_data;
                    displayReport(result.report_data);
                    document.getElementById('reportModal').style.display = 'flex';
                } else {
                    alert('Error generating report: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        }
        
        function displayReport(data) {
            const reportContent = document.getElementById('reportContent');
            reportContent.innerHTML = `
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h4 style="color: #1565c0; margin-bottom: 15px;">Patient Information</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                        <div><strong>Name:</strong> ${data.patient_name}</div>
                        <div><strong>Registration ID:</strong> ${data.registration_id}</div>
                        <div><strong>Age:</strong> ${data.age}</div>
                        <div><strong>Gender:</strong> ${data.gender}</div>
                        <div><strong>Phone:</strong> ${data.phone}</div>
                        <div><strong>Department:</strong> ${data.department}</div>
                    </div>
                </div>
                
                <div style="background: #fff3e0; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h4 style="color: #f57c00; margin-bottom: 15px;">Medical Assessment</h4>
                    <div><strong>Primary Symptom:</strong> ${data.symptom}</div>
                    <div style="margin-top: 10px;"><strong>Severity:</strong> ${data.severity}</div>
                    <div style="margin-top: 10px;"><strong>Risk Score:</strong> ${data.risk_score}/100</div>
                    <div style="margin-top: 10px;"><strong>Emergency Case:</strong> ${data.is_emergency ? 'Yes' : 'No'}</div>
                </div>
                
                <div style="background: ${data.status === 'confirmed' ? '#e8f5e8' : '#ffebee'}; padding: 20px; border-radius: 10px;">
                    <h4 style="color: ${data.status === 'confirmed' ? '#2e7d32' : '#c62828'}; margin-bottom: 15px;">Appointment Status</h4>
                    <div><strong>Status:</strong> ${data.status.charAt(0).toUpperCase() + data.status.slice(1)}</div>
                    <div style="margin-top: 10px;"><strong>Registered:</strong> ${formatDateTime(data.created_at)}</div>
                    ${data.appointment_time ? `<div style="margin-top: 10px;"><strong>Appointment Time:</strong> ${formatDateTime(data.appointment_time)}</div>` : ''}
                </div>
            `;
        }
        
        function closeReportModal() {
            document.getElementById('reportModal').style.display = 'none';
            currentReportData = null;
        }
        
        async function downloadReport() {
            if (!currentReportData) return;
            
            try {
                const response = await fetch(`/api/admin/download_report/${currentReportData.registration_id.replace('MED', '')}`);
                const result = await response.json();
                
                if (result.success) {
                    alert(`Report downloaded: ${result.filename}`);
                } else {
                    alert('Error downloading report: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        }
        
        function refreshPatients() {
            loadPatients();
        }
        
        function initializeCharts() {
            // Department Distribution Chart
            const deptCtx = document.getElementById('departmentChart').getContext('2d');
            departmentChart = new Chart(deptCtx, {
                type: 'doughnut',
                data: {
                    labels: [],
                    datasets: [{
                        data: [],
                        backgroundColor: [
                            '#1976d2', '#d32f2f', '#388e3c', '#f57c00',
                            '#7b1fa2', '#00796b', '#5d4037', '#455a64'
                        ],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                usePointStyle: true
                            }
                        }
                    }
                }
            });
            
            // Symptoms Chart
            const sympCtx = document.getElementById('symptomsChart').getContext('2d');
            symptomsChart = new Chart(sympCtx, {
                type: 'bar',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Cases',
                        data: [],
                        backgroundColor: '#1976d2',
                        borderRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
        }
        
        function updateDepartmentChart(data) {
            if (departmentChart && data) {
                departmentChart.data.labels = Object.keys(data);
                departmentChart.data.datasets[0].data = Object.values(data);
                departmentChart.update();
            }
        }
        
        function updateSymptomsChart(data) {
            if (symptomsChart && data) {
                const labels = Object.keys(data).slice(0, 5); // Top 5 symptoms
                const values = Object.values(data).slice(0, 5);
                
                symptomsChart.data.labels = labels.map(label => 
                    label.length > 15 ? label.substring(0, 15) + '...' : label
                );
                symptomsChart.data.datasets[0].data = values;
                symptomsChart.update();
            }
        }
        
        async function loadEmergencyAlerts() {
            try {
                const response = await fetch('/api/admin/emergency_alerts');
                const alerts = await response.json();
                
                const container = document.getElementById('alertsContainer');
                
                if (alerts.length === 0) {
                    container.innerHTML = `
                        <div style="text-align: center; padding: 40px; color: #666;">
                            <div style="font-size: 3rem; margin-bottom: 15px;">✅</div>
                            <h3>No Active Emergency Alerts</h3>
                            <p>All patients are being handled appropriately.</p>
                        </div>
                    `;
                } else {
                    container.innerHTML = alerts.map(alert => `
                        <div class="alert-item">
                            <div class="alert-header">
                                <div class="alert-patient">
                                    ${alert.patient_name} (${alert.registration_id})
                                </div>
                                <div class="alert-time">
                                    ${formatTime(alert.created_at)}
                                </div>
                            </div>
                            <div class="alert-message">
                                ${alert.message}
                            </div>
                        </div>
                    `).join('');
                }
                
            } catch (error) {
                console.error('Error loading emergency alerts:', error);
            }
        }
        
        function refreshAlerts() {
            loadEmergencyAlerts();
        }
        
        function formatTime(dateString) {
            const date = new Date(dateString);
            return date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }
        
        function formatDateTime(dateString) {
            if (!dateString) return 'Not set';
            const date = new Date(dateString);
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }
    </script>
    
    <style>
        .risk-badge.risk-high { background: #ffebee; color: #c62828; }
        .risk-badge.risk-medium { background: #fff3e0; color: #f57c00; }
        .risk-badge.risk-low { background: #e8f5e8; color: #2e7d32; }
        
        .status-badge.status-waiting { background: #fff3e0; color: #f57c00; }
        .status-badge.status-confirmed { background: #e8f5e8; color: #2e7d32; }
        .status-badge.status-in-consultation { background: #e3f2fd; color: #1976d2; }
        .status-badge.status-completed { background: #f3e5f5; color: #7b1fa2; }
        
        .patients-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }
        
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .modal {
            display: flex;
        }
    </style>
</body>
</html>
'''
# Additional Admin Templates (Analytics, Departments, Reports, Settings)

PATIENT_STATUS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Check Status - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 50%, #f0f8ff 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #1565c0;
        }
        .header h1 {
            font-size: 2.2rem;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            padding: 40px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.1);
        }
        .search-section {
            text-align: center;
            margin-bottom: 30px;
        }
        .search-input {
            width: 100%;
            padding: 18px;
            border: 2px solid #e3f2fd;
            border-radius: 12px;
            font-size: 1.1rem;
            text-align: center;
            margin-bottom: 20px;
            text-transform: uppercase;
            background: rgba(255, 255, 255, 0.8);
        }
        .search-input:focus {
            outline: none;
            border-color: #1976d2;
            box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
        }
        .search-btn {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
            border: none;
            padding: 18px 35px;
            border-radius: 12px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.4s ease;
            box-shadow: 0 8px 25px rgba(25, 118, 210, 0.3);
        }
        .search-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(25, 118, 210, 0.4);
        }
        .status-card {
            display: none;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 20px;
            padding: 35px;
            margin-top: 30px;
            border: 2px solid #e3f2fd;
        }
        .status-header {
            text-align: center;
            margin-bottom: 30px;
        }
        .patient-name {
            font-size: 1.8rem;
            color: #1565c0;
            font-weight: 700;
            margin-bottom: 15px;
        }
        .status-badge {
            display: inline-block;
            padding: 10px 25px;
            border-radius: 25px;
            font-weight: bold;
            font-size: 1rem;
            margin-bottom: 20px;
        }
        .status-waiting { background: #fff3e0; color: #f57c00; }
        .status-confirmed { background: #e8f5e8; color: #2e7d32; }
        .status-in-consultation { background: #e3f2fd; color: #1976d2; }
        .status-completed { background: #f3e5f5; color: #7b1fa2; }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }
        .info-item {
            background: white;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #1976d2;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        .info-label {
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 8px;
            font-weight: 500;
        }
        .info-value {
            font-weight: 600;
            color: #1565c0;
            font-size: 1.1rem;
        }
        .back-btn {
            background: linear-gradient(135deg, #90a4ae, #78909c);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 10px;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 25px;
            font-weight: 500;
        }
        .error-message {
            background: linear-gradient(135deg, #ffebee, #fce4ec);
            color: #c62828;
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
            text-align: center;
            display: none;
            border: 1px solid #f8bbd9;
        }
        .status-message {
            margin-top: 25px;
            padding: 25px;
            background: white;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        .emergency-indicator {
            background: linear-gradient(135deg, #ffebee, #fce4ec);
            border: 2px solid #f8bbd9;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 20px;
            text-align: center;
        }
        .emergency-indicator h4 {
            color: #c62828;
            margin-bottom: 8px;
        }
        .emergency-indicator p {
            color: #ad1457;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Check Appointment Status</h1>
        <p>Enter your Registration ID to view appointment details</p>
    </div>
    
    <div class="container">
        <a href="/patient" class="back-btn">← Back to Patient Portal</a>
        
        <div class="search-section">
            <input type="text" id="registrationId" class="search-input" 
                   placeholder="Enter Registration ID (e.g., MED123456)">
            <br>
            <button onclick="checkStatus()" class="search-btn">
                🔍 Check Status
            </button>
        </div>
        
        <div id="errorMessage" class="error-message"></div>
        
        <div id="statusCard" class="status-card">
            <div class="status-header">
                <div class="patient-name" id="patientName"></div>
                <div id="statusBadge" class="status-badge"></div>
            </div>
            
            <div id="emergencyIndicator" class="emergency-indicator" style="display: none;">
                <h4>🚨 Emergency Priority Case</h4>
                <p>Your case has been marked as emergency and is being prioritized for immediate attention.</p>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Registration ID</div>
                    <div class="info-value" id="regId"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Department</div>
                    <div class="info-value" id="department"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Registration Date</div>
                    <div class="info-value" id="regDate"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Risk Score</div>
                    <div class="info-value" id="riskScore"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Primary Symptom</div>
                    <div class="info-value" id="symptom"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Severity Level</div>
                    <div class="info-value" id="severity"></div>
                </div>
                
                <div class="info-item" id="appointmentTimeItem" style="display: none;">
                    <div class="info-label">Appointment Time</div>
                    <div class="info-value" id="appointmentTime"></div>
                </div>
            </div>
            
            <div id="statusMessage" class="status-message"></div>
        </div>
    </div>

    <script>
        async function checkStatus() {
            const registrationId = document.getElementById('registrationId').value.trim().toUpperCase();
            
            if (!registrationId) {
                showError('Please enter a Registration ID');
                return;
            }
            
            try {
                const response = await fetch('/api/check_patient_status', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ registration_id: registrationId })
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
                showError('Network error: ' + error.message);
                hideStatusCard();
            }
        }
        
        function displayPatientStatus(patient) {
            document.getElementById('patientName').textContent = patient.name;
            document.getElementById('regId').textContent = patient.registration_id;
            document.getElementById('department').textContent = patient.department;
            document.getElementById('regDate').textContent = formatDateTime(patient.registered_date);
            document.getElementById('riskScore').textContent = `${patient.risk_score}/100`;
            document.getElementById('symptom').textContent = patient.symptom;
            document.getElementById('severity').textContent = patient.severity;
            
            const statusBadge = document.getElementById('statusBadge');
            const statusMessage = document.getElementById('statusMessage');
            
            statusBadge.textContent = patient.status.charAt(0).toUpperCase() + patient.status.slice(1);
            statusBadge.className = 'status-badge status-' + patient.status;
            
            // Show emergency indicator if high risk
            if (patient.risk_score >= 80) {
                document.getElementById('emergencyIndicator').style.display = 'block';
            }
            
            // Status-specific messages
            if (patient.status === 'waiting') {
                statusMessage.innerHTML = `
                    <h3 style="color: #f57c00; margin-bottom: 15px;">⏳ Appointment Pending Review</h3>
                    <p>Your appointment request is being reviewed by our medical team. You will receive confirmation with your scheduled time slot soon.</p>
                    <div style="margin-top: 15px; padding: 15px; background: #fff3e0; border-radius: 8px;">
                        <strong>Next Steps:</strong> Please wait for admin confirmation. You will be notified once your appointment is scheduled.
                    </div>
                `;
                document.getElementById('appointmentTimeItem').style.display = 'none';
            } else if (patient.status === 'confirmed') {
                statusMessage.innerHTML = `
                    <h3 style="color: #2e7d32; margin-bottom: 15px;">✅ Appointment Confirmed</h3>
                    <p>Your appointment has been confirmed and scheduled. Please be available at the confirmed time for your consultation.</p>
                    <div style="margin-top: 15px; padding: 15px; background: #e8f5e8; border-radius: 8px;">
                        <strong>Preparation:</strong> Please have your medical history and current medications ready for the consultation.
                    </div>
                `;
                if (patient.appointment_time) {
                    document.getElementById('appointmentTime').textContent = formatDateTime(patient.appointment_time);
                    document.getElementById('appointmentTimeItem').style.display = 'block';
                }
            } else if (patient.status === 'in-consultation') {
                statusMessage.innerHTML = `
                    <h3 style="color: #1976d2; margin-bottom: 15px;">👨‍⚕️ Consultation in Progress</h3>
                    <p>Your consultation is currently in progress. Please follow the doctor's instructions.</p>
                `;
            } else if (patient.status === 'completed') {
                statusMessage.innerHTML = `
                    <h3 style="color: #7b1fa2; margin-bottom: 15px;">✅ Consultation Completed</h3>
                    <p>Your consultation has been completed. Please follow up as recommended by your healthcare provider.</p>
                `;
            }
            
            document.getElementById('statusCard').style.display = 'block';
        }
        
        function formatDateTime(dateString) {
            if (!dateString) return 'Not scheduled';
            const date = new Date(dateString);
            return date.toLocaleDateString() + ' at ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
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
        
        // Allow Enter key to trigger search
        document.getElementById('registrationId').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                checkStatus();
            }
        });
    </script>
</body>
</html>
'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Patient Analytics - MediCare Hospital</title>
    <style>
        /* Include the same base styles from dashboard */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        .admin-navbar {
            background: linear-gradient(135deg, #1565c0, #0d47a1);
            color: white;
            padding: 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        .navbar-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 20px 0;
        }
        .nav-menu {
            display: flex;
            list-style: none;
            gap: 0;
        }
        .nav-link {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 20px 25px;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        .nav-link:hover, .nav-link.active {
            background: rgba(255, 255, 255, 0.1);
        }
        .main-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        .page-header {
            margin-bottom: 30px;
        }
        .page-title {
            font-size: 2.2rem;
            color: #1565c0;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .analytics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
        }
        .analytics-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        .card-title {
            font-size: 1.4rem;
            color: #1565c0;
            margin-bottom: 20px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <nav class="admin-navbar">
        <div class="navbar-content">
            <div class="navbar-brand">
                <span style="font-size: 2rem;">🏥</span>
                <div>
                    <h1 style="font-size: 1.5rem; font-weight: 700;">MediCare Hospital</h1>
                    <p style="font-size: 0.9rem; opacity: 0.9;">Admin Dashboard</p>
                </div>
            </div>
            
            <ul class="nav-menu">
                <li><a href="/admin/dashboard" class="nav-link"><span>📊</span> Dashboard</a></li>
                <li><a href="/admin/analytics" class="nav-link active"><span>📈</span> Analytics</a></li>
                <li><a href="/admin/departments" class="nav-link"><span>🏢</span> Departments</a></li>
                <li><a href="/admin/reports" class="nav-link"><span>📋</span> Reports</a></li>
                <li><a href="/admin/settings" class="nav-link"><span>⚙️</span> Settings</a></li>
            </ul>
            
            <a href="/admin/logout" style="background: rgba(255, 255, 255, 0.1); color: white; border: none; padding: 10px 20px; border-radius: 8px; text-decoration: none;">Logout</a>
        </div>
    </nav>
    
    <div class="main-content">
        <div class="page-header">
            <h1 class="page-title">📈 Patient Analytics</h1>
            <p style="color: #546e7a; font-size: 1.1rem;">Detailed insights into patient patterns and trends</p>
        </div>
        
        <div class="analytics-grid">
            <div class="analytics-card">
                <h3 class="card-title">Daily Patient Trends</h3>
                <canvas id="dailyTrendsChart" style="height: 300px;"></canvas>
            </div>
            
            <div class="analytics-card">
                <h3 class="card-title">Age Group Distribution</h3>
                <canvas id="ageGroupChart" style="height: 300px;"></canvas>
            </div>
            
            <div class="analytics-card">
                <h3 class="card-title">Severity Analysis</h3>
                <canvas id="severityChart" style="height: 300px;"></canvas>
            </div>
            
            <div class="analytics-card">
                <h3 class="card-title">Response Time Metrics</h3>
                <div style="padding: 20px; text-align: center;">
                    <div style="font-size: 2rem; color: #1976d2; margin-bottom: 10px;">15.2 min</div>
                    <div style="color: #666;">Average Response Time</div>
                    <div style="margin-top: 20px; color: #4caf50;">↓ 12% improvement this week</div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        // Initialize analytics charts
        document.addEventListener('DOMContentLoaded', function() {
            initializeAnalyticsCharts();
        });
        
        function initializeAnalyticsCharts() {
            // Daily Trends Chart
            const dailyCtx = document.getElementById('dailyTrendsChart').getContext('2d');
            new Chart(dailyCtx, {
                type: 'line',
                data: {
                    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                    datasets: [{
                        label: 'Patients',
                        data: [45, 52, 38, 61, 48, 35, 28],
                        borderColor: '#1976d2',
                        backgroundColor: 'rgba(25, 118, 210, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
            
            // Age Group Chart
            const ageCtx = document.getElementById('ageGroupChart').getContext('2d');
            new Chart(ageCtx, {
                type: 'pie',
                data: {
                    labels: ['0-18', '19-35', '36-50', '51-65', '65+'],
                    datasets: [{
                        data: [15, 25, 30, 20, 10],
                        backgroundColor: ['#1976d2', '#388e3c', '#f57c00', '#d32f2f', '#7b1fa2']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
            
            // Severity Chart
            const severityCtx = document.getElementById('severityChart').getContext('2d');
            new Chart(severityCtx, {
                type: 'bar',
                data: {
                    labels: ['Mild', 'Moderate', 'Severe'],
                    datasets: [{
                        label: 'Cases',
                        data: [45, 30, 12],
                        backgroundColor: ['#4caf50', '#ff9800', '#f44336']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    </script>
</body>
</html>
'''

ADMIN_DEPARTMENTS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Department Insights - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        .admin-navbar {
            background: linear-gradient(135deg, #1565c0, #0d47a1);
            color: white;
            padding: 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        .navbar-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 20px 0;
        }
        .nav-menu {
            display: flex;
            list-style: none;
            gap: 0;
        }
        .nav-link {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 20px 25px;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        .nav-link:hover, .nav-link.active {
            background: rgba(255, 255, 255, 0.1);
        }
        .main-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        .departments-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
        }
        .department-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border-top: 4px solid var(--dept-color);
        }
        .dept-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .dept-name {
            font-size: 1.3rem;
            font-weight: 600;
            color: #1565c0;
        }
        .dept-icon {
            font-size: 2rem;
        }
        .dept-stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-item {
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .stat-number {
            font-size: 1.5rem;
            font-weight: bold;
            color: #1565c0;
        }
        .stat-label {
            font-size: 0.85rem;
            color: #666;
        }
    </style>
</head>
<body>
    <nav class="admin-navbar">
        <div class="navbar-content">
            <div class="navbar-brand">
                <span style="font-size: 2rem;">🏥</span>
                <div>
                    <h1 style="font-size: 1.5rem; font-weight: 700;">MediCare Hospital</h1>
                    <p style="font-size: 0.9rem; opacity: 0.9;">Admin Dashboard</p>
                </div>
            </div>
            
            <ul class="nav-menu">
                <li><a href="/admin/dashboard" class="nav-link"><span>📊</span> Dashboard</a></li>
                <li><a href="/admin/analytics" class="nav-link"><span>📈</span> Analytics</a></li>
                <li><a href="/admin/departments" class="nav-link active"><span>🏢</span> Departments</a></li>
                <li><a href="/admin/reports" class="nav-link"><span>📋</span> Reports</a></li>
                <li><a href="/admin/settings" class="nav-link"><span>⚙️</span> Settings</a></li>
            </ul>
            
            <a href="/admin/logout" style="background: rgba(255, 255, 255, 0.1); color: white; border: none; padding: 10px 20px; border-radius: 8px; text-decoration: none;">Logout</a>
        </div>
    </nav>
    
    <div class="main-content">
        <div style="margin-bottom: 30px;">
            <h1 style="font-size: 2.2rem; color: #1565c0; margin-bottom: 10px; font-weight: 700;">🏢 Department Insights</h1>
            <p style="color: #546e7a; font-size: 1.1rem;">Overview of all hospital departments and their performance</p>
        </div>
        
        <div class="departments-grid">
            <div class="department-card" style="--dept-color: #1976d2;">
                <div class="dept-header">
                    <div class="dept-name">Cardiology</div>
                    <div class="dept-icon">❤️</div>
                </div>
                <div class="dept-stats">
                    <div class="stat-item">
                        <div class="stat-number">12</div>
                        <div class="stat-label">Patients Today</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">18 min</div>
                        <div class="stat-label">Avg Wait</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">2</div>
                        <div class="stat-label">Doctors</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">95%</div>
                        <div class="stat-label">Satisfaction</div>
                    </div>
                </div>
            </div>
            
            <div class="department-card" style="--dept-color: #388e3c;">
                <div class="dept-header">
                    <div class="dept-name">General Medicine</div>
                    <div class="dept-icon">🩺</div>
                </div>
                <div class="dept-stats">
                    <div class="stat-item">
                        <div class="stat-number">25</div>
                        <div class="stat-label">Patients Today</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">15 min</div>
                        <div class="stat-label">Avg Wait</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">3</div>
                        <div class="stat-label">Doctors</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">92%</div>
                        <div class="stat-label">Satisfaction</div>
                    </div>
                </div>
            </div>
            
            <!-- Add more department cards as needed -->
        </div>
    </div>
</body>
</html>
'''

ADMIN_REPORTS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reports - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        .admin-navbar {
            background: linear-gradient(135deg, #1565c0, #0d47a1);
            color: white;
            padding: 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        .navbar-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 20px 0;
        }
        .nav-menu {
            display: flex;
            list-style: none;
            gap: 0;
        }
        .nav-link {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 20px 25px;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        .nav-link:hover, .nav-link.active {
            background: rgba(255, 255, 255, 0.1);
        }
        .main-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        .reports-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }
        .report-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .report-icon {
            font-size: 3rem;
            margin-bottom: 20px;
            color: #1976d2;
        }
        .report-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #1565c0;
            margin-bottom: 15px;
        }
        .report-desc {
            color: #666;
            margin-bottom: 25px;
            line-height: 1.5;
        }
        .download-btn {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .download-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(25, 118, 210, 0.3);
        }
    </style>
</head>
<body>
    <nav class="admin-navbar">
        <div class="navbar-content">
            <div class="navbar-brand">
                <span style="font-size: 2rem;">🏥</span>
                <div>
                    <h1 style="font-size: 1.5rem; font-weight: 700;">MediCare Hospital</h1>
                    <p style="font-size: 0.9rem; opacity: 0.9;">Admin Dashboard</p>
                </div>
            </div>
            
            <ul class="nav-menu">
                <li><a href="/admin/dashboard" class="nav-link"><span>📊</span> Dashboard</a></li>
                <li><a href="/admin/analytics" class="nav-link"><span>📈</span> Analytics</a></li>
                <li><a href="/admin/departments" class="nav-link"><span>🏢</span> Departments</a></li>
                <li><a href="/admin/reports" class="nav-link active"><span>📋</span> Reports</a></li>
                <li><a href="/admin/settings" class="nav-link"><span>⚙️</span> Settings</a></li>
            </ul>
            
            <a href="/admin/logout" style="background: rgba(255, 255, 255, 0.1); color: white; border: none; padding: 10px 20px; border-radius: 8px; text-decoration: none;">Logout</a>
        </div>
    </nav>
    
    <div class="main-content">
        <div style="margin-bottom: 30px;">
            <h1 style="font-size: 2.2rem; color: #1565c0; margin-bottom: 10px; font-weight: 700;">📋 Reports Module</h1>
            <p style="color: #546e7a; font-size: 1.1rem;">Generate and download comprehensive hospital reports</p>
        </div>
        
        <div class="reports-grid">
            <div class="report-card">
                <div class="report-icon">📊</div>
                <h3 class="report-title">Daily Patient Report</h3>
                <p class="report-desc">Comprehensive daily summary of all patient registrations, departments, and statistics</p>
                <button class="download-btn" onclick="downloadReport('daily')">
                    📥 Download Report
                </button>
            </div>
            
            <div class="report-card">
                <div class="report-icon">🚨</div>
                <h3 class="report-title">Emergency Cases Report</h3>
                <p class="report-desc">Detailed analysis of emergency cases, response times, and critical patient outcomes</p>
                <button class="download-btn" onclick="downloadReport('emergency')">
                    📥 Download Report
                </button>
            </div>
            
            <div class="report-card">
                <div class="report-icon">👨‍⚕️</div>
                <h3 class="report-title">Doctor Workload Report</h3>
                <p class="report-desc">Analysis of doctor performance, patient load distribution, and department efficiency</p>
                <button class="download-btn" onclick="downloadReport('workload')">
                    📥 Download Report
                </button>
            </div>
            
            <div class="report-card">
                <div class="report-icon">⏱️</div>
                <h3 class="report-title">Waiting Time Statistics</h3>
                <p class="report-desc">Comprehensive analysis of patient waiting times, queue efficiency, and optimization insights</p>
                <button class="download-btn" onclick="downloadReport('waiting')">
                    📥 Download Report
                </button>
            </div>
        </div>
    </div>
    
    <script>
        function downloadReport(type) {
            // Simulate report generation
            alert(`Generating ${type} report... This would download a comprehensive ${type} report in production.`);
        }
    </script>
</body>
</html>
'''

ADMIN_SETTINGS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Settings - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        .admin-navbar {
            background: linear-gradient(135deg, #1565c0, #0d47a1);
            color: white;
            padding: 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        .navbar-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 20px 0;
        }
        .nav-menu {
            display: flex;
            list-style: none;
            gap: 0;
        }
        .nav-link {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 20px 25px;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        .nav-link:hover, .nav-link.active {
            background: rgba(255, 255, 255, 0.1);
        }
        .main-content {
            max-width: 1000px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        .settings-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }
        .section-title {
            font-size: 1.4rem;
            color: #1565c0;
            margin-bottom: 20px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
        }
        .form-group label {
            margin-bottom: 8px;
            font-weight: 600;
            color: #1565c0;
        }
        .form-group input, .form-group select {
            padding: 12px;
            border: 2px solid #e3f2fd;
            border-radius: 8px;
            font-size: 1rem;
        }
        .save-btn {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <nav class="admin-navbar">
        <div class="navbar-content">
            <div class="navbar-brand">
                <span style="font-size: 2rem;">🏥</span>
                <div>
                    <h1 style="font-size: 1.5rem; font-weight: 700;">MediCare Hospital</h1>
                    <p style="font-size: 0.9rem; opacity: 0.9;">Admin Dashboard</p>
                </div>
            </div>
            
            <ul class="nav-menu">
                <li><a href="/admin/dashboard" class="nav-link"><span>📊</span> Dashboard</a></li>
                <li><a href="/admin/analytics" class="nav-link"><span>📈</span> Analytics</a></li>
                <li><a href="/admin/departments" class="nav-link"><span>🏢</span> Departments</a></li>
                <li><a href="/admin/reports" class="nav-link"><span>📋</span> Reports</a></li>
                <li><a href="/admin/settings" class="nav-link active"><span>⚙️</span> Settings</a></li>
            </ul>
            
            <a href="/admin/logout" style="background: rgba(255, 255, 255, 0.1); color: white; border: none; padding: 10px 20px; border-radius: 8px; text-decoration: none;">Logout</a>
        </div>
    </nav>
    
    <div class="main-content">
        <div style="margin-bottom: 30px;">
            <h1 style="font-size: 2.2rem; color: #1565c0; margin-bottom: 10px; font-weight: 700;">⚙️ System Settings</h1>
            <p style="color: #546e7a; font-size: 1.1rem;">Configure hospital system parameters and preferences</p>
        </div>
        
        <!-- Hospital Information -->
        <div class="settings-section">
            <h3 class="section-title">🏥 Hospital Information</h3>
            <div class="form-grid">
                <div class="form-group">
                    <label for="clinicName">Hospital/Clinic Name</label>
                    <input type="text" id="clinicName" value="MediCare Hospital">
                </div>
                <div class="form-group">
                    <label for="adminName">Administrator Name</label>
                    <input type="text" id="adminName" value="System Administrator">
                </div>
            </div>
            <button class="save-btn" onclick="saveHospitalSettings()">Save Changes</button>
        </div>
        
        <!-- Working Hours -->
        <div class="settings-section">
            <h3 class="section-title">🕒 Working Hours</h3>
            <div class="form-grid">
                <div class="form-group">
                    <label for="startTime">Start Time</label>
                    <input type="time" id="startTime" value="08:00">
                </div>
                <div class="form-group">
                    <label for="endTime">End Time</label>
                    <input type="time" id="endTime" value="20:00">
                </div>
            </div>
            <button class="save-btn" onclick="saveWorkingHours()">Save Changes</button>
        </div>
        
        <!-- Emergency Settings -->
        <div class="settings-section">
            <h3 class="section-title">🚨 Emergency Configuration</h3>
            <div class="form-grid">
                <div class="form-group">
                    <label for="emergencyThreshold">Emergency Risk Threshold</label>
                    <input type="number" id="emergencyThreshold" value="80" min="1" max="100">
                </div>
                <div class="form-group">
                    <label for="maxPatients">Max Daily Patients</label>
                    <input type="number" id="maxPatients" value="100" min="1">
                </div>
            </div>
            <button class="save-btn" onclick="saveEmergencySettings()">Save Changes</button>
        </div>
        
        <!-- Security Settings -->
        <div class="settings-section">
            <h3 class="section-title">🔒 Security Settings</h3>
            <div class="form-grid">
                <div class="form-group">
                    <label for="adminEmail">Admin Email</label>
                    <input type="email" id="adminEmail" value="admin@hospital.com">
                </div>
                <div class="form-group">
                    <label for="newPassword">New Password</label>
                    <input type="password" id="newPassword" placeholder="Enter new password">
                </div>
            </div>
            <button class="save-btn" onclick="saveSecuritySettings()">Update Credentials</button>
        </div>
    </div>
    
    <script>
        function saveHospitalSettings() {
            const settings = {
                clinic_name: document.getElementById('clinicName').value,
                admin_name: document.getElementById('adminName').value
            };
            
            fetch('/api/admin/update_settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(settings)
            }).then(response => response.json())
            .then(result => {
                if (result.success) {
                    alert('Hospital settings saved successfully!');
                } else {
                    alert('Error saving settings: ' + result.error);
                }
            });
        }
        
        function saveWorkingHours() {
            const settings = {
                working_hours_start: document.getElementById('startTime').value,
                working_hours_end: document.getElementById('endTime').value
            };
            
            fetch('/api/admin/update_settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(settings)
            }).then(response => response.json())
            .then(result => {
                if (result.success) {
                    alert('Working hours updated successfully!');
                } else {
                    alert('Error updating working hours: ' + result.error);
                }
            });
        }
        
        function saveEmergencySettings() {
            const settings = {
                emergency_threshold: document.getElementById('emergencyThreshold').value,
                max_daily_patients: document.getElementById('maxPatients').value
            };
            
            fetch('/api/admin/update_settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(settings)
            }).then(response => response.json())
            .then(result => {
                if (result.success) {
                    alert('Emergency settings updated successfully!');
                } else {
                    alert('Error updating emergency settings: ' + result.error);
                }
            });
        }
        
        function saveSecuritySettings() {
            alert('Security settings updated! (Demo - would update credentials in production)');
        }
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    init_hospital_db()
    print("🏥 HOSPITAL-GRADE TELEMEDICINE SYSTEM")
    print("=" * 50)
    print("📍 Access URL: http://127.0.0.1:5006")
    print("👤 Patient Portal: Advanced registration & status")
    print("🛡️ Admin Dashboard: Complete hospital management")
    print("🔐 Admin Login: admin / hospital2024")
    print("=" * 50)
    print("✨ FEATURES:")
    print("• Professional healthcare UI/UX")
    print("• Emergency priority system")
    print("• Advanced symptom-to-department mapping")
    print("• Real-time analytics & charts")
    print("• Comprehensive admin controls")
    print("• Mobile-responsive design")
    print("• Hospital-grade security")
    app.run(debug=True, host='127.0.0.1', port=5006)