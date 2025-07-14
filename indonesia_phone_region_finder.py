#!/usr/bin/env python3
"""
Indonesia Phone Number Region Finder
Mengidentifikasi wilayah/region dari nomor telepon Indonesia berdasarkan prefix
"""

import re
from typing import Dict, Optional, Tuple

class IndonesiaPhoneRegionFinder:
    def __init__(self):
        # Data prefix nomor telepon Indonesia dan wilayahnya
        # Format: prefix -> (wilayah, operator/jenis)
        self.phone_regions = {
            # Telepon rumah (PSTN) - berdasarkan kode area
            "021": ("DKI Jakarta", "Telepon Rumah"),
            "022": ("Bandung, Jawa Barat", "Telepon Rumah"),
            "024": ("Semarang, Jawa Tengah", "Telepon Rumah"),
            "025": ("Purwokerto, Jawa Tengah", "Telepon Rumah"),
            "026": ("Cirebon, Jawa Barat", "Telepon Rumah"),
            "027": ("Magelang, Jawa Tengah", "Telepon Rumah"),
            "028": ("Yogyakarta", "Telepon Rumah"),
            "029": ("Purwokerto, Jawa Tengah", "Telepon Rumah"),
            "031": ("Surabaya, Jawa Timur", "Telepon Rumah"),
            "032": ("Bogor, Jawa Barat", "Telepon Rumah"),
            "033": ("Sukabumi, Jawa Barat", "Telepon Rumah"),
            "034": ("Tasikmalaya, Jawa Barat", "Telepon Rumah"),
            "035": ("Malang, Jawa Timur", "Telepon Rumah"),
            "036": ("Kediri, Jawa Timur", "Telepon Rumah"),
            "038": ("Probolinggo, Jawa Timur", "Telepon Rumah"),
            
            # Sumatera
            "061": ("Medan, Sumatera Utara", "Telepon Rumah"),
            "062": ("Binjai, Sumatera Utara", "Telepon Rumah"),
            "063": ("Padang Sidempuan, Sumatera Utara", "Telepon Rumah"),
            "065": ("Pematang Siantar, Sumatera Utara", "Telepon Rumah"),
            "071": ("Palembang, Sumatera Selatan", "Telepon Rumah"),
            "075": ("Jambi", "Telepon Rumah"),
            "076": ("Bengkulu", "Telepon Rumah"),
            "0721": ("Bandar Lampung, Lampung", "Telepon Rumah"),
            "0751": ("Padang, Sumatera Barat", "Telepon Rumah"),
            "0752": ("Bukittinggi, Sumatera Barat", "Telepon Rumah"),
            "0761": ("Pekanbaru, Riau", "Telepon Rumah"),
            "0771": ("Batam, Kepulauan Riau", "Telepon Rumah"),
            "0778": ("Tanjung Pinang, Kepulauan Riau", "Telepon Rumah"),
            
            # Kalimantan
            "0511": ("Banjarmasin, Kalimantan Selatan", "Telepon Rumah"),
            "0521": ("Pontianak, Kalimantan Barat", "Telepon Rumah"),
            "0531": ("Sampit, Kalimantan Tengah", "Telepon Rumah"),
            "0541": ("Samarinda, Kalimantan Timur", "Telepon Rumah"),
            "0542": ("Balikpapan, Kalimantan Timur", "Telepon Rumah"),
            "0551": ("Tarakan, Kalimantan Utara", "Telepon Rumah"),
            
            # Sulawesi
            "0411": ("Makassar, Sulawesi Selatan", "Telepon Rumah"),
            "0421": ("Pare-Pare, Sulawesi Selatan", "Telepon Rumah"),
            "0431": ("Palu, Sulawesi Tengah", "Telepon Rumah"),
            "0441": ("Gorontalo", "Telepon Rumah"),
            "0451": ("Manado, Sulawesi Utara", "Telepon Rumah"),
            "0461": ("Kendari, Sulawesi Tenggara", "Telepon Rumah"),
            
            # Papua
            "0967": ("Jayapura, Papua", "Telepon Rumah"),
            "0969": ("Sorong, Papua Barat", "Telepon Rumah"),
            
            # Bali dan Nusa Tenggara
            "0361": ("Denpasar, Bali", "Telepon Rumah"),
            "0362": ("Singaraja, Bali", "Telepon Rumah"),
            "0370": ("Mataram, Nusa Tenggara Barat", "Telepon Rumah"),
            "0380": ("Kupang, Nusa Tenggara Timur", "Telepon Rumah"),
            
            # Maluku
            "0911": ("Ambon, Maluku", "Telepon Rumah"),
            "0921": ("Ternate, Maluku Utara", "Telepon Rumah"),
            
            # Nomor HP berdasarkan operator
            # Telkomsel
            "0811": ("Nasional", "Telkomsel (simPATI)"),
            "0812": ("Nasional", "Telkomsel (simPATI)"),
            "0813": ("Nasional", "Telkomsel (simPATI)"),
            "0821": ("Nasional", "Telkomsel (Kartu Halo)"),
            "0822": ("Nasional", "Telkomsel (Kartu Halo)"),
            "0823": ("Nasional", "Telkomsel (Kartu AS)"),
            "0851": ("Nasional", "Telkomsel (Kartu AS)"),
            "0852": ("Nasional", "Telkomsel (Kartu AS)"),
            "0853": ("Nasional", "Telkomsel (Kartu AS)"),
            
            # Indosat Ooredoo
            "0814": ("Nasional", "Indosat (IM3)"),
            "0815": ("Nasional", "Indosat (Matrix)"),
            "0816": ("Nasional", "Indosat (Matrix)"),
            "0855": ("Nasional", "Indosat (IM3)"),
            "0856": ("Nasional", "Indosat (IM3)"),
            "0857": ("Nasional", "Indosat (IM3)"),
            "0858": ("Nasional", "Indosat (Mentari)"),
            
            # XL Axiata
            "0817": ("Nasional", "XL"),
            "0818": ("Nasional", "XL"),
            "0819": ("Nasional", "XL"),
            "0859": ("Nasional", "XL"),
            "0877": ("Nasional", "XL"),
            "0878": ("Nasional", "XL"),
            
            # Tri (3)
            "0895": ("Nasional", "Tri (3)"),
            "0896": ("Nasional", "Tri (3)"),
            "0897": ("Nasional", "Tri (3)"),
            "0898": ("Nasional", "Tri (3)"),
            "0899": ("Nasional", "Tri (3)"),
            
            # Smartfren
            "0881": ("Nasional", "Smartfren"),
            "0882": ("Nasional", "Smartfren"),
            "0883": ("Nasional", "Smartfren"),
            "0884": ("Nasional", "Smartfren"),
            "0885": ("Nasional", "Smartfren"),
            "0886": ("Nasional", "Smartfren"),
            "0887": ("Nasional", "Smartfren"),
            "0888": ("Nasional", "Smartfren"),
            "0889": ("Nasional", "Smartfren"),
        }
    
    def normalize_phone_number(self, phone_number: str) -> str:
        """
        Menormalisasi nomor telepon ke format standar
        """
        # Hapus semua karakter non-digit
        phone = re.sub(r'[^0-9]', '', phone_number)
        
        # Jika dimulai dengan +62, ganti dengan 0
        if phone.startswith('62'):
            phone = '0' + phone[2:]
        
        # Jika tidak dimulai dengan 0, tambahkan 0
        if not phone.startswith('0'):
            phone = '0' + phone
            
        return phone
    
    def find_region(self, phone_number: str) -> Optional[Tuple[str, str, str]]:
        """
        Mencari region dari nomor telepon
        Returns: (wilayah, operator/jenis, prefix_yang_cocok) atau None jika tidak ditemukan
        """
        normalized = self.normalize_phone_number(phone_number)
        
        # Coba dari prefix terpanjang ke terpendek
        for length in range(6, 2, -1):  # 6, 5, 4, 3
            if len(normalized) >= length:
                prefix = normalized[:length]
                if prefix in self.phone_regions:
                    region, operator = self.phone_regions[prefix]
                    return region, operator, prefix
        
        return None
    
    def analyze_phone_numbers(self, phone_numbers: list) -> Dict:
        """
        Menganalisis multiple nomor telepon sekaligus
        """
        results = []
        stats = {
            'total': len(phone_numbers),
            'found': 0,
            'not_found': 0,
            'regions': {},
            'operators': {}
        }
        
        for phone in phone_numbers:
            result = self.find_region(phone)
            if result:
                region, operator, prefix = result
                results.append({
                    'phone': phone,
                    'normalized': self.normalize_phone_number(phone),
                    'region': region,
                    'operator': operator,
                    'prefix': prefix,
                    'status': 'found'
                })
                stats['found'] += 1
                
                # Update statistics
                if region in stats['regions']:
                    stats['regions'][region] += 1
                else:
                    stats['regions'][region] = 1
                    
                if operator in stats['operators']:
                    stats['operators'][operator] += 1
                else:
                    stats['operators'][operator] = 1
            else:
                results.append({
                    'phone': phone,
                    'normalized': self.normalize_phone_number(phone),
                    'region': 'Tidak ditemukan',
                    'operator': 'Tidak dikenal',
                    'prefix': 'N/A',
                    'status': 'not_found'
                })
                stats['not_found'] += 1
        
        return {
            'results': results,
            'statistics': stats
        }

