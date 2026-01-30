from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'hackathon_secret_key_2024'

def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect('telemedicine.db')
    cursor = conn.cursor()
    
    # Patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            location TEXT NOT NULL,
            main_issue TEXT NOT NULL,
            symptom_severity INTEGER NOT NULL,
            chronic_illness BOOLEAN NOT NULL,
            pregnancy_elderly BOOLEAN NOT NULL,
            travel_distance REAL NOT NULL,
            urgency_score REAL,
            priority_level TEXT,
            recommended_department TEXT,
            queue_position INTEGER,
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
            specialization TEXT
        )
    ''')
    
    # Departments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    ''')
    
    # Insert sample departments
    departments = [
        ('General Medicine', 'General health issues and primary care'),
        ('Cardiology', 'Heart and cardiovascular conditions'),
        ('Orthopedics', 'Bone, joint, and muscle problems'),
        ('Gynecology', 'Women\'s health and reproductive issues'),
        ('Pediatrics', 'Children\'s health and development'),
        ('Dermatology', 'Skin conditions and disorders'),
        ('Neurology', 'Brain and nervous system disorders'),
        ('Emergency', 'Critical and urgent medical situations')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO departments (name, description) VALUES (?, ?)', departments)
    
    # Insert sample doctors
    doctors = [
        ('Dr. Sarah Johnson', 'sarah@doctor.com', 'General Medicine', 'Family Medicine'),
        ('Dr. Michael Chen', 'michael@doctor.com', 'Cardiology', 'Interventional Cardiology'),
        ('Dr. Emily Rodriguez', 'emily@doctor.com', 'Orthopedics', 'Sports Medicine'),
        ('Dr. David Kim', 'david@doctor.com', 'Gynecology', 'Obstetrics'),
        ('Dr. Lisa Thompson', 'lisa@doctor.com', 'Pediatrics', 'Child Development'),
        ('Dr. James Wilson', 'james@doctor.com', 'Dermatology', 'Cosmetic Dermatology'),
        ('Dr. Maria Garcia', 'maria@doctor.com', 'Neurology', 'Stroke Care'),
        ('Dr. Robert Brown', 'robert@doctor.com', 'Emergency', 'Emergency Medicine')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO doctors (name, email, department, specialization) VALUES (?, ?, ?, ?)', doctors)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Patient form page - simplified version"""
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Telemedicine Queue Optimizer</title>
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
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            }
            .hero {
                text-align: center;
                margin-bottom: 30px;
                color: #2c3e50;
            }
            .hero h1 {
                font-size: 2.5rem;
                margin-bottom: 10px;
            }
            .form-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
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
            .submit-btn {
                background: linear-gradient(135deg, #3498db, #2980b9);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 18px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.3s;
                width: 100%;
            }
            .submit-btn:hover {
                transform: translateY(-2px);
            }
            .severity-slider {
                margin-top: 10px;
            }
            .slider {
                width: 100%;
                height: 8px;
                border-radius: 5px;
                background: #ddd;
                outline: none;
            }
            .severity-labels {
                display: flex;
                justify-content: space-between;
                margin-top: 8px;
                font-size: 14px;
                color: #666;
            }
            .checkbox-group {
                flex-direction: row;
                align-items: center;
            }
            .checkbox-group input {
                margin-right: 10px;
                width: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="hero">
                <h1>🏥 Telemedicine Queue Optimizer</h1>
                <p>Get prioritized healthcare access with AI-powered queue optimization</p>
            </div>

            <form id="patientForm" onsubmit="submitForm(event)">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="name">👤 Full Name *</label>
                        <input type="text" id="name" name="name" required>
                    </div>

                    <div class="form-group">
                        <label for="age">📅 Age *</label>
                        <input type="number" id="age" name="age" min="1" max="120" required>
                    </div>

                    <div class="form-group">
                        <label for="gender">⚧ Gender *</label>
                        <select id="gender" name="gender" required>
                            <option value="">Select Gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="location">📍 Location *</label>
                        <select id="location" name="location" required>
                            <option value="">Select Location</option>
                            <option value="Rural">Rural</option>
                            <option value="Urban">Urban</option>
                        </select>
                    </div>

                    <div class="form-group full-width">
                        <label for="main_issue">🩺 Main Issue/Symptom *</label>
                        <textarea id="main_issue" name="main_issue" rows="3" 
                                  placeholder="Describe your main health concern or symptoms..." required></textarea>
                    </div>

                    <div class="form-group">
                        <label for="symptom_severity">🌡️ Symptom Severity *</label>
                        <div class="severity-slider">
                            <input type="range" id="symptom_severity" name="symptom_severity" 
                                   min="1" max="10" value="5" class="slider" oninput="updateSeverity(this.value)">
                            <div class="severity-labels">
                                <span>Mild (1)</span>
                                <span id="severity-value">5</span>
                                <span>Severe (10)</span>
                            </div>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="travel_distance">🛣️ Travel Distance (km) *</label>
                        <input type="number" id="travel_distance" name="travel_distance" 
                               min="0" step="0.1" placeholder="Distance to clinic" required>
                    </div>

                    <div class="form-group checkbox-group">
                        <input type="checkbox" id="chronic_illness" name="chronic_illness" value="yes">
                        <label for="chronic_illness">💊 I have chronic illness</label>
                    </div>

                    <div class="form-group checkbox-group">
                        <input type="checkbox" id="pregnancy_elderly" name="pregnancy_elderly" value="yes">
                        <label for="pregnancy_elderly">👶 I am pregnant or elderly (65+)</label>
                    </div>
                </div>

                <button type="submit" class="submit-btn">
                    ✈️ Submit Registration
                </button>
            </form>

            <div id="results" style="display: none; margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                <h2>🎉 Registration Complete!</h2>
                <div id="result-content"></div>
            </div>
        </div>

        <script>
            function updateSeverity(value) {
                document.getElementById('severity-value').textContent = value;
            }

            async function submitForm(event) {
                event.preventDefault();
                
                const formData = new FormData(document.getElementById('patientForm'));
                
                try {
                    const response = await fetch('/submit_patient', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        document.getElementById('result-content').innerHTML = `
                            <div style="background: white; padding: 20px; border-radius: 8px; margin: 10px 0;">
                                <h3>🏥 Recommended Department: <span style="color: #3498db;">${result.recommended_department}</span></h3>
                                <p><strong>Priority Level:</strong> <span style="color: ${getPriorityColor(result.priority_level)};">${result.priority_level}</span></p>
                                <p><strong>Urgency Score:</strong> ${result.urgency_score}</p>
                                <p><strong>Queue Position:</strong> #${result.queue_position}</p>
                                <button onclick="viewDoctors('${result.recommended_department}')" style="background: #2ecc71; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 10px;">
                                    👨‍⚕️ View Available Doctors
                                </button>
                            </div>
                        `;
                        document.getElementById('results').style.display = 'block';
                    } else {
                        alert('Error: ' + result.error);
                    }
                } catch (error) {
                    alert('Network error: ' + error.message);
                }
            }

            function getPriorityColor(priority) {
                switch(priority) {
                    case 'High': return '#e74c3c';
                    case 'Medium': return '#f39c12';
                    case 'Low': return '#2ecc71';
                    default: return '#333';
                }
            }

            async function viewDoctors(department) {
                try {
                    const response = await fetch(`/department_doctors/${encodeURIComponent(department)}`);
                    const doctors = await response.json();
                    
                    let doctorsHtml = '<h4>👨‍⚕️ Available Doctors:</h4>';
                    doctors.forEach(doctor => {
                        doctorsHtml += `
                            <div style="background: #ecf0f1; padding: 10px; margin: 5px 0; border-radius: 5px;">
                                <strong>${doctor.name}</strong><br>
                                <small>${doctor.specialization}</small>
                            </div>
                        `;
                    });
                    
                    document.getElementById('result-content').innerHTML += doctorsHtml;
                } catch (error) {
                    alert('Error loading doctors: ' + error.message);
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/submit_patient', methods=['POST'])
def submit_patient():
    """Process patient form submission - simplified"""
    try:
        # Simple rule-based urgency calculation for demo
        data = {
            'name': request.form['name'],
            'age': int(request.form['age']),
            'gender': request.form['gender'],
            'location': request.form['location'],
            'main_issue': request.form['main_issue'],
            'symptom_severity': int(request.form['symptom_severity']),
            'chronic_illness': request.form.get('chronic_illness') == 'yes',
            'pregnancy_elderly': request.form.get('pregnancy_elderly') == 'yes',
            'travel_distance': float(request.form['travel_distance'])
        }
        
        # Simple urgency calculation
        urgency_score = data['symptom_severity'] * 10
        if data['chronic_illness']:
            urgency_score += 20
        if data['pregnancy_elderly']:
            urgency_score += 25
        if data['location'] == 'Rural':
            urgency_score += 15
        if data['travel_distance'] > 50:
            urgency_score += 10
        
        urgency_score = min(100, urgency_score)
        
        # Determine priority
        if urgency_score >= 70:
            priority_level = 'High'
        elif urgency_score >= 40:
            priority_level = 'Medium'
        else:
            priority_level = 'Low'
        
        # Simple department recommendation
        issue_lower = data['main_issue'].lower()
        if 'chest pain' in issue_lower or 'heart' in issue_lower:
            recommended_dept = 'Cardiology'
        elif 'joint pain' in issue_lower or 'back pain' in issue_lower or 'fracture' in issue_lower:
            recommended_dept = 'Orthopedics'
        elif 'pregnancy' in issue_lower or 'pregnant' in issue_lower:
            recommended_dept = 'Gynecology'
        elif 'headache' in issue_lower or 'migraine' in issue_lower:
            recommended_dept = 'Neurology'
        elif 'skin' in issue_lower or 'rash' in issue_lower:
            recommended_dept = 'Dermatology'
        elif data['age'] < 18:
            recommended_dept = 'Pediatrics'
        else:
            recommended_dept = 'General Medicine'
        
        # Save to database
        conn = sqlite3.connect('telemedicine.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO patients (name, age, gender, location, main_issue, symptom_severity,
                                chronic_illness, pregnancy_elderly, travel_distance, urgency_score,
                                priority_level, recommended_department, queue_position)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['age'], data['gender'], data['location'], data['main_issue'],
              data['symptom_severity'], data['chronic_illness'], data['pregnancy_elderly'],
              data['travel_distance'], urgency_score, priority_level, recommended_dept, 1))
        
        patient_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'urgency_score': round(urgency_score, 1),
            'priority_level': priority_level,
            'recommended_department': recommended_dept,
            'queue_position': 1
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/department_doctors/<department>')
def department_doctors(department):
    """Get doctors for a specific department"""
    conn = sqlite3.connect('telemedicine.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT name, specialization FROM doctors WHERE department = ?', (department,))
    doctors = cursor.fetchall()
    conn.close()
    
    return jsonify([{'name': doc[0], 'specialization': doc[1]} for doc in doctors])

if __name__ == '__main__':
    init_db()
    print("🏥 Starting Fixed Telemedicine App...")
    print("📍 Access: http://127.0.0.1:5004")
    app.run(debug=True, host='127.0.0.1', port=5004)