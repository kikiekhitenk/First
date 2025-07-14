# 🚀 Quick Start Guide - Location Tracker

Panduan cepat untuk memulai menggunakan Location Tracker dalam 5 menit!

## ⚡ Instalasi Cepat

### 1. Clone dan Setup
```bash
git clone <repository-url>
cd location-tracker
python install_and_test.py
```

### 2. Manual Installation (jika diperlukan)
```bash
pip install -r requirements.txt
```

## 🎯 Penggunaan Cepat

### 🌐 Web Interface (Termudah)
```bash
python web_app.py
```
Buka browser ke: `http://localhost:5000`

### 💻 Command Line

#### Identifikasi Lokasi
```bash
python main.py --mode identify --image foto_anda.jpg
```

#### Tambah Orang Baru
```bash
python main.py --mode add_person \
  --image foto_wajah.jpg \
  --name "Nama Orang" \
  --location "Lokasi" \
  --coordinates "-6.2088,106.8456"
```

#### Demo Lengkap
```bash
python demo_script.py
```

## 📝 Contoh Sederhana

### Python Script
```python
from location_tracker import LocationTracker

# Inisialisasi
tracker = LocationTracker()

# Identifikasi lokasi dari gambar
results = tracker.identify_location_from_image("foto.jpg")

# Tampilkan hasil
if results["gps_coordinates"]:
    print(f"GPS: {results['gps_coordinates']}")
    
if results["face_matches"]:
    for match in results["face_matches"]:
        print(f"Ditemukan: {match['person']} di {match['location']}")
```

## 🎬 Demo Mode

Untuk testing cepat tanpa gambar real:
```bash
python main.py --mode demo
```

## 📊 File yang Dihasilkan

- `location_database.json` - Database lokasi dan wajah
- `face_encodings.pkl` - Encoding wajah
- `location_features.pkl` - Fitur lokasi
- `location_map.html` - Peta interaktif
- `results.json` - Hasil analisis

## 🔧 Troubleshooting Cepat

### Error: Module not found
```bash
pip install -r requirements.txt
```

### Error: No face detected  
- Gunakan foto wajah yang jelas
- Pastikan pencahayaan cukup

### Error: GPS not found
- Gunakan foto dengan GPS metadata
- Atau input koordinat manual

## 📱 Tips Penggunaan

1. **Upload gambar dengan GPS** untuk hasil terbaik
2. **Daftarkan wajah dan lokasi** untuk tracking akurat  
3. **Gunakan web interface** untuk kemudahan
4. **Baca README.md** untuk dokumentasi lengkap

## 🆘 Bantuan

- **Error**: Jalankan `python install_and_test.py` untuk diagnosis
- **Demo**: Gunakan `python demo_script.py` untuk testing
- **Dokumentasi**: Baca `README.md` untuk detail lengkap

---

**Ready to track locations! 🎉**