from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Ambil email dan password dari request
        data = request.get_json()
        email = data.get('email', '')
        password = data.get('password', '')

        # Jalankan script bash dengan email dan password sebagai argument
        result = subprocess.run(
            ['./scripts/your_script.sh', email, password],  # kirim email dan password ke script
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
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