def main():
    """
    Contoh penggunaan
    """
    finder = IndonesiaPhoneRegionFinder()
    
    # Contoh nomor telepon untuk ditest
    test_numbers = [
        "021-12345678",      # Jakarta
        "0811-123-4567",     # Telkomsel
        "022-87654321",      # Bandung
        "+62-812-345-6789",  # Telkomsel
        "0361-123456",       # Bali
        "061-12345678",      # Medan
        "0895-1234-5678",    # Tri
        "0541-123456",       # Samarinda
        "031-87654321",      # Surabaya
        "0877-123-4567",     # XL
    ]
    
    print("=== INDONESIA PHONE REGION FINDER ===\n")
    
    # Test single number
    print("1. Test Single Number:")
    test_phone = "021-12345678"
    result = finder.find_region(test_phone)
    if result:
        region, operator, prefix = result
        print(f"Nomor: {test_phone}")
        print(f"Normalized: {finder.normalize_phone_number(test_phone)}")
        print(f"Wilayah: {region}")
        print(f"Operator/Jenis: {operator}")
        print(f"Prefix: {prefix}")
    else:
        print(f"Nomor {test_phone} tidak ditemukan dalam database")
    
    print("\n" + "="*50 + "\n")
    
    # Test multiple numbers
    print("2. Test Multiple Numbers:")
    analysis = finder.analyze_phone_numbers(test_numbers)
    
    print("Hasil Analisis:")
    print("-" * 80)
    print(f"{'No':<3} {'Nomor':<15} {'Normalized':<15} {'Wilayah':<25} {'Operator':<15}")
    print("-" * 80)
    
    for i, result in enumerate(analysis['results'], 1):
        print(f"{i:<3} {result['phone']:<15} {result['normalized']:<15} {result['region']:<25} {result['operator']:<15}")
    
    print("\n" + "="*50)
    print("\n3. Statistik:")
    stats = analysis['statistics']
    print(f"Total nomor dianalisis: {stats['total']}")
    print(f"Berhasil diidentifikasi: {stats['found']}")
    print(f"Tidak ditemukan: {stats['not_found']}")
    
    print("\n4. Distribusi Wilayah:")
    for region, count in stats['regions'].items():
        print(f"  {region}: {count} nomor")
    
    print("\n5. Distribusi Operator:")
    for operator, count in stats['operators'].items():
        print(f"  {operator}: {count} nomor")

if __name__ == "__main__":
    main()