from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/test')
def test():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
        <style>
            body { background-color: lightblue; font-family: Arial; padding: 20px; }
            h1 { color: navy; }
        </style>
    </head>
    <body>
        <h1>Test Page - If you see this, Flask is working!</h1>
        <p>This is a simple test to verify Flask is serving HTML correctly.</p>
        <p>Time: {{ current_time }}</p>
    </body>
    </html>
    """

@app.route('/simple')
def simple():
    return "<h1>Simple Test</h1><p>If you see this, Flask is working!</p>"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)