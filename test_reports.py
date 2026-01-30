#!/usr/bin/env python3
"""
Test script for report generation functionality
"""

from report_generator import ReportGenerator
from datetime import datetime

def test_patient_report():
    """Test patient PDF report generation"""
    print("Testing patient PDF report generation...")
    
    # Sample patient data
    patient_data = {
        'patient_name': 'John Doe',
        'registration_id': 'MED123456',
        'age': 35,
        'gender': 'Male',
        'phone': '+1-555-0123',
        'symptom': 'Chest pain and shortness of breath',
        'severity': 'Severe',
        'department': 'Cardiology',
        'risk_score': 85,
        'status': 'confirmed',
        'created_at': datetime.now().isoformat(),
        'appointment_time': datetime.now().isoformat(),
        'is_emergency': True
    }
    
    try:
        report_generator = ReportGenerator()
        pdf_buffer = report_generator.generate_patient_pdf_report(patient_data)
        
        # Save to file for testing
        with open('test_patient_report.pdf', 'wb') as f:
            f.write(pdf_buffer.getvalue())
        
        print("✅ Patient PDF report generated successfully: test_patient_report.pdf")
        return True
    except Exception as e:
        print(f"❌ Error generating patient PDF report: {e}")
        return False

def test_daily_report():
    """Test daily PDF report generation"""
    print("Testing daily PDF report generation...")
    
    # Sample daily report data
    report_data = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'total_patients': 25,
        'high_risk_patients': 8,
        'confirmed_appointments': 18,
        'department_breakdown': {
            'Cardiology': 8,
            'General Medicine': 10,
            'Emergency': 5,
            'Dermatology': 2
        },
        'generated_at': datetime.now().isoformat()
    }
    
    try:
        report_generator = ReportGenerator()
        pdf_buffer = report_generator.generate_daily_report_pdf(report_data)
        
        # Save to file for testing
        with open('test_daily_report.pdf', 'wb') as f:
            f.write(pdf_buffer.getvalue())
        
        print("✅ Daily PDF report generated successfully: test_daily_report.pdf")
        return True
    except Exception as e:
        print(f"❌ Error generating daily PDF report: {e}")
        return False

def test_excel_reports():
    """Test Excel report generation"""
    print("Testing Excel report generation...")
    
    # Sample patients data
    patients_data = [
        {
            'Registration ID': 'MED123456',
            'Name': 'John Doe',
            'Age': 35,
            'Gender': 'Male',
            'Phone': '+1-555-0123',
            'Email': 'john.doe@email.com',
            'Primary Symptom': 'Chest pain',
            'Severity': 'Severe',
            'Department': 'Cardiology',
            'Risk Score': 85,
            'Status': 'confirmed',
            'Registration Date': datetime.now().isoformat(),
            'Emergency': 'Yes',
            'Appointment Time': datetime.now().isoformat()
        },
        {
            'Registration ID': 'MED123457',
            'Name': 'Jane Smith',
            'Age': 28,
            'Gender': 'Female',
            'Phone': '+1-555-0124',
            'Email': 'jane.smith@email.com',
            'Primary Symptom': 'Skin rash',
            'Severity': 'Mild',
            'Department': 'Dermatology',
            'Risk Score': 25,
            'Status': 'waiting',
            'Registration Date': datetime.now().isoformat(),
            'Emergency': 'No',
            'Appointment Time': 'Not Scheduled'
        }
    ]
    
    try:
        report_generator = ReportGenerator()
        excel_buffer = report_generator.generate_patients_excel_report(patients_data)
        
        # Save to file for testing
        with open('test_patients_report.xlsx', 'wb') as f:
            f.write(excel_buffer.getvalue())
        
        print("✅ Patients Excel report generated successfully: test_patients_report.xlsx")
        return True
    except Exception as e:
        print(f"❌ Error generating Excel report: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Report Generation System")
    print("=" * 50)
    
    results = []
    results.append(test_patient_report())
    results.append(test_daily_report())
    results.append(test_excel_reports())
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {sum(results)}/{len(results)} tests passed")
    
    if all(results):
        print("🎉 All report generation tests passed!")
        print("\nGenerated test files:")
        print("- test_patient_report.pdf")
        print("- test_daily_report.pdf")
        print("- test_patients_report.xlsx")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()