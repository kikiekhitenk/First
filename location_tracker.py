import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
import face_recognition
import os
import json
import pickle
from sklearn.neighbors import NearestNeighbors
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
from PIL import Image, ExifTags
import exifread
import matplotlib.pyplot as plt
import folium

class LocationTracker:
    def __init__(self, database_path="location_database.json"):
        """
        Inisialisasi Location Tracker
        """
        self.database_path = database_path
        self.location_database = self.load_location_database()
        self.face_encodings = {}
        self.location_features = {}
        self.model = None
        self.geolocator = Nominatim(user_agent="location_tracker")
        
        # Load atau create model
        self.setup_models()
        
    def setup_models(self):
        """Setup deep learning models"""
        try:
            # Load pre-trained model jika ada
            if os.path.exists("location_model.h5"):
                self.model = keras.models.load_model("location_model.h5")
                print("Model lokasi berhasil dimuat")
            else:
                # Buat model baru jika belum ada
                self.create_location_model()
                
            # Load face encodings jika ada
            if os.path.exists("face_encodings.pkl"):
                with open("face_encodings.pkl", "rb") as f:
                    self.face_encodings = pickle.load(f)
                print(f"Face encodings dimuat: {len(self.face_encodings)} wajah")
                
        except Exception as e:
            print(f"Error setup models: {e}")
            self.create_location_model()
    
    def create_location_model(self):
        """Membuat model CNN untuk klasifikasi lokasi"""
        model = keras.Sequential([
            keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(128, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(128, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(512, activation='relu'),
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dense(128, activation='softmax')  # Untuk klasifikasi lokasi
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        print("Model lokasi baru berhasil dibuat")
        
    def load_location_database(self):
        """Load database lokasi"""
        if os.path.exists(self.database_path):
            with open(self.database_path, 'r') as f:
                return json.load(f)
        else:
            # Buat database default dengan beberapa lokasi terkenal
            default_db = {
                "locations": {
                    "monas": {
                        "name": "Monumen Nasional",
                        "coordinates": [-6.1754, 106.8272],
                        "city": "Jakarta",
                        "country": "Indonesia",
                        "description": "Monumen Nasional Jakarta"
                    },
                    "borobudur": {
                        "name": "Candi Borobudur",
                        "coordinates": [-7.6079, 110.2038],
                        "city": "Magelang",
                        "country": "Indonesia",
                        "description": "Candi Buddha terbesar di dunia"
                    },
                    "prambanan": {
                        "name": "Candi Prambanan",
                        "coordinates": [-7.7520, 110.4915],
                        "city": "Yogyakarta",
                        "country": "Indonesia",
                        "description": "Kompleks candi Hindu terbesar di Indonesia"
                    }
                },
                "faces": {}
            }
            self.save_location_database(default_db)
            return default_db
    
    def save_location_database(self, database=None):
        """Simpan database lokasi"""
        if database is None:
            database = self.location_database
        with open(self.database_path, 'w') as f:
            json.dump(database, f, indent=4)
    
    def extract_gps_from_image(self, image_path):
        """Ekstrak koordinat GPS dari metadata gambar"""
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f)
                
            if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                lat_ref = str(tags.get('GPS GPSLatitudeRef', ''))
                lat = tags['GPS GPSLatitude'].values
                lon_ref = str(tags.get('GPS GPSLongitudeRef', ''))
                lon = tags['GPS GPSLongitude'].values
                
                # Konversi ke decimal degrees
                latitude = self.dms_to_decimal(lat, lat_ref)
                longitude = self.dms_to_decimal(lon, lon_ref)
                
                return latitude, longitude
            return None, None
        except Exception as e:
            print(f"Error extracting GPS: {e}")
            return None, None
    
    def dms_to_decimal(self, dms, ref):
        """Konversi DMS (Degrees, Minutes, Seconds) ke decimal"""
        degrees = float(dms[0])
        minutes = float(dms[1])
        seconds = float(dms[2])
        
        decimal = degrees + minutes/60 + seconds/3600
        
        if ref in ['S', 'W']:
            decimal = -decimal
            
        return decimal
    
    def preprocess_image(self, image_path):
        """Preprocessing gambar untuk model"""
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)
        return img
    
    def extract_image_features(self, image_path):
        """Ekstrak fitur gambar menggunakan CNN"""
        try:
            img = self.preprocess_image(image_path)
            
            # Gunakan layer sebelum output untuk ekstrak fitur
            feature_extractor = keras.Model(
                inputs=self.model.input,
                outputs=self.model.layers[-2].output  # Layer sebelum terakhir
            )
            
            features = feature_extractor.predict(img)
            return features.flatten()
        except Exception as e:
            print(f"Error extracting features: {e}")
            return None
    
    def detect_faces_in_image(self, image_path):
        """Deteksi dan encode wajah dalam gambar"""
        try:
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            return face_locations, face_encodings
        except Exception as e:
            print(f"Error detecting faces: {e}")
            return [], []
    
    def add_person_location(self, person_name, image_path, location_name, coordinates):
        """Tambah seseorang dengan lokasi mereka"""
        try:
            # Detect face
            face_locations, face_encodings = self.detect_faces_in_image(image_path)
            
            if not face_encodings:
                print("Tidak ada wajah terdeteksi dalam gambar")
                return False
            
            # Simpan encoding wajah pertama yang ditemukan
            face_encoding = face_encodings[0]
            
            # Simpan ke database
            person_data = {
                "name": person_name,
                "location": location_name,
                "coordinates": coordinates,
                "image_path": image_path
            }
            
            self.face_encodings[person_name] = face_encoding.tolist()
            self.location_database["faces"][person_name] = person_data
            
            # Simpan ke file
            with open("face_encodings.pkl", "wb") as f:
                pickle.dump(self.face_encodings, f)
            self.save_location_database()
            
            print(f"Berhasil menambah {person_name} di lokasi {location_name}")
            return True
            
        except Exception as e:
            print(f"Error adding person: {e}")
            return False
    
    def find_person_location(self, image_path, tolerance=0.6):
        """Cari lokasi seseorang berdasarkan foto mereka"""
        try:
            # Detect faces in query image
            face_locations, face_encodings = self.detect_faces_in_image(image_path)
            
            if not face_encodings:
                return None, "Tidak ada wajah terdeteksi dalam gambar"
            
            results = []
            
            for face_encoding in face_encodings:
                best_match = None
                best_distance = float('inf')
                
                # Compare dengan semua wajah yang tersimpan
                for person_name, stored_encoding in self.face_encodings.items():
                    stored_encoding = np.array(stored_encoding)
                    distance = face_recognition.face_distance([stored_encoding], face_encoding)[0]
                    
                    if distance < tolerance and distance < best_distance:
                        best_distance = distance
                        best_match = person_name
                
                if best_match:
                    person_data = self.location_database["faces"][best_match]
                    confidence = 1 - best_distance
                    
                    results.append({
                        "person": best_match,
                        "location": person_data["location"],
                        "coordinates": person_data["coordinates"],
                        "confidence": confidence,
                        "distance": best_distance
                    })
            
            if results:
                # Sort by confidence
                results.sort(key=lambda x: x["confidence"], reverse=True)
                return results, "Ditemukan"
            else:
                return None, "Tidak ditemukan kecocokan wajah"
                
        except Exception as e:
            print(f"Error finding person: {e}")
            return None, f"Error: {e}"
    
    def identify_location_from_image(self, image_path):
        """Identifikasi lokasi dari gambar menggunakan berbagai metode"""
        results = {
            "gps_coordinates": None,
            "predicted_location": None,
            "similar_locations": [],
            "face_matches": None
        }
        
        try:
            # 1. Cek GPS metadata
            lat, lon = self.extract_gps_from_image(image_path)
            if lat and lon:
                results["gps_coordinates"] = [lat, lon]
                
                # Reverse geocoding untuk mendapatkan nama lokasi
                try:
                    location = self.geolocator.reverse(f"{lat}, {lon}")
                    results["predicted_location"] = {
                        "name": location.address,
                        "coordinates": [lat, lon],
                        "source": "GPS_metadata"
                    }
                except:
                    pass
            
            # 2. Prediksi menggunakan model deep learning
            if self.model:
                features = self.extract_image_features(image_path)
                if features is not None:
                    # Bandingkan dengan fitur lokasi yang tersimpan
                    similar_locations = self.find_similar_locations(features)
                    results["similar_locations"] = similar_locations
            
            # 3. Cek apakah ada wajah yang dikenali
            face_results, face_message = self.find_person_location(image_path)
            if face_results:
                results["face_matches"] = face_results
            
            return results
            
        except Exception as e:
            print(f"Error identifying location: {e}")
            return results
    
    def find_similar_locations(self, image_features, top_k=5):
        """Cari lokasi serupa berdasarkan fitur gambar"""
        try:
            if not self.location_features:
                return []
            
            # Bandingkan dengan semua fitur lokasi yang tersimpan
            similarities = []
            for location_id, stored_features in self.location_features.items():
                similarity = np.dot(image_features, stored_features) / (
                    np.linalg.norm(image_features) * np.linalg.norm(stored_features)
                )
                similarities.append((location_id, similarity))
            
            # Sort by similarity
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            results = []
            for location_id, similarity in similarities[:top_k]:
                if location_id in self.location_database["locations"]:
                    location_data = self.location_database["locations"][location_id]
                    results.append({
                        "location_id": location_id,
                        "name": location_data["name"],
                        "coordinates": location_data["coordinates"],
                        "similarity": similarity,
                        "city": location_data.get("city", ""),
                        "country": location_data.get("country", "")
                    })
            
            return results
            
        except Exception as e:
            print(f"Error finding similar locations: {e}")
            return []
    
    def add_location_reference(self, location_id, image_path, location_data):
        """Tambah referensi lokasi baru"""
        try:
            # Extract features dari gambar referensi
            features = self.extract_image_features(image_path)
            if features is not None:
                self.location_features[location_id] = features
                self.location_database["locations"][location_id] = location_data
                
                # Simpan ke file
                with open("location_features.pkl", "wb") as f:
                    pickle.dump(self.location_features, f)
                self.save_location_database()
                
                print(f"Berhasil menambah referensi lokasi: {location_data['name']}")
                return True
            return False
            
        except Exception as e:
            print(f"Error adding location reference: {e}")
            return False
    
    def create_location_map(self, results, output_path="location_map.html"):
        """Buat peta lokasi hasil pencarian"""
        try:
            # Tentukan center map
            if results.get("gps_coordinates"):
                center = results["gps_coordinates"]
            elif results.get("similar_locations"):
                center = results["similar_locations"][0]["coordinates"]
            elif results.get("face_matches"):
                center = results["face_matches"][0]["coordinates"]
            else:
                center = [-6.2088, 106.8456]  # Jakarta default
            
            # Buat peta
            m = folium.Map(location=center, zoom_start=12)
            
            # Tambah marker untuk GPS coordinates
            if results.get("gps_coordinates"):
                folium.Marker(
                    results["gps_coordinates"],
                    popup="GPS Location",
                    tooltip="Lokasi dari GPS metadata",
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)
            
            # Tambah marker untuk similar locations
            for i, loc in enumerate(results.get("similar_locations", [])):
                folium.Marker(
                    loc["coordinates"],
                    popup=f"{loc['name']} (Similarity: {loc['similarity']:.2f})",
                    tooltip=f"Similar Location {i+1}",
                    icon=folium.Icon(color='blue', icon='cloud')
                ).add_to(m)
            
            # Tambah marker untuk face matches
            for i, match in enumerate(results.get("face_matches", [])):
                folium.Marker(
                    match["coordinates"],
                    popup=f"{match['person']} di {match['location']} (Confidence: {match['confidence']:.2f})",
                    tooltip=f"Face Match: {match['person']}",
                    icon=folium.Icon(color='green', icon='user')
                ).add_to(m)
            
            # Simpan peta
            m.save(output_path)
            print(f"Peta berhasil disimpan: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error creating map: {e}")
            return None
    
    def get_location_info(self, coordinates):
        """Dapatkan informasi lokasi dari koordinat"""
        try:
            lat, lon = coordinates
            location = self.geolocator.reverse(f"{lat}, {lon}")
            
            return {
                "address": location.address,
                "coordinates": [lat, lon],
                "raw": location.raw
            }
        except Exception as e:
            print(f"Error getting location info: {e}")
            return None