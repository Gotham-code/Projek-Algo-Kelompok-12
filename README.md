# SISTA - Sistem Rekomendasi Irigasi dan Stok Agroindustri

**Projek Algoritma - Kelompok 12**

## Deskripsi

SISTA adalah aplikasi berbasis Python yang dirancang untuk membantu petani dan pelaku usaha agroindustri dalam:
- Menghitung kebutuhan air irigasi berdasarkan jenis tanaman, kondisi tanah, dan cuaca
- Mengelola stok benih, pupuk, pestisida, dan hasil panen
- Memberikan rekomendasi jadwal irigasi dan pemesanan stok

## Fitur Utama

### 1. Rekomendasi Irigasi
- Perhitungan kebutuhan air otomatis berdasarkan:
  - Jenis tanaman (padi, jagung, kedelai, tomat, cabai, dll)
  - Kondisi tanah (berpasir, lempung, liat, gambut)
  - Kondisi cuaca (cerah, berawan, hujan ringan, hujan lebat)
- Rekomendasi jadwal irigasi (pagi dan sore)
- Penyesuaian frekuensi berdasarkan cuaca

### 2. Manajemen Stok
- Pengelolaan data stok (tambah, kurang, lihat)
- Kategori produk: benih, pupuk, pestisida, hasil panen
- Peringatan stok minimum
- Rekomendasi pemesanan dengan prioritas

## Cara Menjalankan

```bash
# Clone repository
git clone https://github.com/Gotham-code/Projek-Algo-Kelompok-12.git

# Masuk ke direktori
cd Projek-Algo-Kelompok-12

# Jalankan program utama
python main.py
```

## Struktur File

```
Projek-Algo-Kelompok-12/
├── main.py      # Program utama dengan menu interaktif
├── irigasi.py   # Modul rekomendasi irigasi
├── stok.py      # Modul manajemen stok
└── README.md    # Dokumentasi
```

## Contoh Penggunaan

### Menjalankan Modul Irigasi Secara Mandiri
```bash
python irigasi.py
```

### Menjalankan Modul Stok Secara Mandiri
```bash
python stok.py
```

### Menggunakan Program Utama
```bash
python main.py
```

Ikuti menu interaktif untuk mengakses fitur:
1. **Rekomendasi Irigasi** - Hitung kebutuhan air dan jadwal irigasi
2. **Manajemen Stok** - Kelola stok agroindustri
3. **Tentang Program** - Informasi tentang SISTA

## Algoritma yang Digunakan

1. **Perhitungan Kebutuhan Air**:
   ```
   Kebutuhan Air = Kebutuhan Dasar × Luas Lahan × Faktor Tanah × Faktor Cuaca
   ```

2. **Rekomendasi Pemesanan**:
   - Prioritas TINGGI: Stok = 0
   - Prioritas SEDANG: Stok < 50% batas minimum
   - Prioritas RENDAH: Stok ≤ batas minimum

## Requirements

- Python 3.x

## Lisensi

Projek ini dibuat untuk keperluan akademik (Mata Kuliah Algoritma)