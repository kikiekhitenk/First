# 🔍 Location Tracker - Deep Learning untuk Melacak Lokasi

Sistem deep learning yang dapat melacak suatu wilayah tertentu menggunakan gambar dan menemukan lokasi seseorang melalui foto mereka.

## 📋 Fitur Utama

### 🌍 **Identifikasi Lokasi Multi-Modal**
- **GPS Metadata**: Ekstraksi koordinat GPS dari EXIF data gambar
- **Image Recognition**: Pengenalan lokasi menggunakan CNN deep learning
- **Face Recognition**: Identifikasi orang dan lokasi mereka
- **Reverse Geocoding**: Konversi koordinat ke alamat lengkap

### 👤 **Face Tracking System**
- Deteksi dan encoding wajah menggunakan dlib dan face_recognition
- Database wajah dengan lokasi terkait
- Pencarian lokasi berdasarkan foto seseorang
- Confidence scoring untuk akurasi matching

### 🗺️ **Mapping & Visualization**
- Peta interaktif menggunakan Folium
- Multiple marker types (GPS, Similar Locations, Face Matches)
- Export hasil ke JSON dan HTML
- Web interface yang user-friendly

## 🛠️ Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd location-tracker
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Tambahan (Optional)
Untuk performa optimal, install dlib dengan optimasi:
```bash
# Ubuntu/Debian
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
sudo apt-get install libx11-dev libgtk-3-dev

# Install dlib from source untuk optimasi
pip install dlib --verbose
```

## 🚀 Cara Penggunaan

### 1. Command Line Interface

#### **Identifikasi Lokasi dari Gambar**
```bash
python main.py --mode identify --image path/to/image.jpg --output results/
```

#### **Menambah Orang ke Database**
```bash
python main.py --mode add_person \
  --image foto_wajah.jpg \
  --name "John Doe" \
  --location "Kantor Jakarta" \
  --coordinates "-6.2088,106.8456"
```

#### **Menambah Referensi Lokasi**
```bash
python main.py --mode add_location \
  --image foto_lokasi.jpg \
  --location "Monumen Nasional" \
  --coordinates "-6.1754,106.8272"
```

#### **Jalankan Demo**
```bash
python main.py --mode demo --output demo_results/
```

### 2. Web Interface

Jalankan web server:
```bash
python web_app.py
```

Akses aplikasi di: `http://localhost:5000`

#### Fitur Web Interface:
- **Upload & Analyze**: Drag & drop gambar untuk analisis
- **Real-time Results**: Hasil langsung dengan peta interaktif
- **Database Management**: Kelola database lokasi dan wajah
- **Mobile Responsive**: Dapat diakses dari smartphone

## 📊 Struktur Database

### Location Database (`location_database.json`)
```json
{
  "locations": {
    "location_id": {
      "name": "Nama Lokasi",
      "coordinates": [latitude, longitude],
      "city": "Kota",
      "country": "Negara",
      "description": "Deskripsi lokasi"
    }
  },
  "faces": {
    "person_name": {
      "name": "Nama Orang",
      "location": "Lokasi saat ini",
      "coordinates": [latitude, longitude],
      "image_path": "path/to/image.jpg"
    }
  }
}
```

### Face Encodings (`face_encodings.pkl`)
Binary file berisi encoding wajah untuk face recognition

### Location Features (`location_features.pkl`)
Binary file berisi feature vectors lokasi untuk image matching

## 🔧 Konfigurasi Model

### Model CNN Architecture
```python
- Conv2D(32) -> MaxPool -> Conv2D(64) -> MaxPool
- Conv2D(128) -> MaxPool -> Conv2D(128) -> MaxPool
- Flatten -> Dropout(0.5) -> Dense(512) -> Dense(256) -> Dense(128)
```

### Face Recognition Settings
- **Tolerance**: 0.6 (default) - Semakin rendah = semakin strict
- **Model**: HOG-based face detection + 128-dimension encoding
- **Jarak**: Euclidean distance untuk face matching

## 📈 Contoh Penggunaan Lengkap

### 1. Setup Database Awal
```python
from location_tracker import LocationTracker

tracker = LocationTracker()

# Tambah lokasi referensi
tracker.add_location_reference(
    "monas", 
    "images/monas.jpg", 
    {
        "name": "Monumen Nasional",
        "coordinates": [-6.1754, 106.8272],
        "city": "Jakarta",
        "country": "Indonesia"
    }
)

# Tambah orang dengan lokasi
tracker.add_person_location(
    "John Doe",
    "images/john_face.jpg",
    "Kantor Jakarta",
    [-6.2088, 106.8456]
)
```

