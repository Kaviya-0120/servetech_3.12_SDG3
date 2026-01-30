from flask import Flask, render_template_string, jsonify
import traceback
import sys

app = Flask(__name__)
app.secret_key = 'debug_key'

@app.route('/')
def index():
    """Minimal test route"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Debug Test</title>
        <style>
            body { 
                background: #f0f0f0; 
                font-family: Arial; 
                padding: 20px; 
                margin: 0;
            }
            .debug-box { 
                background: white; 
                border: 2px solid #333; 
                padding: 20px; 
                margin: 10px 0;
                border-radius: 5px;
            }
            .success { border-color: green; background: #e8f5e8; }
            .error { border-color: red; background: #ffe8e8; }
        </style>
    </head>
    <body>
        <div class="debug-box success">
            <h1>🔧 Flask Debug Test</h1>
            <p><strong>Status:</strong> Flask is running successfully!</p>
            <p><strong>Time:</strong> <span id="time"></span></p>
        </div>
        
        <div class="debug-box">
            <h2>Test Links:</h2>
            <ul>
                <li><a href="/test-template">Test Template Rendering</a></li>
                <li><a href="/test-static">Test Static Files</a></li>
                <li><a href="/test-original">Test Original App</a></li>
                <li><a href="/api/test">Test API</a></li>
            </ul>
        </div>
        
        <script>
            document.getElementById('time').textContent = new Date().toLocaleString();
            console.log('JavaScript is working!');
        </script>
    </body>
    </html>
    '''

@app.route('/test-template')
def test_template():
    """Test template rendering"""
    try:
        # Test basic template
        template = '''
        <html>
        <head><title>Template Test</title></head>
        <body>
            <h1>Template Test: {{ status }}</h1>
            <p>Variable rendering: {{ test_var }}</p>
            <p>Loop test:</p>
            <ul>
            {% for item in items %}
                <li>{{ item }}</li>
            {% endfor %}
            </ul>
        </body>
        </html>
        '''
        return render_template_string(template, 
                                    status="SUCCESS", 
                                    test_var="Working!",
                                    items=['Item 1', 'Item 2', 'Item 3'])
    except Exception as e:
        return f'<h1>Template Error:</h1><pre>{traceback.format_exc()}</pre>'

@app.route('/test-static')
def test_static():
    """Test static file serving"""
    return '''
    <html>
    <head>
        <title>Static File Test</title>
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        <h1>Static File Test</h1>
        <p>If this page has styling, static files are working.</p>
        <p>Check browser console for any 404 errors.</p>
        <script src="/static/js/main.js"></script>
    </body>
    </html>
    '''

@app.route('/test-original')
def test_original():
    """Test original patient form"""
    try:
        from app import app as original_app
        with original_app.app_context():
            return original_app.view_functions['index']()
    except Exception as e:
        return f'<h1>Original App Error:</h1><pre>{traceback.format_exc()}</pre>'

@app.route('/api/test')
def api_test():
    """Test API response"""
    return jsonify({
        'status': 'success',
        'message': 'API is working',
        'python_version': sys.version,
        'flask_working': True
    })

if __name__ == '__main__':
    print("🔧 Starting Debug Flask App...")
    print("📍 Access: http://127.0.0.1:5003")
    print("🎯 This will help identify the white screen issue")
    app.run(debug=True, host='127.0.0.1', port=5003)