from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'test_key'

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Minimal Test</title>
        <style>
            body { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                font-family: Arial; 
                padding: 50px; 
                text-align: center;
            }
            .container { 
                background: white; 
                color: black; 
                padding: 30px; 
                border-radius: 15px; 
                max-width: 600px; 
                margin: 0 auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 Telemedicine Queue Optimizer</h1>
            <p>If you can see this styled page, Flask is working correctly!</p>
            <p>The white screen issue might be due to external CSS dependencies.</p>
            <a href="/patient" style="background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Go to Patient Form</a>
        </div>
    </body>
    </html>
    '''

@app.route('/patient')
def patient():
    try:
        return render_template('patient_form.html')
    except Exception as e:
        return f'<h1>Template Error:</h1><p>{str(e)}</p>'

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5002)