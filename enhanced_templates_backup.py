ENHANCED_PATIENT_REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t.book_appointment }} - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            animation: gradientShift 20s ease infinite;
        }
        
        @keyframes gradientShift {
            0%, 100% { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            25% { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
            50% { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
            75% { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 30px;
            padding: 40px;
            box-shadow: 0 30px 100px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(20px);
            animation: slideUp 1s ease-out;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #1565c0;
        }
        
        .header h1 {
            font-size: 2.2rem;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header p {
            font-size: 1.1rem;
            color: #546e7a;
        }
        
        .voice-assistant {
            background: linear-gradient(135deg, #e8f5e8, #ffffff);
            border: 2px solid #4caf50;
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .voice-controls {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        
        .voice-btn {
            background: linear-gradient(135deg, #4caf50, #45a049);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .voice-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3);
        }
        
        .voice-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .voice-status {
            color: #2e7d32;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .voice-instructions {
            color: #388e3c;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        
        .form-section {
            margin-bottom: 35px;
            padding: 25px;
            background: linear-gradient(135deg, #fafafa, #ffffff);
            border-radius: 20px;
            border: 2px solid #e3f2fd;
        }
        
        .section-title {
            font-size: 1.4rem;
            color: #1565c0;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e3f2fd;
            display: flex;
            align-items: center;
            gap: 10px;
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
        
        .form-group label {
            margin-bottom: 8px;
            font-weight: 600;
            color: #1565c0;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            padding: 15px;
            border: 2px solid #e3f2fd;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #1976d2;
            box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
            transform: translateY(-2px);
        }
        
        .voice-input-indicator {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: #4caf50;
            font-size: 1.2rem;
            display: none;
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
            border-radius: 15px;
            background: white;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .severity-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }
        
        .severity-btn.selected {
            border-color: #1976d2;
            background: linear-gradient(135deg, #e3f2fd, #ffffff);
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(25, 118, 210, 0.2);
        }
        
        .severity-btn .severity-title {
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .severity-btn.mild .severity-title { color: #4caf50; }
        .severity-btn.moderate .severity-title { color: #ff9800; }
        .severity-btn.severe .severity-title { color: #f44336; }
        
        .severity-btn .severity-desc {
            font-size: 0.9rem;
            color: #666;
        }
        
        .emergency-section {
            background: linear-gradient(135deg, #ffebee, #fce4ec);
            border: 2px solid #f8bbd9;
            border-radius: 20px;
            padding: 25px;
            margin: 25px 0;
        }
        
        .emergency-toggle {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
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
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        
        .emergency-switch.active::before {
            transform: translateX(30px);
        }
        
        .emergency-label {
            font-size: 1.1rem;
            font-weight: 600;
            color: #c62828;
        }
        
        .emergency-description {
            color: #ad1457;
            font-size: 0.9rem;
            line-height: 1.5;
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
            transition: left 0.5s;
        }
        
        .submit-btn:hover::before {
            left: 100%;
        }
        
        .submit-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(25, 118, 210, 0.4);
        }
        
        .back-btn {
            background: linear-gradient(135deg, #90a4ae, #78909c);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 10px;
            text-decoration: none;
            display: inline-block;
            margin-bottom: 25px;
            transition: all 0.3s ease;
        }
        
        .back-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(144, 164, 174, 0.3);
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
            animation: modalSlideIn 0.3s ease-out;
        }
        
        @keyframes modalSlideIn {
            from { opacity: 0; transform: translateY(-50px) scale(0.9); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        
        .success-icon {
            font-size: 5rem;
            color: #4caf50;
            margin-bottom: 25px;
            animation: successPulse 1s ease-in-out;
        }
        
        @keyframes successPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .registration-id-display {
            background: linear-gradient(135deg, #e3f2fd, #ffffff);
            padding: 25px;
            border-radius: 15px;
            margin: 25px 0;
            border: 2px solid #1976d2;
        }
        
        .registration-id {
            font-size: 2rem;
            font-weight: bold;
            color: #1976d2;
            margin: 15px 0;
            letter-spacing: 2px;
        }
        
        .department-info {
            background: linear-gradient(135deg, #f3e5f5, #ffffff);
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
        }
        
        .emergency-message {
            background: #ffebee;
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            display: none;
        }
        
        .modal-btn {
            background: #1976d2;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1rem;
            margin-top: 20px;
            transition: all 0.3s ease;
        }
        
        .modal-btn:hover {
            background: #1565c0;
            transform: translateY(-2px);
        }
        
        @media (max-width: 768px) {
            .container { padding: 25px 20px; }
            .form-grid { grid-template-columns: 1fr; }
            .severity-grid { grid-template-columns: 1fr; }
            .voice-controls { flex-direction: column; align-items: center; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 {{ t.book_appointment }}</h1>
            <p>{{ t.describe_symptoms }}</p>
        </div>
        
        <a href="/patient" class="back-btn">← {{ t.back }}</a>
        
        <!-- Voice Assistant Section -->
        <div class="voice-assistant">
            <div class="voice-controls">
                <button id="startVoiceBtn" class="voice-btn">
                    <span>🎤</span> {{ t.voice_help }}
                </button>
                <button id="stopVoiceBtn" class="voice-btn" disabled>
                    <span>⏹️</span> Stop
                </button>
                <button id="repeatBtn" class="voice-btn">
                    <span>🔄</span> Repeat
                </button>
            </div>
            <div id="voiceStatus" class="voice-status">{{ t.voice_help }} ready</div>
            <div class="voice-instructions">
                {{ t.speak_now }} to fill out the form. Say "next field" to move to the next input.
            </div>
        </div>
        
        <form id="registrationForm">
            <!-- Personal Information -->
            <div class="form-section">
                <div class="section-title">
                    👤 Personal Information
                </div>
                <div class="form-grid">
                    <div class="form-group">
                        <label for="name">{{ t.full_name }} *</label>
                        <input type="text" id="name" name="name" required>
                        <span class="voice-input-indicator">🎤</span>
                    </div>
                    <div class="form-group">
                        <label for="age">{{ t.age }} *</label>
                        <input type="number" id="age" name="age" min="1" max="120" required>
                    </div>
                    <div class="form-group">
                        <label for="gender">{{ t.gender }} *</label>
                        <select id="gender" name="gender" required>
                            <option value="">{{ t.select_gender }}</option>
                            <option value="Male">{{ t.male }}</option>
                            <option value="Female">{{ t.female }}</option>
                            <option value="Other">{{ t.other }}</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="phone">{{ t.phone }} *</label>
                        <input type="tel" id="phone" name="phone" required>
                    </div>
                    <div class="form-group">
                        <label for="email">{{ t.email }}</label>
                        <input type="email" id="email" name="email">
                    </div>
                </div>
            </div>
            
            <!-- Medical Information -->
            <div class="form-section">
                <div class="section-title">
                    🩺 Medical Information
                </div>
                
                <div class="form-group full-width">
                    <label for="main_symptom">{{ t.primary_symptom }} *</label>
                    <textarea id="main_symptom" name="main_symptom" rows="4" 
                              placeholder="{{ t.describe_symptoms }}" required></textarea>
                </div>
                
                <div class="form-group">
                    <label>{{ t.symptom_severity }} *</label>
                    <div class="severity-grid">
                        <div class="severity-btn mild" onclick="selectSeverity('Mild', this)">
                            <div class="severity-title">{{ t.mild }}</div>
                            <div class="severity-desc">{{ t.manageable_discomfort }}</div>
                        </div>
                        <div class="severity-btn moderate" onclick="selectSeverity('Moderate', this)">
                            <div class="severity-title">{{ t.moderate }}</div>
                            <div class="severity-desc">{{ t.noticeable_impact }}</div>
                        </div>
                        <div class="severity-btn severe" onclick="selectSeverity('Severe', this)">
                            <div class="severity-title">{{ t.severe }}</div>
                            <div class="severity-desc">{{ t.significant_distress }}</div>
                        </div>
                    </div>
                    <input type="hidden" id="severity" name="severity" required>
                </div>
                
                <div class="form-group">
                    <label for="symptom_days">{{ t.symptom_duration }} *</label>
                    <select id="symptom_days" name="symptom_days" required>
                        <option value="">{{ t.select_duration }}</option>
                        <option value="1">{{ t.today }}</option>
                        <option value="2">{{ t.days_2 }}</option>
                        <option value="3">{{ t.days_3 }}</option>
                        <option value="7">{{ t.week }}</option>
                        <option value="14">{{ t.weeks_2 }}</option>
                        <option value="30">{{ t.month }}</option>
                        <option value="90">{{ t.month_plus }}</option>
                    </select>
                </div>
            </div>
            
            <!-- Emergency Section -->
            <div class="emergency-section">
                <div class="emergency-toggle">
                    <div class="emergency-switch" id="emergencySwitch" onclick="toggleEmergency()"></div>
                    <div class="emergency-label">🚨 {{ t.emergency }}</div>
                </div>
                <div class="emergency-description">
                    <strong>{{ t.emergency_priority }}</strong>
                </div>
                <input type="hidden" id="is_emergency" name="is_emergency" value="false">
            </div>
            
            <button type="submit" class="submit-btn">
                📅 {{ t.submit }}
            </button>
        </form>
    </div>
    
    <!-- Success Modal -->
    <div id="successModal" class="modal">
        <div class="modal-content">
            <div class="success-icon">✅</div>
            <h2 style="font-size: 2rem; color: #1565c0; margin-bottom: 20px;">{{ t.success }}</h2>
            
            <div class="registration-id-display">
                <strong>{{ t.registration_id }}:</strong>
                <div id="registrationId" class="registration-id"></div>
            </div>
            
            <div id="departmentInfo" class="department-info">
                <h3 style="color: #9c27b0; margin-bottom: 10px;">📋 {{ t.department }}</h3>
                <div id="departmentName" style="font-size: 1.2rem; font-weight: bold;"></div>
            </div>
            
            <div id="emergencyMessage" class="emergency-message">
                <h4 style="color: #c62828; margin-bottom: 10px;">🚨 Emergency Priority Activated</h4>
                <p style="color: #ad1457;">Your emergency request is being prioritized. You will be contacted shortly.</p>
            </div>
            
            <button onclick="goToPatientPortal()" class="modal-btn">
                {{ t.back }}
            </button>
        </div>
    </div>

    <script>
        let selectedSeverity = '';
        let isEmergency = false;
        let recognition = null;
        let isListening = false;
        let currentField = null;
        
        // Initialize voice recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = '{{ lang }}';
            
            recognition.onstart = function() {
                isListening = true;
                document.getElementById('voiceStatus').textContent = '{{ t.listening }}';
                document.getElementById('startVoiceBtn').disabled = true;
                document.getElementById('stopVoiceBtn').disabled = false;
            };
            
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript.toLowerCase();
                processVoiceInput(transcript);
            };
            
            recognition.onend = function() {
                isListening = false;
                document.getElementById('voiceStatus').textContent = '{{ t.voice_help }} ready';
                document.getElementById('startVoiceBtn').disabled = false;
                document.getElementById('stopVoiceBtn').disabled = true;
            };
            
            recognition.onerror = function(event) {
                console.error('Speech recognition error:', event.error);
                document.getElementById('voiceStatus').textContent = 'Voice recognition error. Please try again.';
            };
        } else {
            document.getElementById('voiceStatus').textContent = '{{ t.voice_not_supported }}';
            document.getElementById('startVoiceBtn').disabled = true;
        }
        
        // Voice control functions
        document.getElementById('startVoiceBtn').addEventListener('click', function() {
            if (recognition && !isListening) {
                recognition.start();
                speakText('{{ t.speak_now }}');
            }
        });
        
        document.getElementById('stopVoiceBtn').addEventListener('click', function() {
            if (recognition && isListening) {
                recognition.stop();
            }
        });
        
        document.getElementById('repeatBtn').addEventListener('click', function() {
            const instructions = 'Please fill out the registration form. You can say your name, age, symptoms, and other information.';
            speakText(instructions);
        });
        
        function speakText(text) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = '{{ lang }}';
                utterance.rate = 0.8;
                speechSynthesis.speak(utterance);
            }
        }
        
        function processVoiceInput(transcript) {
            console.log('Voice input:', transcript);
            
            // Process different types of voice commands
            if (transcript.includes('name') || transcript.includes('नाम') || transcript.includes('பெயர்')) {
                const nameMatch = transcript.match(/(?:name is|नाम है|பெயர்)(.*)/i);
                if (nameMatch) {
                    document.getElementById('name').value = nameMatch[1].trim();
                    speakText('Name recorded');
                }
            }
            
            if (transcript.includes('age') || transcript.includes('उम्र') || transcript.includes('வயது')) {
                const ageMatch = transcript.match(/(?:age is|उम्र है|வயது)(\\d+)/i);
                if (ageMatch) {
                    document.getElementById('age').value = ageMatch[1];
                    speakText('Age recorded');
                }
            }
            
            if (transcript.includes('symptom') || transcript.includes('लक्षण') || transcript.includes('அறிகுறி')) {
                document.getElementById('main_symptom').value = transcript;
                speakText('Symptoms recorded');
            }
            
            if (transcript.includes('emergency') || transcript.includes('आपातकाल') || transcript.includes('அவசர')) {
                toggleEmergency();
                speakText('Emergency status updated');
            }
            
            // Severity detection
            if (transcript.includes('mild') || transcript.includes('हल्का') || transcript.includes('லேசான')) {
                selectSeverity('Mild', document.querySelector('.severity-btn.mild'));
                speakText('Mild severity selected');
            } else if (transcript.includes('moderate') || transcript.includes('मध्यम') || transcript.includes('மிதமான')) {
                selectSeverity('Moderate', document.querySelector('.severity-btn.moderate'));
                speakText('Moderate severity selected');
            } else if (transcript.includes('severe') || transcript.includes('गंभीर') || transcript.includes('கடுமையான')) {
                selectSeverity('Severe', document.querySelector('.severity-btn.severe'));
                speakText('Severe severity selected');
            }
        }
        
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
        
        // Form submission
        document.getElementById('registrationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!selectedSeverity) {
                alert('Please select symptom severity');
                speakText('Please select symptom severity');
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
                    
                    // Voice announcement
                    const announcement = `{{ t.success }} Your registration ID is ${result.registration_id}. Department: ${result.department}`;
                    speakText(announcement);
                } else {
                    alert('Error: ' + result.error);
                    speakText('Registration error. Please try again.');
                }
            } catch (error) {
                alert('Network error: ' + error.message);
                speakText('Network error. Please check your connection.');
            }
        });
        
        function goToPatientPortal() {
            window.location.href = '/patient?lang={{ lang }}';
        }
        
        // Auto-focus and voice guidance
        document.addEventListener('DOMContentLoaded', function() {
            // Welcome message
            setTimeout(() => {
                speakText('Welcome to patient registration. You can use voice commands to fill out the form.');
            }, 1000);
            
            // Add focus listeners for voice guidance
            document.querySelectorAll('input, select, textarea').forEach(field => {
                field.addEventListener('focus', function() {
                    currentField = this;
                    const label = this.previousElementSibling.textContent;
                    speakText(`Now entering ${label}`);
                });
            });
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
    <title>{{ t.check_status }} - MediCare Hospital</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            animation: gradientShift 15s ease infinite;
        }
        
        @keyframes gradientShift {
            0%, 100% { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            50% { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
            animation: slideDown 1s ease-out;
        }
        
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 30px;
            padding: 40px;
            box-shadow: 0 30px 100px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(20px);
            animation: slideUp 1s ease-out;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .voice-assistant {
            background: linear-gradient(135deg, #e8f5e8, #ffffff);
            border: 2px solid #4caf50;
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .voice-btn {
            background: linear-gradient(135deg, #4caf50, #45a049);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            margin: 0 10px;
            transition: all 0.3s ease;
        }
        
        .voice-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3);
        }
        
        .search-section {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .search-input {
            width: 100%;
            padding: 20px;
            border: 3px solid #e3f2fd;
            border-radius: 15px;
            font-size: 1.2rem;
            text-align: center;
            margin-bottom: 20px;
            text-transform: uppercase;
            transition: all 0.3s ease;
        }
        
        .search-input:focus {
            outline: none;
            border-color: #1976d2;
            box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
            transform: translateY(-2px);
        }
        
        .search-btn {
            background: linear-gradient(135deg, #1976d2, #1565c0);
            color: white;
            border: none;
            padding: 20px 40px;
            border-radius: 15px;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.4s ease;
            font-weight: 600;
        }
        
        .search-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(25, 118, 210, 0.4);
        }
        
        .status-card {
            display: none;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 25px;
            padding: 40px;
            margin-top: 30px;
            animation: cardSlideIn 0.5s ease-out;
        }
        
        @keyframes cardSlideIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .patient-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .patient-name {
            font-size: 2rem;
            color: #1565c0;
            font-weight: 700;
            margin-bottom: 15px;
        }
        
        .status-badge {
            display: inline-block;
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: bold;
            font-size: 1.1rem;
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
            margin-bottom: 30px;
        }
        
        .info-item {
            background: white;
            padding: 25px;
            border-radius: 15px;
            border-left: 4px solid #1976d2;
            transition: all 0.3s ease;
        }
        
        .info-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }
        
        .info-label {
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        .info-value {
            font-weight: 600;
            color: #1565c0;
            font-size: 1.2rem;
        }
        
        .status-message {
            margin-top: 25px;
            padding: 30px;
            background: white;
            border-radius: 20px;
            text-align: center;
            border: 2px solid #e3f2fd;
        }
        
        .error-message {
            background: linear-gradient(135deg, #ffebee, #fce4ec);
            color: #c62828;
            padding: 25px;
            border-radius: 15px;
            margin-top: 20px;
            text-align: center;
            display: none;
            animation: shake 0.5s ease-in-out;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        
        .back-btn {
            background: linear-gradient(135deg, #90a4ae, #78909c);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 10px;
            text-decoration: none;
            display: inline-block;
            margin-bottom: 25px;
            transition: all 0.3s ease;
        }
        
        .back-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(144, 164, 174, 0.3);
        }
        
        @media (max-width: 768px) {
            .container { padding: 25px 20px; }
            .info-grid { grid-template-columns: 1fr; }
            .header h1 { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 {{ t.check_status }}</h1>
        <p>{{ t.enter_registration_id }}</p>
    </div>
    
    <div class="container">
        <a href="/patient?lang={{ lang }}" class="back-btn">← {{ t.back }}</a>
        
        <!-- Voice Assistant -->
        <div class="voice-assistant">
            <button id="voiceSearchBtn" class="voice-btn">
                <span>🎤</span> {{ t.voice_help }}
            </button>
            <button id="speakStatusBtn" class="voice-btn" style="display: none;">
                <span>🔊</span> Read Status
            </button>
            <div id="voiceStatus" style="margin-top: 10px; color: #2e7d32; font-weight: 600;">
                {{ t.voice_help }} ready for registration ID
            </div>
        </div>
        
        <div class="search-section">
            <input type="text" id="registrationId" class="search-input" 
                   placeholder="{{ t.enter_registration_id }}">
            <br>
            <button onclick="checkStatus()" class="search-btn">
                🔍 {{ t.check_status_btn }}
            </button>
        </div>
        
        <div id="errorMessage" class="error-message"></div>
        
        <div id="statusCard" class="status-card">
            <div class="patient-header">
                <div id="patientName" class="patient-name"></div>
                <div id="statusBadge" class="status-badge"></div>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">{{ t.registration_id }}</div>
                    <div id="regId" class="info-value"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">{{ t.department }}</div>
                    <div id="department" class="info-value"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Risk Score</div>
                    <div id="riskScore" class="info-value"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">{{ t.symptom_severity }}</div>
                    <div id="severity" class="info-value"></div>
                </div>
                
                <div class="info-item" id="appointmentTimeItem" style="display: none;">
                    <div class="info-label">Appointment Time</div>
                    <div id="appointmentTime" class="info-value"></div>
                </div>
            </div>
            
            <div id="statusMessage" class="status-message"></div>
        </div>
    </div>

    <script>
        let recognition = null;
        let currentPatientData = null;
        
        // Initialize voice recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = '{{ lang }}';
            
            recognition.onstart = function() {
                document.getElementById('voiceStatus').textContent = '{{ t.listening }}';
            };
            
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript.toUpperCase();
                // Extract registration ID from speech
                const regIdMatch = transcript.match(/MED\\d{6}|\\d{6}/);
                if (regIdMatch) {
                    const regId = regIdMatch[0].startsWith('MED') ? regIdMatch[0] : 'MED' + regIdMatch[0];
                    document.getElementById('registrationId').value = regId;
                    checkStatus();
                } else {
                    document.getElementById('registrationId').value = transcript.replace(/\\s/g, '');
                    speakText('Registration ID entered. Click check status or say check status.');
                }
            };
            
            recognition.onend = function() {
                document.getElementById('voiceStatus').textContent = '{{ t.voice_help }} ready';
            };
        }
        
        document.getElementById('voiceSearchBtn').addEventListener('click', function() {
            if (recognition) {
                recognition.start();
                speakText('{{ t.speak_now }} your registration ID');
            }
        });
        
        document.getElementById('speakStatusBtn').addEventListener('click', function() {
            if (currentPatientData) {
                speakPatientStatus(currentPatientData);
            }
        });
        
        function speakText(text) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = '{{ lang }}';
                utterance.rate = 0.8;
                speechSynthesis.speak(utterance);
            }
        }
        
        function speakPatientStatus(patient) {
            const statusText = `Patient ${patient.name}. Status: ${patient.status}. Department: ${patient.department}. Risk score: ${patient.risk_score}. Severity: ${patient.severity}.`;
            speakText(statusText);
        }
        
        async function checkStatus() {
            const registrationId = document.getElementById('registrationId').value.trim().toUpperCase();
            
            if (!registrationId) {
                showError('{{ t.enter_registration_id }}');
                speakText('{{ t.enter_registration_id }}');
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
                    currentPatientData = result.patient;
                    displayPatientStatus(result.patient);
                    hideError();
                    document.getElementById('speakStatusBtn').style.display = 'inline-block';
                    
                    // Voice announcement
                    speakText(`Status found for ${result.patient.name}`);
                } else {
                    showError(result.error);
                    hideStatusCard();
                    speakText(result.error);
                }
            } catch (error) {
                showError('{{ t.network_error }}');
                hideStatusCard();
                speakText('{{ t.network_error }}');
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
                statusMessage.innerHTML = '<h3 style="color: #f57c00; margin-bottom: 15px;">⏳ {{ t.status_waiting }}</h3><p>{{ t.appointment_pending }}</p>';
            } else if (patient.status === 'confirmed') {
                statusMessage.innerHTML = '<h3 style="color: #2e7d32; margin-bottom: 15px;">✅ {{ t.status_confirmed }}</h3><p>{{ t.appointment_confirmed }}</p>';
                if (patient.appointment_time) {
                    document.getElementById('appointmentTime').textContent = formatDateTime(patient.appointment_time);
                    document.getElementById('appointmentTimeItem').style.display = 'block';
                }
            }
            
            document.getElementById('statusCard').style.display = 'block';
        }
        
        function formatDateTime(dateString) {
            if (!dateString) return 'Not scheduled';
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
            document.getElementById('speakStatusBtn').style.display = 'none';
        }
        
        // Enter key support
        document.getElementById('registrationId').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                checkStatus();
            }
        });
        
        // Welcome message
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(() => {
                speakText('Welcome to appointment status check. You can use voice commands to enter your registration ID.');
            }, 1000);
        });
    </script>
</body>
</html>
'''

# Admin templates remain the same as hospital_fixed.py but with enhanced styling
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: gradientShift 15s ease infinite;
        }
        
        @keyframes gradientShift {
            0%, 100% { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            50% { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        }
        
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 30px;
            padding: 60px;
            box-shadow: 0 30px 100px rgba(0, 0, 0, 0.2);
            max-width: 500px;
            width: 90%;
            backdrop-filter: blur(20px);
            animation: slideUp 1s ease-out;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .admin-icon {
            font-size: 4rem;
            color: #d32f2f;
            margin-bottom: 20px;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #1565c0;
        }
        
        input {
            width: 100%;
            padding: 18px;
            border: 2px solid #e3f2fd;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        input:focus {
            outline: none;
            border-color: #d32f2f;
            box-shadow: 0 0 0 3px rgba(211, 47, 47, 0.1);
            transform: translateY(-2px);
        }
        
        .login-btn {
            width: 100%;
            background: linear-gradient(135deg, #d32f2f, #c62828);
            color: white;
            border: none;
            padding: 20px;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.4s ease;
        }
        
        .login-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(211, 47, 47, 0.4);
        }
        
        .error-message {
            background: linear-gradient(135deg, #ffebee, #fce4ec);
            color: #c62828;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            display: none;
        }
        
        .demo-credentials {
            background: linear-gradient(135deg, #f3e5f5, #ffffff);
            padding: 25px;
            border-radius: 15px;
            margin-top: 30px;
            text-align: center;
            border: 2px solid #e1bee7;
        }
        
        .back-btn {
            background: linear-gradient(135deg, #90a4ae, #78909c);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            margin-bottom: 30px;
            transition: all 0.3s ease;
        }
        
        .back-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(144, 164, 174, 0.3);
        }
    </style>
</head>
<body>
    <div class="login-container">
        <a href="/" class="back-btn">← Back to Home</a>
        
        <div class="login-header">
            <div class="admin-icon">🛡️</div>
            <h1 style="color: #1565c0; margin-bottom: 10px; font-size: 2.2rem;">Admin Portal</h1>
            <p style="color: #546e7a;">Hospital Management System</p>
        </div>
        
        <div id="errorMessage" class="error-message"></div>
        
        <form id="loginForm">
            <div class="form-group">
                <label for="username">👤 Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">🔒 Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="login-btn">
                🔐 Secure Login
            </button>
        </form>
        
        <div class="demo-credentials">
            <h3 style="color: #1565c0; margin-bottom: 15px;">🔑 Demo Credentials</h3>
            <p><strong>Username:</strong> admin</p>
            <p><strong>Password:</strong> hospital2024</p>
        </div>
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
                    showError(result.error);
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            }
        });
        
        function showError(message) {
            document.getElementById('errorMessage').textContent = message;
            document.getElementById('errorMessage').style.display = 'block';
        }
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
                </div>
                <div class="stat-number" id="doctorsOnline">0</div>
                <div class="stat-label">Doctors Online</div>
            </div>
        </div>
        
        <!-- Enhanced Patient Management Table -->
        <div class="patients-section">
            <div class="section-header">
                <h3 class="section-title">
                    <span>👥</span> Enhanced Patient Management
                </h3>
                <button onclick="refreshPatients()" class="refresh-btn">
                    🔄 Refresh Patients
                </button>
            </div>
            <div class="table-container">
                <table class="patients-table">
                    <thead>
                        <tr>
                            <th>Patient Info</th>
                            <th>Age</th>
                            <th>Symptoms</th>
                            <th>Risk Level</th>
                            <th>Department</th>
                            <th>Language</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="patientsTableBody">
                        <!-- Enhanced patients will be loaded here -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <!-- Enhanced Confirm Patient Modal -->
    <div id="confirmModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>📅 Confirm Patient Appointment</h3>
            </div>
            <div style="margin-bottom: 20px;">
                <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #1565c0;">Appointment Date & Time:</label>
                <input type="datetime-local" id="appointmentDateTime" style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px;" required>
            </div>
            <div style="display: flex; gap: 15px; justify-content: flex-end;">
                <button onclick="closeConfirmModal()" class="modal-btn secondary">Cancel</button>
                <button onclick="confirmPatient()" class="modal-btn">Confirm Appointment</button>
            </div>
        </div>
    </div>
    
    <!-- Enhanced Report Modal -->
    <div id="reportModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>📋 Enhanced Patient Report</h3>
            </div>
            <div id="reportContent" style="margin-bottom: 20px;">
                <!-- Enhanced report content will be loaded here -->
            </div>
            <div style="display: flex; gap: 15px; justify-content: flex-end;">
                <button onclick="closeReportModal()" class="modal-btn secondary">Close</button>
                <button onclick="downloadReport()" class="modal-btn">📥 Download PDF</button>
                <button onclick="downloadExcel()" class="modal-btn" style="background: linear-gradient(135deg, #2ecc71, #27ae60);">📊 Download Excel</button>
            </div>
        </div>
    </div>
    
    <!-- Language Indicator -->
    <div class="language-indicator">
        🌐 Multilingual Support: EN | HI | TA
    </div>

    <script>
        let currentPatientId = null;
        let currentReportData = null;
        
        // Load enhanced dashboard data on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadDashboardStats();
            loadPatients();
            
            // Auto-refresh every 30 seconds
            setInterval(() => {
                loadDashboardStats();
                loadPatients();
            }, 30000);
            
            // Add loading animation
            showLoadingAnimation();
        });
        
        function showLoadingAnimation() {
            const statNumbers = document.querySelectorAll('.stat-number');
            statNumbers.forEach(num => {
                num.style.opacity = '0.5';
                num.textContent = '...';
            });
        }
        
        async function loadDashboardStats() {
            try {
                const response = await fetch('/api/admin/dashboard_stats');
                const stats = await response.json();
                
                // Animate stat updates
                animateStatUpdate('totalToday', stats.total_today);
                animateStatUpdate('criticalCases', stats.critical_cases);
                animateStatUpdate('avgWaiting', stats.avg_waiting);
                animateStatUpdate('doctorsOnline', stats.doctors_online);
                
            } catch (error) {
                console.error('Error loading dashboard stats:', error);
            }
        }
        
        function animateStatUpdate(elementId, newValue) {
            const element = document.getElementById(elementId);
            element.style.opacity = '1';
            
            // Simple count-up animation
            const currentValue = parseInt(element.textContent) || 0;
            const increment = (newValue - currentValue) / 20;
            let current = currentValue;
            
            const timer = setInterval(() => {
                current += increment;
                if ((increment > 0 && current >= newValue) || (increment < 0 && current <= newValue)) {
                    element.textContent = newValue;
                    clearInterval(timer);
                } else {
                    element.textContent = Math.round(current);
                }
            }, 50);
        }
        
        async function loadPatients() {
            try {
                const response = await fetch('/api/admin/patients');
                const patients = await response.json();
                
                const tbody = document.getElementById('patientsTableBody');
                tbody.innerHTML = '';
                
                patients.forEach((patient, index) => {
                    const row = document.createElement('tr');
                    row.style.animationDelay = `${index * 0.1}s`;
                    row.innerHTML = `
                        <td>
                            <div style="font-weight: 600; color: #1565c0;">${patient.name}</div>
                            <div style="font-size: 0.8rem; color: #666;">${patient.registration_id}</div>
                            <div style="font-size: 0.8rem; color: #666;">📞 ${patient.phone}</div>
                        </td>
                        <td>${patient.age}</td>
                        <td style="max-width: 200px;">
                            <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${patient.symptom}">
                                ${patient.symptom}
                            </div>
                            <div style="font-size: 0.8rem; color: #666; margin-top: 4px;">${patient.severity}</div>
                        </td>
                        <td>
                            <span class="risk-badge risk-${getRiskLevel(patient.risk_score)}">
                                ${getRiskLevel(patient.risk_score)} (${patient.risk_score})
                            </span>
                        </td>
                        <td>
                            <div style="font-weight: 600; color: #1565c0;">${patient.department}</div>
                        </td>
                        <td>
                            <span style="padding: 4px 8px; background: #e3f2fd; color: #1976d2; border-radius: 10px; font-size: 0.8rem; font-weight: 600;">
                                ${getLanguageFlag(patient.language)} ${patient.language.toUpperCase()}
                            </span>
                        </td>
                        <td>
                            <span class="status-badge status-${patient.status}">
                                ${patient.status.charAt(0).toUpperCase() + patient.status.slice(1)}
                            </span>
                        </td>
                        <td>
                            <div style="display: flex; gap: 5px; flex-wrap: wrap;">
                                ${patient.status === 'waiting' ? 
                                    `<button onclick="openConfirmModal(${patient.id})" class="action-btn">✅ Confirm</button>` :
                                    `<button onclick="generateReport(${patient.id})" class="action-btn report">📋 Report</button>`
                                }
                                <button onclick="sendNotification(${patient.id}, '${patient.language}')" class="action-btn" style="background: linear-gradient(135deg, #ff9800, #f57c00);">📧 Notify</button>
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
        
        function getLanguageFlag(lang) {
            const flags = { 'en': '🇺🇸', 'hi': '🇮🇳', 'ta': '🇮🇳' };
            return flags[lang] || '🌐';
        }
        
        function refreshPatients() {
            showLoadingAnimation();
            loadPatients();
            
            // Show refresh feedback
            const btn = event.target;
            const originalText = btn.innerHTML;
            btn.innerHTML = '🔄 Refreshing...';
            btn.disabled = true;
            
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }, 2000);
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
                    showNotification('Patient confirmed successfully! Multilingual notification sent.', 'success');
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
                    displayEnhancedReport(result.report_data);
                    document.getElementById('reportModal').style.display = 'flex';
                } else {
                    alert('Error generating report: ' + result.error);
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        }
        
        function displayEnhancedReport(data) {
            const reportContent = document.getElementById('reportContent');
            reportContent.innerHTML = `
                <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); padding: 25px; border-radius: 15px; margin-bottom: 20px;">
                    <h4 style="color: #1565c0; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                        <span>👤</span> Patient Information
                    </h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                        <div><strong>Name:</strong> ${data.patient_name}</div>
                        <div><strong>Registration ID:</strong> ${data.registration_id}</div>
                        <div><strong>Age:</strong> ${data.age}</div>
                        <div><strong>Gender:</strong> ${data.gender}</div>
                        <div><strong>Phone:</strong> ${data.phone}</div>
                        <div><strong>Email:</strong> ${data.email || 'Not provided'}</div>
                        <div><strong>Language:</strong> ${getLanguageFlag(data.language_preference)} ${data.language_preference.toUpperCase()}</div>
                        <div><strong>Department:</strong> ${data.department}</div>
                    </div>
                </div>
                
                <div style="background: linear-gradient(135deg, #fff3e0, #ffffff); padding: 25px; border-radius: 15px; margin-bottom: 20px;">
                    <h4 style="color: #f57c00; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                        <span>🩺</span> Medical Assessment
                    </h4>
                    <div><strong>Primary Symptom:</strong> ${data.symptom}</div>
                    <div style="margin-top: 10px;"><strong>Severity:</strong> ${data.severity}</div>
                    <div style="margin-top: 10px;"><strong>Duration:</strong> ${data.symptom_days} days</div>
                    <div style="margin-top: 10px;"><strong>Risk Score:</strong> ${data.risk_score}/100</div>
                    <div style="margin-top: 10px;"><strong>Emergency Case:</strong> ${data.is_emergency ? 'Yes' : 'No'}</div>
                </div>
                
                <div style="background: ${data.status === 'confirmed' ? 'linear-gradient(135deg, #e8f5e8, #ffffff)' : 'linear-gradient(135deg, #ffebee, #ffffff)'}; padding: 25px; border-radius: 15px;">
                    <h4 style="color: ${data.status === 'confirmed' ? '#2e7d32' : '#c62828'}; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                        <span>${data.status === 'confirmed' ? '✅' : '⏳'}</span> Appointment Status
                    </h4>
                    <div><strong>Status:</strong> ${data.status.charAt(0).toUpperCase() + data.status.slice(1)}</div>
                    <div style="margin-top: 10px;"><strong>Registered:</strong> ${formatDateTime(data.created_at)}</div>
                    ${data.appointment_time ? `<div style="margin-top: 10px;"><strong>Appointment Time:</strong> ${formatDateTime(data.appointment_time)}</div>` : ''}
                    ${data.admin_notes ? `<div style="margin-top: 10px;"><strong>Admin Notes:</strong> ${data.admin_notes}</div>` : ''}
                </div>
            `;
        }
        
        function closeReportModal() {
            document.getElementById('reportModal').style.display = 'none';
            currentReportData = null;
        }
        
        function downloadReport() {
            if (currentReportData) {
                showNotification('PDF report download would be implemented in production with patient data in their preferred language.', 'info');
            }
        }
        
        function downloadExcel() {
            if (currentReportData) {
                showNotification('Excel report download would be implemented in production with multilingual headers.', 'info');
            }
        }
        
        function sendNotification(patientId, language) {
            showNotification(`Notification sent to patient in ${language.toUpperCase()} language!`, 'success');
        }
        
        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${type === 'success' ? '#4caf50' : type === 'error' ? '#f44336' : '#2196f3'};
                color: white;
                padding: 15px 25px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
                z-index: 3000;
                animation: slideInRight 0.3s ease-out;
                max-width: 300px;
            `;
            notification.textContent = message;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideOutRight 0.3s ease-in';
                setTimeout(() => notification.remove(), 300);
            }, 4000);
        }
        
        function formatDateTime(dateString) {
            if (!dateString) return 'Not scheduled';
            const date = new Date(dateString);
            return date.toLocaleDateString() + ' at ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }
        
        // Add CSS animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOutRight {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
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