### 2. Analisis Gambar
```python
# Identifikasi lokasi dari gambar
results = tracker.identify_location_from_image("test_image.jpg")

print("GPS Coordinates:", results.get("gps_coordinates"))
print("Similar Locations:", results.get("similar_locations"))
print("Face Matches:", results.get("face_matches"))

# Buat peta hasil
tracker.create_location_map(results, "output_map.html")
```

### 3. Pencarian Berdasarkan Wajah
```python
# Cari lokasi berdasarkan foto seseorang
face_results, message = tracker.find_person_location("unknown_person.jpg")

if face_results:
    for match in face_results:
        print(f"Person: {match['person']}")
        print(f"Location: {match['location']}")
        print(f"Coordinates: {match['coordinates']}")
        print(f"Confidence: {match['confidence']:.2f}")
```

## 🎯 Tips & Best Practices

### 📸 **Kualitas Gambar**
- Gunakan gambar dengan resolusi minimal 640x480
- Pastikan pencahayaan cukup untuk deteksi wajah
- Hindari gambar blur atau terdistorsi

### 🗺️ **GPS Metadata**
- Aktifkan GPS di kamera saat mengambil foto
- Format EXIF yang didukung: JPEG dengan GPS tags
- Untuk hasil terbaik, gunakan smartphone modern

### 👥 **Face Recognition**
- Gunakan foto wajah yang jelas dan frontal
- Satu wajah per gambar untuk hasil optimal
- Update database secara berkala untuk akurasi

### 🏗️ **Training Data**
- Kumpulkan minimal 10-20 gambar per lokasi
- Variasikan sudut pandang dan kondisi pencahayaan
- Label data dengan konsisten

## 🔍 Troubleshooting

### Error: "No face detected"
- Pastikan wajah terlihat jelas dalam gambar
- Coba gambar dengan pencahayaan lebih baik
- Periksa format file (JPG/PNG)

### Error: "GPS coordinates not found"
- Gambar tidak memiliki EXIF GPS data
- Gunakan foto yang diambil dengan GPS aktif
- Manual input koordinat sebagai alternatif

### Performance Issues
- Gunakan gambar dengan ukuran maksimal 2MB
- Install OpenCV dengan optimasi CUDA (optional)
- Pertimbangkan resize gambar untuk processing lebih cepat

## 🔧 Development & Customization

### Menambah Model Custom
```python
def create_custom_model(self):
    # Implementasi model CNN custom
    model = keras.Sequential([
        # Layer custom anda
    ])
    return model
```

### Integrasi API External
```python
# Contoh integrasi dengan Google Maps API
def get_place_info(self, coordinates):
    # Implementasi API call
    pass
```

### Database Custom
```python
# Gunakan database lain (PostgreSQL, MongoDB, etc.)
class CustomLocationDatabase:
    def __init__(self, connection_string):
        # Setup connection
        pass
```

## 📊 Performance Metrics

### Akurasi Face Recognition
- **False Accept Rate**: < 0.1% (tolerance=0.6)
- **False Reject Rate**: < 5% (kondisi ideal)
- **Processing Time**: ~2-5 detik per gambar

### GPS Accuracy
- **EXIF GPS**: Akurasi hingga meter (tergantung device)
- **Reverse Geocoding**: Akurasi alamat ~100m radius
- **Processing Time**: ~1-2 detik per query

## 🤝 Contributing

1. Fork repository
2. Buat feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🆘 Support

Jika mengalami masalah atau membutuhkan bantuan:

1. **Issues**: Buat issue di GitHub repository
2. **Documentation**: Baca dokumentasi lengkap
3. **Community**: Join discussion forum

## 🔮 Roadmap

### Version 2.0 (Planned)
- [ ] Real-time video tracking
- [ ] Mobile app (Flutter/React Native)
- [ ] Advanced ML models (YOLO, ResNet)
- [ ] Cloud deployment options
- [ ] Batch processing capabilities

### Version 2.1 (Future)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Integration with social media APIs
- [ ] Automated model retraining
- [ ] Privacy-preserving features

---

**Made with ❤️ for location tracking and computer vision enthusiasts**