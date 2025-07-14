# 📱 Indonesia Phone Region Finder

Kode Python untuk mengidentifikasi wilayah/region dari nomor telepon Indonesia berdasarkan prefix/kode area.

## 🚀 Fitur

- ✅ Identifikasi wilayah dari nomor telepon rumah (PSTN) berdasarkan kode area
- ✅ Identifikasi operator dari nomor HP/cellular
- ✅ Support format nomor internasional (+62) dan lokal (0)
- ✅ Normalisasi otomatis format nomor telepon
- ✅ Analisis batch untuk multiple nomor sekaligus
- ✅ Statistik distribusi wilayah dan operator
- ✅ Database lengkap kode area Indonesia

## 📋 Coverage Wilayah

### Telepon Rumah (PSTN)
- **Jawa**: Jakarta, Bandung, Semarang, Yogyakarta, Surabaya, Malang, dll.
- **Sumatera**: Medan, Palembang, Padang, Pekanbaru, Jambi, Bengkulu, dll.
- **Kalimantan**: Banjarmasin, Pontianak, Samarinda, Balikpapan, dll.
- **Sulawesi**: Makassar, Manado, Palu, Gorontalo, dll.
- **Papua**: Jayapura, Sorong
- **Bali & Nusa Tenggara**: Denpasar, Mataram, Kupang
- **Maluku**: Ambon, Ternate

### Operator Seluler
- **Telkomsel**: simPATI, Kartu Halo, Kartu AS
- **Indosat Ooredoo**: IM3, Matrix, Mentari
- **XL Axiata**: XL
- **Tri**: 3 (Tri)
- **Smartfren**: Smartfren

## 🛠️ Cara Penggunaan

### 1. Penggunaan Dasar

```python
from indonesia_phone_region_finder import IndonesiaPhoneRegionFinder

# Inisialisasi
finder = IndonesiaPhoneRegionFinder()

# Cek satu nomor
result = finder.find_region("021-12345678")
if result:
    wilayah, operator, prefix = result
    print(f"Wilayah: {wilayah}")
    print(f"Operator: {operator}")
    print(f"Prefix: {prefix}")
```

### 2. Analisis Batch

```python
# Daftar nomor telepon
nomor_list = [
    "021-1234567",
    "0811-234-5678", 
    "022-87654321",
    "+62-812-345-6789"
]

# Analisis sekaligus
hasil = finder.analyze_phone_numbers(nomor_list)

# Lihat hasil
for result in hasil['results']:
    print(f"{result['phone']} -> {result['region']}")

# Lihat statistik
print(f"Total: {hasil['statistics']['total']}")
print(f"Berhasil: {hasil['statistics']['found']}")
```

### 3. Jalankan Contoh

```bash
# Jalankan script utama dengan demo
python3 indonesia_phone_region_finder.py

# Jalankan contoh penggunaan
python3 contoh_penggunaan.py
```

## 📝 Format Nomor yang Didukung

```
- 021-12345678 (format dengan strip)
- 02112345678 (format tanpa strip) 
- +62-21-12345678 (format internasional)
- +622112345678 (internasional tanpa strip)
- 0811-123-4567 (HP dengan strip)
- 08111234567 (HP tanpa strip)
- +62-811-123-4567 (HP internasional)
```

## 🔍 Contoh Output

```
=== INDONESIA PHONE REGION FINDER ===

1. Test Single Number:
Nomor: 021-12345678
Normalized: 02112345678
Wilayah: DKI Jakarta
Operator/Jenis: Telepon Rumah
Prefix: 021

📊 Statistik:
Total nomor dianalisis: 10
Berhasil diidentifikasi: 10
Tidak ditemukan: 0

📍 Distribusi Wilayah:
  DKI Jakarta: 1 nomor
  Nasional: 4 nomor
  Bandung, Jawa Barat: 1 nomor
```

## ⚠️ Catatan Penting

- Script ini **HANYA** mengidentifikasi wilayah/region berdasarkan prefix nomor telepon
- **TIDAK** melakukan tracking lokasi real-time atau mengakses data pribadi
- Menggunakan informasi publik tentang kode area Indonesia
- Untuk nomor HP, menunjukkan operator (cakupan nasional)
- Data akurat per 2024, dapat berubah seiring update operator

## 🔧 Requirements

- Python 3.6+
- Tidak memerlukan library eksternal (hanya built-in modules)

## 📁 File Structure

```
.
├── indonesia_phone_region_finder.py  # Script utama
├── contoh_penggunaan.py              # Contoh penggunaan
└── README.md                         # Dokumentasi
```

## 🤝 Kontribusi

Jika menemukan kode area yang belum tercakup atau ingin menambah data operator baru, silakan buat pull request atau issue.

## 📄 License

Free to use for educational and legitimate purposes.

---

**Disclaimer**: Script ini dibuat untuk tujuan edukasi dan identifikasi wilayah berdasarkan kode area publik. Tidak untuk digunakan dalam aktivitas tracking atau surveillance tanpa izin.