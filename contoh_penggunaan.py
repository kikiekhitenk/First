#!/usr/bin/env python3
"""
Contoh penggunaan sederhana untuk Indonesia Phone Region Finder
"""

from indonesia_phone_region_finder import IndonesiaPhoneRegionFinder

def contoh_sederhana():
    """Contoh penggunaan sederhana"""
    
    # Inisialisasi finder
    finder = IndonesiaPhoneRegionFinder()
    
    # Daftar nomor yang ingin dicek
    nomor_telepon = [
        "021-1234567",       # Jakarta
        "0811-234-5678",     # Telkomsel
        "022-87654321",      # Bandung  
        "+62-812-345-6789",  # Telkomsel (format internasional)
        "0361-123456",       # Bali
        "061-12345678",      # Medan
        "031-87654321",      # Surabaya
        "0895-1234-5678",    # Tri
        "0877-123-4567",     # XL
        "024-87654321",      # Semarang
    ]
    
    print("🔍 IDENTIFIKASI WILAYAH NOMOR TELEPON INDONESIA\n")
    print("="*60)
    
    for i, nomor in enumerate(nomor_telepon, 1):
        print(f"\n{i}. Nomor: {nomor}")
        
        result = finder.find_region(nomor)
        if result:
            wilayah, operator, prefix = result
            print(f"   📍 Wilayah: {wilayah}")
            print(f"   📱 Operator: {operator}")
            print(f"   🔢 Prefix: {prefix}")
        else:
            print("   ❌ Wilayah tidak ditemukan")
    
    print("\n" + "="*60)

def analisis_batch():
    """Contoh analisis batch dengan statistik"""
    
    finder = IndonesiaPhoneRegionFinder()
    
    # Simulasi daftar kontak
    daftar_kontak = [
        "021-1111111", "021-2222222", "021-3333333",  # Jakarta (3)
        "022-1111111", "022-2222222",                 # Bandung (2)
        "0811-111-1111", "0812-222-2222", "0813-333-3333",  # Telkomsel (3)
        "0817-111-1111", "0818-222-2222",             # XL (2)
        "0361-111111",                                # Bali (1)
        "061-1111111",                                # Medan (1)
        "031-1111111",                                # Surabaya (1)
        "0895-111-1111",                              # Tri (1)
    ]
    
    print("\n📊 ANALISIS BATCH NOMOR TELEPON")
    print("="*50)
    
    hasil = finder.analyze_phone_numbers(daftar_kontak)
    
    print(f"📈 Total nomor dianalisis: {hasil['statistics']['total']}")
    print(f"✅ Berhasil diidentifikasi: {hasil['statistics']['found']}")
    print(f"❌ Tidak ditemukan: {hasil['statistics']['not_found']}")
    
    print("\n📍 Distribusi Wilayah:")
    for wilayah, jumlah in hasil['statistics']['regions'].items():
        print(f"   {wilayah}: {jumlah} nomor")
    
    print("\n📱 Distribusi Operator:")
    for operator, jumlah in hasil['statistics']['operators'].items():
        print(f"   {operator}: {jumlah} nomor")

def cek_nomor_custom():
    """Memungkinkan user memasukkan nomor sendiri"""
    
    finder = IndonesiaPhoneRegionFinder()
    
    print("\n🔍 CEK NOMOR TELEPON ANDA")
    print("="*30)
    print("Masukkan nomor telepon yang ingin dicek wilayahnya")
    print("Format: 021-1234567, 0811-123-4567, +62-811-123-4567, dll.")
    print("Ketik 'selesai' untuk mengakhiri\n")
    
    while True:
        nomor = input("Masukkan nomor telepon: ").strip()
        
        if nomor.lower() in ['selesai', 'exit', 'quit', '']:
            break
            
        result = finder.find_region(nomor)
        if result:
            wilayah, operator, prefix = result
            print(f"📍 Wilayah: {wilayah}")
            print(f"📱 Operator: {operator}")
            print(f"🔢 Prefix: {prefix}")
        else:
            print("❌ Nomor tidak ditemukan dalam database")
        print("-" * 30)

if __name__ == "__main__":
    # Jalankan contoh
    contoh_sederhana()
    analisis_batch()
    
    # Uncomment baris berikut jika ingin input interaktif
    # cek_nomor_custom()