from flask import Flask, request, jsonify
import subprocess
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data['code']
    file_extension = data.get('file_extension', 'py')
    
    if file_extension == 'java':
        return run_java_code(code)
    elif file_extension == 'py':
        return run_python_code(code)
    else:
        return jsonify({'output': 'Unsupported file extension'})

def run_java_code(code):
    try:
        with open('Main.java', 'w') as java_file:
            java_file.write(code)
        result = subprocess.run(['javac', 'Main.java'], capture_output=True, text=True, check=True)
        if result.returncode != 0:
            return jsonify({'output': result.stderr})
        result = subprocess.run(['java', 'Main'], capture_output=True, text=True, check=True)
        return jsonify({'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'output': e.stderr})
    finally:
        os.remove('Main.java')
        if os.path.exists('Main.class'):
            os.remove('Main.class')

def run_python_code(code):
    try:
        result = subprocess.run(['python', '-c', code], capture_output=True, text=True, check=True)
        return jsonify({'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'output': e.stderr})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
