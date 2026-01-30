import sqlite3
import datetime

DB_NAME = "hospital.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Drop tables if they exist to ensure a clean slate for the demo
    # In production, we would use migrations
    c.execute('DROP TABLE IF EXISTS patients')
    c.execute('DROP TABLE IF EXISTS departments')
    c.execute('DROP TABLE IF EXISTS doctors') # Clean up old table if exists

    # Create Departments
    c.execute('''
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    # Create Patients
    c.execute('''
        CREATE TABLE patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            location TEXT NOT NULL,
            symptom TEXT NOT NULL,
            severity INTEGER NOT NULL,
            chronic_illness TEXT NOT NULL,
            vulnerable_group TEXT NOT NULL,
            distance REAL NOT NULL,
            department_id INTEGER,
            priority_score REAL,
            priority_level TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments (id)
        )
    ''')

    # Seed Departments
    departments = ['General Medicine', 'Cardiology', 'Orthopedics', 'Gynecology', 'Pediatrics']
    for dept in departments:
        c.execute('INSERT OR IGNORE INTO departments (name) VALUES (?)', (dept,))

    conn.commit()
    conn.close()
    print("Database initialized and seeded.")

def add_patient(data):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO patients (name, age, gender, location, symptom, severity, chronic_illness, vulnerable_group, distance, department_id, priority_score, priority_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['name'], data['age'], data['gender'], data['location'], data['symptom'], 
        data['severity'], data['chronic_illness'], data['vulnerable_group'], 
        data['distance'], data['department_id'], data['priority_score'], data['priority_level']
    ))
    conn.commit()
    patient_id = c.lastrowid
    conn.close()
    return patient_id

def get_patients_by_department(department_id):
    conn = get_db_connection()
    # Order by priority score (descending) and then timestamp (ascending)
    patients = conn.execute('''
        SELECT * FROM patients WHERE department_id = ? 
        ORDER BY priority_score DESC, timestamp ASC
    ''', (department_id,)).fetchall()
    conn.close()
    return patients

def get_all_patients():
    conn = get_db_connection()
    patients = conn.execute('''
        SELECT p.*, d.name as dept_name 
        FROM patients p 
        LEFT JOIN departments d ON p.department_id = d.id
        ORDER BY p.priority_score DESC, p.timestamp ASC
    ''').fetchall()
    conn.close()
    return patients

def get_department_by_name(name):
    conn = get_db_connection()
    dept = conn.execute('SELECT * FROM departments WHERE name = ?', (name,)).fetchone()
    conn.close()
    return dept

def get_all_stats():
    conn = get_db_connection()
    
    total_patients = conn.execute('SELECT COUNT(*) FROM patients').fetchone()[0]
    
    dept_stats = conn.execute('''
        SELECT d.name, COUNT(p.id) as count 
        FROM departments d 
        LEFT JOIN patients p ON d.id = p.department_id 
        GROUP BY d.id
    ''').fetchall()
    
    # Get recent patients for global queue view
    recent_patients = conn.execute('''
        SELECT p.name, p.priority_level, d.name as dept_name, p.timestamp 
        FROM patients p 
        JOIN departments d ON p.department_id = d.id 
        ORDER BY p.timestamp DESC LIMIT 10
    ''').fetchall()

    conn.close()
    return {
        'total_patients': total_patients,
        'dept_stats': [dict(row) for row in dept_stats],
        'recent_patients': [dict(row) for row in recent_patients]
    }

def clear_patient_data():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM patients')
    c.execute('DELETE FROM sqlite_sequence WHERE name="patients"')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
