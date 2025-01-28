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

# Menampilkan pesan selesai
echo "Struktur proyek Flask berhasil dibuat!"
echo "Silakan tambahkan file 'app.py', 'index.html', dan 'your_script.sh' ke proyek ini."
