#!/usr/bin/env python3
"""
Demo Script untuk Location Tracker
Mendemonstrasikan semua fitur sistem tracking lokasi
"""

import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json
import time
from location_tracker import LocationTracker

def create_demo_images():
    """Buat gambar demo untuk testing"""
    print("🎨 Membuat gambar demo...")
    
    # Buat folder demo
    demo_dir = "demo_images"
    os.makedirs(demo_dir, exist_ok=True)
    
    # 1. Buat gambar dengan landmark (simulasi Monas)
    img_landmark = Image.new('RGB', (640, 480), color='lightblue')
    draw = ImageDraw.Draw(img_landmark)
    
    # Gambar "monumen" sederhana
    draw.rectangle([300, 200, 340, 450], fill='gray')  # Tiang
    draw.polygon([(320, 200), (300, 180), (340, 180)], fill='gold')  # Puncak
    draw.text((250, 460), "MONAS JAKARTA", fill='black')
    
    landmark_path = os.path.join(demo_dir, "landmark_monas.jpg")
    img_landmark.save(landmark_path)
    
    # 2. Buat gambar wajah demo (kotak sederhana sebagai wajah)
    img_face = Image.new('RGB', (300, 400), color='beige')
    draw = ImageDraw.Draw(img_face)
    
    # Gambar wajah sederhana
    draw.ellipse([75, 50, 225, 200], fill='tan')  # Wajah
    draw.ellipse([100, 100, 120, 120], fill='black')  # Mata kiri
    draw.ellipse([180, 100, 200, 120], fill='black')  # Mata kanan
    draw.ellipse([140, 130, 160, 150], fill='pink')  # Hidung
    draw.arc([120, 160, 180, 180], 0, 180, fill='red', width=3)  # Mulut
    draw.text((100, 350), "DEMO PERSON", fill='black')
    
    face_path = os.path.join(demo_dir, "demo_face.jpg")
    img_face.save(face_path)
    
    # 3. Buat gambar cafe demo
    img_cafe = Image.new('RGB', (640, 480), color='brown')
    draw = ImageDraw.Draw(img_cafe)
    
    # Gambar cafe sederhana
    draw.rectangle([100, 200, 540, 400], fill='darkbrown')  # Bangunan
    draw.rectangle([250, 250, 390, 350], fill='yellow')  # Jendela
    draw.rectangle([300, 350, 340, 400], fill='brown')  # Pintu
    draw.text((250, 420), "DEMO CAFE", fill='white')
    
    cafe_path = os.path.join(demo_dir, "demo_cafe.jpg")
    img_cafe.save(cafe_path)
    
    print(f"✅ Gambar demo berhasil dibuat di folder: {demo_dir}")
    return landmark_path, face_path, cafe_path

def demo_gps_simulation():
    """Simulasi GPS coordinates"""
    print("\n📍 Demo GPS Simulation")
    print("="*50)
    
    # Koordinat lokasi terkenal di Indonesia
    locations = {
        "Monas Jakarta": [-6.1754, 106.8272],
        "Candi Borobudur": [-7.6079, 110.2038],
        "Candi Prambanan": [-7.7520, 110.4915],
        "Pantai Kuta Bali": [-8.7203, 115.1670],
        "Malioboro Yogyakarta": [-7.7928, 110.3656]
    }
    
    for name, coords in locations.items():
        print(f"📌 {name}: {coords[0]:.4f}, {coords[1]:.4f}")
    
    return locations

def demo_face_recognition(tracker, face_image_path):
    """Demo face recognition"""
    print("\n👤 Demo Face Recognition")
    print("="*50)
    
    # Tambah person demo
    print("➕ Menambah orang demo ke database...")
    success = tracker.add_person_location(
        "Demo Person",
        face_image_path,
        "Jakarta Office",
        [-6.2088, 106.8456]
    )
    
    if success:
        print("✅ Demo person berhasil ditambahkan")
        
        # Test face recognition
        print("🔍 Testing face recognition...")
        results, message = tracker.find_person_location(face_image_path)
        
        if results:
            for match in results:
                print(f"   Ditemukan: {match['person']}")
                print(f"   Lokasi: {match['location']}")
                print(f"   Koordinat: {match['coordinates']}")
                print(f"   Confidence: {match['confidence']:.2f}")
        else:
            print(f"   {message}")
    else:
        print("❌ Gagal menambah demo person")

