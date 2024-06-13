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
    elif file_extension == 'c':
        return run_c_code(code)
    elif file_extension == 'cpp':
        return run_cpp_code(code)
    elif file_extension == 'cs':
        return run_csharp_code(code)
    else:
        return jsonify({'output': 'Unsupported file extension', 'errors': ''})

def run_java_code(code):
    try:
        with open('Main.java', 'w') as java_file:
            java_file.write(code)
        compile_result = subprocess.run(['javac', 'Main.java'], capture_output=True, text=True)
        if compile_result.returncode != 0:
            return jsonify({'output': '', 'errors': compile_result.stderr})
        run_result = subprocess.run(['java', 'Main'], capture_output=True, text=True)
        return jsonify({'output': run_result.stdout, 'errors': run_result.stderr})
    except subprocess.CalledProcessError as e:
        return jsonify({'output': '', 'errors': str(e)})
    finally:
        os.remove('Main.java')
        if os.path.exists('Main.class'):
            os.remove('Main.class')

def run_python_code(code):
    try:
        result = subprocess.run(['python', '-c', code], capture_output=True, text=True)
        return jsonify({'output': result.stdout, 'errors': result.stderr})
    except subprocess.CalledProcessError as e:
        return jsonify({'output': '', 'errors': str(e)})

def run_c_code(code):
    try:
        with open('main.c', 'w') as c_file:
            c_file.write(code)
        compile_result = subprocess.run(['gcc', 'main.c', '-o', 'main'], capture_output=True, text=True)
        if compile_result.returncode != 0:
            return jsonify({'output': '', 'errors': compile_result.stderr})
        run_result = subprocess.run(['./main'], capture_output=True, text=True)
        return jsonify({'output': run_result.stdout, 'errors': run_result.stderr})
    except subprocess.CalledProcessError as e:
        return jsonify({'output': '', 'errors': str(e)})
    finally:
        os.remove('main.c')
        if os.path.exists('main'):
            os.remove('main')

def run_cpp_code(code):
    try:
        with open('main.cpp', 'w') as cpp_file:
            cpp_file.write(code)
        compile_result = subprocess.run(['g++', 'main.cpp', '-o', 'main'], capture_output=True, text=True)
        if compile_result.returncode != 0:
            return jsonify({'output': '', 'errors': compile_result.stderr})
        run_result = subprocess.run(['./main'], capture_output=True, text=True)
        return jsonify({'output': run_result.stdout, 'errors': run_result.stderr})
    except subprocess.CalledProcessError as e:
        return jsonify({'output': '', 'errors': str(e)})
    finally:
        os.remove('main.cpp')
        if os.path.exists('main'):
            os.remove('main')

def run_csharp_code(code):
    try:
        with open('Main.cs', 'w') as cs_file:
            cs_file.write(code)
        compile_result = subprocess.run(['csc', 'Main.cs'], capture_output=True, text=True)
        if compile_result.returncode != 0:
            return jsonify({'output': '', 'errors': compile_result.stderr})
        run_result = subprocess.run(['mono', 'Main.exe'], capture_output=True, text=True)
        return jsonify({'output': run_result.stdout, 'errors': run_result.stderr})
    except subprocess.CalledProcessError as e:
        return jsonify({'output': '', 'errors': str(e)})
    finally:
        os.remove('Main.cs')
        if os.path.exists('Main.exe'):
            os.remove('Main.exe')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
