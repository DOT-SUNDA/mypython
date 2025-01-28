from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Ambil argumen dari permintaan POST
        data = request.get_json()
        argument = data.get('argument', '')

        # Jalankan skrip dengan argumen
        result = subprocess.run(
            ['./scripts/joko.sh', argument],  # Argumen ditambahkan di sini
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return jsonify({
            'status': 'success',
            'output': result.stdout,  # Output dari skrip
            'error': result.stderr    # Jika ada error
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