def demo_location_recognition(tracker, landmark_path, cafe_path):
    """Demo location recognition"""
    print("\n🏢 Demo Location Recognition")
    print("="*50)
    
    # Tambah location references
    locations_data = [
        {
            "id": "demo_landmark",
            "image": landmark_path,
            "data": {
                "name": "Demo Landmark",
                "coordinates": [-6.1754, 106.8272],
                "city": "Jakarta",
                "country": "Indonesia",
                "description": "Demo landmark untuk testing"
            }
        },
        {
            "id": "demo_cafe_location",
            "image": cafe_path,
            "data": {
                "name": "Demo Cafe Location",
                "coordinates": [-6.2088, 106.8456],
                "city": "Jakarta", 
                "country": "Indonesia",
                "description": "Demo cafe untuk testing"
            }
        }
    ]
    
    for loc in locations_data:
        print(f"➕ Menambah lokasi: {loc['data']['name']}")
        success = tracker.add_location_reference(
            loc["id"],
            loc["image"],
            loc["data"]
        )
        
        if success:
            print(f"   ✅ Berhasil ditambahkan")
        else:
            print(f"   ❌ Gagal ditambahkan")

def demo_full_analysis(tracker, test_images):
    """Demo analisis lengkap"""
    print("\n🔍 Demo Full Analysis")
    print("="*50)
    
    for i, image_path in enumerate(test_images, 1):
        print(f"\n📊 Analisis Gambar {i}: {os.path.basename(image_path)}")
        print("-" * 40)
        
        # Identifikasi lokasi
        results = tracker.identify_location_from_image(image_path)
        
        # Tampilkan hasil GPS
        if results.get("gps_coordinates"):
            coords = results["gps_coordinates"]
            print(f"🌍 GPS: {coords[0]:.6f}, {coords[1]:.6f}")
        else:
            print("❌ Tidak ada GPS metadata")
        
        # Tampilkan similar locations
        similar_locs = results.get("similar_locations", [])
        if similar_locs:
            print(f"🏢 Lokasi serupa ditemukan: {len(similar_locs)}")
            for loc in similar_locs[:3]:  # Top 3
                print(f"   - {loc['name']} (similarity: {loc['similarity']:.2f})")
        else:
            print("❌ Tidak ada lokasi serupa")
        
        # Tampilkan face matches
        face_matches = results.get("face_matches")
        if face_matches:
            print(f"👤 Wajah dikenali: {len(face_matches)}")
            for match in face_matches:
                print(f"   - {match['person']} di {match['location']}")
        else:
            print("❌ Tidak ada wajah yang dikenali")
        
        # Buat peta untuk setiap analisis
        map_path = f"demo_map_{i}.html"
        tracker.create_location_map(results, map_path)
        print(f"🗺️  Peta disimpan: {map_path}")

def demo_database_status(tracker):
    """Tampilkan status database"""
    print("\n💾 Status Database")
    print("="*50)
    
    db = tracker.location_database
    
    # Lokasi
    locations = db.get("locations", {})
    print(f"📍 Total lokasi: {len(locations)}")
    for loc_id, loc_data in locations.items():
        print(f"   - {loc_data['name']} ({loc_data.get('city', 'Unknown')})")
    
    # Wajah
    faces = db.get("faces", {})
    print(f"👤 Total wajah: {len(faces)}")
    for person_name, person_data in faces.items():
        print(f"   - {person_name} di {person_data['location']}")
    
    # File encodings
    if os.path.exists("face_encodings.pkl"):
        print("✅ Face encodings file tersedia")
    else:
        print("❌ Face encodings file tidak ditemukan")
    
    if os.path.exists("location_features.pkl"):
        print("✅ Location features file tersedia")
    else:
        print("❌ Location features file tidak ditemukan")

