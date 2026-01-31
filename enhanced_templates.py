# Enhanced Templates for Multilingual Telemedicine System

ENHANCED_PATIENT_REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book Appointment - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(147, 197, 253, 0.1) 50%, rgba(219, 234, 254, 0.1) 100%),
                        url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><pattern id="medical" patternUnits="userSpaceOnUse" width="100" height="100"><circle cx="50" cy="50" r="2" fill="%23dbeafe" opacity="0.3"/><path d="M45 45h10v10h-10z" fill="%23bfdbfe" opacity="0.2"/></pattern></defs><rect width="100%" height="100%" fill="url(%23medical)"/></svg>');
            min-height: 100vh;
            padding: 20px;
            background-attachment: fixed;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 24px;
            padding: 48px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(59, 130, 246, 0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            position: relative;
        }
        .header::before {
            content: '';
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: linear-gradient(90deg, #3b82f6, #1d4ed8);
            border-radius: 2px;
        }
        .header h1 {
            color: #1e40af;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 12px;
            letter-spacing: -0.025em;
        }
        .header p {
            color: #64748b;
            font-size: 1.1rem;
            font-weight: 500;
        }
        .form-section {
            margin-bottom: 40px;
            padding: 32px;
            background: linear-gradient(135deg, rgba(248, 250, 252, 0.8), rgba(241, 245, 249, 0.6));
            border-radius: 20px;
            border: 1px solid rgba(226, 232, 240, 0.8);
            position: relative;
            overflow: hidden;
        }
        .form-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #3b82f6, #06b6d4);
        }
        .section-title {
            font-size: 1.4rem;
            color: #1e40af;
            margin-bottom: 24px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
        }
        .form-group.full-width {
            grid-column: 1 / -1;
        }
        .form-group label {
            margin-bottom: 8px;
            font-weight: 600;
            color: #1e40af;
            font-size: 0.95rem;
        }
        .form-group input, .form-group select, .form-group textarea {
            padding: 16px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.9);
            font-family: inherit;
        }
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
            background: rgba(255, 255, 255, 1);
        }
        .severity-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 16px;
            margin-top: 12px;
        }
        .severity-btn {
            padding: 24px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.9);
            cursor: pointer;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .severity-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
            transition: left 0.5s ease;
        }
        .severity-btn:hover::before {
            left: 100%;
        }
        .severity-btn.selected {
            border-color: #3b82f6;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(147, 197, 253, 0.1));
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
        }
        .severity-btn .severity-label {
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 4px;
        }
        .severity-btn.mild .severity-label { color: #059669; }
        .severity-btn.moderate .severity-label { color: #d97706; }
        .severity-btn.severe .severity-label { color: #dc2626; }
        .severity-btn .severity-desc {
            font-size: 0.85rem;
            color: #64748b;
            font-weight: 500;
        }
        .emergency-section {
            background: linear-gradient(135deg, rgba(254, 242, 242, 0.9), rgba(254, 226, 226, 0.7));
            border: 2px solid rgba(248, 113, 113, 0.3);
            border-radius: 20px;
            padding: 32px;
            margin: 32px 0;
            position: relative;
        }
        .emergency-section::before {
            content: '🚨';
            position: absolute;
            top: -15px;
            left: 24px;
            background: white;
            padding: 8px 12px;
            border-radius: 50%;
            font-size: 1.2rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .emergency-toggle {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 16px;
        }
        .emergency-switch {
            position: relative;
            width: 64px;
            height: 32px;
            background: #cbd5e1;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .emergency-switch.active {
            background: linear-gradient(135deg, #dc2626, #b91c1c);
        }
        .emergency-switch::before {
            content: '';
            position: absolute;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: white;
            top: 2px;
            left: 2px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        .emergency-switch.active::before {
            transform: translateX(32px);
        }
        .emergency-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #dc2626;
        }
        .emergency-desc {
            color: #991b1b;
            font-size: 0.95rem;
            line-height: 1.6;
            font-weight: 500;
        }
        .submit-btn {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            border: none;
            padding: 20px 40px;
            border-radius: 16px;
            font-size: 1.2rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-top: 40px;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        .submit-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s ease;
        }
        .submit-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 20px 40px rgba(59, 130, 246, 0.4);
        }
        .submit-btn:hover::before {
            left: 100%;
        }
        .back-btn {
            background: linear-gradient(135deg, #64748b, #475569);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 12px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 32px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .back-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(100, 116, 139, 0.3);
        }
        @media (max-width: 768px) {
            .container { padding: 24px; }
            .form-section { padding: 24px; }
            .form-grid { grid-template-columns: 1fr; }
            .severity-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 Book Appointment</h1>
            <p>Please fill out your information for medical consultation</p>
        </div>
        
        <a href="/patient" class="back-btn">← Back to Patient Portal</a>
        
        <form id="registrationForm">
            <div class="form-section">
                <div class="section-title">
                    👤 Personal Information
                </div>
                <div class="form-grid">
                    <div class="form-group">
                        <label for="name">Full Name *</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="age">Age *</label>
                        <input type="number" id="age" name="age" min="1" max="120" required>
                    </div>
                    <div class="form-group">
                        <label for="gender">Gender *</label>
                        <select id="gender" name="gender" required>
                            <option value="">Select Gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="phone">Phone Number *</label>
                        <input type="tel" id="phone" name="phone" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email Address</label>
                        <input type="email" id="email" name="email">
                    </div>
                </div>
            </div>
            
            <div class="form-section">
                <div class="section-title">
                    🩺 Medical Information
                </div>
                
                <div class="form-group full-width">
                    <label for="main_symptom">Primary Symptom/Concern *</label>
                    <textarea id="main_symptom" name="main_symptom" rows="4" 
                              placeholder="Please describe your main health concern in detail..." required></textarea>
                </div>
                
                <div class="form-group">
                    <label>Symptom Severity *</label>
                    <div class="severity-grid">
                        <div class="severity-btn mild" onclick="selectSeverity('Mild', this)">
                            <div class="severity-label">Mild</div>
                            <div class="severity-desc">Manageable discomfort</div>
                        </div>
                        <div class="severity-btn moderate" onclick="selectSeverity('Moderate', this)">
                            <div class="severity-label">Moderate</div>
                            <div class="severity-desc">Noticeable impact</div>
                        </div>
                        <div class="severity-btn severe" onclick="selectSeverity('Severe', this)">
                            <div class="severity-label">Severe</div>
                            <div class="severity-desc">Significant distress</div>
                        </div>
                    </div>
                    <input type="hidden" id="severity" name="severity" required>
                </div>
                
                <div class="form-group">
                    <label for="symptom_days">Duration of Symptoms *</label>
                    <select id="symptom_days" name="symptom_days" required>
                        <option value="">Select duration</option>
                        <option value="1">Today (1 day)</option>
                        <option value="2">2-3 days</option>
                        <option value="7">About a week</option>
                        <option value="14">About 2 weeks</option>
                        <option value="30">About a month</option>
                        <option value="90">More than a month</option>
                    </select>
                </div>
            </div>
            
            <div class="emergency-section">
                <div class="emergency-toggle">
                    <div class="emergency-switch" id="emergencySwitch" onclick="toggleEmergency()"></div>
                    <div class="emergency-title">This is an Emergency</div>
                </div>
                <div class="emergency-desc">
                    <strong>Emergency Priority:</strong> Selecting this option will prioritize your case and attempt to schedule you for immediate consultation.
                </div>
                <input type="hidden" id="is_emergency" name="is_emergency" value="false">
            </div>
            
            <button type="submit" class="submit-btn">
                📅 Book Appointment
            </button>
        </form>
    </div>

    <script>
        let selectedSeverity = '';
        let isEmergency = false;
        
        function selectSeverity(severity, element) {
            document.querySelectorAll('.severity-btn').forEach(btn => {
                btn.classList.remove('selected');
            });
            
            element.classList.add('selected');
            selectedSeverity = severity;
            document.getElementById('severity').value = severity;
        }
        
        function toggleEmergency() {
            const switchEl = document.getElementById('emergencySwitch');
            const hiddenInput = document.getElementById('is_emergency');
            
            isEmergency = !isEmergency;
            
            if (isEmergency) {
                switchEl.classList.add('active');
                hiddenInput.value = 'true';
            } else {
                switchEl.classList.remove('active');
                hiddenInput.value = 'false';
            }
        }
        
        document.getElementById('registrationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!selectedSeverity) {
                alert('Please select symptom severity');
                return;
            }
            
            const formData = {
                name: document.getElementById('name').value,
                age: parseInt(document.getElementById('age').value),
                gender: document.getElementById('gender').value,
                phone: document.getElementById('phone').value,
                email: document.getElementById('email').value,
                main_symptom: document.getElementById('main_symptom').value,
                severity: selectedSeverity,
                symptom_days: parseInt(document.getElementById('symptom_days').value),
                is_emergency: isEmergency
            };
            
            try {
                const response = await fetch('/api/register_patient', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert(`Registration successful!\\nRegistration ID: ${result.registration_id}\\nDepartment: ${result.department}`);
                    window.location.href = '/patient';
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        });
    </script>
</body>
</html>
'''

ENHANCED_PATIENT_STATUS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Check Status - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(147, 197, 253, 0.1) 50%, rgba(219, 234, 254, 0.1) 100%),
                        url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><pattern id="medical" patternUnits="userSpaceOnUse" width="100" height="100"><circle cx="50" cy="50" r="2" fill="%23dbeafe" opacity="0.3"/><path d="M45 45h10v10h-10z" fill="%23bfdbfe" opacity="0.2"/></pattern></defs><rect width="100%" height="100%" fill="url(%23medical)"/></svg>');
            min-height: 100vh;
            padding: 20px;
            background-attachment: fixed;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 24px;
            padding: 48px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(59, 130, 246, 0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            position: relative;
        }
        .header::before {
            content: '';
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: linear-gradient(90deg, #3b82f6, #1d4ed8);
            border-radius: 2px;
        }
        .header h1 {
            color: #1e40af;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 12px;
            letter-spacing: -0.025em;
        }
        .header p {
            color: #64748b;
            font-size: 1.1rem;
            font-weight: 500;
        }
        .search-section {
            background: linear-gradient(135deg, rgba(248, 250, 252, 0.8), rgba(241, 245, 249, 0.6));
            border-radius: 20px;
            padding: 32px;
            margin-bottom: 32px;
            border: 1px solid rgba(226, 232, 240, 0.8);
            position: relative;
        }
        .search-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #3b82f6, #06b6d4);
        }
        .form-group {
            margin-bottom: 24px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #1e40af;
            font-size: 0.95rem;
        }
        .form-group input {
            width: 100%;
            padding: 16px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 1.1rem;
            text-align: center;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.05em;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.9);
            font-family: 'Monaco', 'Menlo', monospace;
        }
        .form-group input:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
            background: rgba(255, 255, 255, 1);
        }
        .check-btn {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            border: none;
            padding: 18px 36px;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        .check-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s ease;
        }
        .check-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 20px 40px rgba(59, 130, 246, 0.4);
        }
        .check-btn:hover::before {
            left: 100%;
        }
        .back-btn {
            background: linear-gradient(135deg, #64748b, #475569);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 12px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 32px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .back-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(100, 116, 139, 0.3);
        }
        .status-result {
            margin-top: 32px;
            border-radius: 20px;
            display: none;
            overflow: hidden;
            border: 1px solid rgba(226, 232, 240, 0.8);
        }
        .status-success {
            background: linear-gradient(135deg, rgba(236, 253, 245, 0.9), rgba(209, 250, 229, 0.8));
            border-color: rgba(34, 197, 94, 0.3);
        }
        .status-error {
            background: linear-gradient(135deg, rgba(254, 242, 242, 0.9), rgba(254, 226, 226, 0.8));
            border-color: rgba(239, 68, 68, 0.3);
        }
        .status-header {
            padding: 24px 32px;
            border-bottom: 1px solid rgba(226, 232, 240, 0.5);
        }
        .status-success .status-header {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(22, 163, 74, 0.05));
        }
        .status-error .status-header {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.05));
        }
        .status-content {
            padding: 32px;
        }
        .patient-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .info-item {
            background: rgba(255, 255, 255, 0.8);
            padding: 16px;
            border-radius: 12px;
            border-left: 4px solid #3b82f6;
        }
        .info-label {
            font-size: 0.85rem;
            color: #64748b;
            font-weight: 500;
            margin-bottom: 4px;
        }
        .info-value {
            font-weight: 600;
            color: #1e40af;
            font-size: 1rem;
        }
        @media (max-width: 768px) {
            .container { padding: 24px; }
            .search-section { padding: 24px; }
            .patient-info { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Check Appointment Status</h1>
            <p>Enter your registration ID to check your appointment status</p>
        </div>
        
        <a href="/patient" class="back-btn">← Back to Patient Portal</a>
        
        <div class="search-section">
            <form id="statusForm">
                <div class="form-group">
                    <label for="registration_id">Registration ID</label>
                    <input type="text" id="registration_id" name="registration_id" placeholder="MED123456" required>
                </div>
                
                <button type="submit" class="check-btn">
                    🔍 Check Status
                </button>
            </form>
        </div>
        
        <div id="statusResult" class="status-result">
            <!-- Status information will be displayed here -->
        </div>
    </div>

    <script>
        document.getElementById('statusForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const registrationId = document.getElementById('registration_id').value.trim().toUpperCase();
            
            if (!registrationId) {
                alert('Please enter a registration ID');
                return;
            }
            
            try {
                const response = await fetch('/api/check_patient_status', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ registration_id: registrationId })
                });
                
                const result = await response.json();
                const statusDiv = document.getElementById('statusResult');
                
                if (result.success) {
                    const patient = result.patient;
                    statusDiv.className = 'status-result status-success';
                    statusDiv.innerHTML = `
                        <div class="status-header">
                            <h3 style="color: #059669; font-size: 1.5rem; font-weight: 700; display: flex; align-items: center; gap: 12px;">
                                ✅ Patient Found
                            </h3>
                        </div>
                        <div class="status-content">
                            <div style="text-align: center; margin-bottom: 24px;">
                                <h4 style="color: #1e40af; font-size: 1.8rem; font-weight: 700; margin-bottom: 8px;">${patient.name}</h4>
                                <div style="display: inline-block; padding: 8px 16px; background: rgba(34, 197, 94, 0.1); color: #059669; border-radius: 20px; font-weight: 600; text-transform: capitalize;">
                                    ${patient.status}
                                </div>
                            </div>
                            <div class="patient-info">
                                <div class="info-item">
                                    <div class="info-label">Registration ID</div>
                                    <div class="info-value">${patient.registration_id}</div>
                                </div>
                                <div class="info-item">
                                    <div class="info-label">Department</div>
                                    <div class="info-value">${patient.department}</div>
                                </div>
                                <div class="info-item">
                                    <div class="info-label">Risk Score</div>
                                    <div class="info-value">${patient.risk_score}/100</div>
                                </div>
                                <div class="info-item">
                                    <div class="info-label">Registered Date</div>
                                    <div class="info-value">${new Date(patient.registered_date).toLocaleDateString()}</div>
                                </div>
                                ${patient.appointment_time ? `
                                <div class="info-item">
                                    <div class="info-label">Appointment Time</div>
                                    <div class="info-value">${new Date(patient.appointment_time).toLocaleString()}</div>
                                </div>
                                ` : ''}
                            </div>
                        </div>
                    `;
                } else {
                    statusDiv.className = 'status-result status-error';
                    statusDiv.innerHTML = `
                        <div class="status-header">
                            <h3 style="color: #dc2626; font-size: 1.5rem; font-weight: 700; display: flex; align-items: center; gap: 12px;">
                                ❌ Not Found
                            </h3>
                        </div>
                        <div class="status-content">
                            <p style="color: #991b1b; font-size: 1.1rem; text-align: center;">${result.error}</p>
                        </div>
                    `;
                }
                
                statusDiv.style.display = 'block';
                
            } catch (error) {
                const statusDiv = document.getElementById('statusResult');
                statusDiv.className = 'status-result status-error';
                statusDiv.innerHTML = `
                    <div class="status-header">
                        <h3 style="color: #dc2626; font-size: 1.5rem; font-weight: 700; display: flex; align-items: center; gap: 12px;">
                            ❌ Network Error
                        </h3>
                    </div>
                    <div class="status-content">
                        <p style="color: #991b1b; font-size: 1.1rem; text-align: center;">${error.message}</p>
                    </div>
                `;
                statusDiv.style.display = 'block';
            }
        });
        
        // Auto-focus on registration ID input
        document.getElementById('registration_id').focus();
        
        // Format registration ID as user types
        document.getElementById('registration_id').addEventListener('input', function(e) {
            e.target.value = e.target.value.toUpperCase();
        });
    </script>
</body>
</html>
'''

ADMIN_LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1565c0, #0d47a1);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 90%;
        }
        .login-header {
            text-align: center;
            margin-bottom: 30px;
        }
        .login-header h1 {
            color: #1565c0;
            margin-bottom: 10px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #1565c0;
        }
        .form-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
        }
        .login-btn {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1rem;
            cursor: pointer;
            width: 100%;
        }
        .back-btn {
            background: #90a4ae;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>🛡️ Admin Login</h1>
            <p>MediCare Hospital Administration</p>
        </div>
        
        <a href="/" class="back-btn">← Back to Home</a>
        
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="login-btn">Login</button>
        </form>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                username: document.getElementById('username').value,
                password: document.getElementById('password').value
            };
            
            try {
                const response = await fetch('/admin/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    window.location.href = '/admin/dashboard';
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        });
    </script>
</body>
</html>
'''
ENHANCED_ADMIN_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        /* Navigation Bar */
        .admin-navbar {
            background: linear-gradient(135deg, #1565c0, #0d47a1);
            color: white;
            padding: 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .navbar-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 20px 0;
        }
        .brand-icon {
            font-size: 2rem;
        }
        .brand-text h1 {
            font-size: 1.5rem;
            font-weight: 700;
        }
        .brand-text p {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        .user-menu {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .nav-menu {
            display: flex;
            list-style: none;
            gap: 0;
        }
        .nav-item {
            position: relative;
        }
        .nav-link {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 20px 25px;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        .nav-link:hover, .nav-link.active {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        .nav-link.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: #64b5f6;
        }
        .user-info {
            text-align: right;
        }
        .user-name {
            font-weight: 600;
            font-size: 1rem;
        }
        .user-role {
            font-size: 0.8rem;
            opacity: 0.8;
        }
        .logout-btn {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .logout-btn:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        
        /* Main Content */
        .main-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        
        /* Dashboard Header */
        .dashboard-header {
            margin-bottom: 30px;
        }
        .dashboard-title {
            font-size: 2.2rem;
            color: #1565c0;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .dashboard-subtitle {
            color: #546e7a;
            font-size: 1.1rem;
        }
        
        /* Stats Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        .stat-card {
            background: linear-gradient(135deg, #ffffff, #f8f9fa);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--card-color);
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }
        .stat-card.primary { --card-color: linear-gradient(135deg, #1976d2, #1565c0); }
        .stat-card.danger { --card-color: linear-gradient(135deg, #d32f2f, #c62828); }
        .stat-card.success { --card-color: linear-gradient(135deg, #388e3c, #2e7d32); }
        .stat-card.warning { --card-color: linear-gradient(135deg, #f57c00, #ef6c00); }
        
        .stat-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
        }
        .stat-icon {
            font-size: 2.5rem;
            opacity: 0.8;
        }
        .stat-card.primary .stat-icon { color: #1976d2; }
        .stat-card.danger .stat-icon { color: #d32f2f; }
        .stat-card.success .stat-icon { color: #388e3c; }
        .stat-card.warning .stat-icon { color: #f57c00; }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1565c0;
            margin-bottom: 5px;
        }
        .stat-label {
            color: #546e7a;
            font-size: 1rem;
            font-weight: 500;
        }
        
        /* Patient Management Section */
        .patients-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }
        .table-container {
            overflow-x: auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        }
        .patients-table {
            width: 100%;
            border-collapse: collapse;
        }
        .patients-table th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #2c3e50;
            border-bottom: 2px solid #e0e0e0;
            background: #f8f9fa;
        }
        .patients-table td {
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
        }
        .risk-badge {
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .risk-high { background: #ffebee; color: #c62828; }
        .risk-medium { background: #fff3e0; color: #f57c00; }
        .risk-low { background: #e8f5e8; color: #2e7d32; }
        .status-badge {
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .status-waiting { background: #fff3e0; color: #f57c00; }
        .status-confirmed { background: #e8f5e8; color: #2e7d32; }
        .status-in-consultation { background: #e3f2fd; color: #1976d2; }
        .status-completed { background: #f3e5f5; color: #7b1fa2; }
        
        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            max-width: 600px;
            width: 90%;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .navbar-content {
                flex-direction: column;
                gap: 20px;
            }
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <!-- Admin Navigation -->
    <nav class="admin-navbar">
        <div class="navbar-content">
            <div class="navbar-brand">
                <span class="brand-icon">🏥</span>
                <div class="brand-text">
                    <h1>MediCare Hospital</h1>
                    <p>Admin Dashboard</p>
                </div>
            </div>
            
            <ul class="nav-menu">
                <li class="nav-item">
                    <a href="/admin/dashboard" class="nav-link active">
                        <span>📊</span> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/analytics" class="nav-link">
                        <span>📈</span> Analytics
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/reports" class="nav-link">
                        <span>📋</span> Reports
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/settings" class="nav-link">
                        <span>⚙️</span> Settings
                    </a>
                </li>
            </ul>
            
            <div class="user-menu">
                <div class="user-info">
                    <div class="user-name">{{ session.admin_name or 'Administrator' }}</div>
                    <div class="user-role">System Admin</div>
                </div>
                <a href="/admin/logout" class="logout-btn">Logout</a>
            </div>
        </div>
    </nav>
    
    <!-- Main Content -->
    <div class="main-content">
        <!-- Dashboard Header -->
        <div class="dashboard-header">
            <h1 class="dashboard-title">Hospital Dashboard</h1>
            <p class="dashboard-subtitle">Real-time overview of hospital operations and patient management</p>
        </div>
        
        <!-- Statistics Cards -->
        <div class="stats-grid">
            <div class="stat-card primary">
                <div class="stat-header">
                    <div class="stat-icon">👥</div>
                </div>
                <div class="stat-number" id="totalToday">0</div>
                <div class="stat-label">Patients Today</div>
            </div>
            
            <div class="stat-card danger">
                <div class="stat-header">
                    <div class="stat-icon">🚨</div>
                </div>
                <div class="stat-number" id="criticalCases">0</div>
                <div class="stat-label">Critical Cases</div>
            </div>
            
            <div class="stat-card success">
                <div class="stat-header">
                    <div class="stat-icon">⏱️</div>
                </div>
                <div class="stat-number" id="avgWaiting">0</div>
                <div class="stat-label">Avg Wait Time (min)</div>
            </div>
            
            <div class="stat-card warning">
                <div class="stat-header">
                    <div class="stat-icon">👨‍⚕️</div>
                </div>
                <div class="stat-number" id="doctorsOnline">0</div>
                <div class="stat-label">Doctors Online</div>
            </div>
        </div>
        
        <!-- Patient Management Table -->
        <div class="patients-section">
            <div class="section-header">
                <h3 style="font-size: 1.4rem; color: #1565c0; font-weight: 600; display: flex; align-items: center; gap: 10px;">
                    <span>👥</span> Patient Management
                </h3>
                <button onclick="refreshPatients()" style="background: #1976d2; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer;">
                    Refresh Patients
                </button>
            </div>
            <div class="table-container">
                <table class="patients-table">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Age</th>
                            <th>Symptoms</th>
                            <th>Risk Level</th>
                            <th>Department</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="patientsTableBody">
                        <!-- Patients will be loaded here -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <!-- Confirm Patient Modal -->
    <div id="confirmModal" class="modal">
        <div class="modal-content">
            <h3 style="margin-bottom: 20px; color: #1565c0;">📅 Confirm Patient Appointment</h3>
            <div style="margin-bottom: 20px;">
                <label style="display: block; margin-bottom: 8px; font-weight: 600;">Appointment Date & Time:</label>
                <input type="datetime-local" id="appointmentDateTime" style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px;" required>
            </div>
            <div style="display: flex; gap: 15px; justify-content: flex-end;">
                <button onclick="closeConfirmModal()" style="background: #95a5a6; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer;">Cancel</button>
                <button onclick="confirmPatient()" style="background: #1976d2; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer;">Confirm Appointment</button>
            </div>
        </div>
    </div>
    
    <!-- Report Modal -->
    <div id="reportModal" class="modal">
        <div class="modal-content">
            <h3 style="margin-bottom: 20px; color: #1565c0;">📋 Patient Report</h3>
            <div id="reportContent" style="margin-bottom: 20px;">
                <!-- Report content will be loaded here -->
            </div>
            <div style="display: flex; gap: 15px; justify-content: flex-end;">
                <button onclick="closeReportModal()" style="background: #95a5a6; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer;">Close</button>
                <button onclick="downloadReport()" style="background: #2ecc71; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer;">📥 Download PDF</button>
            </div>
        </div>
    </div>

    <script>
        let currentPatientId = null;
        let currentReportData = null;
        
        // Load dashboard data on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadDashboardStats();
            loadPatients();
            
            // Auto-refresh every 30 seconds
            setInterval(() => {
                loadDashboardStats();
                loadPatients();
            }, 30000);
        });
        
        async function loadDashboardStats() {
            try {
                const response = await fetch('/api/admin/dashboard_stats');
                const stats = await response.json();
                
                // Update stat cards
                document.getElementById('totalToday').textContent = stats.total_today;
                document.getElementById('criticalCases').textContent = stats.critical_cases;
                document.getElementById('avgWaiting').textContent = stats.avg_waiting;
                document.getElementById('doctorsOnline').textContent = stats.doctors_online;
                
            } catch (error) {
                console.error('Error loading dashboard stats:', error);
            }
        }
        
        async function loadPatients() {
            try {
                const response = await fetch('/api/admin/patients');
                const patients = await response.json();
                
                const tbody = document.getElementById('patientsTableBody');
                tbody.innerHTML = '';
                
                patients.forEach(patient => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>
                            <div style="font-weight: 600;">${patient.name}</div>
                            <div style="font-size: 0.8rem; color: #666;">${patient.registration_id}</div>
                        </td>
                        <td>${patient.age}</td>
                        <td style="max-width: 200px;">
                            <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${patient.symptom}">
                                ${patient.symptom}
                            </div>
                        </td>
                        <td>
                            <span class="risk-badge risk-${getRiskLevel(patient.risk_score)}">
                                ${getRiskLevel(patient.risk_score)} (${patient.risk_score})
                            </span>
                        </td>
                        <td>
                            <div style="font-weight: 600;">${patient.department}</div>
                            <div style="font-size: 0.8rem; color: #666;">${patient.severity}</div>
                        </td>
                        <td>
                            <span class="status-badge status-${patient.status}">
                                ${patient.status.charAt(0).toUpperCase() + patient.status.slice(1)}
                            </span>
                        </td>
                        <td>
                            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                                ${patient.status === 'waiting' ? 
                                    `<button onclick="openConfirmModal(${patient.id})" style="background: #2ecc71; color: white; border: none; padding: 6px 12px; border-radius: 5px; cursor: pointer; font-size: 0.8rem;">Confirm</button>` :
                                    `<button onclick="generateReport(${patient.id})" style="background: #1976d2; color: white; border: none; padding: 6px 12px; border-radius: 5px; cursor: pointer; font-size: 0.8rem;">📋 Report</button>`
                                }
                            </div>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
                
            } catch (error) {
                console.error('Error loading patients:', error);
            }
        }
        
        function getRiskLevel(score) {
            if (score >= 80) return 'high';
            if (score >= 50) return 'medium';
            return 'low';
        }
        
        function refreshPatients() {
            loadPatients();
        }
        
        function openConfirmModal(patientId) {
            currentPatientId = patientId;
            
            // Set default appointment time to next available slot
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            tomorrow.setHours(10, 0, 0, 0);
            
            document.getElementById('appointmentDateTime').value = tomorrow.toISOString().slice(0, 16);
            document.getElementById('confirmModal').style.display = 'flex';
        }
        
        function closeConfirmModal() {
            document.getElementById('confirmModal').style.display = 'none';
            currentPatientId = null;
        }
        
        async function confirmPatient() {
            const appointmentTime = document.getElementById('appointmentDateTime').value;
            
            if (!appointmentTime) {
                alert('Please select appointment date and time');
                return;
            }
            
            try {
                const response = await fetch('/api/admin/confirm_patient', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        patient_id: currentPatientId,
                        appointment_time: appointmentTime
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    closeConfirmModal();
                    loadPatients(); // Refresh the table
                    alert('Patient confirmed successfully!');
                } else {
                    alert('Error confirming patient: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        }
        
        async function generateReport(patientId) {
            try {
                const response = await fetch(`/api/admin/generate_report/${patientId}`);
                const result = await response.json();
                
                if (result.success) {
                    currentReportData = result.report_data;
                    displayReport(result.report_data);
                    document.getElementById('reportModal').style.display = 'flex';
                } else {
                    alert('Error generating report: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        }
        
        function displayReport(data) {
            const reportContent = document.getElementById('reportContent');
            reportContent.innerHTML = `
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h4 style="color: #1565c0; margin-bottom: 15px;">Patient Information</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                        <div><strong>Name:</strong> ${data.patient_name}</div>
                        <div><strong>Registration ID:</strong> ${data.registration_id}</div>
                        <div><strong>Age:</strong> ${data.age}</div>
                        <div><strong>Gender:</strong> ${data.gender}</div>
                        <div><strong>Phone:</strong> ${data.phone}</div>
                        <div><strong>Department:</strong> ${data.department}</div>
                    </div>
                </div>
                
                <div style="background: #fff3e0; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h4 style="color: #f57c00; margin-bottom: 15px;">Medical Assessment</h4>
                    <div><strong>Primary Symptom:</strong> ${data.symptom}</div>
                    <div style="margin-top: 10px;"><strong>Severity:</strong> ${data.severity}</div>
                    <div style="margin-top: 10px;"><strong>Risk Score:</strong> ${data.risk_score}/100</div>
                    <div style="margin-top: 10px;"><strong>Emergency Case:</strong> ${data.is_emergency ? 'Yes' : 'No'}</div>
                </div>
                
                <div style="background: ${data.status === 'confirmed' ? '#e8f5e8' : '#ffebee'}; padding: 20px; border-radius: 10px;">
                    <h4 style="color: ${data.status === 'confirmed' ? '#2e7d32' : '#c62828'}; margin-bottom: 15px;">Appointment Status</h4>
                    <div><strong>Status:</strong> ${data.status.charAt(0).toUpperCase() + data.status.slice(1)}</div>
                    <div style="margin-top: 10px;"><strong>Registered:</strong> ${formatDateTime(data.created_at)}</div>
                    ${data.appointment_time ? `<div style="margin-top: 10px;"><strong>Appointment Time:</strong> ${formatDateTime(data.appointment_time)}</div>` : ''}
                </div>
            `;
        }
        
        function closeReportModal() {
            document.getElementById('reportModal').style.display = 'none';
            currentReportData = null;
        }
        
        function downloadReport() {
            if (currentReportData) {
                alert('PDF report download would be implemented in production. Report data: ' + JSON.stringify(currentReportData, null, 2));
            }
        }
        
        function formatDateTime(dateString) {
            if (!dateString) return 'Not scheduled';
            const date = new Date(dateString);
            return date.toLocaleDateString() + ' at ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }
    </script>
</body>
</html>
'''
# ===== ADDITIONAL ADMIN TEMPLATES =====

ADMIN_ANALYTICS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        /* Navigation Bar */
        .admin-navbar {
            background: linear-gradient(135deg, #1565c0, #0d47a1);
            color: white;
            padding: 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .navbar-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 20px 0;
        }
        .brand-icon { font-size: 2rem; }
        .brand-text h1 { font-size: 1.5rem; font-weight: 700; }
        .brand-text p { font-size: 0.9rem; opacity: 0.9; }
        .nav-menu {
            display: flex;
            list-style: none;
            gap: 0;
        }
        .nav-item { position: relative; }
        .nav-link {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 20px 25px;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        .nav-link:hover, .nav-link.active {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        .nav-link.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: #64b5f6;
        }
        .user-menu {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .user-info { text-align: right; }
        .user-name { font-weight: 600; font-size: 1rem; }
        .user-role { font-size: 0.8rem; opacity: 0.8; }
        .logout-btn {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .logout-btn:hover { background: rgba(255, 255, 255, 0.2); }
        
        /* Main Content */
        .main-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        .page-header {
            margin-bottom: 30px;
        }
        .page-title {
            font-size: 2.2rem;
            color: #1565c0;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .page-subtitle {
            color: #546e7a;
            font-size: 1.1rem;
        }
        
        /* Analytics Cards */
        .analytics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        .analytics-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        .card-header {
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }
        .card-title {
            font-size: 1.4rem;
            color: #1565c0;
            font-weight: 600;
            margin-bottom: 5px;
        }
        .card-subtitle {
            color: #546e7a;
            font-size: 0.9rem;
        }
        .chart-container {
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .navbar-content { flex-direction: column; gap: 20px; }
            .nav-menu { flex-wrap: wrap; justify-content: center; }
            .analytics-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <!-- Admin Navigation -->
    <nav class="admin-navbar">
        <div class="navbar-content">
            <div class="navbar-brand">
                <span class="brand-icon">🏥</span>
                <div class="brand-text">
                    <h1>MediCare Hospital</h1>
                    <p>Admin Dashboard</p>
                </div>
            </div>
            
            <ul class="nav-menu">
                <li class="nav-item">
                    <a href="/admin/dashboard" class="nav-link">
                        <span>📊</span> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/analytics" class="nav-link active">
                        <span>📈</span> Analytics
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/reports" class="nav-link">
                        <span>📋</span> Reports
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/settings" class="nav-link">
                        <span>⚙️</span> Settings
                    </a>
                </li>
            </ul>
            
            <div class="user-menu">
                <div class="user-info">
                    <div class="user-name">{{ session.admin_name or 'Administrator' }}</div>
                    <div class="user-role">System Admin</div>
                </div>
                <a href="/admin/logout" class="logout-btn">Logout</a>
            </div>
        </div>
    </nav>
    
    <!-- Main Content -->
    <div class="main-content">
        <!-- Page Header -->
        <div class="page-header">
            <h1 class="page-title">📈 Analytics Dashboard</h1>
            <p class="page-subtitle">Comprehensive insights into hospital operations and patient trends</p>
        </div>
        
        <!-- Analytics Grid -->
        <div class="analytics-grid">
            <div class="analytics-card">
                <div class="card-header">
                    <h3 class="card-title">Analytics Coming Soon</h3>
                    <p class="card-subtitle">Advanced analytics features will be available here</p>
                </div>
                <div class="chart-container">
                    <p style="color: #666; text-align: center;">Analytics dashboard under development</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

ADMIN_REPORTS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reports - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        /* Navigation Bar */
        .admin-navbar {
            background: linear-gradient(135deg, #1565c0, #0d47a1);
            color: white;
            padding: 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .navbar-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 20px 0;
        }
        .brand-icon { font-size: 2rem; }
        .brand-text h1 { font-size: 1.5rem; font-weight: 700; }
        .brand-text p { font-size: 0.9rem; opacity: 0.9; }
        .nav-menu {
            display: flex;
            list-style: none;
            gap: 0;
        }
        .nav-item { position: relative; }
        .nav-link {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 20px 25px;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        .nav-link:hover, .nav-link.active {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        .nav-link.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: #64b5f6;
        }
        .user-menu {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .user-info { text-align: right; }
        .user-name { font-weight: 600; font-size: 1rem; }
        .user-role { font-size: 0.8rem; opacity: 0.8; }
        .logout-btn {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .logout-btn:hover { background: rgba(255, 255, 255, 0.2); }
        
        /* Main Content */
        .main-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        .page-header {
            margin-bottom: 30px;
        }
        .page-title {
            font-size: 2.2rem;
            color: #1565c0;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .page-subtitle {
            color: #546e7a;
            font-size: 1.1rem;
        }
        
        /* Reports Grid */
        .reports-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        .report-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .report-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }
        .report-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }
        .report-icon {
            font-size: 2.5rem;
            color: #1976d2;
        }
        .report-title {
            font-size: 1.3rem;
            color: #1565c0;
            font-weight: 600;
        }
        .report-description {
            color: #546e7a;
            margin-bottom: 25px;
            line-height: 1.5;
        }
        .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(25, 118, 210, 0.3);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .navbar-content { flex-direction: column; gap: 20px; }
            .nav-menu { flex-wrap: wrap; justify-content: center; }
            .reports-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <!-- Admin Navigation -->
    <nav class="admin-navbar">
        <div class="navbar-content">
            <div class="navbar-brand">
                <span class="brand-icon">🏥</span>
                <div class="brand-text">
                    <h1>MediCare Hospital</h1>
                    <p>Admin Dashboard</p>
                </div>
            </div>
            
            <ul class="nav-menu">
                <li class="nav-item">
                    <a href="/admin/dashboard" class="nav-link">
                        <span>📊</span> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/analytics" class="nav-link">
                        <span>📈</span> Analytics
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/reports" class="nav-link active">
                        <span>📋</span> Reports
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/settings" class="nav-link">
                        <span>⚙️</span> Settings
                    </a>
                </li>
            </ul>
            
            <div class="user-menu">
                <div class="user-info">
                    <div class="user-name">{{ session.admin_name or 'Administrator' }}</div>
                    <div class="user-role">System Admin</div>
                </div>
                <a href="/admin/logout" class="logout-btn">Logout</a>
            </div>
        </div>
    </nav>
    
    <!-- Main Content -->
    <div class="main-content">
        <!-- Page Header -->
        <div class="page-header">
            <h1 class="page-title">📋 Reports Center</h1>
            <p class="page-subtitle">Generate and download comprehensive hospital reports</p>
        </div>
        
        <!-- Reports Grid -->
        <div class="reports-grid">
            <div class="report-card">
                <div class="report-header">
                    <div class="report-icon">📅</div>
                    <div class="report-title">Daily Operations Report</div>
                </div>
                <div class="report-description">
                    Comprehensive daily summary including patient registrations, department performance, and key metrics.
                </div>
                <button onclick="generateDailyReport()" class="btn btn-primary">
                    <span>📥</span> Generate Report
                </button>
            </div>
        </div>
    </div>

    <script>
        async function generateDailyReport() {
            try {
                const response = await fetch('/api/admin/generate_daily_report');
                const result = await response.json();
                
                if (result.success) {
                    alert(`Daily report generated successfully!\\n\\nFilename: ${result.filename}`);
                } else {
                    alert('Error generating report: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        }
    </script>
</body>
</html>
'''

ADMIN_SETTINGS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Settings - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        /* Navigation Bar */
        .admin-navbar {
            background: linear-gradient(135deg, #1565c0, #0d47a1);
            color: white;
            padding: 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .navbar-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        }
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 20px 0;
        }
        .brand-icon { font-size: 2rem; }
        .brand-text h1 { font-size: 1.5rem; font-weight: 700; }
        .brand-text p { font-size: 0.9rem; opacity: 0.9; }
        .nav-menu {
            display: flex;
            list-style: none;
            gap: 0;
        }
        .nav-item { position: relative; }
        .nav-link {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 20px 25px;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        .nav-link:hover, .nav-link.active {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        .nav-link.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: #64b5f6;
        }
        .user-menu {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .user-info { text-align: right; }
        .user-name { font-weight: 600; font-size: 1rem; }
        .user-role { font-size: 0.8rem; opacity: 0.8; }
        .logout-btn {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .logout-btn:hover { background: rgba(255, 255, 255, 0.2); }
        
        /* Main Content */
        .main-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        .page-header {
            margin-bottom: 30px;
        }
        .page-title {
            font-size: 2.2rem;
            color: #1565c0;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .page-subtitle {
            color: #546e7a;
            font-size: 1.1rem;
        }
        
        /* Settings Sections */
        .settings-container {
            display: grid;
            grid-template-columns: 1fr;
            gap: 30px;
        }
        .settings-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        .section-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }
        .section-icon {
            font-size: 2rem;
            color: #1976d2;
        }
        .section-title {
            font-size: 1.4rem;
            color: #1565c0;
            font-weight: 600;
        }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
        }
        .form-group label {
            margin-bottom: 8px;
            font-weight: 600;
            color: #1565c0;
        }
        .form-group input, .form-group select {
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #1976d2;
            box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
        }
        .btn {
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(25, 118, 210, 0.3);
        }
        .section-actions {
            display: flex;
            gap: 15px;
            justify-content: flex-end;
            margin-top: 25px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }
        .success-message {
            background: linear-gradient(135deg, #e8f5e8, #c8e6c9);
            color: #2e7d32;
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: none;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .navbar-content { flex-direction: column; gap: 20px; }
            .nav-menu { flex-wrap: wrap; justify-content: center; }
            .form-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <!-- Admin Navigation -->
    <nav class="admin-navbar">
        <div class="navbar-content">
            <div class="navbar-brand">
                <span class="brand-icon">🏥</span>
                <div class="brand-text">
                    <h1>MediCare Hospital</h1>
                    <p>Admin Dashboard</p>
                </div>
            </div>
            
            <ul class="nav-menu">
                <li class="nav-item">
                    <a href="/admin/dashboard" class="nav-link">
                        <span>📊</span> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/analytics" class="nav-link">
                        <span>📈</span> Analytics
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/reports" class="nav-link">
                        <span>📋</span> Reports
                    </a>
                </li>
                <li class="nav-item">
                    <a href="/admin/settings" class="nav-link active">
                        <span>⚙️</span> Settings
                    </a>
                </li>
            </ul>
            
            <div class="user-menu">
                <div class="user-info">
                    <div class="user-name">{{ session.admin_name or 'Administrator' }}</div>
                    <div class="user-role">System Admin</div>
                </div>
                <a href="/admin/logout" class="logout-btn">Logout</a>
            </div>
        </div>
    </nav>
    
    <!-- Main Content -->
    <div class="main-content">
        <!-- Page Header -->
        <div class="page-header">
            <h1 class="page-title">⚙️ System Settings</h1>
            <p class="page-subtitle">Configure hospital system preferences and administrative settings</p>
        </div>
        
        <div id="successMessage" class="success-message">
            <strong>✅ Settings updated successfully!</strong>
        </div>
        
        <!-- Settings Container -->
        <div class="settings-container">
            <!-- Hospital Settings -->
            <div class="settings-section">
                <div class="section-header">
                    <div class="section-icon">🏥</div>
                    <div class="section-title">Hospital Configuration</div>
                </div>
                
                <form id="hospitalForm">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="clinicName">Hospital/Clinic Name</label>
                            <input type="text" id="clinicName" name="clinicName" placeholder="Enter hospital name">
                        </div>
                        
                        <div class="form-group">
                            <label for="workingHoursStart">Working Hours Start</label>
                            <input type="time" id="workingHoursStart" name="workingHoursStart">
                        </div>
                        
                        <div class="form-group">
                            <label for="workingHoursEnd">Working Hours End</label>
                            <input type="time" id="workingHoursEnd" name="workingHoursEnd">
                        </div>
                        
                        <div class="form-group">
                            <label for="emergencyThreshold">Emergency Risk Threshold</label>
                            <input type="number" id="emergencyThreshold" name="emergencyThreshold" min="50" max="100" placeholder="80">
                        </div>
                    </div>
                    
                    <div class="section-actions">
                        <button type="submit" class="btn btn-primary">
                            <span>💾</span> Save Settings
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            loadSettings();
        });
        
        async function loadSettings() {
            try {
                const response = await fetch('/api/admin/get_settings');
                const settings = await response.json();
                
                document.getElementById('clinicName').value = settings.clinic_name || '';
                document.getElementById('workingHoursStart').value = settings.working_hours_start || '';
                document.getElementById('workingHoursEnd').value = settings.working_hours_end || '';
                document.getElementById('emergencyThreshold').value = settings.emergency_threshold || '';
                
            } catch (error) {
                console.error('Error loading settings:', error);
            }
        }
        
        document.getElementById('hospitalForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                clinic_name: document.getElementById('clinicName').value,
                working_hours_start: document.getElementById('workingHoursStart').value,
                working_hours_end: document.getElementById('workingHoursEnd').value,
                emergency_threshold: document.getElementById('emergencyThreshold').value
            };
            
            try {
                const response = await fetch('/api/admin/update_settings', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('successMessage').style.display = 'block';
                    setTimeout(() => {
                        document.getElementById('successMessage').style.display = 'none';
                    }, 3000);
                } else {
                    alert('Error updating settings: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        });
    </script>
</body>
</html>
'''

# Template mappings to ensure enhanced templates are used
PATIENT_REGISTER_TEMPLATE = ENHANCED_PATIENT_REGISTER_TEMPLATE
PATIENT_STATUS_TEMPLATE = ENHANCED_PATIENT_STATUS_TEMPLATE