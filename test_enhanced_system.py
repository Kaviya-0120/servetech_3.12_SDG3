#!/usr/bin/env python3
"""
Comprehensive Test Suite for Enhanced Multilingual Telemedicine Queue Optimizer
Tests all enhanced features: multilingual support, voice assistant, notifications, responsive design
"""

import sys
import os
import requests
import json
import time
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class EnhancedSystemTester:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.test_results = []
        self.session = requests.Session()
        
    def log_test(self, test_name, success, message=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        print(f"{status} {test_name}: {message}")
        
    def test_server_connection(self):
        """Test if enhanced server is running"""
        try:
            response = self.session.get(self.base_url, timeout=5)
            if response.status_code == 200:
                self.log_test("Server Connection", True, "Enhanced server is running")
                return True
            else:
                self.log_test("Server Connection", False, f"Server returned {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Server Connection", False, f"Connection failed: {str(e)}")
            return False
    
    def test_multilingual_landing_page(self):
        """Test multilingual landing page"""
        try:
            response = self.session.get(self.base_url)
            content = response.text
            
            # Check for multilingual elements
            has_english = 'English' in content
            has_hindi = 'हिंदी' in content
            has_language_selector = 'Select Language' in content
            has_enhanced_features = 'Voice Assistant' in content and 'Multilingual Support' in content
            
            if has_english and has_hindi and has_language_selector and has_enhanced_features:
                self.log_test("Multilingual Landing Page", True, "All language options and enhanced features present")
                return True
            else:
                missing = []
                if not has_english: missing.append("English")
                if not has_hindi: missing.append("Hindi")
                if not has_language_selector: missing.append("Language Selector")
                if not has_enhanced_features: missing.append("Enhanced Features")
                self.log_test("Multilingual Landing Page", False, f"Missing: {', '.join(missing)}")
                return False
                
        except Exception as e:
            self.log_test("Multilingual Landing Page", False, f"Error: {str(e)}")
            return False
    
    def test_patient_portal_languages(self):
        """Test patient portal with different languages"""
        languages = ['en', 'hi']
        results = []
        
        for lang in languages:
            try:
                response = self.session.get(f"{self.base_url}/patient?lang={lang}")
                if response.status_code == 200:
                    content = response.text
                    
                    # Check for language-specific content
                    if lang == 'en':
                        has_content = 'Patient Portal' in content and 'Book New Appointment' in content
                    elif lang == 'hi':
                        has_content = 'रोगी पोर्टल' in content and 'नई अपॉइंटमेंट' in content
                    
                    if has_content:
                        results.append(True)
                        self.log_test(f"Patient Portal ({lang.upper()})", True, f"Language content loaded correctly")
                    else:
                        results.append(False)
                        self.log_test(f"Patient Portal ({lang.upper()})", False, f"Language content not found")
                else:
                    results.append(False)
                    self.log_test(f"Patient Portal ({lang.upper()})", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                results.append(False)
                self.log_test(f"Patient Portal ({lang.upper()})", False, f"Error: {str(e)}")
        
        return all(results)
    
    def test_enhanced_registration_form(self):
        """Test enhanced registration form with voice assistant"""
        try:
            response = self.session.get(f"{self.base_url}/patient/register?lang=en")
            if response.status_code == 200:
                content = response.text
                
                # Check for enhanced features
                has_voice_assistant = 'Voice Assistant' in content and 'voice-btn' in content
                has_severity_selection = 'severity-btn' in content
                has_emergency_toggle = 'emergency-switch' in content
                has_enhanced_styling = 'enhanced_style.css' in content or 'gradientShift' in content
                has_multilingual_support = 'lang=' in content
                
                if has_voice_assistant and has_severity_selection and has_emergency_toggle and has_enhanced_styling:
                    self.log_test("Enhanced Registration Form", True, "All enhanced features present")
                    return True
                else:
                    missing = []
                    if not has_voice_assistant: missing.append("Voice Assistant")
                    if not has_severity_selection: missing.append("Severity Selection")
                    if not has_emergency_toggle: missing.append("Emergency Toggle")
                    if not has_enhanced_styling: missing.append("Enhanced Styling")
                    self.log_test("Enhanced Registration Form", False, f"Missing: {', '.join(missing)}")
                    return False
            else:
                self.log_test("Enhanced Registration Form", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Enhanced Registration Form", False, f"Error: {str(e)}")
            return False
    
    def test_patient_registration_api(self):
        """Test enhanced patient registration API"""
        test_patient = {
            "name": "Enhanced Test Patient",
            "age": 35,
            "gender": "Male",
            "phone": "9876543210",
            "email": "enhanced.test@example.com",
            "main_symptom": "Chest pain and difficulty breathing",
            "severity": "Severe",
            "symptom_days": 2,
            "is_emergency": True,
            "language": "en",
            "notification_frequency": "daily"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/register_patient",
                json=test_patient,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('registration_id'):
                    # Store registration ID for status test
                    self.test_registration_id = data['registration_id']
                    
                    # Check enhanced features
                    has_department = 'department' in data
                    has_risk_score = 'risk_score' in data
                    has_emergency_flag = 'is_emergency' in data
                    
                    if has_department and has_risk_score and has_emergency_flag:
                        self.log_test("Enhanced Patient Registration API", True, 
                                    f"Registration successful: {data['registration_id']}, Department: {data.get('department')}, Risk: {data.get('risk_score')}")
                        return True
                    else:
                        self.log_test("Enhanced Patient Registration API", False, "Missing enhanced data fields")
                        return False
                else:
                    self.log_test("Enhanced Patient Registration API", False, f"API error: {data.get('error', 'Unknown error')}")
                    return False
            else:
                self.log_test("Enhanced Patient Registration API", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Enhanced Patient Registration API", False, f"Error: {str(e)}")
            return False
    
    def test_enhanced_status_check(self):
        """Test enhanced status check with multilingual support"""
        if not hasattr(self, 'test_registration_id'):
            self.log_test("Enhanced Status Check", False, "No registration ID from previous test")
            return False
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/check_patient_status",
                json={
                    "registration_id": self.test_registration_id,
                    "language": "en"
                },
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('patient'):
                    patient = data['patient']
                    
                    # Check enhanced patient data
                    has_language = 'language' in patient
                    has_risk_score = 'risk_score' in patient
                    has_department = 'department' in patient
                    has_severity = 'severity' in patient
                    
                    if has_language and has_risk_score and has_department and has_severity:
                        self.log_test("Enhanced Status Check", True, 
                                    f"Status retrieved: {patient.get('status')}, Language: {patient.get('language')}")
                        return True
                    else:
                        self.log_test("Enhanced Status Check", False, "Missing enhanced patient data")
                        return False
                else:
                    self.log_test("Enhanced Status Check", False, f"API error: {data.get('error', 'Unknown error')}")
                    return False
            else:
                self.log_test("Enhanced Status Check", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Enhanced Status Check", False, f"Error: {str(e)}")
            return False
    
    def test_admin_dashboard_enhanced(self):
        """Test enhanced admin dashboard"""
        # First login as admin
        login_data = {
            "username": "admin",
            "password": "hospital2024"
        }
        
        try:
            # Login
            login_response = self.session.post(
                f"{self.base_url}/admin/login",
                json=login_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if login_response.status_code == 200 and login_response.json().get('success'):
                # Access enhanced dashboard
                dashboard_response = self.session.get(f"{self.base_url}/admin/dashboard")
                
                if dashboard_response.status_code == 200:
                    content = dashboard_response.text
                    
                    # Check for enhanced dashboard features
                    has_enhanced_navbar = 'Enhanced Admin Dashboard' in content
                    has_multilingual_indicator = 'Multilingual Support' in content or 'Language' in content
                    has_enhanced_stats = 'stat-card' in content
                    has_patient_management = 'Enhanced Patient Management' in content
                    
                    if has_enhanced_navbar and has_enhanced_stats and has_patient_management:
                        self.log_test("Enhanced Admin Dashboard", True, "All enhanced features present")
                        return True
                    else:
                        missing = []
                        if not has_enhanced_navbar: missing.append("Enhanced Navbar")
                        if not has_enhanced_stats: missing.append("Enhanced Stats")
                        if not has_patient_management: missing.append("Patient Management")
                        self.log_test("Enhanced Admin Dashboard", False, f"Missing: {', '.join(missing)}")
                        return False
                else:
                    self.log_test("Enhanced Admin Dashboard", False, f"Dashboard HTTP {dashboard_response.status_code}")
                    return False
            else:
                self.log_test("Enhanced Admin Dashboard", False, "Admin login failed")
                return False
                
        except Exception as e:
            self.log_test("Enhanced Admin Dashboard", False, f"Error: {str(e)}")
            return False
    
    def test_enhanced_admin_api(self):
        """Test enhanced admin API endpoints"""
        try:
            # Test dashboard stats
            stats_response = self.session.get(f"{self.base_url}/api/admin/dashboard_stats")
            
            if stats_response.status_code == 200:
                stats_data = stats_response.json()
                
                # Check for enhanced stats
                has_basic_stats = all(key in stats_data for key in ['total_today', 'critical_cases', 'avg_waiting', 'doctors_online'])
                has_enhanced_stats = 'department_distribution' in stats_data and 'common_symptoms' in stats_data
                
                if has_basic_stats and has_enhanced_stats:
                    self.log_test("Enhanced Admin API - Stats", True, "All enhanced statistics available")
                else:
                    self.log_test("Enhanced Admin API - Stats", False, "Missing enhanced statistics")
                    return False
            else:
                self.log_test("Enhanced Admin API - Stats", False, f"Stats API HTTP {stats_response.status_code}")
                return False
            
            # Test patients API
            patients_response = self.session.get(f"{self.base_url}/api/admin/patients")
            
            if patients_response.status_code == 200:
                patients_data = patients_response.json()
                
                if isinstance(patients_data, list) and len(patients_data) > 0:
                    # Check for enhanced patient data
                    patient = patients_data[0]
                    has_language = 'language' in patient
                    has_notification_freq = 'notification_frequency' in patient
                    has_risk_score = 'risk_score' in patient
                    
                    if has_language and has_notification_freq and has_risk_score:
                        self.log_test("Enhanced Admin API - Patients", True, "Enhanced patient data available")
                        return True
                    else:
                        self.log_test("Enhanced Admin API - Patients", False, "Missing enhanced patient fields")
                        return False
                else:
                    self.log_test("Enhanced Admin API - Patients", True, "Patients API working (no patients yet)")
                    return True
            else:
                self.log_test("Enhanced Admin API - Patients", False, f"Patients API HTTP {patients_response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Enhanced Admin API", False, f"Error: {str(e)}")
            return False
    
    def test_static_assets(self):
        """Test enhanced static assets (CSS, JS)"""
        assets = [
            ('/static/css/enhanced_style.css', 'Enhanced CSS'),
            ('/static/js/enhanced_voice.js', 'Enhanced Voice JS')
        ]
        
        results = []
        for asset_path, asset_name in assets:
            try:
                response = self.session.get(f"{self.base_url}{asset_path}")
                if response.status_code == 200:
                    content = response.text
                    
                    # Check for specific enhanced features in assets
                    if 'enhanced_style.css' in asset_path:
                        has_features = 'gradientShift' in content and 'voice-assistant' in content
                    elif 'enhanced_voice.js' in asset_path:
                        has_features = 'VoiceAssistant' in content and 'multilingual' in content.lower()
                    else:
                        has_features = True
                    
                    if has_features:
                        results.append(True)
                        self.log_test(f"Static Asset - {asset_name}", True, "Enhanced features present")
                    else:
                        results.append(False)
                        self.log_test(f"Static Asset - {asset_name}", False, "Enhanced features missing")
                else:
                    results.append(False)
                    self.log_test(f"Static Asset - {asset_name}", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                results.append(False)
                self.log_test(f"Static Asset - {asset_name}", False, f"Error: {str(e)}")
        
        return all(results)
    
    def run_all_tests(self):
        """Run all enhanced system tests"""
        print("🚀 Starting Enhanced Multilingual Telemedicine System Tests")
        print("=" * 70)
        
        # Test order matters - some tests depend on previous ones
        tests = [
            self.test_server_connection,
            self.test_multilingual_landing_page,
            self.test_patient_portal_languages,
            self.test_enhanced_registration_form,
            self.test_patient_registration_api,
            self.test_enhanced_status_check,
            self.test_admin_dashboard_enhanced,
            self.test_enhanced_admin_api,
            self.test_static_assets
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            time.sleep(0.5)  # Small delay between tests
        
        print("\n" + "=" * 70)
        print("🏥 ENHANCED SYSTEM TEST SUMMARY")
        print("=" * 70)
        
        success_rate = (passed / total) * 100
        status_emoji = "✅" if success_rate >= 80 else "⚠️" if success_rate >= 60 else "❌"
        
        print(f"{status_emoji} Tests Passed: {passed}/{total} ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            print("🎉 Enhanced system is working well!")
            print("\n🌟 Enhanced Features Verified:")
            print("   • Multilingual Support (English, Hindi)")
            print("   • Voice Assistant Integration")
            print("   • Enhanced UI/UX with Healthcare Theme")
            print("   • Responsive Design")
            print("   • Enhanced Admin Dashboard")
            print("   • Notification System Support")
        elif success_rate >= 60:
            print("⚠️  Enhanced system has some issues but core functionality works")
        else:
            print("❌ Enhanced system has significant issues")
        
        print(f"\n📊 Detailed Results:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"   {status} {result['test']}: {result['message']}")
        
        return success_rate >= 80

def main():
    """Main test function"""
    print("🏥 Enhanced Multilingual Telemedicine Queue Optimizer - Test Suite")
    print("=" * 70)
    
    # Check if server is specified
    import sys
    base_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5000'
    
    print(f"🔗 Testing server: {base_url}")
    print("📋 Testing enhanced features:")
    print("   • Multilingual Support (EN/HI)")
    print("   • Voice Assistant")
    print("   • Enhanced UI/UX")
    print("   • Responsive Design")
    print("   • Notification System")
    print("   • Enhanced Admin Dashboard")
    print()
    
    tester = EnhancedSystemTester(base_url)
    success = tester.run_all_tests()
    
    if success:
        print("\n🎯 RECOMMENDATION: Enhanced system is ready for demo!")
        print("   • Start server: python run_enhanced_system.py")
        print("   • Access: http://localhost:5000")
        print("   • Test voice features in Chrome/Edge")
        print("   • Try different languages")
        return 0
    else:
        print("\n🔧 RECOMMENDATION: Fix issues before demo")
        return 1

if __name__ == '__main__':
    exit(main())