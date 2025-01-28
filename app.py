from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)

# Batasi domain asal dengan Flask-CORS
CORS(app, resources={r"/*": {"origins": ["https://dot-aja.my.id"]}})

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Ambil email, password, dan script yang dipilih dari request
        data = request.get_json()
        email = data.get('email', '')
        password = data.get('password', '')
        script_name = data.get('script', '')

        # Validasi input
        if not email or not password or not script_name:
            return jsonify({'status': 'error', 'message': 'Email, password, and script are required'}), 400
        
        # Tentukan path script berdasarkan nama script yang dipilih
        script_path = f'./scripts/{script_name}'

        # Periksa apakah script yang diminta ada
        if not script_path or not script_name.endswith('.sh'):
            return jsonify({'status': 'error', 'message': 'Invalid script selected'}), 400
        
        # Jalankan script bash dengan email dan password sebagai argument
        result = subprocess.run(
            [script_path, email, password],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        return jsonify({
            'status': 'success',
            'output': result.stdout,
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
