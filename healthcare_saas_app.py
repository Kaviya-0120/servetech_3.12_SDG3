from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import sqlite3
import random
import string
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = 'healthcare_saas_2024_secure_key'

def init_healthcare_db():
    """Initialize healthcare SaaS database"""
    conn = sqlite3.connect('healthcare_saas.db')
    cursor = conn.cursor()
    
    # Appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL,
            main_symptom TEXT NOT NULL,
            severity TEXT NOT NULL,
            symptom_days INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            appointment_time TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            confirmed_at TIMESTAMP,
            admin_notes TEXT
        )
    ''')
    
    # Admin users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'admin'
        )
    ''')
    
    # Insert default admin
    cursor.execute('INSERT OR IGNORE INTO admin_users (username, password) VALUES (?, ?)', 
                  ('admin', 'healthcare2024'))
    
    conn.commit()
    conn.close()

def generate_registration_id():
    """Generate unique registration ID"""
    return 'REG' + ''.join(random.choices(string.digits, k=6))

@app.route('/')
def role_selection():
    """Main role selection screen"""
    return render_template_string(ROLE_SELECTION_TEMPLATE)

@app.route('/patient')
def patient_options():
    """Patient options screen"""
    return render_template_string(PATIENT_OPTIONS_TEMPLATE)

@app.route('/patient/register')
def patient_register():
    """Patient registration form"""
    return render_template_string(PATIENT_REGISTER_TEMPLATE)
@app.route('/patient/status')
def patient_status():
    """Patient status check"""
    return render_template_string(PATIENT_STATUS_TEMPLATE)

@app.route('/api/register_appointment', methods=['POST'])
def register_appointment():
    """Process appointment registration"""
    try:
        data = request.get_json()
        
        # Generate unique registration ID
        registration_id = generate_registration_id()
        
        # Save to database
        conn = sqlite3.connect('healthcare_saas.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO appointments (registration_id, name, age, gender, phone, 
                                    main_symptom, severity, symptom_days)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (registration_id, data['name'], data['age'], data['gender'], 
              data['phone'], data['main_symptom'], data['severity'], data['symptom_days']))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'registration_id': registration_id,
            'message': 'Your appointment has been registered successfully.'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/check_status', methods=['POST'])
def check_status():
    """Check appointment status"""
    try:
        data = request.get_json()
        registration_id = data['registration_id']
        
        conn = sqlite3.connect('healthcare_saas.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT registration_id, name, status, appointment_time, created_at, severity, main_symptom
            FROM appointments WHERE registration_id = ?
        ''', (registration_id,))
        
        appointment = cursor.fetchone()
        conn.close()
        
        if appointment:
            return jsonify({
                'success': True,
                'appointment': {
                    'registration_id': appointment[0],
                    'name': appointment[1],
                    'status': appointment[2],
                    'appointment_time': appointment[3],
                    'registered_date': appointment[4],
                    'severity': appointment[5],
                    'symptom': appointment[6]
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Registration ID not found'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin')
def admin_login():
    """Admin login screen"""
    return render_template_string(ADMIN_LOGIN_TEMPLATE)

@app.route('/admin/login', methods=['POST'])
def admin_authenticate():
    """Admin authentication"""
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        conn = sqlite3.connect('healthcare_saas.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM admin_users WHERE username = ? AND password = ?', 
                      (username, password))
        admin = cursor.fetchone()
        conn.close()
        
        if admin:
            session['admin_logged_in'] = True
            session['admin_id'] = admin[0]
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if not session.get('admin_logged_in'):
        return redirect('/admin')
    
    return render_template_string(ADMIN_DASHBOARD_TEMPLATE)

@app.route('/api/admin/appointments')
def get_appointments():
    """Get all appointments for admin"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('healthcare_saas.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT registration_id, name, age, gender, phone, main_symptom, 
               severity, symptom_days, status, appointment_time, created_at
        FROM appointments ORDER BY created_at DESC
    ''')
    
    appointments = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'registration_id': apt[0],
        'name': apt[1],
        'age': apt[2],
        'gender': apt[3],
        'phone': apt[4],
        'symptom': apt[5],
        'severity': apt[6],
        'symptom_days': apt[7],
        'status': apt[8],
        'appointment_time': apt[9],
        'created_at': apt[10]
    } for apt in appointments])

