#!/usr/bin/env python3
"""
EDUCATIONAL SIMULATION: Phone Tracking Concepts
Untuk keperluan akademis - belajar konsep tracking tanpa melanggar privacy

⚠️  DISCLAIMER: 
- Ini hanya simulasi dengan data MOCK
- TIDAK melakukan tracking real
- Untuk tujuan edukasi dan penelitian saja
"""

import random
import time
import math
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

class MockCellTower:
    """Simulasi Cell Tower untuk keperluan edukasi"""
    
    def __init__(self, tower_id: str, lat: float, lon: float, range_km: float):
        self.tower_id = tower_id
        self.latitude = lat
        self.longitude = lon
        self.range_km = range_km
        self.technology = random.choice(['2G', '3G', '4G', '5G'])
        
    def __repr__(self):
        return f"Tower({self.tower_id}, {self.latitude}, {self.longitude})"

class MockPhone:
    """Simulasi phone untuk keperluan edukasi"""
    
    def __init__(self, phone_number: str, imei: str = None):
        self.phone_number = phone_number
        self.imei = imei or self._generate_mock_imei()
        self.current_position = None
        self.signal_strength = 0
        self.connected_towers = []
        
    def _generate_mock_imei(self):
        """Generate IMEI palsu untuk simulasi"""
        return f"86{random.randint(100000000000000, 999999999999999)}"

