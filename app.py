from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)

# Batasi domain asal dengan Flask-CORS
CORS(app, resources={r"/*": {"origins": ["https://dot-aja.my.id", "http://localhost:5500"]}})

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Ambil email, password, dan script yang dipilih dari request
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        script_name = data.get('script', '').strip()

        # Validasi input
        if not email or not password or not script_name:
            return jsonify({'status': 'error', 'message': 'Email, password, dan script harus diisi'}), 400
        
        # Tentukan path script berdasarkan nama script yang dipilih
        script_directory = './scripts'
        script_path = os.path.join(script_directory, script_name)

        # Debugging: Log path script yang dihasilkan
        print(f"Current working directory: {os.getcwd()}")
        print(f"Script path: {script_path}")
        print(f"Abs path: {os.path.abspath(script_path)}")
        
        # Periksa apakah script yang diminta ada dan berada di direktori yang diizinkan
        if not os.path.isfile(script_path):
            return jsonify({'status': 'error', 'message': f'Script {script_name} tidak ditemukan atau tidak valid'}), 400

        # Pastikan script memiliki hak akses eksekusi
        if not os.access(script_path, os.X_OK):
            return jsonify({'status': 'error', 'message': f'Script {script_name} tidak memiliki hak akses eksekusi'}), 400
        
        # Jalankan script bash dengan email dan password sebagai argument
        result = subprocess.run(
            ['bash', script_path, email, password],  # Menjalankan dengan bash
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=False  # Tidak menggunakan shell untuk keamanan
        )

        # Kembalikan hanya output dari script (stdout)
        return jsonify({
            'status': 'success',
            'output': result.stdout.strip()  # Hapus whitespace ekstra
        })
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': f'Script execution failed: {e}'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
