from flask import Flask, render_template, request, redirect, url_for, session, flash
import database as db
import ml_logic as ml
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_hackathon'

# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html', page='home')

@app.route('/submit', methods=['POST'])
def submit_patient():
    if request.method == 'POST':
        # 1. Collect Data
        data = {
            'name': request.form['name'],
            'age': int(request.form['age']),
            'gender': request.form['gender'],
            'location': request.form['location'],
            'symptom': request.form['symptom'],
            'severity': int(request.form['severity']),
            'chronic_illness': request.form.get('chronic_illness', 'no'),
            'vulnerable_group': request.form.get('vulnerable_group', 'no'),
            'distance': float(request.form['distance'])
        }

        # 2. Logic: Priority & Department
        urgency_score, priority_level = ml.calculate_priority(data)
        data['priority_score'] = urgency_score
        data['priority_level'] = priority_level

        recommended_dept_name = ml.recommend_department(data['symptom'], data['age'])
        dept = db.get_department_by_name(recommended_dept_name)
        
        if dept:
            department_id = dept['id']
            department_name = dept['name']
        else:
            department_name = "General Medicine"
            department_id = db.get_department_by_name(department_name)['id']
        
        data['department_id'] = department_id

        # 3. Save to DB
        db.add_patient(data)

        return render_template('result.html', 
                               department=department_name, 
                               priority=priority_level, 
                               score=urgency_score,
                               page='result')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Only Admin Login remains
        if email == 'admin@gmail.com' and password == 'admin': # Simple check
            session['user_type'] = 'admin'
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid admin credentials')
            
    return render_template('login.html', page='login')

@app.route('/dashboard')
def dashboard():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    stats = db.get_all_stats()
    return render_template('dashboard.html', stats=stats, page='dashboard')

@app.route('/queue')
def queue():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    patients = db.get_all_patients()
    return render_template('queue.html', patients=patients, page='queue')

@app.route('/analytics')
def analytics():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    stats = db.get_all_stats()
    return render_template('analytics.html', stats=stats, page='analytics')

@app.route('/settings')
def settings():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    return render_template('settings.html', page='settings')

@app.route('/admin/reset', methods=['POST'])
def reset_system():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    db.clear_patient_data()
    flash('System reset: All patient data cleared.')
    return redirect(url_for('settings'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    if not os.path.exists(db.DB_NAME):
        db.init_db()
    app.run(debug=True, port=5000)
