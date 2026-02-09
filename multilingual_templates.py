#!/usr/bin/env python3
"""
Multilingual Templates for Patient-facing Pages
"""

MULTILINGUAL_PATIENT_REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html lang="{{ session.get('language', 'en') }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t('book_appointment_title') }} - {{ t('hospital_name') }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 50%, #f0f8ff 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 25px;
            padding: 40px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.1);
            position: relative;
        }
        .language-selector {
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            gap: 8px;
        }
        .lang-btn {
            background: rgba(25, 118, 210, 0.1);
            color: #1976d2;
            border: 2px solid #1976d2;
            padding: 6px 10px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.8rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .lang-btn:hover, .lang-btn.active {
            background: #1976d2;
            color: white;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #1565c0;
        }
        .form-section {
            margin-bottom: 35px;
            padding: 25px;
            background: linear-gradient(135deg, #fafafa, #ffffff);
            border-radius: 15px;
        }
        .section-title {
            font-size: 1.3rem;
            color: #1565c0;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e3f2fd;
        }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
        }
        .form-group.full-width {
            grid-column: 1 / -1;
        }
        label {
            margin-bottom: 8px;
            font-weight: 600;
            color: #1565c0;
        }
        input, select, textarea {
            padding: 15px;
            border: 2px solid #e3f2fd;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #1976d2;
            box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
        }
        .severity-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 10px;
        }
        .severity-btn {
            padding: 20px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            background: white;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s ease;
        }
        .severity-btn.selected {
            border-color: #1976d2;
            background: linear-gradient(135deg, #e3f2fd, #ffffff);
        }
        .emergency-section {
            background: linear-gradient(135deg, #ffebee, #fce4ec);
            border: 2px solid #f8bbd9;
            border-radius: 15px;
            padding: 25px;
            margin: 25px 0;
        }
        .emergency-switch {
            position: relative;
            width: 60px;
            height: 30px;
            background: #ccc;
            border-radius: 15px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .emergency-switch.active {
            background: #f44336;
        }
        .emergency-switch::before {
            content: '';
            position: absolute;
            width: 26px;
            height: 26px;
            border-radius: 50%;
            background: white;
            top: 2px;
            left: 2px;
            transition: transform 0.3s;
        }
        .emergency-switch.active::before {
            transform: translateX(30px);
        }
        .submit-btn {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
            border: none;
            padding: 20px 40px;
            border-radius: 15px;
            font-size: 1.2rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-top: 30px;
            transition: all 0.4s ease;
        }
        .submit-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(25, 118, 210, 0.4);
        }
        .back-btn {
            background: #90a4ae;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 10px;
            text-decoration: none;
            display: inline-block;
            margin-bottom: 25px;
        }
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        .modal-content {
            background: white;
            padding: 50px;
            border-radius: 25px;
            text-align: center;
            max-width: 600px;
            width: 90%;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="language-selector">
            <a href="/set_language/en" class="lang-btn {{ 'active' if session.get('language', 'en') == 'en' else '' }}">EN</a>
            <a href="/set_language/hi" class="lang-btn {{ 'active' if session.get('language') == 'hi' else '' }}">हिं</a>
            <a href="/set_language/ta" class="lang-btn {{ 'active' if session.get('language') == 'ta' else '' }}">த</a>
        </div>
        
        <div class="header">
            <h1>📝 {{ t('book_appointment_title') }}</h1>
            <p>{{ t('registration_subtitle') }}</p>
        </div>
        
        <a href="/patient" class="back-btn">← {{ t('back_to_patient_portal') }}</a>
        
        <form id="registrationForm">
            <!-- Personal Information -->
            <div class="form-section">
                <div class="section-title">
                    👤 {{ t('personal_information') }}
                </div>
                <div class="form-grid">
                    <div class="form-group">
                        <label for="name">{{ t('full_name') }} {{ t('required') }}</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="age">{{ t('age') }} {{ t('required') }}</label>
                        <input type="number" id="age" name="age" min="1" max="120" required>
                    </div>
                    <div class="form-group">
                        <label for="gender">{{ t('gender') }} {{ t('required') }}</label>
                        <select id="gender" name="gender" required>
                            <option value="">{{ t('select_gender') }}</option>
                            <option value="Male">{{ t('male') }}</option>
                            <option value="Female">{{ t('female') }}</option>
                            <option value="Other">{{ t('other') }}</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="phone">{{ t('phone_number') }} {{ t('required') }}</label>
                        <input type="tel" id="phone" name="phone" required>
                    </div>
                    <div class="form-group">
                        <label for="email">{{ t('email_address') }}</label>
                        <input type="email" id="email" name="email">
                    </div>
                </div>
            </div>
            
            <!-- Medical Information -->
            <div class="form-section">
                <div class="section-title">
                    🩺 {{ t('medical_information') }}
                </div>
                
                <div class="form-group full-width">
                    <label for="main_symptom">{{ t('primary_symptom') }} {{ t('required') }}</label>
                    <textarea id="main_symptom" name="main_symptom" rows="4" 
                              placeholder="{{ t('symptom_placeholder') }}" required></textarea>
                </div>
                
                <div class="form-group">
                    <label>{{ t('symptom_severity') }} {{ t('required') }}</label>
                    <div class="severity-grid">
                        <div class="severity-btn mild" onclick="selectSeverity('Mild', this)">
                            <div style="font-weight: bold; color: #4caf50;">{{ t('mild') }}</div>
                            <div style="font-size: 0.9rem; color: #666;">{{ t('mild_desc') }}</div>
                        </div>
                        <div class="severity-btn moderate" onclick="selectSeverity('Moderate', this)">
                            <div style="font-weight: bold; color: #ff9800;">{{ t('moderate') }}</div>
                            <div style="font-size: 0.9rem; color: #666;">{{ t('moderate_desc') }}</div>
                        </div>
                        <div class="severity-btn severe" onclick="selectSeverity('Severe', this)">
                            <div style="font-weight: bold; color: #f44336;">{{ t('severe') }}</div>
                            <div style="font-size: 0.9rem; color: #666;">{{ t('severe_desc') }}</div>
                        </div>
                    </div>
                    <input type="hidden" id="severity" name="severity" required>
                </div>
                
                <div class="form-group">
                    <label for="symptom_days">{{ t('symptom_duration') }} {{ t('required') }}</label>
                    <select id="symptom_days" name="symptom_days" required>
                        <option value="">{{ t('select_duration') }}</option>
                        <option value="1">{{ t('today') }}</option>
                        <option value="2">{{ t('2_days') }}</option>
                        <option value="3">{{ t('3_days') }}</option>
                        <option value="7">{{ t('week') }}</option>
                        <option value="14">{{ t('2_weeks') }}</option>
                        <option value="30">{{ t('month') }}</option>
                        <option value="90">{{ t('more_month') }}</option>
                    </select>
                </div>
            </div>
            
            <!-- Emergency Section -->
            <div class="emergency-section">
                <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                    <div class="emergency-switch" id="emergencySwitch" onclick="toggleEmergency()"></div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: #c62828;">🚨 {{ t('emergency') }}</div>
                </div>
                <div style="color: #ad1457; font-size: 0.9rem; line-height: 1.5;">
                    <strong>{{ t('emergency_priority') }}:</strong> {{ t('emergency_desc') }}
                </div>
                <input type="hidden" id="is_emergency" name="is_emergency" value="false">
            </div>
            
            <button type="submit" class="submit-btn">
                📅 {{ t('book_appointment_btn') }}
            </button>
        </form>
    </div>
    
    <!-- Success Modal -->
    <div id="successModal" class="modal">
        <div class="modal-content">
            <div style="font-size: 5rem; color: #4caf50; margin-bottom: 25px;">✅</div>
            <h2 style="font-size: 2rem; color: #1565c0; margin-bottom: 20px;">{{ t('success_title') }}</h2>
            
            <div style="background: linear-gradient(135deg, #e3f2fd, #ffffff); padding: 25px; border-radius: 15px; margin: 25px 0; border: 2px solid #1976d2;">
                <strong>{{ t('registration_id') }}</strong>
                <div id="registrationId" style="font-size: 2rem; font-weight: bold; color: #1976d2; margin: 15px 0;"></div>
            </div>
            
            <div id="departmentInfo" style="background: linear-gradient(135deg, #f3e5f5, #ffffff); padding: 20px; border-radius: 12px; margin: 20px 0;">
                <h3 style="color: #9c27b0; margin-bottom: 10px;">📋 {{ t('recommended_dept') }}</h3>
                <div id="departmentName" style="font-size: 1.2rem; font-weight: bold;"></div>
            </div>
            
            <div id="emergencyMessage" style="display: none; background: #ffebee; padding: 20px; border-radius: 12px; margin: 20px 0;">
                <h4 style="color: #c62828; margin-bottom: 10px;">🚨 {{ t('emergency_priority') }}</h4>
                <p style="color: #ad1457;">{{ t('emergency_msg') }}</p>
            </div>
            
            <button onclick="goToPatientPortal()" style="background: #1976d2; color: white; border: none; padding: 15px 30px; border-radius: 10px; cursor: pointer; font-size: 1rem; margin-top: 20px;">
                {{ t('back_to_portal') }}
            </button>
        </div>
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
                alert('{{ t("symptom_severity") }} {{ t("required") }}');
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
                    document.getElementById('registrationId').textContent = result.registration_id;
                    document.getElementById('departmentName').textContent = result.department;
                    
                    if (result.is_emergency || result.risk_score >= 80) {
                        document.getElementById('emergencyMessage').style.display = 'block';
                    }
                    
                    document.getElementById('successModal').style.display = 'flex';
                } else {
                    alert('{{ t("error") }}: ' + result.error);
                }
            } catch (error) {
                alert('{{ t("error") }}: ' + error.message);
            }
        });
        
        function goToPatientPortal() {
            window.location.href = '/patient';
        }
    </script>
