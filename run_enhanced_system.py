#!/usr/bin/env python3
"""
Simple runner for the Enhanced Multilingual Telemedicine Queue Optimizer
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 Starting Enhanced Multilingual Telemedicine Queue Optimizer")
    print("=" * 60)
    
    try:
        # Import and initialize the system
        from enhanced_hospital_system_fixed import app, init_hospital_db
        
        print("✅ Successfully imported enhanced system")
        
        # Initialize database
        print("🔧 Initializing database...")
        init_hospital_db()
        print("✅ Database initialized successfully")
        
        print("\n🌐 Enhanced Features:")
        print("   • Multilingual Support (English, Hindi, Tamil)")
        print("   • Voice Assistant for Patients")
        print("   • Professional Healthcare UI/UX")
        print("   • Enhanced Admin Dashboard")
        print("   • Notification System")
        
        print(f"\n🚀 Starting server on http://localhost:5000")
        print("   📱 Access from mobile devices using your computer's IP")
        print("   🎤 Voice features work best in Chrome/Edge browsers")
        print("   🌍 Select your language at the homepage")
        
        print("\n" + "=" * 60)
        print("🏥 MediCare Hospital - Enhanced Digital Healthcare Platform")
        print("=" * 60)
        
        # Start the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Please ensure all required files are present")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting system: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()