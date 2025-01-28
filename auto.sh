#!/bin/bash

# Nama proyek
PROJECT_NAME="flask_app"

# Buat direktori proyek
echo "Membuat direktori proyek: $PROJECT_NAME"
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME || exit

# Buat virtual environment
echo "Membuat virtual environment..."
python3 -m venv venv

# Aktifkan virtual environment
echo "Mengaktifkan virtual environment..."
source venv/bin/activate

# Install Flask
echo "Menginstall Flask..."
pip install flask

# Membuat struktur folder
echo "Membuat struktur folder..."
mkdir -p static templates scripts

# Membuat file app.py
echo "Membuat file app.py..."
cat > app.py <<EOF
from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        data = request.get_json()
        argument = data.get('argument', '')

        result = subprocess.run(
            ['./scripts/your_script.sh', argument],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
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
EOF

# Membuat file HTML untuk template
echo "Membuat file template HTML..."
cat > templates/index.html <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Run Script</title>
</head>
<body>
    <h1>Run Script and See Output</h1>
    <label for="argument">Enter Argument:</label>
    <input type="text" id="argument" placeholder="Type your argument">
    <button id="runBtn">Run Script</button>
    <pre id="output"></pre>

    <script>
        document.getElementById('runBtn').addEventListener('click', async () => {
            const argument = document.getElementById('argument').value;
            document.getElementById('output').innerText = 'Running script...';

            try {
                const response = await fetch('/run-script', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ argument })
                });
                const result = await response.json();
                if (result.status === 'success') {
                    document.getElementById('output').innerText = result.output;
                } else {
                    document.getElementById('output').innerText = `Error: ${result.message}`;
                }
            } catch (error) {
                document.getElementById('output').innerText = `Request failed: ${error}`;
            }
        });
    </script>
</body>
</html>
EOF

# Membuat skrip bash
echo "Membuat skrip bash..."
cat > scripts/your_script.sh <<EOF
#!/bin/bash
echo "Argument received: \$1"
echo "Script executed successfully!"
EOF

# Berikan izin eksekusi pada skrip bash
chmod +x scripts/your_script.sh

# Menjalankan aplikasi Flask
echo "Proyek Flask berhasil dibuat!"
echo "Untuk menjalankan aplikasi, aktifkan virtual environment dengan:"
echo "  source venv/bin/activate"
echo "Kemudian jalankan:"
echo "  python app.py"
