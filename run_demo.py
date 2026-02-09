#!/usr/bin/env python3
"""
Demo script for Telemedicine Queue Optimizer
Adds sample patients for demonstration purposes
"""

import sqlite3
import random
from datetime import datetime, timedelta
from ml_engine import MLEngine
from department_recommender import DepartmentRecommender

def add_sample_patients():
    """Add sample patients to demonstrate the system"""
    
    # Initialize ML components
    ml_engine = MLEngine()
    dept_recommender = DepartmentRecommender()
    
    # Sample patient data
    sample_patients = [
        {
            'name': 'Maria Rodriguez',
            'age': 67,
            'gender': 'Female',
            'location': 'Rural',
            'main_issue': 'Chest pain and difficulty breathing for 2 hours',
            'symptom_severity': 9,
            'chronic_illness': True,
            'pregnancy_elderly': True,
            'travel_distance': 85.5
        },
        {
            'name': 'James Thompson',
            'age': 34,
            'gender': 'Male',
            'location': 'Urban',
            'main_issue': 'Severe back pain after lifting heavy objects',
            'symptom_severity': 7,
            'chronic_illness': False,
            'pregnancy_elderly': False,
            'travel_distance': 12.3
        },
        {
            'name': 'Sarah Johnson',
            'age': 28,
            'gender': 'Female',
            'location': 'Rural',
            'main_issue': 'Pregnancy complications, bleeding and cramping',
            'symptom_severity': 8,
            'chronic_illness': False,
            'pregnancy_elderly': True,
            'travel_distance': 67.2
        },
        {
            'name': 'Michael Chen',
            'age': 45,
            'gender': 'Male',
            'location': 'Urban',
            'main_issue': 'Persistent headache and dizziness for 3 days',
            'symptom_severity': 6,
            'chronic_illness': True,
            'pregnancy_elderly': False,
            'travel_distance': 8.7
        },
        {
            'name': 'Emma Wilson',
            'age': 3,
            'gender': 'Female',
            'location': 'Rural',
            'main_issue': 'High fever and difficulty breathing in toddler',
            'symptom_severity': 8,
            'chronic_illness': False,
            'pregnancy_elderly': False,
            'travel_distance': 45.8
        },
        {
            'name': 'Robert Davis',
            'age': 72,
            'gender': 'Male',
            'location': 'Rural',
            'main_issue': 'Heart palpitations and chest tightness',
            'symptom_severity': 7,
            'chronic_illness': True,
            'pregnancy_elderly': True,
            'travel_distance': 92.1
        },
        {
            'name': 'Lisa Anderson',
            'age': 29,
            'gender': 'Female',
            'location': 'Urban',
            'main_issue': 'Skin rash and severe itching all over body',
            'symptom_severity': 5,
            'chronic_illness': False,
            'pregnancy_elderly': False,
            'travel_distance': 15.4
        },
        {
            'name': 'David Martinez',
            'age': 52,
            'gender': 'Male',
            'location': 'Rural',
            'main_issue': 'Joint pain and swelling in knees and hands',
            'symptom_severity': 6,
            'chronic_illness': True,
            'pregnancy_elderly': False,
            'travel_distance': 38.9
        },
        {
            'name': 'Jennifer Brown',
            'age': 31,
            'gender': 'Female',
            'location': 'Urban',
            'main_issue': 'Severe migraine with nausea and light sensitivity',
            'symptom_severity': 8,
            'chronic_illness': False,
            'pregnancy_elderly': False,
            'travel_distance': 6.2
        },
        {
            'name': 'William Garcia',
            'age': 19,
            'gender': 'Male',
            'location': 'Rural',
            'main_issue': 'Sports injury - possible ankle fracture',
            'symptom_severity': 7,
            'chronic_illness': False,
            'pregnancy_elderly': False,
            'travel_distance': 28.7
        }
    ]
    
    conn = sqlite3.connect('telemedicine.db')
    cursor = conn.cursor()
    
    print("Adding sample patients to demonstrate the system...")
    
    for i, patient_data in enumerate(sample_patients):
        # Calculate urgency score and priority using ML
        urgency_score, priority_level = ml_engine.predict_urgency(patient_data)
        
        # Get department recommendation
        recommended_dept = dept_recommender.recommend_department(patient_data['main_issue'])
        
        # Calculate queue position
        cursor.execute('''
            SELECT COUNT(*) FROM patients 
            WHERE recommended_department = ? AND urgency_score > ?
        ''', (recommended_dept, urgency_score))
        
        queue_position = cursor.fetchone()[0] + 1
        
        # Create timestamp (spread over last 2 hours)
        created_at = datetime.now() - timedelta(minutes=random.randint(0, 120))
        
        # Insert patient
        cursor.execute('''
            INSERT INTO patients (name, age, gender, location, main_issue, symptom_severity,
                                chronic_illness, pregnancy_elderly, travel_distance, urgency_score,
                                priority_level, recommended_department, queue_position, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            patient_data['name'],
            patient_data['age'],
            patient_data['gender'],
            patient_data['location'],
            patient_data['main_issue'],
            patient_data['symptom_severity'],
            patient_data['chronic_illness'],
            patient_data['pregnancy_elderly'],
            patient_data['travel_distance'],
            urgency_score,
            priority_level,
            recommended_dept,
            queue_position,
            created_at.strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        print(f"✓ Added {patient_data['name']} - {priority_level} priority, {recommended_dept}")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Successfully added {len(sample_patients)} sample patients!")
    print("\nDemo patients include:")
    print("- Emergency cases (chest pain, pregnancy complications)")
    print("- Rural patients with travel distance priority")
    print("- Chronic illness cases")
    print("- Pediatric cases")
    print("- Various departments (Cardiology, Orthopedics, Gynecology, etc.)")
    
    print("\n🚀 Ready for demo! Start the application with: python app.py")

def show_demo_info():
    """Display demo information and credentials"""
    print("=" * 60)
    print("🏥 TELEMEDICINE QUEUE OPTIMIZER - DEMO SETUP")
    print("=" * 60)
    
    print("\n📋 DEMO CREDENTIALS:")
    print("\n👨‍⚕️ Doctor Logins (any password works):")
    print("  • General Medicine: sarah@doctor.com")
    print("  • Cardiology: michael@doctor.com")
    print("  • Orthopedics: emily@doctor.com")
    print("  • Gynecology: david@doctor.com")
    print("  • Pediatrics: lisa@doctor.com")
    
    print("\n👨‍💼 Admin Login:")
    print("  • Email: admin@gmail.com")
    print("  • Password: any password")
    
    print("\n🌐 ACCESS URLS:")
    print("  • Patient Registration: http://localhost:5000")
    print("  • Doctor Login: http://localhost:5000/doctor_login")
    print("  • Admin Login: http://localhost:5000/admin_login")
    
    print("\n🎯 DEMO FLOW:")
    print("  1. Register as a patient with symptoms")
    print("  2. See AI-powered department recommendation")
    print("  3. Login as doctor to see department queue")
    print("  4. Login as admin to see system overview")
    
    print("\n⭐ KEY FEATURES TO DEMONSTRATE:")
    print("  • ML-based urgency scoring")
    print("  • Rural patient prioritization")
    print("  • Department recommendation AI")
    print("  • Role-based dashboards")
    print("  • Live queue updates")
    print("  • Priority color coding")
    print("  • Search and filtering")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    show_demo_info()
    
    # Ask if user wants to add sample data
    response = input("\n🤔 Add sample patients for demo? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        add_sample_patients()
    else:
        print("\n✅ Skipping sample data. You can add patients manually through the web interface.")
    
    print("\n🚀 Run the application with: python app.py")
    print("📱 Then open: http://localhost:5000")