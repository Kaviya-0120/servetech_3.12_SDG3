#!/usr/bin/env python3
"""
Script to populate test data for analytics charts
"""

import sqlite3
import random
from datetime import datetime, timedelta

def populate_test_data():
    """Populate database with test patient data"""
    conn = sqlite3.connect('hospital_system.db')
    cursor = conn.cursor()
    
    # Sample patient data
    departments = ['Cardiology', 'General Medicine', 'Emergency', 'Pulmonology', 'Dermatology', 'Orthopedics', 'Neurology']
    severities = ['Mild', 'Moderate', 'Severe']
    genders = ['Male', 'Female']
    statuses = ['waiting', 'confirmed', 'in-consultation', 'completed']
    
    # Sample symptoms by department
    symptoms_by_dept = {
        'Cardiology': ['Chest pain', 'Heart palpitations', 'Shortness of breath', 'High blood pressure'],
        'General Medicine': ['Fever', 'Headache', 'Fatigue', 'Body aches'],
        'Emergency': ['Severe chest pain', 'Difficulty breathing', 'Severe bleeding', 'Unconsciousness'],
        'Pulmonology': ['Chronic cough', 'Breathing difficulties', 'Asthma attack', 'Lung pain'],
        'Dermatology': ['Skin rash', 'Acne', 'Eczema', 'Allergic reaction'],
        'Orthopedics': ['Joint pain', 'Back pain', 'Fracture', 'Muscle strain'],
        'Neurology': ['Headache', 'Dizziness', 'Memory issues', 'Seizures']
    }
    
    # Generate test patients for the last 7 days
    for i in range(50):  # Generate 50 test patients
        # Random date within last 7 days
        days_ago = random.randint(0, 6)
        created_date = datetime.now() - timedelta(days=days_ago)
        
        # Random department
        department = random.choice(departments)
        
        # Random patient data
        name = f"Test Patient {i+1}"
        age = random.randint(18, 80)
        gender = random.choice(genders)
        phone = f"+1-555-{random.randint(1000, 9999)}"
        email = f"patient{i+1}@test.com"
        
        # Department-specific symptom
        symptom = random.choice(symptoms_by_dept[department])
        severity = random.choice(severities)
        symptom_days = random.randint(1, 14)
        
        # Emergency cases more likely for Emergency department
        is_emergency = department == 'Emergency' and random.random() < 0.7
        
        # Calculate risk score based on severity and emergency
        base_risk = {'Mild': 20, 'Moderate': 50, 'Severe': 80}[severity]
        age_factor = 20 if age > 65 else 10 if age < 18 else 0
        emergency_factor = 30 if is_emergency else 0
        risk_score = min(100, base_risk + age_factor + emergency_factor + random.randint(-10, 10))
        
        # Status distribution
        status = random.choices(statuses, weights=[30, 40, 20, 10])[0]
        
        # Registration ID
        reg_id = f"MED{100000 + i}"
        
        # Appointment time for confirmed patients
        appointment_time = None
        if status in ['confirmed', 'in-consultation', 'completed']:
            appointment_time = (created_date + timedelta(hours=random.randint(2, 48))).isoformat()
        
        try:
            cursor.execute('''
                INSERT INTO patients (registration_id, name, age, gender, phone, email,
                                    main_symptom, severity, symptom_days, is_emergency,
                                    department, risk_score, status, created_at, appointment_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (reg_id, name, age, gender, phone, email, symptom, severity, 
                  symptom_days, is_emergency, department, risk_score, status, 
                  created_date.isoformat(), appointment_time))
            
            # Create emergency alerts for high-risk cases
            if risk_score >= 80 or is_emergency:
                cursor.execute('''
                    INSERT INTO emergency_alerts (patient_id, alert_type, message, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (cursor.lastrowid, 'high_risk', 
                      f'High-risk patient {name} requires immediate attention',
                      created_date.isoformat()))
                      
        except sqlite3.IntegrityError:
            # Skip if registration ID already exists
            continue
    
    conn.commit()
    conn.close()
    
    print(f"✅ Successfully populated database with test patient data")
    print("📊 Data includes:")
    print(f"   - Patients across {len(departments)} departments")
    print(f"   - Various risk levels and severities")
    print(f"   - Data spread across last 7 days")
    print(f"   - Emergency cases and alerts")

def show_data_summary():
    """Show summary of current data"""
    conn = sqlite3.connect('hospital_system.db')
    cursor = conn.cursor()
    
    # Total patients
    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]
    
    # Department breakdown
    cursor.execute('''
        SELECT department, COUNT(*) as count 
        FROM patients 
        GROUP BY department 
        ORDER BY count DESC
    ''')
    dept_breakdown = cursor.fetchall()
    
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
    risk_breakdown = cursor.fetchall()
    
    conn.close()
    
    print("\n📈 Current Database Summary:")
    print(f"Total Patients: {total_patients}")
    
    print("\n🏢 Department Breakdown:")
    for dept, count in dept_breakdown:
        print(f"   {dept}: {count} patients")
    
    print("\n⚠️ Risk Level Distribution:")
    for risk, count in risk_breakdown:
        print(f"   {risk}: {count} patients")

if __name__ == "__main__":
    print("🧪 Populating Test Data for Analytics")
    print("=" * 50)
    
    populate_test_data()
    show_data_summary()
    
    print("\n🎯 Ready for Analytics Testing!")
    print("Start the hospital system and visit /admin/analytics to see the charts.")