from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import os
from datetime import datetime
import json
from ml_engine import MLEngine
from department_recommender import DepartmentRecommender

app = Flask(__name__)
app.secret_key = 'hackathon_secret_key_2024'

# Initialize ML components
ml_engine = MLEngine()
dept_recommender = DepartmentRecommender()

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
    """Patient form page"""
    return render_template('patient_form.html')

@app.route('/submit_patient', methods=['POST'])
def submit_patient():
    """Process patient form submission"""
    try:
        # Extract form data
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
        
        # Calculate urgency score and priority using ML
        urgency_score, priority_level = ml_engine.predict_urgency(data)
        
        # Get department recommendation
        recommended_dept = dept_recommender.recommend_department(data['main_issue'])
        
        # Calculate queue position
        queue_position = get_queue_position(recommended_dept, urgency_score)
        
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
              data['travel_distance'], urgency_score, priority_level, recommended_dept, queue_position))
        
        patient_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'urgency_score': round(urgency_score, 2),
            'priority_level': priority_level,
            'recommended_department': recommended_dept,
            'queue_position': queue_position
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

@app.route('/doctor_login')
def doctor_login():
    """Doctor login page"""
    return render_template('doctor_login.html')

@app.route('/admin_login')
def admin_login():
    """Admin login page"""
    return render_template('admin_login.html')

@app.route('/login', methods=['POST'])
def login():
    """Handle login for both doctors and admins"""
    email = request.form['email']
    password = request.form['password']
    
    # Admin login
    if email == 'admin@gmail.com':
        session['user_type'] = 'admin'
        session['email'] = email
        return redirect(url_for('admin_dashboard'))
    
    # Doctor login
    elif email.endswith('@doctor.com'):
        conn = sqlite3.connect('telemedicine.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, department FROM doctors WHERE email = ?', (email,))
        doctor = cursor.fetchone()
        conn.close()
        
        if doctor:
            session['user_type'] = 'doctor'
            session['email'] = email
            session['name'] = doctor[0]
            session['department'] = doctor[1]
            return redirect(url_for('doctor_dashboard'))
    
    return render_template('doctor_login.html', error='Invalid credentials')

@app.route('/doctor_dashboard')
def doctor_dashboard():
    """Doctor dashboard showing department patients"""
    if session.get('user_type') != 'doctor':
        return redirect(url_for('doctor_login'))
    
    department = session.get('department')
    
    conn = sqlite3.connect('telemedicine.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, age, main_issue, priority_level, urgency_score, queue_position,
               created_at, travel_distance
        FROM patients 
        WHERE recommended_department = ?
        ORDER BY urgency_score DESC, queue_position ASC
    ''', (department,))
    
    patients = cursor.fetchall()
    conn.close()
    
    return render_template('doctor_dashboard.html', 
                         patients=patients, 
                         department=department,
                         doctor_name=session.get('name'))

@app.route('/admin_dashboard')
def admin_dashboard():
    """Admin dashboard with complete system overview"""
    if session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('telemedicine.db')
    cursor = conn.cursor()
    
    # Get all patients
    cursor.execute('''
        SELECT id, name, age, gender, location, main_issue, priority_level, 
               urgency_score, recommended_department, queue_position, created_at
        FROM patients 
        ORDER BY created_at DESC
    ''')
    patients = cursor.fetchall()
    
    # Get all doctors
    cursor.execute('SELECT name, email, department, specialization FROM doctors')
    doctors = cursor.fetchall()
    
    # Get department statistics
    cursor.execute('''
        SELECT recommended_department, COUNT(*) as patient_count,
               AVG(urgency_score) as avg_urgency
        FROM patients 
        GROUP BY recommended_department
    ''')
    dept_stats = cursor.fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html',
                         patients=patients,
                         doctors=doctors,
                         dept_stats=dept_stats)

@app.route('/api/queue_status')
def queue_status():
    """API endpoint for live queue updates"""
    conn = sqlite3.connect('telemedicine.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT recommended_department, COUNT(*) as count,
               AVG(urgency_score) as avg_urgency
        FROM patients 
        GROUP BY recommended_department
    ''')
    
    queue_data = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'department': row[0],
        'patient_count': row[1],
        'avg_urgency': round(row[2], 2) if row[2] else 0
    } for row in queue_data])

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('index'))

def get_queue_position(department, urgency_score):
    """Calculate queue position based on urgency score"""
    conn = sqlite3.connect('telemedicine.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) FROM patients 
        WHERE recommended_department = ? AND urgency_score > ?
    ''', (department, urgency_score))
    
    position = cursor.fetchone()[0] + 1
    conn.close()
    
    return position

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)