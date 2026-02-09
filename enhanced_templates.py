# Enhanced Templates for Multilingual Telemedicine System

ENHANCED_PATIENT_REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book Appointment - MediCare Hospital</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #005eb8;
            --primary-dark: #003d78;
            --secondary: #00b0b9;
            --accent: #ed8b00;
            --bg-color: #f0f4f8;
            --surface: #ffffff;
            --text-main: #212529;
            --text-light: #55595c;
            --border: #dee2e6;
            --success: #007f3b;
            --shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            line-height: 1.6;
        }
        
        .container {
            max-width: 900px;
            margin: 40px auto;
            background: var(--surface);
            border-radius: 12px;
            box-shadow: var(--shadow);
            overflow: hidden;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .header-panel {
            background-color: var(--primary);
            color: white;
            padding: 40px 30px;
            text-align: center;
            background-image: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        }
        
        .header-panel h1 {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 10px;
        }
        
        .header-panel p {
            font-size: 1.1rem;
            opacity: 0.9;
            font-weight: 300;
        }
        
        .content-body {
            padding: 40px;
        }
        
        .back-link {
            display: inline-flex;
            align-items: center;
            color: var(--text-light);
            text-decoration: none;
            font-weight: 500;
            margin-bottom: 30px;
            transition: color 0.2s;
        }
        
        .back-link:hover {
            color: var(--primary);
        }
        
        .form-section {
            background: #fff;
            margin-bottom: 30px;
        }
        
        .section-title {
            font-size: 1.25rem;
            color: var(--primary);
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eef2f6;
            font-weight: 600;
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 24px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group.full-width {
            grid-column: span 2;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--text-main);
            font-size: 0.95rem;
        }
        
        .form-group label span {
            color: #d32f2f;
        }
        
        .form-control {
            width: 100%;
            padding: 12px 16px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 1rem;
            font-family: inherit;
            transition: border-color 0.2s, box-shadow 0.2s;
            background-color: #fcfcfc;
        }
        
        .form-control:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(0, 94, 184, 0.15);
            background-color: #fff;
        }
        
        textarea.form-control {
            resize: vertical;
            min-height: 100px;
        }
        
        .checkbox-wrapper {
            display: flex;
            align-items: center;
            padding: 15px;
            background-color: #fff8e1;
            border: 1px solid #ffe082;
            border-radius: 8px;
        }
        
        .checkbox-wrapper input[type="checkbox"] {
            width: 20px;
            height: 20px;
            margin-right: 12px;
            accent-color: #d32f2f;
        }
        
        .checkbox-wrapper label {
            margin: 0;
            color: #bf360c;
            font-weight: 600;
        }
        
        .submit-btn {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 16px 32px;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: all 0.2s;
            box-shadow: 0 4px 6px rgba(0,94,184,0.2);
        }
        
        .submit-btn:hover {
            background-color: var(--primary-dark);
            transform: translateY(-1px);
            box-shadow: 0 6px 12px rgba(0,94,184,0.3);
        }
        
        @media (max-width: 768px) {
            .container { margin: 0; border-radius: 0; box-shadow: none; }
            .form-grid { grid-template-columns: 1fr; }
            .form-group.full-width { grid-column: auto; }
            .content-body { padding: 25px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-panel">
            <h1>New Appointment</h1>
            <p>Complete the form below to schedule your consultation</p>
        </div>
        
        <div class="content-body">
            <a href="/patient" class="back-link">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
                Back to Dashboard
            </a>
            
            <form id="registrationForm">
                <div class="form-section">
                    <h3 class="section-title">Personal Information</h3>
                    <div class="form-grid">
                        <div class="form-group full-width">
                            <label for="name">Full Name <span>*</span></label>
                            <input type="text" id="name" name="name" class="form-control" placeholder="Enter your full name" required>
                        </div>
                        <div class="form-group">
                            <label for="age">Age <span>*</span></label>
                            <input type="number" id="age" name="age" class="form-control" min="1" max="120" placeholder="Years" required>
                        </div>
                        <div class="form-group">
                            <label for="gender">Gender <span>*</span></label>
                            <select id="gender" name="gender" class="form-control" required>
                                <option value="">Select Gender</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="phone">Phone Number <span>*</span></label>
                            <input type="tel" id="phone" name="phone" class="form-control" placeholder="Mobile number" required>
                        </div>
                        <div class="form-group">
                            <label for="email">Email Address</label>
                            <input type="email" id="email" name="email" class="form-control" placeholder="email@example.com">
                        </div>
                    </div>
                </div>
                
                <div class="form-section">
                    <h3 class="section-title">Medical Details</h3>
                    <div class="form-group full-width">
                        <label for="main_symptom">Primary Concern / Symptom <span>*</span></label>
                        <textarea id="main_symptom" name="main_symptom" class="form-control" rows="3" placeholder="Describe what you are feeling..." required></textarea>
                    </div>
                    
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="severity">Severity Assessment <span>*</span></label>
                            <select id="severity" name="severity" class="form-control" required>
                                <option value="">How severe is it?</option>
                                <option value="Mild">Mild (Annoying but bearable)</option>
                                <option value="Moderate">Moderate (Affects daily life)</option>
                                <option value="Severe">Severe (Unbearable pain/distress)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="symptom_days">Duration <span>*</span></label>
                            <select id="symptom_days" name="symptom_days" class="form-control" required>
                                <option value="">How long?</option>
                                <option value="1">Today / < 24 Hours</option>
                                <option value="2">2-3 Days</option>
                                <option value="7">One Week</option>
                                <option value="30">One Month or more</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="form-group full-width">
                        <div class="checkbox-wrapper">
                            <input type="checkbox" id="is_emergency" name="is_emergency">
                            <label for="is_emergency">This is a Medical Emergency (Priority Queue)</label>
                        </div>
                    </div>
                </div>
                
                <button type="submit" class="submit-btn" id="submitBtn">Book Appointment Now</button>
            </form>
        </div>
    </div>

    <script>
        document.getElementById('registrationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const btn = document.getElementById('submitBtn');
            const originalText = btn.innerText;
            btn.disabled = true;
            btn.innerText = 'Processing...';
            
            const formData = {
                name: document.getElementById('name').value,
                age: parseInt(document.getElementById('age').value),
                gender: document.getElementById('gender').value,
                phone: document.getElementById('phone').value,
                email: document.getElementById('email').value,
                main_symptom: document.getElementById('main_symptom').value,
                severity: document.getElementById('severity').value,
                symptom_days: parseInt(document.getElementById('symptom_days').value),
                is_emergency: document.getElementById('is_emergency').checked
            };
            
            try {
                const response = await fetch('/api/register_patient', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Success UI feedback could be better here, but alert is robust
                    alert(`✅ Appointment Booked Successfully!\n\nRegistration ID: ${result.registration_id}\nDepartment: ${result.department}`);
                    window.location.href = '/patient';
                } else {
                    alert('❌ Error: ' + result.error);
                }
            } catch (error) {
                alert('⚠️ Network Connection Error: ' + error.message);
            } finally {
                btn.disabled = false;
                btn.innerText = originalText;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #005eb8;
            --primary-dark: #003d78;
            --secondary: #00b0b9;
            --accent: #ed8b00;
            --bg-color: #f0f4f8;
            --surface: #ffffff;
            --text-main: #212529;
            --text-light: #55595c;
            --border: #dee2e6;
            --success: #007f3b;
            --error: #d32f2f;
            --shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            line-height: 1.6;
        }
        
        .container {
            max-width: 600px;
            margin: 60px auto;
            background: var(--surface);
            border-radius: 12px;
            box-shadow: var(--shadow);
            overflow: hidden;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .header-panel {
            background-color: var(--primary);
            color: white;
            padding: 40px 30px;
            text-align: center;
            background-image: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        }
        
        .header-panel h1 {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 10px;
        }
        
        .header-panel p {
            font-size: 1rem;
            opacity: 0.9;
        }
        
        .content-body {
            padding: 40px;
        }
        
        .back-link {
            display: inline-flex;
            align-items: center;
            color: var(--text-light);
            text-decoration: none;
            font-weight: 500;
            margin-bottom: 30px;
            transition: color 0.2s;
        }
        
        .back-link:hover {
            color: var(--primary);
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--text-main);
            font-size: 0.95rem;
        }
        
        .form-control {
            width: 100%;
            padding: 14px 16px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.2s, box-shadow 0.2s;
            font-family: inherit;
        }
        
        .form-control:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(0, 94, 184, 0.15);
        }
        
        .check-btn {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 16px 32px;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: all 0.2s;
            box-shadow: 0 4px 6px rgba(0,94,184,0.2);
        }
        
        .check-btn:hover {
            background-color: var(--primary-dark);
            transform: translateY(-1px);
            box-shadow: 0 6px 12px rgba(0,94,184,0.3);
        }
        
        .status-result {
            margin-top: 30px;
            padding: 25px;
            border-radius: 8px;
            display: none;
            animation: slideUp 0.3s ease;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .status-success {
            background-color: #e6f6f6;
            border-left: 4px solid var(--primary);
        }
        
        .status-error {
            background-color: #fde8e8;
            border-left: 4px solid var(--error);
        }
        
        .status-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        
        .status-success .status-title { color: var(--primary-dark); }
        .status-error .status-title { color: var(--error); }
        
        .status-details p {
            margin-bottom: 8px;
            font-size: 0.95rem;
            color: #333;
        }
        
        .status-details strong {
            font-weight: 600;
            color: var(--text-main);
            min-width: 100px;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-panel">
            <h1>Check Status</h1>
            <p>Enter your registration ID to view appointment details</p>
        </div>
        
        <div class="content-body">
            <a href="/patient" class="back-link">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
                Back to Dashboard
            </a>
            
            <form id="statusForm">
                <div class="form-group">
                    <label for="registration_id">Registration ID</label>
                    <input type="text" id="registration_id" name="registration_id" class="form-control" placeholder="e.g., MED123456" required>
                </div>
                
                <button type="submit" class="check-btn" id="checkBtn">Check Status</button>
            </form>
            
            <div id="statusResult" class="status-result">
                <!-- Content injected via JS -->
            </div>
        </div>
    </div>

    <script>
        document.getElementById('statusForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const btn = document.getElementById('checkBtn');
            const originalText = btn.innerText;
            btn.disabled = true;
            btn.innerText = 'Checking...';
            
            const registrationId = document.getElementById('registration_id').value;
            
            try {
                const response = await fetch('/api/check_patient_status', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ registration_id: registrationId })
                });
                
                const result = await response.json();
                const statusDiv = document.getElementById('statusResult');
                
                if (result.success) {
                    const patient = result.patient;
                    statusDiv.className = 'status-result status-success';
                    statusDiv.innerHTML = `
                        <div class="status-title">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 10px;"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                            Record Found
                        </div>
                        <div class="status-details">
                            <p><strong>Name:</strong> ${patient.name}</p>
                            <p><strong>Status:</strong> ${patient.status}</p>
                            <p><strong>Department:</strong> ${patient.department}</p>
                            <p><strong>Date:</strong> ${new Date(patient.registered_date).toLocaleDateString()}</p>
                            ${patient.appointment_time ? `<p><strong>Appointment:</strong> ${new Date(patient.appointment_time).toLocaleString()}</p>` : ''}
                        </div>
                    `;
                } else {
                    statusDiv.className = 'status-result status-error';
                    statusDiv.innerHTML = `
                        <div class="status-title">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 10px;"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
                            Not Found
                        </div>
                        <div class="status-details">
                            <p>${result.error}</p>
                        </div>
                    `;
                }
                
                statusDiv.style.display = 'block';
                
            } catch (error) {
                const statusDiv = document.getElementById('statusResult');
                statusDiv.className = 'status-result status-error';
                statusDiv.innerHTML = `
                   <div class="status-title">Network Error</div>
                   <p>${error.message}</p>
                `;
                statusDiv.style.display = 'block';
            } finally {
                btn.disabled = false;
                btn.innerText = originalText;
            }
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #005eb8;
            --primary-dark: #003d78;
            --bg-color: #f0f4f8;
            --surface: #ffffff;
            --text-main: #212529;
            --text-light: #55595c;
            --border: #dee2e6;
            --shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 10% 10%, rgba(0, 94, 184, 0.05) 0%, transparent 50%),
                radial-gradient(at 90% 90%, rgba(0, 176, 185, 0.05) 0%, transparent 50%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .login-container {
            background: var(--surface);
            padding: 50px;
            border-radius: 16px;
            box-shadow: var(--shadow);
            max-width: 420px;
            width: 90%;
            border: 1px solid rgba(255,255,255,0.8);
            backdrop-filter: blur(10px);
            animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .logo {
            font-size: 3rem;
            margin-bottom: 15px;
            display: inline-block;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .login-header h1 {
            color: var(--primary-dark);
            font-size: 1.8rem;
            margin-bottom: 8px;
            font-weight: 700;
        }
        
        .login-header p {
            color: var(--text-light);
            font-size: 0.95rem;
        }
        
        .form-group {
            margin-bottom: 24px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--text-main);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .form-control {
            width: 100%;
            padding: 14px 16px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.2s;
            font-family: inherit;
            background-color: #fcfcfc;
        }
        
        .form-control:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(0, 94, 184, 0.15);
            background-color: #fff;
        }
        
        .login-btn {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 16px 32px;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: all 0.2s;
            box-shadow: 0 4px 10px rgba(0,94,184,0.25);
            margin-top: 10px;
        }
        
        .login-btn:hover {
            background-color: var(--primary-dark);
            transform: translateY(-1px);
            box-shadow: 0 6px 14px rgba(0,94,184,0.35);
        }
        
        .back-link {
            display: block;
            text-align: center;
            margin-top: 25px;
            text-decoration: none;
            color: var(--text-light);
            font-size: 0.9rem;
            transition: color 0.2s;
        }
        
        .back-link:hover {
            color: var(--primary);
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <div class="logo">🛡️</div>
            <h1>Admin Portal</h1>
            <p>Secure Access for Hospital Staff</p>
        </div>
        
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" class="form-control" placeholder="Enter username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" class="form-control" placeholder="••••••••" required>
            </div>
            
            <button type="submit" class="login-btn" id="loginBtn">Sign In</button>
        </form>
        
        <a href="/" class="back-link">← Return to Main Page</a>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const btn = document.getElementById('loginBtn');
            const originalText = btn.innerText;
            btn.disabled = true;
            btn.innerText = 'Authenticating...';
            
            const formData = {
                username: document.getElementById('username').value,
                password: document.getElementById('password').value
            };
            
            try {
                const response = await fetch('/admin/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    window.location.href = '/admin/dashboard';
                } else {
                    alert('❌ Access Denied: ' + result.error);
                }
            } catch (error) {
                alert('⚠️ Connection Error: ' + error.message);
            } finally {
                btn.disabled = false;
                btn.innerText = originalText;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #005eb8;
            --primary-dark: #003d78;
            --secondary: #00b0b9;
            --accent: #ed8b00;
            --bg-color: #f0f4f8;
            --surface: #ffffff;
            --text-main: #212529;
            --text-light: #55595c;
            --border: #dee2e6;
            --success: #007f3b;
            --warning: #ffc20e;
            --error: #d32f2f;
            --sidebar-width: 260px;
            --header-height: 70px;
            --shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
        }
        
        /* Sidebar */
        .sidebar {
            width: var(--sidebar-width);
            background-color: var(--primary-dark);
            color: white;
            position: fixed;
            height: 100vh;
            left: 0;
            top: 0;
            display: flex;
            flex-direction: column;
            z-index: 100;
        }
        
        .sidebar-header {
            height: var(--header-height);
            display: flex;
            align-items: center;
            padding: 0 24px;
            background-color: rgba(0,0,0,0.1);
            font-weight: 700;
            font-size: 1.25rem;
            letter-spacing: 0.5px;
        }
        
        .sidebar-header span {
            color: var(--secondary);
            margin-right: 8px;
        }
        
        .nav-menu {
            list-style: none;
            padding: 24px 0;
            flex-grow: 1;
        }
        
        .nav-item {
            margin-bottom: 4px;
        }
        
        .nav-link {
            display: flex;
            align-items: center;
            padding: 12px 24px;
            color: rgba(255,255,255,0.7);
            text-decoration: none;
            transition: all 0.2s;
            font-weight: 500;
        }
        
        .nav-link:hover, .nav-link.active {
            color: white;
            background-color: rgba(255,255,255,0.1);
            border-right: 3px solid var(--secondary);
        }
        
        .nav-icon {
            margin-right: 12px;
            width: 20px;
            text-align: center;
        }
        
        .user-profile {
            padding: 24px;
            background-color: rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .user-info {
            font-size: 0.9rem;
        }
        
        .user-name {
            font-weight: 600;
            display: block;
        }
        
        .user-role {
            font-size: 0.8rem;
            opacity: 0.7;
        }
        
        .logout-btn {
            color: white;
            opacity: 0.5;
            transition: opacity 0.2s;
        }
        
        .logout-btn:hover {
            opacity: 1;
        }
        
        /* Main Content */
        .main-content {
            margin-left: var(--sidebar-width);
            flex-grow: 1;
            padding: 30px;
            max-width: 1600px;
        }
        
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            height: 40px;
        }
        
        .page-title {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text-main);
        }
        
        .last-updated {
            font-size: 0.9rem;
            color: var(--text-light);
        }
        
        /* Stats Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 24px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: var(--surface);
            border-radius: 12px;
            padding: 24px;
            box-shadow: var(--shadow);
            border: 1px solid var(--border);
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
        }
        
        .stat-info h3 {
            font-size: 0.9rem;
            color: var(--text-light);
            font-weight: 500;
            margin-bottom: 8px;
            text-transform: uppercase;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-main);
        }
        
        .stat-icon {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        
        .icon-blue { background-color: #e3f2fd; color: #1976d2; }
        .icon-red { background-color: #ffebee; color: #d32f2f; }
        .icon-green { background-color: #e8f5e8; color: #388e3c; }
        .icon-orange { background-color: #fff3e0; color: #f57c00; }
        
        /* Dashboard Sections */
        .section-card {
            background: var(--surface);
            border-radius: 12px;
            box-shadow: var(--shadow);
            border: 1px solid var(--border);
            overflow: hidden;
            margin-bottom: 30px;
        }
        
        .section-header {
            padding: 20px 24px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .section-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--primary);
        }
        
        .action-btn {
            padding: 8px 16px;
            background-color: var(--bg-color);
            color: var(--primary);
            border: 1px solid var(--border);
            border-radius: 6px;
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
        }
        
        .action-btn:hover {
            background-color: #e3f2fd;
            border-color: var(--primary);
        }
        
        .table-responsive {
            overflow-x: auto;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .data-table th {
            text-align: left;
            padding: 16px 24px;
            background-color: #f8f9fa;
            color: var(--text-light);
            font-weight: 600;
            font-size: 0.85rem;
            border-bottom: 1px solid var(--border);
            text-transform: uppercase;
        }
        
        .data-table td {
            padding: 16px 24px;
            border-bottom: 1px solid var(--border);
            color: var(--text-main);
            font-size: 0.95rem;
            vertical-align: middle;
        }
        
        .data-table tr:last-child td {
            border-bottom: none;
        }
        
        .risk-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 50px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .risk-high { background-color: #ffebee; color: #c62828; }
        .risk-medium { background-color: #fff3e0; color: #ef6c00; }
        .risk-low { background-color: #e8f5e8; color: #2e7d32; }
        
        .status-badge {
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .status-waiting { background-color: #fff8e1; color: #f57f17; }
        .status-confirmed { background-color: #e8f5e8; color: #2e7d32; }
        .status-completed { background-color: #e3f2fd; color: #1565c0; }
        
        .btn-sm {
            padding: 6px 12px;
            font-size: 0.85rem;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 500;
            margin-right: 6px;
        }
        
        .btn-primary-sm { background-color: var(--primary); color: white; }
        .btn-outline-sm { background-color: transparent; border: 1px solid var(--border); color: var(--text-main); }
        .btn-primary-sm:hover { background-color: var(--primary-dark); }
        .btn-outline-sm:hover { background-color: #f5f5f5; }
        
        /* Modal */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            backdrop-filter: blur(4px);
            align-items: center;
            justify-content: center;
        }
        
        .modal-content {
            background-color: var(--surface);
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 500px;
            padding: 30px;
            animation: slideUp 0.3s ease;
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
        
        .modal-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--primary);
        }
        
        .form-group { margin-bottom: 20px; }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            font-size: 0.9rem;
        }
        
        .form-control {
            width: 100%;
            padding: 12px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-family: inherit;
        }
        
        .modal-actions {
            display: flex;
            justify-content: flex-end;
            gap: 12px;
            margin-top: 30px;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @media (max-width: 900px) {
            .sidebar { width: 70px; }
            .sidebar-header span, .nav-link span:last-child, .user-profile { display: none; }
            .nav-link { justify-content: center; padding: 16px; }
            .nav-icon { margin: 0; font-size: 1.2rem; }
            .main-content { margin-left: 70px; }
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-header">
            <span>🛡️</span> MediCare
        </div>
        <ul class="nav-menu">
            <li class="nav-item">
                <a href="/admin/dashboard" class="nav-link active">
                    <span class="nav-icon">📊</span>
                    <span>Dashboard</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="/admin/analytics" class="nav-link">
                    <span class="nav-icon">📈</span>
                    <span>Analytics</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="/admin/reports" class="nav-link">
                    <span class="nav-icon">📋</span>
                    <span>Reports</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="/admin/settings" class="nav-link">
                    <span class="nav-icon">⚙️</span>
                    <span>Settings</span>
                </a>
            </li>
        </ul>
        <div class="user-profile">
            <div class="user-info">
                <span class="user-name">Admin</span>
                <span class="user-role">Administrator</span>
            </div>
            <a href="/admin/logout" class="logout-btn" title="Logout">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
            </a>
        </div>
    </div>
    
    <div class="main-content">
        <div class="page-header">
            <h1 class="page-title">Dashboard Overview</h1>
            <div class="last-updated" id="lastUpdated">Updated just now</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-info">
                    <h3>Patients Today</h3>
                    <div class="stat-value" id="totalToday">--</div>
                </div>
                <div class="stat-icon icon-blue">👥</div>
            </div>
            <div class="stat-card">
                <div class="stat-info">
                    <h3>Critical Cases</h3>
                    <div class="stat-value" id="criticalCases">--</div>
                </div>
                <div class="stat-icon icon-red">🚨</div>
            </div>
            <div class="stat-card">
                <div class="stat-info">
                    <h3>Avg Wait Time</h3>
                    <div class="stat-value" id="avgWaiting">--</div>
                </div>
                <div class="stat-icon icon-orange">⏱️</div>
            </div>
            <div class="stat-card">
                <div class="stat-info">
                    <h3>Active Doctors</h3>
                    <div class="stat-value" id="doctorsOnline">--</div>
                </div>
                <div class="stat-icon icon-green">👨‍⚕️</div>
            </div>
        </div>
        
        <div class="section-card">
            <div class="section-header">
                <h2 class="section-title">Patient Queue Management</h2>
                <button onclick="refreshPatients()" class="action-btn">🔄 Refresh Data</button>
            </div>
            <div class="table-responsive">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Patient Name</th>
                            <th>Age/Gender</th>
                            <th>Symptoms</th>
                            <th>Priority Score</th>
                            <th>Department</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="patientsTableBody">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <!-- Confirm Modal -->
    <div id="confirmModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">Confirm Appointment</h3>
                <button onclick="closeConfirmModal()" style="background:none; border:none; cursor:pointer; font-size:1.2rem;">&times;</button>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label>Appointment Date & Time</label>
                    <input type="datetime-local" id="appointmentDateTime" class="form-control">
                </div>
                <div class="modal-actions">
                    <button onclick="closeConfirmModal()" class="btn-sm btn-outline-sm">Cancel</button>
                    <button onclick="confirmPatient()" class="btn-sm btn-primary-sm">Confirm Booking</button>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Report Modal -->
    <div id="reportModal" class="modal">
        <div class="modal-content" style="max-width: 700px;">
             <div class="modal-header">
                <h3 class="modal-title">Patient Medical Report</h3>
                <button onclick="closeReportModal()" style="background:none; border:none; cursor:pointer; font-size:1.2rem;">&times;</button>
            </div>
            <div id="reportContent" style="margin-bottom: 24px;">
                <!-- Content -->
            </div>
            <div class="modal-actions">
                <button onclick="closeReportModal()" class="btn-sm btn-outline-sm">Close</button>
                <button onclick="downloadReport()" class="btn-sm btn-primary-sm">Download PDF</button>
            </div>
        </div>
    </div>

    <script>
        let currentPatientId = null;
        let currentReportData = null;
        
        document.addEventListener('DOMContentLoaded', function() {
            loadDashboardStats();
            loadPatients();
            
            // Update time
            setInterval(() => {
                const now = new Date();
                document.getElementById('lastUpdated').innerText = 'Last updated: ' + now.toLocaleTimeString();
            }, 60000);
            
            setInterval(() => {
                loadDashboardStats();
                loadPatients();
            }, 30000);
        });
        
        async function loadDashboardStats() {
            try {
                const response = await fetch('/api/admin/dashboard_stats');
                const stats = await response.json();
                
                document.getElementById('totalToday').textContent = stats.total_today;
                document.getElementById('criticalCases').textContent = stats.critical_cases;
                document.getElementById('avgWaiting').textContent = stats.avg_waiting;
                document.getElementById('doctorsOnline').textContent = stats.doctors_online;
                
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }
        
        async function loadPatients() {
            try {
                const response = await fetch('/api/admin/patients');
                const patients = await response.json();
                
                const tbody = document.getElementById('patientsTableBody');
                tbody.innerHTML = '';
                
                if (patients.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding: 40px; color: #888;">No patients currently in queue</td></tr>';
                    return;
                }
                
                patients.forEach(patient => {
                    const row = document.createElement('tr');
                    
                    const riskClass = getRiskLevel(patient.risk_score);
                    const statusClass = 'status-' + patient.status.toLowerCase().replace(' ', '-');
                    
                    row.innerHTML = `
                        <td>
                            <div style="font-weight: 600;">${patient.name}</div>
                            <div style="font-size: 0.8rem; color: #888;">ID: ${patient.registration_id}</div>
                        </td>
                        <td>${patient.age} / ${patient.gender}</td>
                        <td>
                            <div style="max-width: 200px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${patient.symptom}">
                                ${patient.symptom}
                            </div>
                        </td>
                        <td>
                            <span class="risk-badge risk-${riskClass}">
                                Score: ${patient.risk_score}
                            </span>
                        </td>
                        <td>${patient.department}</td>
                        <td>
                            <span class="status-badge ${statusClass}">
                                ${capitalize(patient.status)}
                            </span>
                        </td>
                        <td>
                           ${patient.status === 'waiting' ? 
                                `<button onclick="openConfirmModal(${patient.id})" class="btn-sm btn-primary-sm">Confirm</button>` :
                                `<button onclick="generateReport(${patient.id})" class="btn-sm btn-outline-sm">View Report</button>`
                           }
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
        
        function capitalize(s) {
            return s && s[0].toUpperCase() + s.slice(1);
        }
        
        function refreshPatients() {
            loadPatients();
            loadDashboardStats();
            const now = new Date();
            document.getElementById('lastUpdated').innerText = 'Last updated: ' + now.toLocaleTimeString();
        }
        
        function openConfirmModal(patientId) {
            currentPatientId = patientId;
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            tomorrow.setHours(9, 0, 0, 0);
            
            // Format for datetime-local input
            const pad = num => num.toString().padStart(2, '0');
            const str = `${tomorrow.getFullYear()}-${pad(tomorrow.getMonth()+1)}-${pad(tomorrow.getDate())}T${pad(tomorrow.getHours())}:${pad(tomorrow.getMinutes())}`;
            
            document.getElementById('appointmentDateTime').value = str;
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
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        patient_id: currentPatientId,
                        appointment_time: appointmentTime
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    closeConfirmModal();
                    loadPatients();
                    alert('✅ Appointment Confirmed');
                } else {
                    alert('❌ Error: ' + result.error);
                }
            } catch (error) {
                alert('⚠️ Network error: ' + error.message);
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
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Network error');
            }
        }
        
        function displayReport(data) {
            const content = document.getElementById('reportContent');
            content.innerHTML = `
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h4 style="color: var(--primary); margin-bottom: 15px; border-bottom: 1px solid #ddd; padding-bottom: 10px;">Patient Details</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.95rem;">
                        <div><strong>Name:</strong> ${data.patient_name}</div>
                        <div><strong>ID:</strong> ${data.registration_id}</div>
                        <div><strong>Age/Gender:</strong> ${data.age} / ${data.gender}</div>
                        <div><strong>Phone:</strong> ${data.phone}</div>
                    </div>
                </div>
                
                <div style="padding: 20px; border: 1px solid #eee; border-radius: 8px;">
                    <h4 style="color: var(--primary); margin-bottom: 15px;">Clinical Assessment</h4>
                    <p><strong>Primary Symptom:</strong> ${data.symptom}</p>
                    <p><strong>Severity:</strong> ${data.severity}</p>
                    <p><strong>AI Risk Score:</strong> ${data.risk_score}/100</p>
                    <p><strong>Recommended Department:</strong> ${data.department}</p>
                    <div style="margin-top: 15px; padding-top: 15px; border-top: 1px dashed #ddd;">
                         <strong>Status:</strong> ${data.status.toUpperCase()} <br>
                         ${data.appointment_time ? `<strong>Appointment:</strong> ${new Date(data.appointment_time).toLocaleString()}` : ''}
                    </div>
                </div>
            `;
        }
        
        function closeReportModal() {
            document.getElementById('reportModal').style.display = 'none';
        }
        
        function downloadReport() {
            alert('📥 Downloading PDF Report...\n(This is a demo feature)');
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