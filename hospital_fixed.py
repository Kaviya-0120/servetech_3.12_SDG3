from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for, send_file
import sqlite3
import random
import string
from datetime import datetime, timedelta
import json
import hashlib
from report_generator import ReportGenerator
from translations import get_translation, get_supported_languages
from multilingual_templates import MULTILINGUAL_PATIENT_REGISTER_TEMPLATE, MULTILINGUAL_PATIENT_STATUS_TEMPLATE

app = Flask(__name__)
app.secret_key = 'hospital_grade_secure_key_2024'

def get_user_language():
    """Get user's selected language from session or default to English"""
    return session.get('language', 'en')

def t(key, default=None):
    """Translation helper function"""
    return get_translation(get_user_language(), key, default)

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

def render_patient_template(template_string, **kwargs):
    """Render template with translation support for patient pages"""
    # Add translation function and language info to template context
    kwargs['t'] = t
    kwargs['session'] = session
    kwargs['get_supported_languages'] = get_supported_languages
    return render_template_string(template_string, **kwargs)

@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    """Set user language preference"""
    supported_languages = get_supported_languages()
    if lang_code in supported_languages:
        session['language'] = lang_code
    return redirect(request.referrer or '/')

@app.route('/')
def home():
    """Hospital landing page"""
    return render_patient_template(HOSPITAL_LANDING_TEMPLATE)

@app.route('/patient')
def patient_portal():
    """Patient portal"""
    return render_patient_template(PATIENT_PORTAL_TEMPLATE)

@app.route('/patient/register')
def patient_register():
    """Enhanced patient registration"""
    return render_patient_template(MULTILINGUAL_PATIENT_REGISTER_TEMPLATE)

@app.route('/patient/status')
def patient_status():
    """Patient status check page"""
    return render_patient_template(MULTILINGUAL_PATIENT_STATUS_TEMPLATE)

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
            'id': patient_id,  # Add patient ID for download functionality
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

@app.route('/admin/analytics')
def admin_analytics():
    """Admin analytics page"""
    if not session.get('admin_logged_in'):
        return redirect('/admin')
    return render_template_string(ADMIN_ANALYTICS_TEMPLATE)

@app.route('/admin/reports')
def admin_reports():
    """Admin reports page"""
    if not session.get('admin_logged_in'):
        return redirect('/admin')
    return render_template_string(ADMIN_REPORTS_TEMPLATE)

@app.route('/admin/settings')
def admin_settings():
    """Admin settings page"""
    if not session.get('admin_logged_in'):
        return redirect('/admin')
    return render_template_string(ADMIN_SETTINGS_TEMPLATE)