</body>
</html>
'''

MULTILINGUAL_PATIENT_STATUS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="{{ session.get('language', 'en') }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t('check_status_title') }} - {{ t('hospital_name') }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 50%, #f0f8ff 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #1565c0;
            position: relative;
        }
        .language-selector {
            position: absolute;
            top: 0;
            right: 0;
            display: flex;
            gap: 8px;
        }
        .lang-btn {
            background: rgba(25, 118, 210, 0.1);
            color: #1976d2;
            border: 2px solid #1976d2;
            padding: 6px 10px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.8rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .lang-btn:hover, .lang-btn.active {
            background: #1976d2;
            color: white;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 25px;
            padding: 40px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.1);
        }
        .search-input {
            width: 100%;
            padding: 18px;
            border: 2px solid #e3f2fd;
            border-radius: 12px;
            font-size: 1.1rem;
            text-align: center;
            margin-bottom: 20px;
            text-transform: uppercase;
        }
        .search-btn {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
            border: none;
            padding: 18px 35px;
            border-radius: 12px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.4s ease;
        }
        .status-card {
            display: none;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 20px;
            padding: 35px;
            margin-top: 30px;
        }
        .status-badge {
            display: inline-block;
            padding: 10px 25px;
            border-radius: 25px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .status-waiting { background: #fff3e0; color: #f57c00; }
        .status-confirmed { background: #e8f5e8; color: #2e7d32; }
        .status-in-consultation { background: #e3f2fd; color: #1976d2; }
        .status-completed { background: #f3e5f5; color: #7b1fa2; }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        .info-item {
            background: white;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #1976d2;
        }
        .error-message {
            background: linear-gradient(135deg, #ffebee, #fce4ec);
            color: #c62828;
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
            text-align: center;
            display: none;
        }
        .back-btn {
            background: #90a4ae;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 10px;
            text-decoration: none;
            display: inline-block;
            margin-bottom: 25px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="language-selector">
            <a href="/set_language/en" class="lang-btn {{ 'active' if session.get('language', 'en') == 'en' else '' }}">EN</a>
            <a href="/set_language/hi" class="lang-btn {{ 'active' if session.get('language') == 'hi' else '' }}">हिं</a>
            <a href="/set_language/ta" class="lang-btn {{ 'active' if session.get('language') == 'ta' else '' }}">த</a>
        </div>
        <h1>🔍 {{ t('check_status_title') }}</h1>
        <p>{{ t('status_subtitle') }}</p>
    </div>
    
    <div class="container">
        <a href="/patient" class="back-btn">← {{ t('back_to_patient_portal') }}</a>
        
        <div style="text-align: center; margin-bottom: 30px;">
            <input type="text" id="registrationId" class="search-input" 
                   placeholder="{{ t('registration_id_placeholder') }}">
            <br>
            <button onclick="checkStatus()" class="search-btn">
                🔍 {{ t('check_status_btn') }}
            </button>
        </div>
        
        <div id="errorMessage" class="error-message"></div>
        
        <div id="statusCard" class="status-card">
            <div style="text-align: center; margin-bottom: 30px;">
                <div id="patientName" style="font-size: 1.8rem; color: #1565c0; font-weight: 700; margin-bottom: 15px;"></div>
                <div id="statusBadge" class="status-badge"></div>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 8px;">{{ t('registration_id') }}</div>
                    <div id="regId" style="font-weight: 600; color: #1565c0; font-size: 1.1rem;"></div>
                </div>
                
                <div class="info-item">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 8px;">{{ t('department') }}</div>
                    <div id="department" style="font-weight: 600; color: #1565c0; font-size: 1.1rem;"></div>
                </div>
                
                <div class="info-item">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 8px;">{{ t('risk_score') }}</div>
                    <div id="riskScore" style="font-weight: 600; color: #1565c0; font-size: 1.1rem;"></div>
                </div>
                
                <div class="info-item">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 8px;">{{ t('severity') }}</div>
                    <div id="severity" style="font-weight: 600; color: #1565c0; font-size: 1.1rem;"></div>
                </div>
                
                <div class="info-item" id="appointmentTimeItem" style="display: none;">
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 8px;">{{ t('appointment_time') }}</div>
                    <div id="appointmentTime" style="font-weight: 600; color: #1565c0; font-size: 1.1rem;"></div>
                </div>
            </div>
            
            <div id="statusMessage" style="margin-top: 25px; padding: 25px; background: white; border-radius: 15px; text-align: center;"></div>
        </div>
    </div>

    <script>
        async function checkStatus() {
            const registrationId = document.getElementById('registrationId').value.trim().toUpperCase();
            
            if (!registrationId) {
                showError('{{ t("registration_id_placeholder") }}');
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
                
                if (result.success) {
                    displayPatientStatus(result.patient);
                    hideError();
                } else {
                    showError(result.error);
                    hideStatusCard();
                }
            } catch (error) {
                showError('{{ t("error") }}: ' + error.message);
                hideStatusCard();
            }
        }
        
        function displayPatientStatus(patient) {
            document.getElementById('patientName').textContent = patient.name;
            document.getElementById('regId').textContent = patient.registration_id;
            document.getElementById('department').textContent = patient.department;
            document.getElementById('riskScore').textContent = patient.risk_score + '/100';
            document.getElementById('severity').textContent = patient.severity;
            
            const statusBadge = document.getElementById('statusBadge');
            statusBadge.textContent = patient.status.charAt(0).toUpperCase() + patient.status.slice(1);
            statusBadge.className = 'status-badge status-' + patient.status;
            
            const statusMessage = document.getElementById('statusMessage');
            
            if (patient.status === 'waiting') {
                statusMessage.innerHTML = '<h3 style="color: #f57c00; margin-bottom: 15px;">⏳ {{ t("appointment_pending") }}</h3><p>{{ t("pending_msg") }}</p>';
            } else if (patient.status === 'confirmed') {
                statusMessage.innerHTML = '<h3 style="color: #2e7d32; margin-bottom: 15px;">✅ {{ t("appointment_confirmed") }}</h3><p>{{ t("confirmed_msg") }}</p>';
                if (patient.appointment_time) {
                    document.getElementById('appointmentTime').textContent = formatDateTime(patient.appointment_time);
                    document.getElementById('appointmentTimeItem').style.display = 'block';
                }
            }
            
            document.getElementById('statusCard').style.display = 'block';
        }
        
        function formatDateTime(dateString) {
            if (!dateString) return '{{ t("not_scheduled") }}';
            const date = new Date(dateString);
            return date.toLocaleDateString() + ' at ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }
        
        function showError(message) {
            document.getElementById('errorMessage').textContent = message;
            document.getElementById('errorMessage').style.display = 'block';
        }
        
        function hideError() {
            document.getElementById('errorMessage').style.display = 'none';
        }
        
        function hideStatusCard() {
            document.getElementById('statusCard').style.display = 'none';
        }
        
        document.getElementById('registrationId').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                checkStatus();
            }
        });
    </script>
</body>
</html>
'''