def demo_performance_test(tracker, test_images):
    """Test performa sistem"""
    print("\n⚡ Performance Test")
    print("="*50)
    
    total_time = 0
    successful_analyses = 0
    
    for i, image_path in enumerate(test_images, 1):
        print(f"🔍 Testing image {i}: {os.path.basename(image_path)}")
        
        start_time = time.time()
        try:
            results = tracker.identify_location_from_image(image_path)
            end_time = time.time()
            
            processing_time = end_time - start_time
            total_time += processing_time
            successful_analyses += 1
            
            print(f"   ⏱️  Processing time: {processing_time:.2f} seconds")
            
            # Count results
            gps_found = bool(results.get("gps_coordinates"))
            similar_found = len(results.get("similar_locations", []))
            faces_found = len(results.get("face_matches", []))
            
            print(f"   📊 GPS: {gps_found}, Similar: {similar_found}, Faces: {faces_found}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    if successful_analyses > 0:
        avg_time = total_time / successful_analyses
        print(f"\n📈 Performance Summary:")
        print(f"   ✅ Successful analyses: {successful_analyses}/{len(test_images)}")
        print(f"   ⏱️  Average processing time: {avg_time:.2f} seconds")
        print(f"   🚀 Throughput: {1/avg_time:.2f} images/second")

def generate_report(tracker):
    """Generate laporan demo"""
    print("\n📄 Generating Demo Report")
    print("="*50)
    
    report = {
        "demo_info": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "system": "Location Tracker v1.0",
            "demo_type": "Full System Demo"
        },
        "database_status": {
            "total_locations": len(tracker.location_database.get("locations", {})),
            "total_faces": len(tracker.location_database.get("faces", {})),
            "files_created": []
        },
        "features_tested": [
            "GPS Metadata Extraction",
            "Face Recognition",
            "Location Recognition",
            "Image Feature Extraction",
            "Interactive Map Generation",
            "Database Management"
        ]
    }
    
    # List files yang dibuat
    demo_files = []
    for file in os.listdir("."):
        if file.startswith("demo_") and (file.endswith(".html") or file.endswith(".json")):
            demo_files.append(file)
    
    report["database_status"]["files_created"] = demo_files
    
    # Simpan report
    report_path = "demo_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)
    
    print(f"✅ Demo report saved: {report_path}")
    
    return report

def main():
    """Main demo function"""
    print("🎬 LOCATION TRACKER - FULL SYSTEM DEMO")
    print("=" * 60)
    print("Demo ini akan menguji semua fitur Location Tracker:")
    print("✅ GPS Metadata Extraction")
    print("✅ Face Recognition") 
    print("✅ Location Recognition")
    print("✅ Image Analysis")
    print("✅ Interactive Mapping")
    print("✅ Database Management")
    print("✅ Performance Testing")
    print("=" * 60)
    
    # Inisialisasi tracker
    print("\n🔧 Initializing Location Tracker...")
    tracker = LocationTracker()
    
    # Buat gambar demo
    landmark_path, face_path, cafe_path = create_demo_images()
    test_images = [landmark_path, face_path, cafe_path]
    
    # Demo GPS simulation
    demo_gps_simulation()
    
    # Demo face recognition
    demo_face_recognition(tracker, face_path)
    
    # Demo location recognition  
    demo_location_recognition(tracker, landmark_path, cafe_path)
    
    # Demo full analysis
    demo_full_analysis(tracker, test_images)
    
    # Show database status
    demo_database_status(tracker)
    
    # Performance test
    demo_performance_test(tracker, test_images)
    
    # Generate report
    report = generate_report(tracker)
    
    print("\n🎉 DEMO SELESAI!")
    print("=" * 60)
    print("📁 File yang dihasilkan:")
    print("   - demo_images/ (folder gambar demo)")
    print("   - demo_map_*.html (peta interaktif)")
    print("   - demo_report.json (laporan demo)")
    print("   - location_database.json (database lokasi)")
    print("   - face_encodings.pkl (encoding wajah)")
    
    print("\n🚀 Selanjutnya:")
    print("   1. Jalankan web interface: python web_app.py")
    print("   2. Upload gambar real untuk testing")
    print("   3. Tambahkan lebih banyak data training")
    print("   4. Eksplorasi fitur advanced")
    
    print("\n📞 Support:")
    print("   - Baca README.md untuk dokumentasi lengkap")
    print("   - Check demo_report.json untuk detail hasil")

if __name__ == "__main__":
    main()