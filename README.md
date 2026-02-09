# 🏥 Hospital-Grade Telemedicine Queue Optimizer

A comprehensive, hospital-grade telemedicine queue optimization system built with Flask, featuring ML-based patient prioritization, advanced admin controls, and professional healthcare UI/UX.

## ✨ Features

### 🎯 Core Functionality
- **Smart Patient Registration**: Conditional form logic with emergency handling
- **ML-Powered Risk Assessment**: Advanced scoring algorithm for patient prioritization
- **Intelligent Department Mapping**: Symptom-to-department recommendation system
- **Real-time Queue Management**: Live updates and status tracking
- **Emergency Priority System**: Automatic escalation for critical cases

### 👥 Multi-Role Access System
- **Patient Portal**: Registration, status checking, appointment tracking
- **Admin Dashboard**: Complete hospital management system
- **Professional UI/UX**: Healthcare-themed design with modern interface

### 📊 Advanced Admin Features
- **Analytics Dashboard**: Comprehensive insights with charts and KPIs
- **Reports Center**: Generate daily, weekly, and custom reports
- **Settings Panel**: System configuration and preferences
- **Patient Management**: Full CRUD operations with confirmation system
- **PDF Report Generation**: Detailed patient consultation reports

### 🚨 Emergency & Safety Features
- **Emergency Detection**: Automatic risk score boosting
- **Alert System**: Real-time notifications for critical cases
- **Status Tracking**: Waiting → Confirmed → In Consultation → Completed
- **Appointment Scheduling**: Time slot management with confirmation

## 🛠️ Tech Stack

- **Backend**: Python Flask with SQLite database
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **ML Engine**: scikit-learn for risk assessment
- **Charts**: Chart.js for analytics visualization
- **UI Framework**: Custom healthcare-themed CSS with responsive design
- **Security**: Session management, role-based access control

## 📁 Project Structure

```
telemedicine_queue_optimizer/
├── hospital_fixed.py          # Main application (latest version)
├── app.py                     # Original MVP version
├── healthcare_saas_app.py     # SaaS redesign version
├── hospital_grade_system.py   # Hospital-grade upgrade
├── ml_engine.py              # Machine learning algorithms
├── department_recommender.py  # Symptom-to-department mapping
├── requirements.txt          # Python dependencies
├── demo_hospital_system.py   # Demo launcher script
├── static/
│   ├── css/style.css        # Styling
│   └── js/main.js           # JavaScript functionality
├── templates/               # HTML templates
└── *.db                    # SQLite databases
```

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/Kaviya-0120/servetech_3.12_SDG3.git
cd servetech_3.12_SDG3
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python hospital_fixed.py
```

4. **Access the system**:
   - Open your browser to `http://localhost:5000`
   - The system will automatically initialize the database

### Demo Launch
```bash
python demo_hospital_system.py
```

## 🔐 Demo Credentials

### Admin Access
- **Username**: `admin`
- **Password**: `hospital2024`
- **Features**: Full system access, patient management, analytics, reports, settings

### Patient Access
- **No login required**
- **Features**: Registration, status checking, appointment tracking

## 📋 Usage Guide

### For Patients
1. **Register**: Fill out the smart registration form
2. **Emergency**: Toggle emergency flag for priority handling
3. **Track Status**: Use registration ID to check appointment status
4. **Receive Care**: Get department recommendation and appointment confirmation

### For Administrators
1. **Dashboard**: Monitor real-time hospital operations
2. **Patient Management**: Confirm appointments, generate reports
3. **Analytics**: View trends, performance metrics, and insights
4. **Reports**: Generate daily, weekly, and custom reports
5. **Settings**: Configure system preferences and hospital details

## 🎯 Key Algorithms

### Risk Assessment Engine
```python
def calculate_risk_score(patient_data):
    score = 0
    # Severity scoring (20-80 points)
    score += severity_scores.get(severity, 20)
    # Age factor (0-30 points)
    if age < 2 or age > 70: score += 30
    # Symptom duration (0-15 points)
    if symptom_days > 7: score += 15
    # Emergency flag (+40 points)
    if is_emergency: score += 40
    return min(100, score)
```

### Department Mapping
- **Emergency**: Chest pain, heart attack, stroke, severe bleeding
- **Cardiology**: Heart-related symptoms, blood pressure issues
- **Pulmonology**: Breathing problems, cough, lung issues
- **Dermatology**: Skin conditions, rashes, allergies
- **General Medicine**: Default for unspecified symptoms

## 📊 System Capabilities

### Analytics & Reporting
- **Real-time Dashboards**: Live patient statistics and KPIs
- **Trend Analysis**: Weekly patient trends and department performance
- **Risk Distribution**: Visual breakdown of patient risk levels
- **Performance Metrics**: Response times, satisfaction scores, uptime

### Data Management
- **Patient Records**: Comprehensive patient information storage
- **Appointment Tracking**: Full lifecycle management
- **Emergency Alerts**: Automated notification system
- **Audit Trail**: Complete system activity logging

## 🔧 Configuration

### System Settings
- **Hospital Information**: Name, address, working hours
- **Emergency Thresholds**: Risk score limits for alerts
- **Notification Preferences**: Email alerts, emergency notifications
- **User Management**: Admin profiles and permissions

### Database Schema
- **Patients**: Registration, medical info, status tracking
- **Admin Users**: Authentication and profile management
- **Emergency Alerts**: Critical case notifications
- **System Settings**: Configuration parameters

## 🌟 Advanced Features

### Emergency Handling
- **Automatic Detection**: Keywords and severity-based flagging
- **Priority Boosting**: Risk score enhancement for urgent cases
- **Alert Generation**: Real-time notifications to admin and medical staff
- **Queue Reordering**: Dynamic prioritization based on urgency

### Professional UI/UX
- **Healthcare Theme**: Medical-grade color scheme and typography
- **Responsive Design**: Mobile-friendly interface
- **Accessibility**: WCAG compliant design elements
- **Professional Cards**: Clean, structured information display

## 🔒 Security Features

- **Role-Based Access**: Patient, Admin role separation
- **Session Management**: Secure authentication system
- **Data Protection**: SQLite with proper schema design
- **Input Validation**: Form sanitization and validation

## 📈 Performance & Scalability

- **Optimized Queries**: Efficient database operations
- **Real-time Updates**: 30-second auto-refresh intervals
- **Caching Strategy**: Session-based data management
- **Scalable Architecture**: Modular design for easy expansion

## 🤝 Contributing

This project was developed as part of the Servetech 3.12 SDG3 (Good Health and Well-being) initiative. Contributions are welcome!

## 📄 License

This project is developed for educational and healthcare improvement purposes as part of the UN SDG3 initiative.

## 🏆 Project Evolution

1. **MVP Version** (`app.py`): Basic 3-role system with ML prioritization
2. **SaaS Redesign** (`healthcare_saas_app.py`): Professional user flow and conditional forms
3. **Hospital-Grade** (`hospital_grade_system.py`): Advanced features and analytics
4. **Production Ready** (`hospital_fixed.py`): Complete system with all features working

## 📞 Support

For technical support or questions about the telemedicine queue optimizer system, please refer to the documentation or create an issue in the repository.

---

**Built with ❤️ for better healthcare accessibility and efficiency**