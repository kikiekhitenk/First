#!/usr/bin/env python3
"""
Main script untuk Location Tracker
Sistem Deep Learning untuk melacak lokasi menggunakan gambar dan face recognition
"""

import os
import sys
import argparse
from location_tracker import LocationTracker
import cv2
import numpy as np
from PIL import Image
import json

def main():
    parser = argparse.ArgumentParser(description='Location Tracker - Deep Learning untuk melacak lokasi')
    parser.add_argument('--mode', choices=['identify', 'add_person', 'add_location', 'train', 'demo'], 
                       required=True, help='Mode operasi')
    parser.add_argument('--image', type=str, help='Path ke gambar')
    parser.add_argument('--name', type=str, help='Nama orang (untuk add_person)')
    parser.add_argument('--location', type=str, help='Nama lokasi')
    parser.add_argument('--coordinates', type=str, help='Koordinat dalam format "lat,lon"')
    parser.add_argument('--output', type=str, default='results', help='Folder output')
    
    args = parser.parse_args()
    
    # Buat folder output jika belum ada
    os.makedirs(args.output, exist_ok=True)
    
    # Inisialisasi LocationTracker
    print("🔍 Menginisialisasi Location Tracker...")
    tracker = LocationTracker()
    
    if args.mode == 'identify':
        if not args.image:
            print("❌ Error: --image harus diberikan untuk mode identify")
            return
        
        identify_location(tracker, args.image, args.output)
    
    elif args.mode == 'add_person':
        if not all([args.image, args.name, args.location, args.coordinates]):
            print("❌ Error: --image, --name, --location, dan --coordinates harus diberikan untuk mode add_person")
            return
        
        add_person(tracker, args.name, args.image, args.location, args.coordinates)
    
    elif args.mode == 'add_location':
        if not all([args.image, args.location, args.coordinates]):
            print("❌ Error: --image, --location, dan --coordinates harus diberikan untuk mode add_location")
            return
        
        add_location_reference(tracker, args.image, args.location, args.coordinates)
    
    elif args.mode == 'train':
        train_model(tracker)
    
    elif args.mode == 'demo':
        run_demo(tracker, args.output)

