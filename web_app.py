#!/usr/bin/env python3
"""
Web Interface untuk Location Tracker
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import os
import json
import base64
from werkzeug.utils import secure_filename
from location_tracker import LocationTracker
import cv2
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Buat folder upload jika belum ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Inisialisasi LocationTracker
tracker = LocationTracker()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Halaman utama"""
    return render_template('index.html')

@app.route('/identify', methods=['GET', 'POST'])
def identify_location():
    """Identifikasi lokasi dari gambar"""
    if request.method == 'GET':
        return render_template('identify.html')
    
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diunggah'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Tidak ada file yang dipilih'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Identifikasi lokasi
            results = tracker.identify_location_from_image(filepath)
            
            # Buat peta
            map_path = os.path.join('static', 'current_map.html')
            tracker.create_location_map(results, map_path)
            
            # Encode gambar ke base64 untuk tampilan
            with open(filepath, 'rb') as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode()
            
            # Hapus file upload setelah diproses
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'results': results,
                'image': f"data:image/jpeg;base64,{img_base64}",
                'map_url': '/static/current_map.html'
            })
            
        except Exception as e:
            return jsonify({'error': f'Error memproses gambar: {str(e)}'})
    
    return jsonify({'error': 'Format file tidak didukung'})

@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    """Tambah seseorang ke database"""
    if request.method == 'GET':
        return render_template('add_person.html')
    
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diunggah'})
    
    file = request.files['file']
    name = request.form.get('name')
    location = request.form.get('location')
    coordinates = request.form.get('coordinates')
    
    if not all([name, location, coordinates]):
        return jsonify({'error': 'Semua field harus diisi'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Parse coordinates
            lat, lon = map(float, coordinates.split(','))
            coords = [lat, lon]
            
            # Tambah person
            success = tracker.add_person_location(name, filepath, location, coords)
            
            # Hapus file setelah diproses
            os.remove(filepath)
            
            if success:
                return jsonify({'success': True, 'message': f'Berhasil menambah {name}'})
            else:
                return jsonify({'error': 'Gagal menambah person ke database'})
                
        except Exception as e:
            return jsonify({'error': f'Error: {str(e)}'})
    
    return jsonify({'error': 'Format file tidak didukung'})

@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    """Tambah lokasi referensi"""
    if request.method == 'GET':
        return render_template('add_location.html')
    
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diunggah'})
    
    file = request.files['file']
    location_name = request.form.get('location_name')
    coordinates = request.form.get('coordinates')
    city = request.form.get('city', '')
    country = request.form.get('country', 'Indonesia')
    
    if not all([location_name, coordinates]):
        return jsonify({'error': 'Nama lokasi dan koordinat harus diisi'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Parse coordinates
            lat, lon = map(float, coordinates.split(','))
            coords = [lat, lon]
            
            # Buat location data
            location_id = location_name.lower().replace(' ', '_')
            location_data = {
                "name": location_name,
                "coordinates": coords,
                "city": city,
                "country": country,
                "description": f"Referensi lokasi untuk {location_name}"
            }
            
            # Tambah location
            success = tracker.add_location_reference(location_id, filepath, location_data)
            
            # Hapus file setelah diproses
            os.remove(filepath)
            
            if success:
                return jsonify({'success': True, 'message': f'Berhasil menambah lokasi {location_name}'})
            else:
                return jsonify({'error': 'Gagal menambah lokasi ke database'})
                
        except Exception as e:
            return jsonify({'error': f'Error: {str(e)}'})
    
    return jsonify({'error': 'Format file tidak didukung'})

@app.route('/database')
def view_database():
    """Lihat database lokasi dan orang"""
    return render_template('database.html', 
                         locations=tracker.location_database.get('locations', {}),
                         faces=tracker.location_database.get('faces', {}))

@app.route('/api/locations')
def api_locations():
    """API untuk mendapatkan daftar lokasi"""
    return jsonify(tracker.location_database.get('locations', {}))

@app.route('/api/faces')
def api_faces():
    """API untuk mendapatkan daftar wajah"""
    return jsonify(tracker.location_database.get('faces', {}))

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_file(os.path.join('static', filename))

def create_templates():
    """Buat template HTML"""
    
    # Template base
    base_template = '''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Location Tracker{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .navbar-brand { font-weight: bold; }
        .result-card { margin: 10px 0; }
        .map-container { height: 400px; }
        .upload-area { 
            border: 2px dashed #ccc; 
            padding: 40px; 
            text-align: center; 
            margin: 20px 0;
            cursor: pointer;
        }
        .upload-area:hover { border-color: #007bff; }
        .image-preview { max-width: 300px; max-height: 300px; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">🔍 Location Tracker</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Home</a>
                <a class="nav-link" href="/identify">Identifikasi</a>
                <a class="nav-link" href="/add_person">Tambah Orang</a>
                <a class="nav-link" href="/add_location">Tambah Lokasi</a>
                <a class="nav-link" href="/database">Database</a>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>'''
    
    # Template index
    index_template = '''{% extends "base.html" %}
{% block title %}Location Tracker - Home{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-8">
        <h1>🔍 Location Tracker</h1>
        <p class="lead">Sistem Deep Learning untuk melacak lokasi menggunakan gambar dan face recognition</p>
        
        <h3>Fitur Utama:</h3>
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">📍 Identifikasi Lokasi</h5>
                        <p class="card-text">Upload gambar untuk mengidentifikasi lokasi menggunakan GPS metadata, pengenalan gambar, dan face recognition.</p>
                        <a href="/identify" class="btn btn-primary">Mulai Identifikasi</a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">👤 Tambah Orang</h5>
                        <p class="card-text">Daftarkan wajah seseorang dengan lokasi mereka untuk tracking di masa depan.</p>
                        <a href="/add_person" class="btn btn-success">Tambah Orang</a>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-3">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">🏢 Tambah Lokasi</h5>
                        <p class="card-text">Tambahkan referensi lokasi baru ke database untuk pengenalan yang lebih akurat.</p>
                        <a href="/add_location" class="btn btn-info">Tambah Lokasi</a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">💾 Database</h5>
                        <p class="card-text">Lihat dan kelola database lokasi dan wajah yang tersimpan.</p>
                        <a href="/database" class="btn btn-secondary">Lihat Database</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        <h3>Cara Penggunaan:</h3>
        <ol>
            <li><strong>Upload Gambar:</strong> Pilih gambar yang ingin dianalisis</li>
            <li><strong>Analisis Otomatis:</strong> Sistem akan menganalisis GPS, fitur gambar, dan wajah</li>
            <li><strong>Hasil Lokasi:</strong> Dapatkan koordinat dan informasi lokasi</li>
            <li><strong>Peta Interaktif:</strong> Lihat hasil di peta yang interaktif</li>
        </ol>
        
        <div class="alert alert-info">
            <h6>💡 Tips:</h6>
            <ul class="mb-0">
                <li>Gunakan gambar dengan GPS metadata untuk hasil terbaik</li>
                <li>Daftarkan wajah dan lokasi untuk tracking yang akurat</li>
                <li>Gambar yang jelas menghasilkan analisis yang lebih baik</li>
            </ul>
        </div>
    </div>
</div>
{% endblock %}'''
    
    # Template identify
    identify_template = '''{% extends "base.html" %}
{% block title %}Identifikasi Lokasi{% endblock %}
{% block content %}
<h2>📍 Identifikasi Lokasi dari Gambar</h2>

<form id="identifyForm" enctype="multipart/form-data">
    <div class="upload-area" onclick="document.getElementById('fileInput').click()">
        <input type="file" id="fileInput" name="file" accept="image/*" style="display:none" required>
        <div id="uploadText">
            <h4>📁 Klik untuk upload gambar</h4>
            <p>Atau drag & drop gambar di sini</p>
            <small>Format: JPG, PNG, GIF (Max: 16MB)</small>
        </div>
        <img id="imagePreview" class="image-preview" style="display:none">
    </div>
    
    <button type="submit" class="btn btn-primary btn-lg">🔍 Identifikasi Lokasi</button>
</form>

<div id="loading" class="text-center" style="display:none">
    <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>
    <p>Menganalisis gambar...</p>
</div>

<div id="results" style="display:none">
    <h3>📊 Hasil Analisis</h3>
    <div id="resultsContent"></div>
    <div id="mapContainer" class="mt-3">
        <iframe id="mapFrame" width="100%" height="400px" frameborder="0"></iframe>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
document.getElementById('fileInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('imagePreview').src = e.target.result;
            document.getElementById('imagePreview').style.display = 'block';
            document.getElementById('uploadText').style.display = 'none';
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('identifyForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData();
    const fileInput = document.getElementById('fileInput');
    
    if (!fileInput.files[0]) {
        alert('Pilih gambar terlebih dahulu!');
        return;
    }
    
    formData.append('file', fileInput.files[0]);
    
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    
    fetch('/identify', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        
        if (data.success) {
            displayResults(data);
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        alert('Error: ' + error);
    });
});

function displayResults(data) {
    const results = data.results;
    let html = '';
    
    // GPS Coordinates
    if (results.gps_coordinates) {
        html += `
        <div class="alert alert-success">
            <h5>🌍 GPS Coordinates Ditemukan</h5>
            <p>Latitude: ${results.gps_coordinates[0].toFixed(6)}</p>
            <p>Longitude: ${results.gps_coordinates[1].toFixed(6)}</p>
            ${results.predicted_location ? `<p>Lokasi: ${results.predicted_location.name}</p>` : ''}
        </div>`;
    } else {
        html += '<div class="alert alert-warning">❌ Tidak ada GPS coordinates dalam metadata gambar</div>';
    }
    
    // Similar Locations
    if (results.similar_locations && results.similar_locations.length > 0) {
        html += '<h5>🏢 Lokasi Serupa:</h5>';
        results.similar_locations.forEach((loc, i) => {
            html += `
            <div class="card result-card">
                <div class="card-body">
                    <h6>${loc.name} (${loc.city}, ${loc.country})</h6>
                    <p>Koordinat: ${loc.coordinates[0].toFixed(6)}, ${loc.coordinates[1].toFixed(6)}</p>
                    <p>Similarity: ${(loc.similarity * 100).toFixed(1)}%</p>
                </div>
            </div>`;
        });
    }
    
    // Face Matches
    if (results.face_matches && results.face_matches.length > 0) {
        html += '<h5>👤 Wajah yang Dikenali:</h5>';
        results.face_matches.forEach((match, i) => {
            html += `
            <div class="card result-card">
                <div class="card-body">
                    <h6>${match.person} di ${match.location}</h6>
                    <p>Koordinat: ${match.coordinates[0].toFixed(6)}, ${match.coordinates[1].toFixed(6)}</p>
                    <p>Confidence: ${(match.confidence * 100).toFixed(1)}%</p>
                </div>
            </div>`;
        });
    }
    
    document.getElementById('resultsContent').innerHTML = html;
    document.getElementById('mapFrame').src = data.map_url;
    document.getElementById('results').style.display = 'block';
}
</script>
{% endblock %}'''
    
    # Buat file template
    templates = {
        'base.html': base_template,
        'index.html': index_template,
        'identify.html': identify_template
    }
    
    for filename, content in templates.items():
        with open(f'templates/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    # Buat template HTML
    create_templates()
    
    print("🌐 Starting Location Tracker Web Interface...")
    print("📍 Access the app at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)