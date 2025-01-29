from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/run-script", methods=["POST"])
def run_script():
    # Mengambil data yang diterima dari frontend
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    selected_script = data.get("script")

    # Tentukan path file bash berdasarkan pilihan script
    script_paths = {
        "script1.sh": "/scripts/script1.sh",
        "script2.sh": "/scripts/script2.sh",
        "script3.sh": "/scripts/script3.sh"
    }

    script_path = script_paths.get(selected_script)

    if not script_path:
        return jsonify({"status": "error", "message": "Invalid script selected"}), 400

    # Jalankan skrip bash dengan email dan password sebagai argumen
    try:
        command = ["bash", script_path, email, password]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        return jsonify({"status": "success", "output": output.decode("utf-8")})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": e.output.decode("utf-8")})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