@app.route('/api/admin/confirm_appointment', methods=['POST'])
def confirm_appointment():
    """Confirm appointment and assign time slot"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        registration_id = data['registration_id']
        appointment_time = data['appointment_time']
        
        conn = sqlite3.connect('healthcare_saas.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE appointments 
            SET status = 'confirmed', appointment_time = ?, confirmed_at = ?
            WHERE registration_id = ?
        ''', (appointment_time, datetime.now().isoformat(), registration_id))
        
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
# ===== UI TEMPLATES =====

ROLE_SELECTION_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HealthCare SaaS - Role Selection</title>
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
        .container {
            background: white;
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
            text-align: center;
            max-width: 500px;
            width: 90%;
        }
        .logo {
            font-size: 3rem;
            margin-bottom: 20px;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.2rem;
        }
        .subtitle {
            color: #7f8c8d;
            margin-bottom: 40px;
            font-size: 1.1rem;
        }
        .role-buttons {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .role-btn {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border: none;
            padding: 20px 30px;
            border-radius: 15px;
            font-size: 1.3rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: block;
        }
        .role-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(52, 152, 219, 0.4);
        }
        .role-btn.admin {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
        }
        .role-btn.admin:hover {
            box-shadow: 0 10px 25px rgba(231, 76, 60, 0.4);
        }
        .footer {
            margin-top: 30px;
            color: #95a5a6;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🏥</div>
        <h1>HealthCare SaaS</h1>
        <p class="subtitle">Professional Telemedicine Platform</p>
        
        <div class="role-buttons">
            <a href="/patient" class="role-btn">
                👤 Patient
                <div style="font-size: 0.9rem; font-weight: normal; margin-top: 5px;">
                    Book appointments & check status
                </div>
            </a>
            
            <a href="/admin" class="role-btn admin">
                🛡️ Admin
                <div style="font-size: 0.9rem; font-weight: normal; margin-top: 5px;">
                    Manage appointments & system
                </div>
            </a>
        </div>
        
        <div class="footer">
            Secure • Professional • Healthcare Ready
        </div>
    </div>
</body>
</html>
'''

PATIENT_OPTIONS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Patient Portal - HealthCare SaaS</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        }
        .options {
            display: flex;
            flex-direction: column;
            gap: 25px;
        }
        .option-card {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            color: inherit;
        }
        .option-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
            border-color: #3498db;
        }
        .option-icon {
            font-size: 3rem;
            margin-bottom: 15px;
        }
        .option-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .option-desc {
            color: #7f8c8d;
            font-size: 1rem;
        }
        .back-btn {
            background: #95a5a6;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 30px;
            text-decoration: none;
            display: inline-block;
        }
        .back-btn:hover {
            background: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>👤 Patient Portal</h1>
        <p>Choose your action below</p>
    </div>
    
    <div class="container">
        <div class="options">
            <a href="/patient/register" class="option-card">
                <div class="option-icon">📝</div>
                <div class="option-title">Register for Appointment</div>
                <div class="option-desc">Book a new telemedicine consultation</div>
            </a>
            
            <a href="/patient/status" class="option-card">
                <div class="option-icon">🔍</div>
                <div class="option-title">Already Registered? Check Status</div>
                <div class="option-desc">View your appointment details and schedule</div>
            </a>
        </div>
        
        <a href="/" class="back-btn">← Back to Role Selection</a>
    </div>
</body>
</html>
'''
PATIENT_REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register Appointment - HealthCare SaaS</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        }
        .form-section {
            margin-bottom: 30px;
        }
        .section-title {
            font-size: 1.3rem;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
        }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
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
            color: #2c3e50;
        }
        input, select, textarea {
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #3498db;
        }
        .severity-options {
            display: flex;
            gap: 15px;
            margin-top: 10px;
        }
        .severity-btn {
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            background: white;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s;
        }
        .severity-btn.selected {
            border-color: #3498db;
            background: #ebf3fd;
        }
        .severity-btn.mild.selected { border-color: #2ecc71; background: #e8f8f5; }
        .severity-btn.moderate.selected { border-color: #f39c12; background: #fef9e7; }
        .severity-btn.severe.selected { border-color: #e74c3c; background: #fdf2f2; }
        .submit-btn {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border: none;
            padding: 18px 40px;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
            transition: transform 0.3s;
        }
        .submit-btn:hover {
            transform: translateY(-2px);
        }
        .back-btn {
            background: #95a5a6;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin-bottom: 20px;
        }
        .success-modal {
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
            text-align: center;
            max-width: 500px;
            width: 90%;
        }
        .success-icon {
            font-size: 4rem;
            color: #2ecc71;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📝 Register for Appointment</h1>
        <p>Please fill in your details below</p>
    </div>
    
    <div class="container">
        <a href="/patient" class="back-btn">← Back to Patient Portal</a>
        
        <form id="registrationForm">
            <!-- Basic Information -->
            <div class="form-section">
                <div class="section-title">👤 Basic Information</div>
                <div class="form-grid">
                    <div class="form-group">
                        <label for="name">Full Name *</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="age">Age *</label>
                        <input type="number" id="age" name="age" min="1" max="120" required onchange="handleAgeChange()">
                    </div>
                    
                    <div class="form-group">
                        <label for="gender">Gender *</label>
                        <select id="gender" name="gender" required onchange="handleGenderChange()">
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
                </div>
            </div>
            
            <!-- Symptom Information -->
            <div class="form-section">
                <div class="section-title">🩺 Symptom Information</div>
                
                <div class="form-group full-width">
                    <label for="main_symptom">Main Symptom *</label>
                    <textarea id="main_symptom" name="main_symptom" rows="3" 
                              placeholder="Describe your primary health concern..." required></textarea>
                </div>
                
                <div class="form-group">
                    <label>Symptom Severity *</label>
                    <div class="severity-options">
                        <div class="severity-btn mild" onclick="selectSeverity('Mild', this)">
                            <div style="font-weight: bold; color: #2ecc71;">Mild</div>
                            <div style="font-size: 0.9rem; color: #666;">Manageable discomfort</div>
                        </div>
                        <div class="severity-btn moderate" onclick="selectSeverity('Moderate', this)">
                            <div style="font-weight: bold; color: #f39c12;">Moderate</div>
                            <div style="font-size: 0.9rem; color: #666;">Noticeable impact</div>
                        </div>
                        <div class="severity-btn severe" onclick="selectSeverity('Severe', this)">
                            <div style="font-weight: bold; color: #e74c3c;">Severe</div>
                            <div style="font-size: 0.9rem; color: #666;">Significant distress</div>
                        </div>
                    </div>
                    <input type="hidden" id="severity" name="severity" required>
                </div>
                
                <div class="form-group">
                    <label for="symptom_days">How many days have you had this symptom? *</label>
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
            
            <button type="submit" class="submit-btn">
                📅 Register Appointment
            </button>
        </form>
    </div>
    
    <!-- Success Modal -->
    <div id="successModal" class="success-modal">
        <div class="modal-content">
            <div class="success-icon">✅</div>
            <h2>Registration Successful!</h2>
            <p style="margin: 20px 0;">Your appointment has been registered successfully.</p>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <strong>Registration ID:</strong>
                <div id="registrationId" style="font-size: 1.5rem; color: #3498db; font-weight: bold; margin-top: 10px;"></div>
            </div>
            <p style="color: #666; margin-bottom: 20px;">
                Save this ID to check your appointment status later.
                You will receive confirmation via in-app notification.
            </p>
            <button onclick="goToPatientPortal()" style="background: #3498db; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer;">
                Back to Patient Portal
            </button>
        </div>
    </div>

    <script>
        let selectedSeverity = '';
        
        function handleAgeChange() {
            // Age-based logic can be added here if needed
            console.log('Age changed:', document.getElementById('age').value);
        }
        
        function handleGenderChange() {
            // Gender-based conditional logic
            const gender = document.getElementById('gender').value;
            console.log('Gender changed:', gender);
            // No pregnancy questions for males - handled by not showing them
        }
        
        function selectSeverity(severity, element) {
            // Remove previous selection
            document.querySelectorAll('.severity-btn').forEach(btn => {
                btn.classList.remove('selected');
            });
            
            // Add selection to clicked element
            element.classList.add('selected');
            selectedSeverity = severity;
            document.getElementById('severity').value = severity;
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
                main_symptom: document.getElementById('main_symptom').value,
                severity: selectedSeverity,
                symptom_days: parseInt(document.getElementById('symptom_days').value)
            };
            
            try {
                const response = await fetch('/api/register_appointment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('registrationId').textContent = result.registration_id;
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
    <title>Check Status - HealthCare SaaS</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        }
        .search-section {
            text-align: center;
            margin-bottom: 30px;
        }
        .search-input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1.1rem;
            text-align: center;
            margin-bottom: 20px;
        }
        .search-btn {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: transform 0.3s;
        }
        .search-btn:hover {
            transform: translateY(-2px);
        }
        .status-card {
            display: none;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 15px;
            padding: 30px;
            margin-top: 30px;
        }
        .status-header {
            text-align: center;
            margin-bottom: 25px;
        }
        .status-badge {
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .status-pending { background: #fff3cd; color: #856404; }
        .status-confirmed { background: #d4edda; color: #155724; }
        .status-completed { background: #cce7ff; color: #004085; }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        .info-item {
            background: white;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #3498db;
        }
        .info-label {
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 5px;
        }
        .info-value {
            font-weight: 600;
            color: #2c3e50;
        }
        .back-btn {
            background: #95a5a6;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin-bottom: 20px;
        }
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
            display: none;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Check Appointment Status</h1>
        <p>Enter your Registration ID to view details</p>
    </div>
    
    <div class="container">
        <a href="/patient" class="back-btn">← Back to Patient Portal</a>
        
        <div class="search-section">
            <input type="text" id="registrationId" class="search-input" 
                   placeholder="Enter Registration ID (e.g., REG123456)" 
                   style="text-transform: uppercase;">
            <br>
            <button onclick="checkStatus()" class="search-btn">
                🔍 Check Status
            </button>
        </div>
        
        <div id="errorMessage" class="error-message"></div>
        
        <div id="statusCard" class="status-card">
            <div class="status-header">
                <h2 id="patientName"></h2>
                <div id="statusBadge" class="status-badge"></div>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Registration ID</div>
                    <div class="info-value" id="regId"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Registration Date</div>
                    <div class="info-value" id="regDate"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Symptom</div>
                    <div class="info-value" id="symptom"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Severity</div>
                    <div class="info-value" id="severity"></div>
                </div>
                
                <div class="info-item" id="appointmentTimeItem" style="display: none;">
                    <div class="info-label">Appointment Time</div>
                    <div class="info-value" id="appointmentTime"></div>
                </div>
            </div>
            
            <div id="statusMessage" style="margin-top: 25px; padding: 20px; background: white; border-radius: 10px; text-align: center;"></div>
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
                const response = await fetch('/api/check_status', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ registration_id: registrationId })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    displayAppointment(result.appointment);
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
        
        function displayAppointment(appointment) {
            document.getElementById('patientName').textContent = appointment.name;
            document.getElementById('regId').textContent = appointment.registration_id;
            document.getElementById('regDate').textContent = formatDate(appointment.registered_date);
            document.getElementById('symptom').textContent = appointment.symptom;
            document.getElementById('severity').textContent = appointment.severity;
            
            const statusBadge = document.getElementById('statusBadge');
            const statusMessage = document.getElementById('statusMessage');
            
            statusBadge.textContent = appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1);
            statusBadge.className = 'status-badge status-' + appointment.status;
            
            if (appointment.status === 'pending') {
                statusMessage.innerHTML = `
                    <h3 style="color: #f39c12; margin-bottom: 10px;">⏳ Appointment Pending</h3>
                    <p>Your appointment is being reviewed by our medical team. You will receive a confirmation with your scheduled time slot soon.</p>
                `;
                document.getElementById('appointmentTimeItem').style.display = 'none';
            } else if (appointment.status === 'confirmed') {
                statusMessage.innerHTML = `
                    <h3 style="color: #2ecc71; margin-bottom: 10px;">✅ Appointment Confirmed</h3>
                    <p>Your appointment has been scheduled. Please be available at the confirmed time.</p>
                `;
                document.getElementById('appointmentTime').textContent = formatDateTime(appointment.appointment_time);
                document.getElementById('appointmentTimeItem').style.display = 'block';
            }
            
            document.getElementById('statusCard').style.display = 'block';
        }
        
        function formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString() + ' at ' + date.toLocaleTimeString();
        }
        
        function formatDateTime(dateString) {
            if (!dateString) return 'Not scheduled';
            const date = new Date(dateString);
            return date.toLocaleDateString() + ' at ' + date.toLocaleTimeString();
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
ADMIN_LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login - HealthCare SaaS</title>
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
            background: white;
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
            max-width: 450px;
            width: 90%;
        }
        .login-header {
            text-align: center;
            margin-bottom: 40px;
        }
        .admin-icon {
            font-size: 4rem;
            color: #e74c3c;
            margin-bottom: 20px;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #7f8c8d;
        }
        .form-group {
            margin-bottom: 25px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
        }
        input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #e74c3c;
        }
        .login-btn {
            width: 100%;
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
            border: none;
            padding: 18px;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s;
        }
        .login-btn:hover {
            transform: translateY(-2px);
        }
        .back-btn {
            background: #95a5a6;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin-bottom: 30px;
        }
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            display: none;
        }
        .demo-credentials {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
            text-align: center;
        }
        .demo-credentials h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        .demo-credentials p {
            color: #666;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <a href="/" class="back-btn">← Back to Home</a>
        
        <div class="login-header">
            <div class="admin-icon">🛡️</div>
            <h1>Admin Login</h1>
            <p class="subtitle">Secure access to healthcare management</p>
        </div>
        
        <div id="errorMessage" class="error-message"></div>
        
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="login-btn">
                🔐 Secure Login
            </button>
        </form>
        
        <div class="demo-credentials">
            <h3>Demo Credentials</h3>
            <p><strong>Username:</strong> admin</p>
            <p><strong>Password:</strong> healthcare2024</p>
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
ADMIN_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - HealthCare SaaS</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f6fa;
            min-height: 100vh;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 {
            font-size: 1.8rem;
        }
        .logout-btn {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
        }
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        .stat-label {
            color: #7f8c8d;
            font-size: 0.9rem;
        }
        .appointments-section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        }
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #ecf0f1;
        }
        .refresh-btn {
            background: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
        }
        .appointments-table {
            width: 100%;
            border-collapse: collapse;
        }
        .appointments-table th,
        .appointments-table td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }
        .appointments-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
        }
        .status-badge {
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .status-pending { background: #fff3cd; color: #856404; }
        .status-confirmed { background: #d4edda; color: #155724; }
        .severity-mild { color: #2ecc71; font-weight: bold; }
        .severity-moderate { color: #f39c12; font-weight: bold; }
        .severity-severe { color: #e74c3c; font-weight: bold; }
        .action-btn {
            background: #2ecc71;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9rem;
        }
        .action-btn:hover {
            background: #27ae60;
        }
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
            max-width: 500px;
            width: 90%;
        }
        .modal h3 {
            margin-bottom: 20px;
            color: #2c3e50;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
        }
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
        }
        .modal-buttons {
            display: flex;
            gap: 15px;
            justify-content: flex-end;
        }
        .btn-primary {
            background: #3498db;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
        }
        .btn-secondary {
            background: #95a5a6;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>🛡️ Admin Dashboard</h1>
            <a href="/admin/logout" class="logout-btn">Logout</a>
        </div>
    </div>
    
    <div class="container">
        <!-- Statistics Cards -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">📅</div>
                <div class="stat-number" id="totalToday">0</div>
                <div class="stat-label">Appointments Today</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">⏳</div>
                <div class="stat-number" id="pendingCount">0</div>
                <div class="stat-label">Pending Confirmations</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">✅</div>
                <div class="stat-number" id="confirmedCount">0</div>
                <div class="stat-label">Confirmed Appointments</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">🚨</div>
                <div class="stat-number" id="criticalCount">0</div>
                <div class="stat-label">Critical Cases</div>
            </div>
        </div>
        
        <!-- Appointments Management -->
        <div class="appointments-section">
            <div class="section-header">
                <h2>📋 Appointment Queue Management</h2>
                <button class="refresh-btn" onclick="loadAppointments()">🔄 Refresh</button>
            </div>
            
            <div style="overflow-x: auto;">
                <table class="appointments-table">
                    <thead>
                        <tr>
                            <th>Registration ID</th>
                            <th>Patient Name</th>
                            <th>Age</th>
                            <th>Phone</th>
                            <th>Symptom</th>
                            <th>Severity</th>
                            <th>Days</th>
                            <th>Status</th>
                            <th>Registered</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="appointmentsTableBody">
                        <!-- Appointments will be loaded here -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <!-- Confirm Appointment Modal -->
    <div id="confirmModal" class="modal">
        <div class="modal-content">
            <h3>📅 Confirm Appointment</h3>
            <div class="form-group">
                <label for="appointmentDateTime">Appointment Date & Time:</label>
                <input type="datetime-local" id="appointmentDateTime" required>
            </div>
            <div class="modal-buttons">
                <button class="btn-secondary" onclick="closeModal()">Cancel</button>
                <button class="btn-primary" onclick="confirmAppointment()">Confirm Appointment</button>
            </div>
        </div>
    </div>

    <script>
        let currentRegistrationId = '';
        
        // Load appointments on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadAppointments();
        });
        
        async function loadAppointments() {
            try {
                const response = await fetch('/api/admin/appointments');
                const appointments = await response.json();
                
                displayAppointments(appointments);
                updateStatistics(appointments);
            } catch (error) {
                console.error('Error loading appointments:', error);
            }
        }
        
        function displayAppointments(appointments) {
            const tbody = document.getElementById('appointmentsTableBody');
            tbody.innerHTML = '';
            
            appointments.forEach(appointment => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><strong>${appointment.registration_id}</strong></td>
                    <td>${appointment.name}</td>
                    <td>${appointment.age}</td>
                    <td>${appointment.phone}</td>
                    <td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" 
                        title="${appointment.symptom}">${appointment.symptom}</td>
                    <td><span class="severity-${appointment.severity.toLowerCase()}">${appointment.severity}</span></td>
                    <td>${appointment.symptom_days} days</td>
                    <td><span class="status-badge status-${appointment.status}">${appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1)}</span></td>
                    <td>${formatDate(appointment.created_at)}</td>
                    <td>
                        ${appointment.status === 'pending' ? 
                            `<button class="action-btn" onclick="openConfirmModal('${appointment.registration_id}')">Confirm</button>` :
                            appointment.appointment_time ? formatDateTime(appointment.appointment_time) : 'Confirmed'
                        }
                    </td>
                `;
                tbody.appendChild(row);
            });
        }
        
        function updateStatistics(appointments) {
            const today = new Date().toDateString();
            
            const todayAppointments = appointments.filter(apt => 
                new Date(apt.created_at).toDateString() === today
            );
            
            const pendingCount = appointments.filter(apt => apt.status === 'pending').length;
            const confirmedCount = appointments.filter(apt => apt.status === 'confirmed').length;
            const criticalCount = appointments.filter(apt => apt.severity === 'Severe').length;
            
            document.getElementById('totalToday').textContent = todayAppointments.length;
            document.getElementById('pendingCount').textContent = pendingCount;
            document.getElementById('confirmedCount').textContent = confirmedCount;
            document.getElementById('criticalCount').textContent = criticalCount;
        }
        
        function openConfirmModal(registrationId) {
            currentRegistrationId = registrationId;
            
            // Set default appointment time to tomorrow at 10 AM
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            tomorrow.setHours(10, 0, 0, 0);
            
            document.getElementById('appointmentDateTime').value = tomorrow.toISOString().slice(0, 16);
            document.getElementById('confirmModal').style.display = 'flex';
        }
        
        function closeModal() {
            document.getElementById('confirmModal').style.display = 'none';
            currentRegistrationId = '';
        }
        
        async function confirmAppointment() {
            const appointmentTime = document.getElementById('appointmentDateTime').value;
            
            if (!appointmentTime) {
                alert('Please select appointment date and time');
                return;
            }
            
            try {
                const response = await fetch('/api/admin/confirm_appointment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        registration_id: currentRegistrationId,
                        appointment_time: appointmentTime
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    closeModal();
                    loadAppointments(); // Refresh the table
                    alert('Appointment confirmed successfully!');
                } else {
                    alert('Error confirming appointment: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        }
        
        function formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString();
        }
        
        function formatDateTime(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }
        
        // Auto-refresh every 30 seconds
        setInterval(loadAppointments, 30000);
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    init_healthcare_db()
    print("🏥 HealthCare SaaS Platform Starting...")
    print("📍 Access: http://127.0.0.1:5005")
    print("👤 Patient Portal: Register & Check Status")
    print("🛡️ Admin Portal: Manage Appointments")
    print("🔐 Admin Login: admin / healthcare2024")
    app.run(debug=True, host='127.0.0.1', port=5005)