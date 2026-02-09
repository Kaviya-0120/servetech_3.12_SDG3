#!/usr/bin/env python3
"""
Demo script for the Hospital-Grade Telemedicine Queue Optimizer
This script demonstrates the key features and functionality.
"""

import subprocess
import webbrowser
import time
import sys
import os

def print_banner():
    print("=" * 80)
    print("🏥 HOSPITAL-GRADE TELEMEDICINE QUEUE OPTIMIZER - DEMO")
    print("=" * 80)
    print()
    print("✨ ENHANCED FEATURES COMPLETED:")
    print("   • Professional hospital-grade UI/UX with medical theme")
    print("   • Complete admin dashboard with patient management table")
    print("   • Patient confirmation system with appointment scheduling")
    print("   • PDF report generation functionality")
    print("   • Real-time status tracking (Waiting → Confirmed → Completed)")
    print("   • Emergency priority handling with risk score boosting")
    print("   • Comprehensive patient information display")
    print("   • Role-based access control (Patient/Admin)")
    print("   • Responsive design for all devices")
    print()
    print("🔐 DEMO CREDENTIALS:")
    print("   Admin Username: admin")
    print("   Admin Password: hospital2024")
    print()
    print("📋 DEMO WORKFLOW:")
    print("   1. Patient registers for appointment")
    print("   2. System calculates risk score and assigns department")
    print("   3. Admin reviews and confirms appointments")
    print("   4. Admin can generate detailed patient reports")
    print("   5. Patients can check their appointment status")
    print()

def main():
    print_banner()
    
    # Check if we're in the right directory
    if not os.path.exists('hospital_fixed.py'):
        print("❌ Error: hospital_fixed.py not found!")
        print("Please run this script from the telemedicine_queue_optimizer directory.")
        return
    
    try:
        print("🚀 Starting Hospital System...")
        print("   Server will start at: http://127.0.0.1:5000")
        print("   Press Ctrl+C to stop the server")
        print()
        
        # Wait a moment then open browser
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://127.0.0.1:5000')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the Flask application
        subprocess.run([sys.executable, 'hospital_fixed.py'], check=True)
        
    except KeyboardInterrupt:
        print("\n\n✅ Hospital System stopped successfully!")
        print("Thank you for testing the enhanced telemedicine system!")
    except Exception as e:
        print(f"\n❌ Error starting system: {e}")
        print("Please ensure Python and Flask are properly installed.")

if __name__ == '__main__':
    main()