class PhoneTrackingSimulator:
    """
    SIMULASI EDUKATIF: Konsep-konsep phone tracking
    
    Menjelaskan bagaimana tracking bekerja secara teori,
    tanpa melakukan tracking asli
    """
    
    def __init__(self):
        self.mock_towers = self._create_mock_towers()
        self.mock_phones = {}
        self.tracking_logs = []
        
    def _create_mock_towers(self) -> List[MockCellTower]:
        """Buat mock cell towers untuk Jakarta area"""
        towers = [
            MockCellTower("JKT001", -6.2088, 106.8456, 5.0),  # Monas area
            MockCellTower("JKT002", -6.1751, 106.8650, 3.5),  # Kemayoran
            MockCellTower("JKT003", -6.2297, 106.8467, 4.0),  # Blok M
            MockCellTower("JKT004", -6.1944, 106.8229, 3.0),  # Menteng
            MockCellTower("JKT005", -6.2614, 106.7811, 4.5),  # Senayan
            MockCellTower("BDG001", -6.9175, 107.6191, 5.0),  # Bandung
            MockCellTower("SBY001", -7.2575, 112.7521, 5.0),  # Surabaya
        ]
        return towers
    
    def register_mock_phone(self, phone_number: str) -> str:
        """Daftarkan phone untuk simulasi tracking"""
        phone = MockPhone(phone_number)
        self.mock_phones[phone_number] = phone
        return f"Mock phone {phone_number} registered with IMEI: {phone.imei}"
    
    def simulate_triangulation(self, phone_number: str, target_lat: float, target_lon: float) -> Dict:
        """
        SIMULASI: Triangulation method
        Menjelaskan bagaimana 3+ cell tower bisa menentukan lokasi
        """
        if phone_number not in self.mock_phones:
            return {"error": "Phone not registered"}
            
        phone = self.mock_phones[phone_number]
        
        # Cari towers dalam range
        nearby_towers = []
        for tower in self.mock_towers:
            distance = self._calculate_distance(
                tower.latitude, tower.longitude,
                target_lat, target_lon
            )
            if distance <= tower.range_km:
                signal_strength = max(0, 100 - (distance / tower.range_km) * 100)
                nearby_towers.append({
                    'tower': tower,
                    'distance_km': distance,
                    'signal_strength': signal_strength
                })
        
        # Sort by signal strength
        nearby_towers.sort(key=lambda x: x['signal_strength'], reverse=True)
        
        # Simulasi triangulation (butuh minimal 3 towers)
        if len(nearby_towers) >= 3:
            # Add some random error to simulate real-world inaccuracy
            error_margin = random.uniform(0.001, 0.01)  # ~100m-1km error
            estimated_lat = target_lat + random.uniform(-error_margin, error_margin)
            estimated_lon = target_lon + random.uniform(-error_margin, error_margin)
            
            result = {
                'method': 'triangulation',
                'phone': phone_number,
                'estimated_position': {
                    'latitude': estimated_lat,
                    'longitude': estimated_lon,
                    'accuracy_radius_m': random.randint(50, 1000)
                },
                'towers_used': [
                    {
                        'tower_id': t['tower'].tower_id,
                        'distance_km': t['distance_km'],
                        'signal_strength': t['signal_strength']
                    } for t in nearby_towers[:3]
                ],
                'timestamp': datetime.now().isoformat(),
                'note': 'SIMULASI: Data ini palsu untuk tujuan edukasi'
            }
        else:
            result = {
                'method': 'triangulation',
                'error': 'Insufficient towers for triangulation',
                'towers_found': len(nearby_towers),
                'note': 'Butuh minimal 3 cell towers untuk triangulation'
            }
            
        self.tracking_logs.append(result)
        return result
    
    def simulate_gps_tracking(self, phone_number: str) -> Dict:
        """
        SIMULASI: GPS-based tracking
        Menjelaskan konsep GPS tracking (dengan user permission)
        """
        if phone_number not in self.mock_phones:
            return {"error": "Phone not registered"}
        
        # Simulasi GPS coordinates (Jakarta area)
        mock_gps = {
            'latitude': -6.2088 + random.uniform(-0.1, 0.1),
            'longitude': 106.8456 + random.uniform(-0.1, 0.1),
            'altitude': random.randint(1, 50),
            'accuracy': random.randint(3, 15),  # meters
            'timestamp': datetime.now().isoformat(),
            'satellites_used': random.randint(6, 12),
            'note': 'SIMULASI: GPS tracking requires user permission'
        }
        
        result = {
            'method': 'gps',
            'phone': phone_number,
            'position': mock_gps,
            'privacy_note': 'Real GPS tracking requires explicit user consent',
            'technical_note': 'GPS signals can be blocked indoors or in urban canyons'
        }
        
        self.tracking_logs.append(result)
        return result
    
    def simulate_wifi_triangulation(self, phone_number: str) -> Dict:
        """
        SIMULASI: WiFi-based positioning
        Menggunakan WiFi access points untuk estimasi lokasi
        """
        if phone_number not in self.mock_phones:
            return {"error": "Phone not registered"}
        
        # Mock WiFi networks
        mock_wifi_networks = [
            {'ssid': 'CafeWiFi_001', 'mac': '00:11:22:33:44:55', 'signal': -45},
            {'ssid': 'OfficeNet', 'mac': '00:11:22:33:44:56', 'signal': -52},
            {'ssid': 'HomeRouter', 'mac': '00:11:22:33:44:57', 'signal': -38},
        ]
        
        result = {
            'method': 'wifi_triangulation',
            'phone': phone_number,
            'wifi_networks': mock_wifi_networks,
            'estimated_position': {
                'latitude': -6.2088 + random.uniform(-0.01, 0.01),
                'longitude': 106.8456 + random.uniform(-0.01, 0.01),
                'accuracy_radius_m': random.randint(20, 100)
            },
            'timestamp': datetime.now().isoformat(),
            'note': 'SIMULASI: WiFi positioning requires access to WiFi database'
        }
        
        self.tracking_logs.append(result)
        return result
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Hitung jarak antara dua koordinat (Haversine formula)"""
        R = 6371  # Earth radius in km
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2) * math.sin(dlat/2) + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon/2) * math.sin(dlon/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance
    
    def explain_tracking_methods(self) -> Dict:
        """Penjelasan metode-metode tracking untuk edukasi"""
        return {
            'tracking_methods': {
                'cell_tower_triangulation': {
                    'description': 'Menggunakan 3+ cell tower untuk menentukan lokasi',
                    'accuracy': '100m - 2km',
                    'requirements': 'Akses ke database cell tower operator',
                    'legal_status': 'Hanya untuk law enforcement dengan warrant'
                },
                'gps_tracking': {
                    'description': 'Menggunakan sinyal satelit GPS',
                    'accuracy': '3-5 meters',
                    'requirements': 'User permission, GPS enabled',
                    'legal_status': 'Legal dengan explicit consent'
                },
                'wifi_positioning': {
                    'description': 'Menggunakan WiFi access points',
                    'accuracy': '20-100 meters',
                    'requirements': 'Access to WiFi database (Google, Apple)',
                    'legal_status': 'Requires user consent'
                },
                'imei_tracking': {
                    'description': 'Tracking berdasarkan IMEI device',
                    'accuracy': 'Depends on method used',
                    'requirements': 'IMEI database access',
                    'legal_status': 'Restricted to law enforcement'
                }
            },
            'privacy_notes': [
                'Semua metode tracking memerlukan izin atau warrant',
                'Civilian tidak memiliki akses ke infrastruktur telecom',
                'Real tracking memerlukan kerjasama dengan operator',
                'Privacy laws melindungi data lokasi personal'
            ]
        }
    
    def generate_research_data(self, num_samples: int = 100) -> List[Dict]:
        """Generate mock data untuk research/thesis"""
        research_data = []
        
        for i in range(num_samples):
            # Random phone numbers untuk simulasi
            phone = f"0811{random.randint(1000000, 9999999)}"
            
            # Random Jakarta coordinates
            lat = -6.2088 + random.uniform(-0.2, 0.2)
            lon = 106.8456 + random.uniform(-0.2, 0.2)
            
            # Simulasi tracking result
            accuracy = random.randint(50, 1000)
            method = random.choice(['triangulation', 'gps', 'wifi'])
            
            sample = {
                'sample_id': i + 1,
                'phone_number_hash': f"hash_{hash(phone) % 1000000}",  # Anonymized
                'timestamp': (datetime.now() - timedelta(minutes=random.randint(0, 1440))).isoformat(),
                'method': method,
                'estimated_location': {
                    'latitude': lat,
                    'longitude': lon,
                    'accuracy_radius_m': accuracy
                },
                'signal_strength': random.randint(-80, -20),
                'num_towers': random.randint(2, 6),
                'note': 'MOCK DATA for research purposes only'
            }
            research_data.append(sample)
        
        return research_data

def demo_educational_simulation():
    """Demo untuk mahasiswa IT"""
    
    print("🎓 PHONE TRACKING SIMULATION - EDUCATIONAL PURPOSE")
    print("=" * 60)
    print("⚠️  Disclaimer: Ini simulasi untuk belajar konsep, bukan tracking asli\n")
    
    # Initialize simulator
    sim = PhoneTrackingSimulator()
    
    # Register mock phones
    phone1 = "0811-123-4567"
    phone2 = "0812-987-6543"
    
    print("1. REGISTERING MOCK PHONES:")
    print(f"   {sim.register_mock_phone(phone1)}")
    print(f"   {sim.register_mock_phone(phone2)}")
    
    print("\n2. TRIANGULATION SIMULATION:")
    print("   Simulasi tracking menggunakan cell tower triangulation...")
    result1 = sim.simulate_triangulation(phone1, -6.2088, 106.8456)  # Jakarta
    print(f"   Phone: {result1.get('phone')}")
    if 'estimated_position' in result1:
        pos = result1['estimated_position']
        print(f"   Estimated Location: {pos['latitude']:.4f}, {pos['longitude']:.4f}")
        print(f"   Accuracy: ±{pos['accuracy_radius_m']}m")
        print(f"   Towers used: {len(result1.get('towers_used', []))}")
    
    print("\n3. GPS SIMULATION:")
    result2 = sim.simulate_gps_tracking(phone2)
    if 'position' in result2:
        pos = result2['position']
        print(f"   GPS Location: {pos['latitude']:.4f}, {pos['longitude']:.4f}")
        print(f"   Accuracy: ±{pos['accuracy']}m")
        print(f"   Satellites: {pos['satellites_used']}")
    
    print("\n4. WIFI POSITIONING SIMULATION:")
    result3 = sim.simulate_wifi_triangulation(phone1)
    if 'estimated_position' in result3:
        pos = result3['estimated_position']
        print(f"   WiFi Location: {pos['latitude']:.4f}, {pos['longitude']:.4f}")
        print(f"   Accuracy: ±{pos['accuracy_radius_m']}m")
    
    print("\n5. TRACKING METHODS EXPLANATION:")
    methods = sim.explain_tracking_methods()
    for method, info in methods['tracking_methods'].items():
        print(f"   📡 {method.upper()}:")
        print(f"      - Accuracy: {info['accuracy']}")
        print(f"      - Requirements: {info['requirements']}")
        print(f"      - Legal Status: {info['legal_status']}")
    
    print("\n6. RESEARCH DATA GENERATION:")
    research_data = sim.generate_research_data(10)
    print(f"   Generated {len(research_data)} mock samples for research")
    print(f"   Sample data: {research_data[0]['phone_number_hash']}")
    
    print("\n" + "=" * 60)
    print("📚 EDUCATIONAL NOTES:")
    print("• Real tracking memerlukan akses infrastruktur telecom")
    print("• Civilian/mahasiswa tidak bisa akses cell tower data")
    print("• Semua tracking real memerlukan legal authorization")
    print("• Untuk research, gunakan anonymized/synthetic data")
    print("• Simulation ini hanya untuk memahami konsep teknis")

if __name__ == "__main__":
    demo_educational_simulation()