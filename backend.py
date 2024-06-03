from flask import Flask, request, jsonify
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data['code']
    
    try:
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = e.stderr
    
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