@app.route('/api/admin/analytics_data')
def get_analytics_data():
    """Get analytics data"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('hospital_system.db')
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
    
    conn = sqlite3.connect('hospital_system.db')
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
        
        conn = sqlite3.connect('hospital_system.db')
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
    
    conn = sqlite3.connect('hospital_system.db')
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

@app.route('/api/admin/download_report/<int:patient_id>')
def download_patient_report(patient_id):
    """Download patient report as PDF"""
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
        
        # Prepare patient data for report
        patient_data = {
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
        
        # Generate PDF report
        report_generator = ReportGenerator()
        pdf_buffer = report_generator.generate_patient_pdf_report(patient_data)
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'patient_report_{patient_data["registration_id"]}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/download_daily_report')
def download_daily_report():
    """Download daily report as PDF"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        conn = sqlite3.connect('hospital_system.db')
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Generate daily report data
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
        
        # Generate PDF report
        report_generator = ReportGenerator()
        pdf_buffer = report_generator.generate_daily_report_pdf(report_data)
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'daily_report_{today}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/download_patients_excel')
def download_patients_excel():
    """Download all patients data as Excel"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        conn = sqlite3.connect('hospital_system.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT registration_id, name, age, gender, phone, email, main_symptom, 
                   severity, department, risk_score, status, created_at, is_emergency, appointment_time
            FROM patients ORDER BY created_at DESC
        ''')
        
        patients = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        patients_data = []
        for p in patients:
            patients_data.append({
                'Registration ID': p[0],
                'Name': p[1],
                'Age': p[2],
                'Gender': p[3],
                'Phone': p[4],
                'Email': p[5] or '',
                'Primary Symptom': p[6],
                'Severity': p[7],
                'Department': p[8],
                'Risk Score': p[9],
                'Status': p[10],
                'Registration Date': p[11],
                'Emergency': 'Yes' if p[12] else 'No',
                'Appointment Time': p[13] or 'Not Scheduled'
            })
        
        # Generate Excel report
        report_generator = ReportGenerator()
        excel_buffer = report_generator.generate_patients_excel_report(patients_data)
        
        return send_file(
            excel_buffer,
            as_attachment=True,
            download_name=f'patients_report_{datetime.now().strftime("%Y%m%d")}.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/download_daily_excel')
def download_daily_excel():
    """Download daily report as Excel"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        conn = sqlite3.connect('hospital_system.db')
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Generate daily report data
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
        
        # Generate Excel report
        report_generator = ReportGenerator()
        excel_buffer = report_generator.generate_daily_report_excel(report_data)
        
        return send_file(
            excel_buffer,
            as_attachment=True,
            download_name=f'daily_report_{today}.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.clear()
    return redirect('/')
# ===== HOSPITAL-GRADE UI TEMPLATES =====

HOSPITAL_LANDING_TEMPLATE = '''
<!DOCTYPE html>
<html lang="{{ session.get('language', 'en') }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t('hospital_name') }} - {{ t('hospital_tagline') }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* Mobile Sidebar */
        .mobile-sidebar {
            position: fixed;
            top: 0;
            left: -280px;
            width: 280px;
            height: 100vh;
            background: white;
            z-index: 1000;
            transition: left 0.3s ease;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
            overflow-y: auto;
        }
        .mobile-sidebar.open { left: 0; }
        
        .sidebar-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 999;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }
        .sidebar-overlay.active {
            opacity: 1;
            visibility: visible;
        }
        
        .sidebar-header {
            padding: 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .sidebar-close {
            position: absolute;
            top: 15px;
            right: 15px;
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 5px;
        }
        
        .sidebar-menu {
            padding: 20px 0;
        }
        
        .sidebar-item {
            display: block;
            padding: 15px 20px;
            color: #333;
            text-decoration: none;
            border-bottom: 1px solid #f0f0f0;
            transition: background 0.3s ease;
        }
        .sidebar-item:hover { background: #f8f9fa; }
        
        .sidebar-item-icon {
            margin-right: 12px;
            font-size: 18px;
        }
        
        /* Desktop Layout */
        .desktop-container {
            display: none;
            max-width: 1200px;
            margin: 0 auto;
            min-height: 100vh;
            background: white;
            box-shadow: 0 0 50px rgba(0, 0, 0, 0.2);
        }
        
        .desktop-header {
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 40px;
            text-align: center;
            color: white;
            position: relative;
        }
        
        .desktop-content {
            padding: 60px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
            align-items: center;
        }
        
        /* Mobile App Container */
        .app-container {
            max-width: 414px;
            margin: 0 auto;
            min-height: 100vh;
            background: #ffffff;
            position: relative;
            box-shadow: 0 0 50px rgba(0, 0, 0, 0.3);
        }
        
        .status-bar {
            height: 44px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            color: white;
            font-size: 14px;
            font-weight: 600;
        }
        
        .hamburger-menu {
            background: none;
            border: none;
            color: white;
            font-size: 18px;
            cursor: pointer;
            padding: 5px;
        }
        
        .app-header {
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 20px 24px 40px;
            text-align: center;
            position: relative;
        }
        
        .language-selector {
            position: absolute;
            top: 15px;
            right: 20px;
            display: flex;
            gap: 6px;
        }
        
        .lang-btn {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 6px 10px;
            border-radius: 12px;
            text-decoration: none;
            font-size: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .lang-btn:hover, .lang-btn.active {
            background: rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.5);
        }
        
        .app-icon {
            width: 80px;
            height: 80px;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            margin: 0 auto 16px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .app-title {
            color: white;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }
        
        .app-subtitle {
            color: rgba(255, 255, 255, 0.8);
            font-size: 16px;
            font-weight: 400;
        }
        
        .app-content {
            padding: 32px 24px 100px;
            background: #f8f9fa;
            min-height: calc(100vh - 164px);
            overflow-y: auto;
        }
        
        .feature-grid {
            display: grid;
            gap: 16px;
            margin-bottom: 32px;
        }
        
        .feature-card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            text-decoration: none;
            color: inherit;
        }
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        }
        
        .feature-header {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }
        
        .feature-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            margin-right: 16px;
            flex-shrink: 0;
        }
        
        .feature-title {
            font-size: 18px;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 4px;
        }
        
        .feature-subtitle {
            font-size: 14px;
            color: #666;
            line-height: 1.4;
        }
        
        .admin-card {
            background: linear-gradient(135deg, #ff6b6b, #ee5a52);
            color: white;
        }
        .admin-card .feature-icon { background: rgba(255, 255, 255, 0.2); }
        .admin-card .feature-title,
        .admin-card .feature-subtitle { color: white; }
        .admin-card .feature-subtitle { color: rgba(255, 255, 255, 0.8); }
        
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 414px;
            background: white;
            border-top: 1px solid #e0e0e0;
            padding: 12px 0 20px;
            display: flex;
            justify-content: center;
        }
        
        .nav-indicator {
            width: 134px;
            height: 5px;
            background: #000;
            border-radius: 3px;
        }
        
        /* Responsive Design */
        @media (min-width: 768px) {
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px 20px;
            }
            .app-container { display: none; }
            .desktop-container {
                display: block;
                border-radius: 20px;
                overflow: hidden;
            }
            .desktop-header .app-icon {
                width: 120px;
                height: 120px;
                font-size: 60px;
                margin: 0 auto 24px;
            }
            .desktop-header .app-title {
                font-size: 48px;
                margin-bottom: 16px;
            }
            .desktop-header .app-subtitle { font-size: 20px; }
            .desktop-content .feature-card {
                padding: 40px;
                text-align: center;
            }
            .desktop-content .feature-header {
                flex-direction: column;
                text-align: center;
            }
            .desktop-content .feature-icon {
                width: 80px;
                height: 80px;
                font-size: 40px;
                margin: 0 auto 20px;
            }
            .desktop-content .feature-title {
                font-size: 24px;
                margin-bottom: 12px;
            }
            .desktop-content .feature-subtitle { font-size: 16px; }
        }
        
        @media (max-width: 480px) {
            .app-container {
                max-width: 100%;
                box-shadow: none;
            }
            .bottom-nav { max-width: 100%; }
            .app-content { padding: 24px 16px 100px; }
            .feature-card { padding: 20px; }
            .language-selector {
                position: static;
                justify-content: center;
                margin-bottom: 20px;
            }
        }
        
        @media (max-width: 360px) {
            .feature-header {
                flex-direction: column;
                text-align: center;
            }
            .feature-icon { margin: 0 auto 12px; }
        }
            right: 20px;
            display: flex;
            gap: 6px;
        }
        
        .lang-btn {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 6px 10px;
            border-radius: 12px;
            text-decoration: none;
            font-size: 12px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .lang-btn:hover, .lang-btn.active {
            background: rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.5);
        }
        
        .app-icon {
            width: 80px;
            height: 80px;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            margin: 0 auto 16px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .app-title {
            color: white;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }
        
        .app-subtitle {
            color: rgba(255, 255, 255, 0.8);
            font-size: 16px;
            font-weight: 400;
        }
        
        .app-content {
            padding: 32px 24px;
            background: #f8f9fa;
            min-height: calc(100vh - 164px);
        }
        
        .feature-grid {
            display: grid;
            gap: 16px;
            margin-bottom: 32px;
        }
        
        .feature-card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            text-decoration: none;
            color: inherit;
        }
        
        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        }
        
        .feature-header {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }
        
        .feature-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            margin-right: 16px;
        }
        
        .feature-title {
            font-size: 18px;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 4px;
        }
        
        .feature-subtitle {
            font-size: 14px;
            color: #666;
            line-height: 1.4;
        }
        
        .admin-card {
            background: linear-gradient(135deg, #ff6b6b, #ee5a52);
            color: white;
        }
        
        .admin-card .feature-icon {
            background: rgba(255, 255, 255, 0.2);
        }
        
        .admin-card .feature-title,
        .admin-card .feature-subtitle {
            color: white;
        }
        
        .admin-card .feature-subtitle {
            color: rgba(255, 255, 255, 0.8);
        }
        
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 414px;
            background: white;
            border-top: 1px solid #e0e0e0;
            padding: 12px 0 20px;
            display: flex;
            justify-content: center;
        }
        
        .nav-indicator {
            width: 134px;
            height: 5px;
            background: #000;
            border-radius: 3px;
        }
        
        @media (max-width: 480px) {
            .app-container {
                max-width: 100%;
                box-shadow: none;
            }
            
            .bottom-nav {
                max-width: 100%;
            }
        }
    </style>
</head>
<body>
    <!-- Mobile Sidebar -->
    <div class="mobile-sidebar" id="mobileSidebar">
        <div class="sidebar-header">
            <button class="sidebar-close" onclick="closeSidebar()">×</button>
            <div class="app-icon" style="width: 60px; height: 60px; font-size: 30px; margin: 0 auto 12px;">🏥</div>
            <h3>{{ t('hospital_name') }}</h3>
        </div>
        <div class="sidebar-menu">
            <a href="/patient" class="sidebar-item">
                <span class="sidebar-item-icon">👤</span>
                {{ t('patient_portal') }}
            </a>
            <a href="/admin" class="sidebar-item">
                <span class="sidebar-item-icon">🛡️</span>
                {{ t('admin_dashboard') }}
            </a>
            <div class="sidebar-item" style="border-bottom: none; padding-top: 20px;">
                <span class="sidebar-item-icon">🌐</span>
                Language / भाषा / மொழி
                <div style="margin-top: 10px; display: flex; gap: 8px;">
                    <a href="/set_language/en" class="lang-btn {{ 'active' if session.get('language', 'en') == 'en' else '' }}" style="background: #667eea; color: white; border: none;">EN</a>
                    <a href="/set_language/hi" class="lang-btn {{ 'active' if session.get('language') == 'hi' else '' }}" style="background: #667eea; color: white; border: none;">हिं</a>
                    <a href="/set_language/ta" class="lang-btn {{ 'active' if session.get('language') == 'ta' else '' }}" style="background: #667eea; color: white; border: none;">த</a>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Sidebar Overlay -->
    <div class="sidebar-overlay" id="sidebarOverlay" onclick="closeSidebar()"></div>
    
    <!-- Mobile App Container -->
    <div class="app-container">
        <!-- Status Bar -->
        <div class="status-bar">
            <button class="hamburger-menu" onclick="openSidebar()">☰</button>
            <span>MediCare</span>
            <span>100%</span>
        </div>
        
        <!-- App Header -->
        <div class="app-header">
            <div class="language-selector">
                <a href="/set_language/en" class="lang-btn {{ 'active' if session.get('language', 'en') == 'en' else '' }}">EN</a>
                <a href="/set_language/hi" class="lang-btn {{ 'active' if session.get('language') == 'hi' else '' }}">हिं</a>
                <a href="/set_language/ta" class="lang-btn {{ 'active' if session.get('language') == 'ta' else '' }}">த</a>
            </div>
            
            <div class="app-icon">🏥</div>
            <h1 class="app-title">{{ t('hospital_name') }}</h1>
            <p class="app-subtitle">{{ t('hospital_tagline') }}</p>
        </div>
        
        <!-- App Content -->
        <div class="app-content">
            <div class="feature-grid">
                <a href="/patient" class="feature-card">
                    <div class="feature-header">
                        <div class="feature-icon">👤</div>
                        <div>
                            <div class="feature-title">{{ t('patient_portal') }}</div>
                            <div class="feature-subtitle">{{ t('patient_portal_desc') }}</div>
                        </div>
                    </div>
                </a>
                
                <a href="/admin" class="feature-card admin-card">
                    <div class="feature-header">
                        <div class="feature-icon">🛡️</div>
                        <div>
                            <div class="feature-title">{{ t('admin_dashboard') }}</div>
                            <div class="feature-subtitle">{{ t('admin_dashboard_desc') }}</div>
                        </div>
                    </div>
                </a>
            </div>
        </div>
        
        <!-- Bottom Navigation -->
        <div class="bottom-nav">
            <div class="nav-indicator"></div>
        </div>
    </div>
    
    <!-- Desktop Container -->
    <div class="desktop-container">
        <!-- Desktop Header -->
        <div class="desktop-header">
            <div class="language-selector" style="position: absolute; top: 20px; right: 20px;">
                <a href="/set_language/en" class="lang-btn {{ 'active' if session.get('language', 'en') == 'en' else '' }}">EN</a>
                <a href="/set_language/hi" class="lang-btn {{ 'active' if session.get('language') == 'hi' else '' }}">हिं</a>
                <a href="/set_language/ta" class="lang-btn {{ 'active' if session.get('language') == 'ta' else '' }}">த</a>
            </div>
            
            <div class="app-icon">🏥</div>
            <h1 class="app-title">{{ t('hospital_name') }}</h1>
            <p class="app-subtitle">{{ t('hospital_tagline') }}</p>
        </div>
        
        <!-- Desktop Content -->
        <div class="desktop-content">
            <a href="/patient" class="feature-card">
                <div class="feature-header">
                    <div class="feature-icon">👤</div>
                    <div>
                        <div class="feature-title">{{ t('patient_portal') }}</div>
                        <div class="feature-subtitle">{{ t('patient_portal_desc') }}</div>
                    </div>
                </div>
            </a>
            
            <a href="/admin" class="feature-card admin-card">
                <div class="feature-header">
                    <div class="feature-icon">🛡️</div>
                    <div>
                        <div class="feature-title">{{ t('admin_dashboard') }}</div>
                        <div class="feature-subtitle">{{ t('admin_dashboard_desc') }}</div>
                    </div>
                </div>
            </a>
        </div>
    </div>

    <script>
        function openSidebar() {
            document.getElementById('mobileSidebar').classList.add('open');
            document.getElementById('sidebarOverlay').classList.add('active');
            document.body.style.overflow = 'hidden';
        }
        
        function closeSidebar() {
            document.getElementById('mobileSidebar').classList.remove('open');
            document.getElementById('sidebarOverlay').classList.remove('active');
            document.body.style.overflow = 'auto';
        }
        
        // Close sidebar when clicking on links
        document.querySelectorAll('.sidebar-item').forEach(item => {
            item.addEventListener('click', () => {
                if (item.getAttribute('href')) {
                    closeSidebar();
                }
            });
        });
        
        // Handle window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth >= 768) {
                closeSidebar();
            }
        });
    </script>
</body>
</html>
'''

PATIENT_PORTAL_TEMPLATE = '''
<!DOCTYPE html>
<html lang="{{ session.get('language', 'en') }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t('patient_portal_title') }} - {{ t('hospital_name') }}</title>
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
            position: relative;
            padding-top: 50px;
        }
        .language-selector {
            position: absolute;
            top: 0;
            right: 0;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        .lang-btn {
            background: rgba(25, 118, 210, 0.1);
            color: #1976d2;
            border: 2px solid #1976d2;
            padding: 6px 10px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.8rem;
            font-weight: 600;
            transition: all 0.3s ease;
            white-space: nowrap;
        }
        .lang-btn:hover, .lang-btn.active {
            background: #1976d2;
            color: white;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 25px;
            padding: 50px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.1);
        }
        .options-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
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
            transform: translateY(-8px);
            box-shadow: 0 20px 60px rgba(25, 118, 210, 0.2);
        }
        .option-icon {
            font-size: 4rem;
            margin-bottom: 20px;
            color: #1976d2;
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
        }
        
        /* Responsive Design for Mobile */
        @media (max-width: 768px) {
            .header {
                padding-top: 60px;
            }
            .language-selector {
                position: static;
                justify-content: center;
                margin-bottom: 20px;
                gap: 6px;
            }
            .lang-btn {
                font-size: 0.75rem;
                padding: 5px 8px;
            }
            .container {
                padding: 30px 20px;
            }
            .options-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
        }
        
        @media (max-width: 480px) {
            .header {
                padding-top: 40px;
            }
            .header h1 {
                font-size: 1.8rem;
            }
            .container {
                padding: 20px 15px;
            }
            .option-card {
                padding: 30px 20px;
            }
            .language-selector {
                gap: 4px;
            }
            .lang-btn {
                font-size: 0.7rem;
                padding: 4px 6px;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="language-selector">
            <a href="/set_language/en" class="lang-btn {{ 'active' if session.get('language', 'en') == 'en' else '' }}">EN</a>
            <a href="/set_language/hi" class="lang-btn {{ 'active' if session.get('language') == 'hi' else '' }}">हिं</a>
            <a href="/set_language/ta" class="lang-btn {{ 'active' if session.get('language') == 'ta' else '' }}">த</a>
        </div>
        <h1>👤 {{ t('patient_portal_title') }}</h1>
        <p>{{ t('patient_portal_welcome') }}</p>
    </div>
    
    <div class="container">
        <div class="options-grid">
            <a href="/patient/register" class="option-card">
                <div class="option-icon">📝</div>
                <div style="font-size: 1.6rem; font-weight: 600; color: #1565c0; margin-bottom: 15px;">{{ t('book_appointment') }}</div>
                <div style="color: #546e7a;">{{ t('book_appointment_desc') }}</div>
            </a>
            
            <a href="/patient/status" class="option-card">
                <div class="option-icon">🔍</div>
                <div style="font-size: 1.6rem; font-weight: 600; color: #1565c0; margin-bottom: 15px;">{{ t('check_status') }}</div>
                <div style="color: #546e7a;">{{ t('check_status_desc') }}</div>
            </a>
        </div>
        
        <a href="/" class="back-btn" style="margin-top: 30px;">
            ← {{ t('back_to_home') }}
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
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 25px;
            padding: 40px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.1);
        }
        .form-section {
            margin-bottom: 35px;
            padding: 25px;
            background: linear-gradient(135deg, #fafafa, #ffffff);
            border-radius: 15px;
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
        }
        input, select, textarea {
            padding: 15px;
            border: 2px solid #e3f2fd;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #1976d2;
            box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
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
        }
        .severity-btn.selected {
            border-color: #1976d2;
            background: linear-gradient(135deg, #e3f2fd, #ffffff);
        }
        .emergency-section {
            background: linear-gradient(135deg, #ffebee, #fce4ec);
            border: 2px solid #f8bbd9;
            border-radius: 15px;
            padding: 25px;
            margin: 25px 0;
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
        }
        .submit-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(25, 118, 210, 0.4);
        }
        .modal {
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
        }
    </style>
</head>
<body>
    <div class="container">
        <div style="text-align: center; margin-bottom: 30px; color: #1565c0;">
            <h1>📝 Book New Appointment</h1>
            <p>Please provide your details for consultation</p>
        </div>
        
        <a href="/patient" style="background: #90a4ae; color: white; border: none; padding: 12px 25px; border-radius: 10px; text-decoration: none; display: inline-block; margin-bottom: 25px;">← Back to Patient Portal</a>
        
        <form id="registrationForm">
            <!-- Personal Information -->
            <div class="form-section">
                <div style="font-size: 1.3rem; color: #1565c0; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #e3f2fd;">
                    👤 Personal Information
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
                <div style="font-size: 1.3rem; color: #1565c0; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #e3f2fd;">
                    🩺 Medical Information
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
                            <div style="font-weight: bold; color: #4caf50;">Mild</div>
                            <div style="font-size: 0.9rem; color: #666;">Manageable discomfort</div>
                        </div>
                        <div class="severity-btn moderate" onclick="selectSeverity('Moderate', this)">
                            <div style="font-weight: bold; color: #ff9800;">Moderate</div>
                            <div style="font-size: 0.9rem; color: #666;">Noticeable impact</div>
                        </div>
                        <div class="severity-btn severe" onclick="selectSeverity('Severe', this)">
                            <div style="font-weight: bold; color: #f44336;">Severe</div>
                            <div style="font-size: 0.9rem; color: #666;">Significant distress</div>
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
                <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                    <div class="emergency-switch" id="emergencySwitch" onclick="toggleEmergency()"></div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: #c62828;">🚨 This is an Emergency</div>
                </div>
                <div style="color: #ad1457; font-size: 0.9rem; line-height: 1.5;">
                    <strong>Emergency Priority:</strong> Selecting this option will prioritize your case and attempt to schedule you for immediate consultation.
                </div>
                <input type="hidden" id="is_emergency" name="is_emergency" value="false">
            </div>
            
            <button type="submit" class="submit-btn">
                📅 Book Appointment
            </button>
        </form>
    </div>
    
    <!-- Success Modal -->
    <div id="successModal" class="modal">
        <div class="modal-content">
            <div style="font-size: 5rem; color: #4caf50; margin-bottom: 25px;">✅</div>
            <h2 style="font-size: 2rem; color: #1565c0; margin-bottom: 20px;">Appointment Booked Successfully!</h2>
            
            <div style="background: linear-gradient(135deg, #e3f2fd, #ffffff); padding: 25px; border-radius: 15px; margin: 25px 0; border: 2px solid #1976d2;">
                <strong>Your Registration ID:</strong>
                <div id="registrationId" style="font-size: 2rem; font-weight: bold; color: #1976d2; margin: 15px 0;"></div>
            </div>
            
            <div id="departmentInfo" style="background: linear-gradient(135deg, #f3e5f5, #ffffff); padding: 20px; border-radius: 12px; margin: 20px 0;">
                <h3 style="color: #9c27b0; margin-bottom: 10px;">📋 Recommended Department</h3>
                <div id="departmentName" style="font-size: 1.2rem; font-weight: bold;"></div>
            </div>
            
            <div id="emergencyMessage" style="display: none; background: #ffebee; padding: 20px; border-radius: 12px; margin: 20px 0;">
                <h4 style="color: #c62828; margin-bottom: 10px;">🚨 Emergency Priority Activated</h4>
                <p style="color: #ad1457;">Your emergency request is being prioritized. You will be contacted shortly.</p>
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
        .container {
            max-width: 700px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 25px;
            padding: 40px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.1);
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
        }
        .status-card {
            display: none;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 20px;
            padding: 35px;
            margin-top: 30px;
        }
        .status-badge {
            display: inline-block;
            padding: 10px 25px;
            border-radius: 25px;
            font-weight: bold;
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
        }
        .info-item {
            background: white;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #1976d2;
        }
        .error-message {
            background: linear-gradient(135deg, #ffebee, #fce4ec);
            color: #c62828;
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
            text-align: center;
            display: none;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Check Appointment Status</h1>
        <p>Enter your Registration ID to view appointment details</p>
    </div>
    
    <div class="container">
        <a href="/patient" style="background: #90a4ae; color: white; border: none; padding: 12px 25px; border-radius: 10px; text-decoration: none; display: inline-block; margin-bottom: 25px;">← Back to Patient Portal</a>
        
        <div style="text-align: center; margin-bottom: 30px;">
            <input type="text" id="registrationId" class="search-input" 
                   placeholder="Enter Registration ID (e.g., MED123456)">
            <br>
            <button onclick="checkStatus()" class="search-btn">
                🔍 Check Status
            </button>
        </div>
        
        <div id="errorMessage" class="error-message"></div>
        
        <div id="statusCard" class="status-card">
            <div style="text-align: center; margin-bottom: 30px;">
                <div id="patientName" style="font-size: 1.8rem; color: #1565c0; font-weight: 700; margin-bottom: 15px;"></div>
                <div id="statusBadge" class="status-badge"></div>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 8px;">Registration ID</div>
                    <div id="regId" style="font-weight: 600; color: #1565c0; font-size: 1.1rem;"></div>
                </div>
                
                <div class="info-item">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 8px;">Department</div>
                    <div id="department" style="font-weight: 600; color: #1565c0; font-size: 1.1rem;"></div>
                </div>
                
                <div class="info-item">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 8px;">Risk Score</div>
                    <div id="riskScore" style="font-weight: 600; color: #1565c0; font-size: 1.1rem;"></div>
                </div>
                
                <div class="info-item">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 8px;">Severity</div>
                    <div id="severity" style="font-weight: 600; color: #1565c0; font-size: 1.1rem;"></div>
                </div>
                
                <div class="info-item" id="appointmentTimeItem" style="display: none;">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 8px;">Appointment Time</div>
                    <div id="appointmentTime" style="font-weight: 600; color: #1565c0; font-size: 1.1rem;"></div>
                </div>
            </div>
            
            <div id="statusMessage" style="margin-top: 25px; padding: 25px; background: white; border-radius: 15px; text-align: center;"></div>
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
            document.getElementById('riskScore').textContent = patient.risk_score + '/100';
            document.getElementById('severity').textContent = patient.severity;
            
            const statusBadge = document.getElementById('statusBadge');
            statusBadge.textContent = patient.status.charAt(0).toUpperCase() + patient.status.slice(1);
            statusBadge.className = 'status-badge status-' + patient.status;
            
            const statusMessage = document.getElementById('statusMessage');
            
            if (patient.status === 'waiting') {
                statusMessage.innerHTML = '<h3 style="color: #f57c00; margin-bottom: 15px;">⏳ Appointment Pending Review</h3><p>Your appointment is being reviewed by our medical team.</p>';
            } else if (patient.status === 'confirmed') {
                statusMessage.innerHTML = '<h3 style="color: #2e7d32; margin-bottom: 15px;">✅ Appointment Confirmed</h3><p>Your appointment has been scheduled.</p>';
                if (patient.appointment_time) {
                    document.getElementById('appointmentTime').textContent = formatDateTime(patient.appointment_time);
                    document.getElementById('appointmentTimeItem').style.display = 'block';
                }
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
        
        document.getElementById('registrationId').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                checkStatus();
            }
        });
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
            border-radius: 25px;
            padding: 60px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            width: 90%;
        }
        .login-header {
            text-align: center;
            margin-bottom: 40px;
        }
        .admin-icon {
            font-size: 4rem;
            color: #d32f2f;
            margin-bottom: 20px;
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
        }
        input:focus {
            outline: none;
            border-color: #d32f2f;
            box-shadow: 0 0 0 3px rgba(211, 47, 47, 0.1);
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
        }
        .login-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(211, 47, 47, 0.4);
        }
        .error-message {
            background: linear-gradient(135deg, #ffebee, #fce4ec);
            color: #c62828;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            display: none;
        }
        .demo-credentials {
            background: linear-gradient(135deg, #f3e5f5, #ffffff);
            padding: 25px;
            border-radius: 15px;
            margin-top: 30px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <a href="/" style="background: #90a4ae; color: white; border: none; padding: 10px 20px; border-radius: 8px; text-decoration: none; display: inline-block; margin-bottom: 30px;">← Back to Home</a>
        
        <div class="login-header">
            <div class="admin-icon">🛡️</div>
            <h1 style="color: #1565c0; margin-bottom: 10px; font-size: 2.2rem;">Admin Portal</h1>
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
            <h3 style="color: #1565c0; margin-bottom: 15px;">🔑 Demo Credentials</h3>
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
'''

ENHANCED_ADMIN_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="theme-color" content="#1565c0">
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
        .user-menu {
            display: flex;
            align-items: center;
            gap: 20px;
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
        
        /* Patient Management Section */
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
        .table-container {
            overflow-x: auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        }
        .patients-table {
            width: 100%;
            border-collapse: collapse;
        }
        .patients-table th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #2c3e50;
            border-bottom: 2px solid #e0e0e0;
            background: #f8f9fa;
        }
        .patients-table td {
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
        }
        .risk-badge {
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .risk-high { background: #ffebee; color: #c62828; }
        .risk-medium { background: #fff3e0; color: #f57c00; }
        .risk-low { background: #e8f5e8; color: #2e7d32; }
        .status-badge {
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .status-waiting { background: #fff3e0; color: #f57c00; }
        .status-confirmed { background: #e8f5e8; color: #2e7d32; }
        .status-in-consultation { background: #e3f2fd; color: #1976d2; }
        .status-completed { background: #f3e5f5; color: #7b1fa2; }
        
        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            max-width: 600px;
            width: 90%;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .admin-navbar {
                position: relative;
            }
            .navbar-content {
                flex-direction: column;
                gap: 10px;
                padding: 0 15px;
            }
            .navbar-brand {
                padding: 12px 0;
            }
            .brand-icon {
                font-size: 1.5rem;
            }
            .brand-text h1 {
                font-size: 1.1rem;
            }
            .brand-text p {
                font-size: 0.75rem;
                opacity: 0.8;
            }
            .nav-menu {
                flex-wrap: wrap;
                justify-content: center;
                gap: 4px;
                width: 100%;
                margin: 5px 0;
            }
            .nav-link {
                padding: 8px 12px;
                font-size: 0.8rem;
                border-radius: 6px;
                background: rgba(255, 255, 255, 0.1);
                margin: 1px;
                min-height: 36px;
            }
            .nav-link span {
                font-size: 0.9rem;
            }
            .user-menu {
                flex-direction: row;
                gap: 10px;
                text-align: center;
                width: 100%;
                justify-content: center;
                align-items: center;
                padding: 8px 0;
            }
            .user-info {
                text-align: center;
            }
            .user-name {
                font-size: 0.85rem;
            }
            .user-role {
                font-size: 0.7rem;
            }
            .logout-btn {
                padding: 6px 12px;
                font-size: 0.8rem;
                min-height: 32px;
            }
            .main-content {
                padding: 20px 15px;
            }
            .dashboard-title {
                font-size: 1.8rem;
                margin-bottom: 10px;
            }
            .dashboard-subtitle {
                font-size: 1rem;
                margin-bottom: 20px;
            }
            .stats-grid {
                grid-template-columns: 1fr;
                gap: 15px;
                margin-bottom: 25px;
            }
            .stat-card {
                padding: 20px;
                border-radius: 12px;
            }
            .stat-header {
                margin-bottom: 12px;
            }
            .stat-icon {
                font-size: 2.2rem;
            }
            .stat-number {
                font-size: 1.8rem;
                margin-bottom: 6px;
            }
            .stat-label {
                font-size: 0.9rem;
            }
            .patients-section {
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 12px;
            }
            .section-header h3 {
                font-size: 1.2rem;
            }
            .table-container {
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                border-radius: 8px;
                margin-top: 15px;
            }
            .patients-table {
                min-width: 800px;
                font-size: 0.85rem;
            }
            .patients-table th,
            .patients-table td {
                padding: 10px 8px;
                white-space: nowrap;
            }
            .patients-table th {
                font-size: 0.8rem;
                font-weight: 600;
            }
            .risk-badge,
            .status-badge {
                font-size: 0.7rem;
                padding: 3px 6px;
                border-radius: 6px;
            }
            .modal-content {
                width: 95%;
                padding: 20px;
                margin: 10px;
                border-radius: 12px;
            }
        }
        
        @media (max-width: 480px) {
            .navbar-content {
                padding: 0 10px;
            }
            .navbar-brand {
                padding: 10px 0;
                flex-direction: row;
                gap: 8px;
            }
            .brand-icon {
                font-size: 1.3rem;
            }
            .brand-text h1 {
                font-size: 1rem;
            }
            .brand-text p {
                display: none;
            }
            .nav-menu {
                gap: 2px;
                margin: 3px 0;
            }
            .nav-link {
                padding: 6px 8px;
                font-size: 0.75rem;
                min-height: 32px;
            }
            .nav-link span {
                font-size: 0.8rem;
            }
            .user-menu {
                padding: 6px 0;
                gap: 8px;
            }
            .user-name {
                font-size: 0.8rem;
            }
            .user-role {
                font-size: 0.65rem;
            }
            .logout-btn {
                padding: 5px 10px;
                font-size: 0.75rem;
                min-height: 28px;
            }
            .main-content {
                padding: 15px 10px;
            }
            .dashboard-title {
                font-size: 1.5rem;
            }
            .dashboard-subtitle {
                font-size: 0.9rem;
            }
            .stat-card {
                padding: 15px;
            }
            .stat-header {
                flex-direction: column;
                align-items: center;
                text-align: center;
                gap: 8px;
            }
            .stat-icon {
                font-size: 2rem;
            }
            .stat-number {
                font-size: 1.6rem;
            }
            .patients-section {
                padding: 15px;
            }
            .section-header {
                flex-direction: column;
                gap: 10px;
                text-align: center;
            }
            .section-header h3 {
                font-size: 1.1rem;
            }
            .patients-table {
                min-width: 700px;
            }
            .patients-table th,
            .patients-table td {
                padding: 8px 6px;
                font-size: 0.8rem;
            }
            .modal-content {
                padding: 15px;
            }
        }
        
        /* Android-specific optimizations */
        @media (max-width: 414px) {
            .navbar-brand {
                flex-direction: column;
                text-align: center;
                gap: 8px;
            }
            .brand-icon {
                font-size: 1.8rem;
            }
            .brand-text h1 {
                font-size: 1.1rem;
            }
            .brand-text p {
                font-size: 0.8rem;
            }
            .main-content {
                padding: 15px 12px;
            }
            .dashboard-header {
                margin-bottom: 20px;
            }
            .dashboard-title {
                font-size: 1.5rem;
                line-height: 1.3;
            }
            .dashboard-subtitle {
                font-size: 0.95rem;
                line-height: 1.4;
            }
            .stats-grid {
                gap: 15px;
            }
            .stat-card {
                padding: 18px;
            }
            .stat-icon {
                font-size: 2.2rem;
            }
            .stat-number {
                font-size: 1.8rem;
            }
            .stat-label {
                font-size: 0.9rem;
            }
            .patients-section {
                padding: 18px;
            }
            .section-header h3 {
                font-size: 1.1rem;
            }
        }
        
        /* Touch-friendly buttons */
        button, .btn, .nav-link, .lang-btn {
            min-height: 44px;
            touch-action: manipulation;
            -webkit-tap-highlight-color: rgba(0, 0, 0, 0.1);
        }
        
        /* Smooth scrolling for mobile */
        .table-container {
            -webkit-overflow-scrolling: touch;
            scroll-behavior: smooth;
        }
        
        /* Prevent zoom on input focus */
        input, select, textarea {
            font-size: 16px;
        }
    </style>
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
            </div>
            
            <div class="stat-card danger">
                <div class="stat-header">
                    <div class="stat-icon">🚨</div>
                </div>
                <div class="stat-number" id="criticalCases">0</div>
                <div class="stat-label">Critical Cases</div>
            </div>
            
            <div class="stat-card success">
                <div class="stat-header">
                    <div class="stat-icon">⏱️</div>
                </div>
                <div class="stat-number" id="avgWaiting">0</div>
                <div class="stat-label">Avg Wait Time (min)</div>
            </div>
            
            <div class="stat-card warning">
                <div class="stat-header">
                    <div class="stat-icon">👨‍⚕️</div>
                </div>
                <div class="stat-number" id="doctorsOnline">0</div>
                <div class="stat-label">Doctors Online</div>
            </div>
        </div>
        
        <!-- Patient Management Table -->
        <div class="patients-section">
            <div class="section-header">
                <h3 style="font-size: 1.4rem; color: #1565c0; font-weight: 600; display: flex; align-items: center; gap: 10px;">
                    <span>👥</span> Patient Management
                </h3>
                <div style="display: flex; gap: 10px;">
                    <button onclick="downloadPatientsExcel()" style="background: #2ecc71; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 8px;">
                        📥 Download Excel
                    </button>
                    <button onclick="refreshPatients()" style="background: #1976d2; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer;">
                        Refresh Patients
                    </button>
                </div>
            </div>
            <div class="table-container">
                <table class="patients-table">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Age</th>
                            <th>Symptoms</th>
                            <th>Risk Level</th>
                            <th>Department</th>
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
    </div>
    
    <!-- Confirm Patient Modal -->
    <div id="confirmModal" class="modal">
        <div class="modal-content">
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
    <div id="reportModal" class="modal">
        <div class="modal-content">
            <h3 style="margin-bottom: 20px; color: #1565c0;">📋 Patient Report</h3>
            <div id="reportContent" style="margin-bottom: 20px;">
                <!-- Report content will be loaded here -->
            </div>
            <div style="display: flex; gap: 15px; justify-content: flex-end;">
                <button onclick="closeReportModal()" style="background: #95a5a6; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer;">Close</button>
                <button onclick="downloadReportExcel()" style="background: #27ae60; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer;">📊 Download Excel</button>
                <button onclick="downloadReport()" style="background: #2ecc71; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer;">📥 Download PDF</button>
            </div>
        </div>
    </div>

    <script>
        let currentPatientId = null;
        let currentReportData = null;
        
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
                
                // Update stat cards
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
                        <td style="max-width: 200px;">
                            <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${patient.symptom}">
                                ${patient.symptom}
                            </div>
                        </td>
                        <td>
                            <span class="risk-badge risk-${getRiskLevel(patient.risk_score)}">
                                ${getRiskLevel(patient.risk_score)} (${patient.risk_score})
                            </span>
                        </td>
                        <td>
                            <div style="font-weight: 600;">${patient.department}</div>
                            <div style="font-size: 0.8rem; color: #666;">${patient.severity}</div>
                        </td>
                        <td>
                            <span class="status-badge status-${patient.status}">
                                ${patient.status.charAt(0).toUpperCase() + patient.status.slice(1)}
                            </span>
                        </td>
                        <td>
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
        
        function refreshPatients() {
            loadPatients();
        }
        
        function downloadPatientsExcel() {
            const link = document.createElement('a');
            link.href = '/api/admin/download_patients_excel';
            link.download = `patients_report_${new Date().toISOString().split('T')[0]}.xlsx`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
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
        
        function downloadReport() {
            if (currentReportData) {
                // Extract patient ID from the report data
                const patientId = currentReportData.id || currentReportData.patient_id;
                if (patientId) {
                    // Create a temporary link to trigger download
                    const downloadUrl = `/api/admin/download_report/${patientId}`;
                    const link = document.createElement('a');
                    link.href = downloadUrl;
                    link.download = `patient_report_${currentReportData.registration_id}.pdf`;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                } else {
                    alert('Unable to download report: Patient ID not found');
                }
            }
        }
        
        function downloadReportExcel() {
            if (currentReportData) {
                // Create Excel data for single patient
                const patientData = [{
                    'Registration ID': currentReportData.registration_id,
                    'Name': currentReportData.patient_name,
                    'Age': currentReportData.age,
                    'Gender': currentReportData.gender,
                    'Phone': currentReportData.phone,
                    'Primary Symptom': currentReportData.symptom,
                    'Severity': currentReportData.severity,
                    'Department': currentReportData.department,
                    'Risk Score': currentReportData.risk_score,
                    'Status': currentReportData.status,
                    'Registration Date': currentReportData.created_at,
                    'Emergency': currentReportData.is_emergency ? 'Yes' : 'No',
                    'Appointment Time': currentReportData.appointment_time || 'Not Scheduled'
                }];
                
                // For now, show alert with data (in production, would generate Excel)
                alert(`Excel report data for ${currentReportData.patient_name}:\\n\\n` + 
                      JSON.stringify(patientData[0], null, 2) + 
                      '\\n\\nIn production, this would download an Excel file.');
            }
        }
        
        function formatDateTime(dateString) {
            if (!dateString) return 'Not scheduled';
            const date = new Date(dateString);
            return date.toLocaleDateString() + ' at ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }
    </script>
</body>
</html>
'''

# ===== ADDITIONAL ADMIN TEMPLATES =====

ADMIN_ANALYTICS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics - MediCare Hospital</title>
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
        .brand-icon { font-size: 2rem; }
        .brand-text h1 { font-size: 1.5rem; font-weight: 700; }
        .brand-text p { font-size: 0.9rem; opacity: 0.9; }
        .nav-menu {
            display: flex;
            list-style: none;
            gap: 0;
        }
        .nav-item { position: relative; }
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
        .user-info { text-align: right; }
        .user-name { font-weight: 600; font-size: 1rem; }
        .user-role { font-size: 0.8rem; opacity: 0.8; }
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
        .logout-btn:hover { background: rgba(255, 255, 255, 0.2); }
        
        /* Main Content */
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
        .page-subtitle {
            color: #546e7a;
            font-size: 1.1rem;
        }
        
        /* Analytics Cards */
        .analytics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        .analytics-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        .card-header {
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }
        .card-title {
            font-size: 1.4rem;
            color: #1565c0;
            font-weight: 600;
            margin-bottom: 5px;
        }
        .card-subtitle {
            color: #546e7a;
            font-size: 0.9rem;
        }
        .chart-container {
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
        }
        .data-table th, .data-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        .data-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1565c0;
        }
        .metric-label {
            color: #546e7a;
            font-size: 0.9rem;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .navbar-content { 
                flex-direction: column; 
                gap: 15px; 
                padding: 0 15px;
            }
            .navbar-brand {
                padding: 15px 0;
            }
            .brand-text h1 {
                font-size: 1.2rem;
            }
            .nav-menu { 
                flex-wrap: wrap; 
                justify-content: center; 
                gap: 5px;
            }
            .nav-link {
                padding: 12px 15px;
                font-size: 0.9rem;
            }
            .user-menu {
                flex-direction: column;
                gap: 10px;
                text-align: center;
            }
            .main-content {
                padding: 20px 15px;
            }
            .page-title {
                font-size: 1.8rem;
            }
            .analytics-grid { 
                grid-template-columns: 1fr; 
                gap: 20px;
            }
            .analytics-card {
                padding: 20px;
            }
        }
        
        @media (max-width: 480px) {
            .nav-menu {
                flex-direction: column;
                width: 100%;
            }
            .nav-link {
                padding: 10px;
                justify-content: center;
            }
            .main-content {
                padding: 15px 10px;
            }
            .page-title {
                font-size: 1.5rem;
            }
            .analytics-card {
                padding: 15px;
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
                    <a href="/admin/dashboard" class="nav-link">
                        <span>📊</span> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/analytics" class="nav-link active">
                        <span>📈</span> Analytics
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
        <!-- Page Header -->
        <div class="page-header">
            <h1 class="page-title">📈 Analytics Dashboard</h1>
            <p class="page-subtitle">Comprehensive insights into hospital operations and patient trends</p>
        </div>
        
        <!-- Analytics Grid -->
        <div class="analytics-grid">
            <!-- Weekly Patient Trends -->
            <div class="analytics-card">
                <div class="card-header">
                    <h3 class="card-title">Weekly Patient Trends</h3>
                    <p class="card-subtitle">Patient registration trends over the last 7 days</p>
                </div>
                <div class="chart-container">
                    <canvas id="weeklyTrendsChart"></canvas>
                </div>
            </div>
            
            <!-- Risk Distribution -->
            <div class="analytics-card">
                <div class="card-header">
                    <h3 class="card-title">Risk Level Distribution</h3>
                    <p class="card-subtitle">Patient distribution by risk assessment</p>
                </div>
                <div class="chart-container">
                    <canvas id="riskDistributionChart"></canvas>
                </div>
            </div>
            
            <!-- Department Wise Patient Distribution -->
            <div class="analytics-card">
                <div class="card-header">
                    <h3 class="card-title">Department Wise Patients</h3>
                    <p class="card-subtitle">Patient distribution across different departments</p>
                    <div style="margin-top: 10px;">
                        <button onclick="toggleDepartmentChartType()" id="chartTypeBtn" style="background: #1976d2; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 0.9rem;">
                            Switch to Horizontal
                        </button>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="departmentWiseChart"></canvas>
                </div>
            </div>
            
            <!-- Department Performance -->
            <div class="analytics-card" style="grid-column: 1 / -1;">
                <div class="card-header">
                    <h3 class="card-title">Department Performance</h3>
                    <p class="card-subtitle">Detailed performance metrics by department</p>
                </div>
                <div style="overflow-x: auto;">
                    <table class="data-table" id="departmentTable">
                        <thead>
                            <tr>
                                <th>Department</th>
                                <th>Total Patients</th>
                                <th>Average Risk Score</th>
                                <th>Confirmed Appointments</th>
                                <th>Confirmation Rate</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- Data will be loaded here -->
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- Key Metrics -->
            <div class="analytics-card">
                <div class="card-header">
                    <h3 class="card-title">Key Performance Indicators</h3>
                    <p class="card-subtitle">Important metrics at a glance</p>
                </div>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
                    <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                        <div class="metric-value" id="avgResponseTime">2.3</div>
                        <div class="metric-label">Avg Response Time (hrs)</div>
                    </div>
                    <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                        <div class="metric-value" id="patientSatisfaction">4.8/5</div>
                        <div class="metric-label">Patient Satisfaction</div>
                    </div>
                    <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                        <div class="metric-value" id="emergencyResponseRate">98%</div>
                        <div class="metric-label">Emergency Response Rate</div>
                    </div>
                    <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                        <div class="metric-value" id="systemUptime">99.9%</div>
                        <div class="metric-label">System Uptime</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let weeklyChart, riskChart, departmentChart;
        let departmentData = [];
        let isHorizontalChart = false;
        
        document.addEventListener('DOMContentLoaded', function() {
            loadAnalyticsData();
        });
        
        async function loadAnalyticsData() {
            try {
                const response = await fetch('/api/admin/analytics_data');
                const data = await response.json();
                
                // Store department data for chart toggling
                departmentData = data.department_performance;
                
                // Update charts
                updateWeeklyTrendsChart(data.weekly_trends);
                updateRiskDistributionChart(data.risk_distribution);
                updateDepartmentWiseChart(data.department_performance);
                updateDepartmentTable(data.department_performance);
                
            } catch (error) {
                console.error('Error loading analytics data:', error);
            }
        }
        
        function toggleDepartmentChartType() {
            isHorizontalChart = !isHorizontalChart;
            updateDepartmentWiseChart(departmentData);
            
            const btn = document.getElementById('chartTypeBtn');
            btn.textContent = isHorizontalChart ? 'Switch to Vertical' : 'Switch to Horizontal';
        }
        
        function updateWeeklyTrendsChart(data) {
            const ctx = document.getElementById('weeklyTrendsChart').getContext('2d');
            
            if (weeklyChart) weeklyChart.destroy();
            
            weeklyChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.map(d => new Date(d.date).toLocaleDateString()),
                    datasets: [{
                        label: 'Patients',
                        data: data.map(d => d.count),
                        borderColor: '#1976d2',
                        backgroundColor: 'rgba(25, 118, 210, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }
        
        function updateRiskDistributionChart(data) {
            const ctx = document.getElementById('riskDistributionChart').getContext('2d');
            
            if (riskChart) riskChart.destroy();
            
            riskChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.map(d => d.level),
                    datasets: [{
                        data: data.map(d => d.count),
                        backgroundColor: ['#f44336', '#ff9800', '#4caf50'],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
        
        function updateDepartmentWiseChart(data) {
            const ctx = document.getElementById('departmentWiseChart').getContext('2d');
            
            if (departmentChart) departmentChart.destroy();
            
            // Define colors for different departments
            const departmentColors = {
                'Cardiology': '#e74c3c',
                'General Medicine': '#3498db',
                'Emergency': '#e67e22',
                'Pulmonology': '#9b59b6',
                'Dermatology': '#2ecc71',
                'Orthopedics': '#f39c12',
                'Neurology': '#1abc9c',
                'Pediatrics': '#34495e'
            };
            
            const backgroundColors = data.map(dept => 
                departmentColors[dept.department] || '#95a5a6'
            );
            
            // Sort data by total patients for better visualization
            const sortedData = [...data].sort((a, b) => b.total - a.total);
            const sortedColors = sortedData.map(dept => 
                departmentColors[dept.department] || '#95a5a6'
            );
            
            departmentChart = new Chart(ctx, {
                type: isHorizontalChart ? 'bar' : 'bar',
                data: {
                    labels: sortedData.map(d => d.department),
                    datasets: [{
                        label: 'Total Patients',
                        data: sortedData.map(d => d.total),
                        backgroundColor: sortedColors,
                        borderColor: sortedColors.map(color => color),
                        borderWidth: 2,
                        borderRadius: 8,
                        borderSkipped: false,
                    }]
                },
                options: {
                    indexAxis: isHorizontalChart ? 'y' : 'x',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { 
                            display: false 
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleColor: 'white',
                            bodyColor: 'white',
                            borderColor: '#1976d2',
                            borderWidth: 1,
                            callbacks: {
                                title: function(context) {
                                    return context[0].label + ' Department';
                                },
                                label: function(context) {
                                    return `Total Patients: ${context.parsed.y || context.parsed.x}`;
                                },
                                afterLabel: function(context) {
                                    const dept = sortedData[context.dataIndex];
                                    const confirmationRate = dept.total > 0 ? ((dept.confirmed / dept.total) * 100).toFixed(1) : '0.0';
                                    return [
                                        `Confirmed: ${dept.confirmed}`,
                                        `Average Risk: ${dept.avg_risk}`,
                                        `Confirmation Rate: ${confirmationRate}%`
                                    ];
                                }
                            }
                        }
                    },
                    scales: {
                        [isHorizontalChart ? 'x' : 'y']: { 
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Number of Patients',
                                font: {
                                    size: 12,
                                    weight: 'bold'
                                }
                            },
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            }
                        },
                        [isHorizontalChart ? 'y' : 'x']: {
                            title: {
                                display: true,
                                text: 'Departments',
                                font: {
                                    size: 12,
                                    weight: 'bold'
                                }
                            },
                            grid: {
                                display: false
                            }
                        }
                    },
                    animation: {
                        duration: 1000,
                        easing: 'easeInOutQuart'
                    },
                    onHover: (event, activeElements) => {
                        event.native.target.style.cursor = activeElements.length > 0 ? 'pointer' : 'default';
                    }
                }
            });
        }
        
        function updateDepartmentTable(data) {
            const tbody = document.querySelector('#departmentTable tbody');
            tbody.innerHTML = '';
            
            data.forEach(dept => {
                const confirmationRate = dept.total > 0 ? ((dept.confirmed / dept.total) * 100).toFixed(1) : '0.0';
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td style="font-weight: 600;">${dept.department}</td>
                    <td>${dept.total}</td>
                    <td>${dept.avg_risk}</td>
                    <td>${dept.confirmed}</td>
                    <td>${confirmationRate}%</td>
                `;
                tbody.appendChild(row);
            });
        }
    </script>
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
        .brand-icon { font-size: 2rem; }
        .brand-text h1 { font-size: 1.5rem; font-weight: 700; }
        .brand-text p { font-size: 0.9rem; opacity: 0.9; }
        .nav-menu {
            display: flex;
            list-style: none;
            gap: 0;
        }
        .nav-item { position: relative; }
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
        .user-info { text-align: right; }
        .user-name { font-weight: 600; font-size: 1rem; }
        .user-role { font-size: 0.8rem; opacity: 0.8; }
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
        .logout-btn:hover { background: rgba(255, 255, 255, 0.2); }
        
        /* Main Content */
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
        .page-subtitle {
            color: #546e7a;
            font-size: 1.1rem;
        }
        
        /* Reports Grid */
        .reports-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        .report-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .report-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }
        .report-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }
        .report-icon {
            font-size: 2.5rem;
            color: #1976d2;
        }
        .report-title {
            font-size: 1.3rem;
            color: #1565c0;
            font-weight: 600;
        }
        .report-description {
            color: #546e7a;
            margin-bottom: 25px;
            line-height: 1.5;
        }
        .report-actions {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(25, 118, 210, 0.3);
        }
        .btn-secondary {
            background: #f8f9fa;
            color: #546e7a;
            border: 2px solid #e0e0e0;
        }
        .btn-secondary:hover {
            background: #e9ecef;
            border-color: #1976d2;
        }
        
        /* Report Generation Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        .modal-content {
            background: white;
            padding: 40px;
            border-radius: 20px;
            max-width: 600px;
            width: 90%;
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
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #1976d2;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .navbar-content { 
                flex-direction: column; 
                gap: 15px; 
                padding: 0 15px;
            }
            .navbar-brand {
                padding: 15px 0;
            }
            .brand-text h1 {
                font-size: 1.2rem;
            }
            .nav-menu { 
                flex-wrap: wrap; 
                justify-content: center; 
                gap: 5px;
            }
            .nav-link {
                padding: 12px 15px;
                font-size: 0.9rem;
            }
            .user-menu {
                flex-direction: column;
                gap: 10px;
                text-align: center;
            }
            .main-content {
                padding: 20px 15px;
            }
            .page-title {
                font-size: 1.8rem;
            }
            .reports-grid { 
                grid-template-columns: 1fr; 
                gap: 20px;
            }
            .report-card {
                padding: 20px;
            }
        }
        
        @media (max-width: 480px) {
            .nav-menu {
                flex-direction: column;
                width: 100%;
            }
            .nav-link {
                padding: 10px;
                justify-content: center;
            }
            .main-content {
                padding: 15px 10px;
            }
            .page-title {
                font-size: 1.5rem;
            }
            .report-card {
                padding: 15px;
            }
            .report-header {
                flex-direction: column;
                text-align: center;
                gap: 15px;
            }
            .report-icon {
                font-size: 2rem;
            }
        }
    </style>
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
                    <a href="/admin/dashboard" class="nav-link">
                        <span>📊</span> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/analytics" class="nav-link">
                        <span>📈</span> Analytics
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/reports" class="nav-link active">
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
        <!-- Page Header -->
        <div class="page-header">
            <h1 class="page-title">📋 Reports Center</h1>
            <p class="page-subtitle">Generate and download comprehensive hospital reports</p>
        </div>
        
        <!-- Reports Grid -->
        <div class="reports-grid">
            <!-- Daily Report -->
            <div class="report-card">
                <div class="report-header">
                    <div class="report-icon">📅</div>
                    <div class="report-title">Daily Operations Report</div>
                </div>
                <div class="report-description">
                    Comprehensive daily summary including patient registrations, department performance, and key metrics for today's operations.
                </div>
                <div class="report-actions">
                    <button onclick="generateDailyReport()" class="btn btn-primary">
                        <span>📥</span> Generate Report
                    </button>
                    <button onclick="scheduleDailyReport()" class="btn btn-secondary">
                        <span>⏰</span> Schedule
                    </button>
                </div>
            </div>
            
            <!-- Weekly Report -->
            <div class="report-card">
                <div class="report-header">
                    <div class="report-icon">📊</div>
                    <div class="report-title">Weekly Performance Report</div>
                </div>
                <div class="report-description">
                    Weekly analysis of patient trends, department efficiency, emergency response times, and overall hospital performance metrics.
                </div>
                <div class="report-actions">
                    <button onclick="openCustomReportModal('weekly')" class="btn btn-primary">
                        <span>📥</span> Generate Report
                    </button>
                    <button class="btn btn-secondary">
                        <span>📧</span> Email Report
                    </button>
                </div>
            </div>
            
            <!-- Patient Demographics -->
            <div class="report-card">
                <div class="report-header">
                    <div class="report-icon">👥</div>
                    <div class="report-title">Patient Demographics Report</div>
                </div>
                <div class="report-description">
                    Detailed breakdown of patient demographics, age groups, risk distributions, and geographic analysis for strategic planning.
                </div>
                <div class="report-actions">
                    <button onclick="openCustomReportModal('demographics')" class="btn btn-primary">
                        <span>📥</span> Generate Report
                    </button>
                    <button class="btn btn-secondary">
                        <span>📈</span> View Trends
                    </button>
                </div>
            </div>
            
            <!-- Emergency Response -->
            <div class="report-card">
                <div class="report-header">
                    <div class="report-icon">🚨</div>
                    <div class="report-title">Emergency Response Report</div>
                </div>
                <div class="report-description">
                    Analysis of emergency cases, response times, critical patient outcomes, and emergency department efficiency metrics.
                </div>
                <div class="report-actions">
                    <button onclick="openCustomReportModal('emergency')" class="btn btn-primary">
                        <span>📥</span> Generate Report
                    </button>
                    <button class="btn btn-secondary">
                        <span>⚡</span> Real-time View
                    </button>
                </div>
            </div>
            
            <!-- Department Analysis -->
            <div class="report-card">
                <div class="report-header">
                    <div class="report-icon">🏢</div>
                    <div class="report-title">Department Analysis Report</div>
                </div>
                <div class="report-description">
                    Comprehensive analysis of each department's performance, patient load, confirmation rates, and resource utilization.
                </div>
                <div class="report-actions">
                    <button onclick="openCustomReportModal('department')" class="btn btn-primary">
                        <span>📥</span> Generate Report
                    </button>
                    <button class="btn btn-secondary">
                        <span>🔍</span> Compare Depts
                    </button>
                </div>
            </div>
            
            <!-- Custom Report -->
            <div class="report-card">
                <div class="report-header">
                    <div class="report-icon">⚙️</div>
                    <div class="report-title">Custom Report Builder</div>
                </div>
                <div class="report-description">
                    Create custom reports with specific date ranges, departments, metrics, and filters tailored to your specific needs.
                </div>
                <div class="report-actions">
                    <button onclick="openCustomReportModal('custom')" class="btn btn-primary">
                        <span>🛠️</span> Build Report
                    </button>
                    <button class="btn btn-secondary">
                        <span>💾</span> Saved Templates
                    </button>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Custom Report Modal -->
    <div id="customReportModal" class="modal">
        <div class="modal-content">
            <h3 style="margin-bottom: 25px; color: #1565c0; display: flex; align-items: center; gap: 10px;">
                <span>📋</span> <span id="modalTitle">Generate Custom Report</span>
            </h3>
            
            <div class="form-group">
                <label for="reportType">Report Type</label>
                <select id="reportType">
                    <option value="daily">Daily Operations</option>
                    <option value="weekly">Weekly Performance</option>
                    <option value="demographics">Patient Demographics</option>
                    <option value="emergency">Emergency Response</option>
                    <option value="department">Department Analysis</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="dateFrom">From Date</label>
                <input type="date" id="dateFrom">
            </div>
            
            <div class="form-group">
                <label for="dateTo">To Date</label>
                <input type="date" id="dateTo">
            </div>
            
            <div class="form-group">
                <label for="reportFormat">Format</label>
                <select id="reportFormat">
                    <option value="pdf">PDF Document</option>
                    <option value="excel">Excel Spreadsheet</option>
                    <option value="json">JSON Data</option>
                </select>
            </div>
            
            <div style="display: flex; gap: 15px; justify-content: flex-end; margin-top: 30px;">
                <button onclick="closeCustomReportModal()" class="btn btn-secondary">Cancel</button>
                <button onclick="generateCustomReport()" class="btn btn-primary">
                    <span>📥</span> Generate Report
                </button>
            </div>
        </div>
    </div>

    <script>
        let currentReportType = '';
        
        async function generateDailyReport() {
            try {
                const response = await fetch('/api/admin/generate_daily_report');
                const result = await response.json();
                
                if (result.success) {
                    // Show options for PDF and Excel download
                    const downloadChoice = confirm(`Daily report generated successfully!\\n\\nReport includes:\\n- Total patients: ${result.report_data.total_patients}\\n- High-risk cases: ${result.report_data.high_risk_patients}\\n- Confirmed appointments: ${result.report_data.confirmed_appointments}\\n\\nClick OK to download PDF, Cancel to download Excel`);
                    
                    if (downloadChoice) {
                        // Download PDF
                        const link = document.createElement('a');
                        link.href = '/api/admin/download_daily_report';
                        link.download = `daily_report_${result.report_data.date}.pdf`;
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                    } else {
                        // Download Excel
                        const link = document.createElement('a');
                        link.href = '/api/admin/download_daily_excel';
                        link.download = `daily_report_${result.report_data.date}.xlsx`;
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                    }
                } else {
                    alert('Error generating report: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        }
        
        function openCustomReportModal(reportType) {
            currentReportType = reportType;
            
            const titles = {
                'weekly': 'Generate Weekly Report',
                'demographics': 'Generate Demographics Report',
                'emergency': 'Generate Emergency Report',
                'department': 'Generate Department Report',
                'custom': 'Build Custom Report'
            };
            
            document.getElementById('modalTitle').textContent = titles[reportType] || 'Generate Report';
            document.getElementById('reportType').value = reportType === 'custom' ? 'daily' : reportType;
            
            // Set default dates
            const today = new Date();
            const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
            
            document.getElementById('dateFrom').value = weekAgo.toISOString().split('T')[0];
            document.getElementById('dateTo').value = today.toISOString().split('T')[0];
            
            document.getElementById('customReportModal').style.display = 'flex';
        }
        
        function closeCustomReportModal() {
            document.getElementById('customReportModal').style.display = 'none';
            currentReportType = '';
        }
        
        function generateCustomReport() {
            const reportType = document.getElementById('reportType').value;
            const dateFrom = document.getElementById('dateFrom').value;
            const dateTo = document.getElementById('dateTo').value;
            const format = document.getElementById('reportFormat').value;
            
            if (!dateFrom || !dateTo) {
                alert('Please select both from and to dates');
                return;
            }
            
            // Simulate report generation
            const reportData = {
                type: reportType,
                dateRange: `${dateFrom} to ${dateTo}`,
                format: format,
                generatedAt: new Date().toISOString()
            };
            
            alert(`Custom report generated successfully!\\n\\nType: ${reportType}\\nDate Range: ${dateFrom} to ${dateTo}\\nFormat: ${format.toUpperCase()}\\n\\nIn production, this would download the actual ${format.toUpperCase()} file.`);
            
            closeCustomReportModal();
        }
        
        function scheduleDailyReport() {
            alert('Daily report scheduling would be implemented in production.\\n\\nFeatures would include:\\n- Email delivery schedule\\n- Automatic generation times\\n- Recipient management\\n- Report customization');
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
        .brand-icon { font-size: 2rem; }
        .brand-text h1 { font-size: 1.5rem; font-weight: 700; }
        .brand-text p { font-size: 0.9rem; opacity: 0.9; }
        .nav-menu {
            display: flex;
            list-style: none;
            gap: 0;
        }
        .nav-item { position: relative; }
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
        .user-info { text-align: right; }
        .user-name { font-weight: 600; font-size: 1rem; }
        .user-role { font-size: 0.8rem; opacity: 0.8; }
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
        .logout-btn:hover { background: rgba(255, 255, 255, 0.2); }
        
        /* Main Content */
        .main-content {
            max-width: 1200px;
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
        .page-subtitle {
            color: #546e7a;
            font-size: 1.1rem;
        }
        
        /* Settings Sections */
        .settings-container {
            display: grid;
            grid-template-columns: 1fr;
            gap: 30px;
        }
        .settings-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        .section-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }
        .section-icon {
            font-size: 2rem;
            color: #1976d2;
        }
        .section-title {
            font-size: 1.4rem;
            color: #1565c0;
            font-weight: 600;
        }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
        }
        .form-group.full-width {
            grid-column: 1 / -1;
        }
        .form-group label {
            margin-bottom: 8px;
            font-weight: 600;
            color: #1565c0;
        }
        .form-group input, .form-group select, .form-group textarea {
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
        .btn {
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(25, 118, 210, 0.3);
        }
        .btn-secondary {
            background: #f8f9fa;
            color: #546e7a;
            border: 2px solid #e0e0e0;
        }
        .btn-secondary:hover {
            background: #e9ecef;
            border-color: #1976d2;
        }
        .btn-danger {
            background: linear-gradient(135deg, #d32f2f, #c62828);
            color: white;
        }
        .btn-danger:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(211, 47, 47, 0.3);
        }
        .section-actions {
            display: flex;
            gap: 15px;
            justify-content: flex-end;
            margin-top: 25px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }
        .success-message {
            background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
            color: #2e7d32;
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: none;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .navbar-content { 
                flex-direction: column; 
                gap: 15px; 
                padding: 0 15px;
            }
            .navbar-brand {
                padding: 15px 0;
            }
            .brand-text h1 {
                font-size: 1.2rem;
            }
            .nav-menu { 
                flex-wrap: wrap; 
                justify-content: center; 
                gap: 5px;
            }
            .nav-link {
                padding: 12px 15px;
                font-size: 0.9rem;
            }
            .user-menu {
                flex-direction: column;
                gap: 10px;
                text-align: center;
            }
            .main-content {
                padding: 20px 15px;
            }
            .page-title {
                font-size: 1.8rem;
            }
            .settings-section {
                padding: 20px;
            }
            .form-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
        }
        
        @media (max-width: 480px) {
            .nav-menu {
                flex-direction: column;
                width: 100%;
            }
            .nav-link {
                padding: 10px;
                justify-content: center;
            }
            .main-content {
                padding: 15px 10px;
            }
            .page-title {
                font-size: 1.5rem;
            }
            .settings-section {
                padding: 15px;
            }
            .section-header {
                flex-direction: column;
                text-align: center;
                gap: 15px;
            }
            .section-icon {
                font-size: 1.5rem;
            }
            .section-actions { 
                flex-direction: column; 
                gap: 10px;
            }
            .form-group input, 
            .form-group select {
                padding: 12px;
                font-size: 0.9rem;
            }
        }
    </style>
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
                    <a href="/admin/dashboard" class="nav-link">
                        <span>📊</span> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/analytics" class="nav-link">
                        <span>📈</span> Analytics
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/reports" class="nav-link">
                        <span>📋</span> Reports
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/settings" class="nav-link active">
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
        <!-- Page Header -->
        <div class="page-header">
            <h1 class="page-title">⚙️ System Settings</h1>
            <p class="page-subtitle">Configure hospital system preferences and administrative settings</p>
        </div>
        
        <div id="successMessage" class="success-message">
            <strong>✅ Settings updated successfully!</strong>
        </div>
        
        <!-- Settings Container -->
        <div class="settings-container">
            <!-- Admin Profile Settings -->
            <div class="settings-section">
                <div class="section-header">
                    <div class="section-icon">👤</div>
                    <div class="section-title">Admin Profile Settings</div>
                </div>
                
                <form id="profileForm">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="adminName">Full Name</label>
                            <input type="text" id="adminName" name="adminName" placeholder="Enter your full name">
                        </div>
                        
                        <div class="form-group">
                            <label for="adminEmail">Email Address</label>
                            <input type="email" id="adminEmail" name="adminEmail" placeholder="Enter your email" readonly>
                        </div>
                        
                        <div class="form-group">
                            <label for="currentPassword">Current Password</label>
                            <input type="password" id="currentPassword" name="currentPassword" placeholder="Enter current password">
                        </div>
                        
                        <div class="form-group">
                            <label for="newPassword">New Password</label>
                            <input type="password" id="newPassword" name="newPassword" placeholder="Enter new password (optional)">
                        </div>
                    </div>
                    
                    <div class="section-actions">
                        <button type="button" onclick="resetProfileForm()" class="btn btn-secondary">
                            <span>↺</span> Reset
                        </button>
                        <button type="submit" class="btn btn-primary">
                            <span>💾</span> Save Profile
                        </button>
                    </div>
                </form>
            </div>
            
            <!-- Hospital Settings -->
            <div class="settings-section">
                <div class="section-header">
                    <div class="section-icon">🏥</div>
                    <div class="section-title">Hospital Configuration</div>
                </div>
                
                <form id="hospitalForm">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="clinicName">Hospital/Clinic Name</label>
                            <input type="text" id="clinicName" name="clinicName" placeholder="Enter hospital name">
                        </div>
                        
                        <div class="form-group">
                            <label for="workingHoursStart">Working Hours Start</label>
                            <input type="time" id="workingHoursStart" name="workingHoursStart">
                        </div>
                        
                        <div class="form-group">
                            <label for="workingHoursEnd">Working Hours End</label>
                            <input type="time" id="workingHoursEnd" name="workingHoursEnd">
                        </div>
                        
                        <div class="form-group">
                            <label for="emergencyThreshold">Emergency Risk Threshold</label>
                            <input type="number" id="emergencyThreshold" name="emergencyThreshold" min="50" max="100" placeholder="80">
                        </div>
                        
                        <div class="form-group full-width">
                            <label for="hospitalAddress">Hospital Address</label>
                            <textarea id="hospitalAddress" name="hospitalAddress" rows="3" placeholder="Enter complete hospital address"></textarea>
                        </div>
                    </div>
                    
                    <div class="section-actions">
                        <button type="button" onclick="resetHospitalForm()" class="btn btn-secondary">
                            <span>↺</span> Reset
                        </button>
                        <button type="submit" class="btn btn-primary">
                            <span>💾</span> Save Settings
                        </button>
                    </div>
                </form>
            </div>
            
            <!-- System Preferences -->
            <div class="settings-section">
                <div class="section-header">
                    <div class="section-icon">🔧</div>
                    <div class="section-title">System Preferences</div>
                </div>
                
                <form id="systemForm">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="autoRefreshInterval">Dashboard Auto-Refresh (seconds)</label>
                            <select id="autoRefreshInterval" name="autoRefreshInterval">
                                <option value="30">30 seconds</option>
                                <option value="60">1 minute</option>
                                <option value="300">5 minutes</option>
                                <option value="0">Disabled</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="defaultLanguage">Default Language</label>
                            <select id="defaultLanguage" name="defaultLanguage">
                                <option value="en">English</option>
                                <option value="es">Spanish</option>
                                <option value="fr">French</option>
                                <option value="de">German</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="timezone">Timezone</label>
                            <select id="timezone" name="timezone">
                                <option value="UTC">UTC</option>
                                <option value="America/New_York">Eastern Time</option>
                                <option value="America/Chicago">Central Time</option>
                                <option value="America/Denver">Mountain Time</option>
                                <option value="America/Los_Angeles">Pacific Time</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="maxPatientsPerDay">Max Patients Per Day</label>
                            <input type="number" id="maxPatientsPerDay" name="maxPatientsPerDay" min="50" max="500" placeholder="100">
                        </div>
                    </div>
                    
                    <div class="section-actions">
                        <button type="button" onclick="resetSystemForm()" class="btn btn-secondary">
                            <span>↺</span> Reset
                        </button>
                        <button type="submit" class="btn btn-primary">
                            <span>💾</span> Save Preferences
                        </button>
                    </div>
                </form>
            </div>
            
            <!-- Notification Settings -->
            <div class="settings-section">
                <div class="section-header">
                    <div class="section-icon">🔔</div>
                    <div class="section-title">Notification Settings</div>
                </div>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label>
                            <input type="checkbox" id="emailNotifications" checked style="margin-right: 10px;">
                            Email Notifications
                        </label>
                        <small style="color: #666; margin-top: 5px;">Receive email alerts for critical events</small>
                    </div>
                    
                    <div class="form-group">
                        <label>
                            <input type="checkbox" id="emergencyAlerts" checked style="margin-right: 10px;">
                            Emergency Alerts
                        </label>
                        <small style="color: #666; margin-top: 5px;">Immediate notifications for emergency cases</small>
                    </div>
                    
                    <div class="form-group">
                        <label>
                            <input type="checkbox" id="dailyReports" style="margin-right: 10px;">
                            Daily Report Emails
                        </label>
                        <small style="color: #666; margin-top: 5px;">Automated daily summary reports</small>
                    </div>
                    
                    <div class="form-group">
                        <label>
                            <input type="checkbox" id="systemMaintenance" checked style="margin-right: 10px;">
                            System Maintenance Alerts
                        </label>
                        <small style="color: #666; margin-top: 5px;">Notifications about system updates</small>
                    </div>
                </div>
                
                <div class="section-actions">
                    <button type="button" onclick="saveNotificationSettings()" class="btn btn-primary">
                        <span>💾</span> Save Notifications
                    </button>
                </div>
            </div>
            
            <!-- Danger Zone -->
            <div class="settings-section" style="border: 2px solid #ffcdd2;">
                <div class="section-header">
                    <div class="section-icon" style="color: #d32f2f;">⚠️</div>
                    <div class="section-title" style="color: #d32f2f;">Danger Zone</div>
                </div>
                
                <div style="background: #ffebee; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h4 style="color: #c62828; margin-bottom: 10px;">⚠️ Warning</h4>
                    <p style="color: #ad1457;">These actions are irreversible and can cause data loss. Please proceed with extreme caution.</p>
                </div>
                
                <div class="section-actions">
                    <button type="button" onclick="exportData()" class="btn btn-secondary">
                        <span>📤</span> Export All Data
                    </button>
                    <button type="button" onclick="resetSystem()" class="btn btn-danger">
                        <span>🔄</span> Reset System
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            loadCurrentSettings();
        });
        
        async function loadCurrentSettings() {
            try {
                const response = await fetch('/api/admin/get_settings');
                const settings = await response.json();
                
                // Populate form fields
                document.getElementById('adminName').value = settings.admin_name || '';
                document.getElementById('adminEmail').value = settings.admin_email || '';
                document.getElementById('clinicName').value = settings.clinic_name || '';
                document.getElementById('workingHoursStart').value = settings.working_hours_start || '';
                document.getElementById('workingHoursEnd').value = settings.working_hours_end || '';
                document.getElementById('emergencyThreshold').value = settings.emergency_threshold || '';
                
            } catch (error) {
                console.error('Error loading settings:', error);
            }
        }
        
        document.getElementById('profileForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            await saveSettings('profile');
        });
        
        document.getElementById('hospitalForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            await saveSettings('hospital');
        });
        
        document.getElementById('systemForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            await saveSettings('system');
        });
        
        async function saveSettings(type) {
            const formData = {};
            
            if (type === 'profile') {
                formData.admin_name = document.getElementById('adminName').value;
            } else if (type === 'hospital') {
                formData.clinic_name = document.getElementById('clinicName').value;
                formData.working_hours_start = document.getElementById('workingHoursStart').value;
                formData.working_hours_end = document.getElementById('workingHoursEnd').value;
                formData.emergency_threshold = document.getElementById('emergencyThreshold').value;
            }
            
            try {
                const response = await fetch('/api/admin/update_settings', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showSuccessMessage();
                } else {
                    alert('Error saving settings: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        }
        
        function showSuccessMessage() {
            const message = document.getElementById('successMessage');
            message.style.display = 'block';
            setTimeout(() => {
                message.style.display = 'none';
            }, 3000);
        }
        
        function resetProfileForm() {
            document.getElementById('profileForm').reset();
            loadCurrentSettings();
        }
        
        function resetHospitalForm() {
            document.getElementById('hospitalForm').reset();
            loadCurrentSettings();
        }
        
        function resetSystemForm() {
            document.getElementById('systemForm').reset();
        }
        
        function saveNotificationSettings() {
            const settings = {
                emailNotifications: document.getElementById('emailNotifications').checked,
                emergencyAlerts: document.getElementById('emergencyAlerts').checked,
                dailyReports: document.getElementById('dailyReports').checked,
                systemMaintenance: document.getElementById('systemMaintenance').checked
            };
            
            alert('Notification settings saved successfully!\\n\\n' + JSON.stringify(settings, null, 2));
            showSuccessMessage();
        }
        
        function exportData() {
            if (confirm('Are you sure you want to export all system data?\\n\\nThis will create a backup file with all patient records, settings, and system data.')) {
                alert('Data export initiated.\\n\\nIn production, this would generate a comprehensive backup file containing:\\n- All patient records\\n- System settings\\n- User accounts\\n- Analytics data\\n\\nThe file would be available for download shortly.');
            }
        }
        
        function resetSystem() {
            if (confirm('⚠️ DANGER: Are you absolutely sure you want to reset the entire system?\\n\\nThis will permanently delete:\\n- All patient records\\n- All user accounts (except admin)\\n- All system settings\\n- All analytics data\\n\\nThis action CANNOT be undone!')) {
                if (confirm('This is your final warning. Type "RESET" in the next dialog to confirm.')) {
                    const confirmation = prompt('Type "RESET" to confirm system reset:');
                    if (confirmation === 'RESET') {
                        alert('System reset would be initiated in production.\\n\\nThis demo prevents actual data deletion for safety.');
                    } else {
                        alert('System reset cancelled - confirmation text did not match.');
                    }
                }
            }
        }
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    init_hospital_db()
    app.run(debug=True, port=5000)