def identify_location(tracker, image_path, output_dir):
    """Identifikasi lokasi dari gambar"""
    print(f"🔍 Menganalisis gambar: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"❌ Error: File gambar tidak ditemukan: {image_path}")
        return
    
    # Identifikasi lokasi
    results = tracker.identify_location_from_image(image_path)
    
    # Tampilkan hasil
    print("\n" + "="*50)
    print("📍 HASIL IDENTIFIKASI LOKASI")
    print("="*50)
    
    # GPS Coordinates
    if results.get("gps_coordinates"):
        lat, lon = results["gps_coordinates"]
        print(f"🌍 GPS Coordinates: {lat:.6f}, {lon:.6f}")
        if results.get("predicted_location"):
            print(f"📍 Lokasi GPS: {results['predicted_location']['name']}")
    else:
        print("❌ Tidak ada koordinat GPS dalam metadata gambar")
    
    # Similar Locations
    if results.get("similar_locations"):
        print(f"\n🏢 LOKASI SERUPA DITEMUKAN ({len(results['similar_locations'])}):")
        for i, loc in enumerate(results["similar_locations"], 1):
            print(f"  {i}. {loc['name']} ({loc['city']}, {loc['country']})")
            print(f"     Koordinat: {loc['coordinates'][0]:.6f}, {loc['coordinates'][1]:.6f}")
            print(f"     Similarity: {loc['similarity']:.3f}")
    else:
        print("\n❌ Tidak ditemukan lokasi serupa dalam database")
    
    # Face Matches
    if results.get("face_matches"):
        print(f"\n👤 WAJAH YANG DIKENALI ({len(results['face_matches'])}):")
        for i, match in enumerate(results["face_matches"], 1):
            print(f"  {i}. {match['person']} di {match['location']}")
            print(f"     Koordinat: {match['coordinates'][0]:.6f}, {match['coordinates'][1]:.6f}")
            print(f"     Confidence: {match['confidence']:.3f}")
    else:
        print("\n❌ Tidak ditemukan wajah yang dikenali")
    
    # Buat peta lokasi
    map_path = os.path.join(output_dir, "location_map.html")
    tracker.create_location_map(results, map_path)
    
    # Simpan hasil ke JSON
    results_path = os.path.join(output_dir, "results.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f"\n💾 Hasil disimpan:")
    print(f"   📄 JSON: {results_path}")
    print(f"   🗺️  Peta: {map_path}")

def add_person(tracker, name, image_path, location_name, coordinates_str):
    """Tambah seseorang ke database"""
    print(f"👤 Menambah {name} ke database...")
    
    try:
        # Parse coordinates
        lat, lon = map(float, coordinates_str.split(','))
        coordinates = [lat, lon]
        
        # Tambah person
        success = tracker.add_person_location(name, image_path, location_name, coordinates)
        
        if success:
            print(f"✅ Berhasil menambah {name} di {location_name}")
        else:
            print(f"❌ Gagal menambah {name}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def add_location_reference(tracker, image_path, location_name, coordinates_str):
    """Tambah referensi lokasi baru"""
    print(f"🏢 Menambah referensi lokasi: {location_name}")
    
    try:
        # Parse coordinates
        lat, lon = map(float, coordinates_str.split(','))
        coordinates = [lat, lon]
        
        # Buat location data
        location_id = location_name.lower().replace(' ', '_')
        location_data = {
            "name": location_name,
            "coordinates": coordinates,
            "city": "",  # Bisa diisi manual
            "country": "Indonesia",
            "description": f"Referensi lokasi untuk {location_name}"
        }
        
        # Tambah location
        success = tracker.add_location_reference(location_id, image_path, location_data)
        
        if success:
            print(f"✅ Berhasil menambah referensi lokasi: {location_name}")
        else:
            print(f"❌ Gagal menambah referensi lokasi: {location_name}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def train_model(tracker):
    """Train model dengan data yang ada"""
    print("🎓 Training model belum diimplementasi secara penuh.")
    print("📝 Untuk training yang optimal, Anda perlu:")
    print("   1. Kumpulkan dataset gambar lokasi yang besar")
    print("   2. Label setiap gambar dengan lokasi yang benar")
    print("   3. Implementasikan training loop")
    print("   4. Validasi dan test model")

def run_demo(tracker, output_dir):
    """Jalankan demo sistem"""
    print("🎬 DEMO MODE - Location Tracker")
    print("="*50)
    
    # Buat gambar demo jika belum ada
    demo_dir = "demo_images"
    os.makedirs(demo_dir, exist_ok=True)
    
    # Demo 1: Tambah beberapa contoh lokasi
    print("\n1️⃣ Menambah contoh lokasi dan orang...")
    
    # Demo locations
    demo_locations = [
        {
            "id": "demo_cafe",
            "name": "Demo Cafe",
            "coordinates": [-6.2088, 106.8456],
            "description": "Contoh cafe untuk demo"
        },
        {
            "id": "demo_park",
            "name": "Demo Park", 
            "coordinates": [-6.2300, 106.8200],
            "description": "Contoh taman untuk demo"
        }
    ]
    
    for loc in demo_locations:
        tracker.location_database["locations"][loc["id"]] = {
            "name": loc["name"],
            "coordinates": loc["coordinates"],
            "city": "Jakarta",
            "country": "Indonesia",
            "description": loc["description"]
        }
    
    tracker.save_location_database()
    print("✅ Demo locations berhasil ditambahkan")
    
    # Demo 2: Simulasi identifikasi lokasi
    print("\n2️⃣ Simulasi identifikasi lokasi...")
    
    # Buat hasil demo
    demo_results = {
        "gps_coordinates": [-6.2088, 106.8456],
        "predicted_location": {
            "name": "Jakarta, Indonesia",
            "coordinates": [-6.2088, 106.8456],
            "source": "GPS_metadata"
        },
        "similar_locations": [
            {
                "location_id": "demo_cafe",
                "name": "Demo Cafe",
                "coordinates": [-6.2088, 106.8456],
                "similarity": 0.85,
                "city": "Jakarta",
                "country": "Indonesia"
            }
        ],
        "face_matches": None
    }
    
    # Buat peta demo
    map_path = os.path.join(output_dir, "demo_map.html")
    tracker.create_location_map(demo_results, map_path)
    
    print("✅ Demo selesai!")
    print(f"🗺️  Peta demo: {map_path}")
    print("\n📖 Cara menggunakan sistem:")
    print("   1. Untuk identifikasi lokasi:")
    print("      python main.py --mode identify --image path/to/image.jpg")
    print("   2. Untuk menambah orang:")
    print("      python main.py --mode add_person --image face.jpg --name 'John' --location 'Office' --coordinates '-6.2088,106.8456'")
    print("   3. Untuk menambah lokasi referensi:")
    print("      python main.py --mode add_location --image location.jpg --location 'New Place' --coordinates '-6.2088,106.8456'")

if __name__ == "__main__":
    main()