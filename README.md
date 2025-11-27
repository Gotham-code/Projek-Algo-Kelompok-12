# SISTA - Sistem Rekomendasi Irigasi dan Stok Agroindustri

## Projek Algoritma - Kelompok 12

### Deskripsi
SISTA adalah aplikasi berbasis command-line yang dirancang untuk membantu petani dan pelaku agroindustri dalam mengelola kebutuhan irigasi dan stok produk pertanian.

### Fitur Utama

#### 1. Rekomendasi Irigasi
Sistem ini menghitung kebutuhan air irigasi berdasarkan:
- **Jenis Tanaman**: Padi, Jagung, Kedelai, Cabai, Tomat, Bawang, Tebu, Kelapa Sawit
- **Jenis Tanah**: Lempung, Berpasir, Liat, Gambut
- **Kondisi Cuaca**: Cerah, Berawan, Hujan Ringan, Hujan Deras
- **Luas Lahan**: Dalam satuan meter persegi (m²)

Output yang dihasilkan:
- Kebutuhan air per m² per hari
- Total kebutuhan air untuk seluruh lahan
- Prioritas irigasi (Rendah/Sedang/Normal/Tinggi)
- Rekomendasi aksi yang harus dilakukan

#### 2. Manajemen Stok Agroindustri
Fitur pengelolaan stok meliputi:
- **Tambah Stok**: Menambahkan produk baru ke dalam inventaris
- **Lihat Stok**: Menampilkan seluruh data stok
- **Update Stok**: Menambah atau mengurangi jumlah stok
- **Hapus Stok**: Menghapus item dari inventaris
- **Cari Stok**: Mencari produk berdasarkan nama atau kategori
- **Peringatan Stok Rendah**: Menampilkan item dengan stok di bawah batas minimum

### Cara Menjalankan

```bash
# Pastikan Python 3 terinstall
python3 sista.py
```

### Struktur Menu

```
MENU UTAMA
├── 1. Rekomendasi Irigasi
│   └── Input: Tanaman, Tanah, Cuaca, Luas Lahan
│   └── Output: Kebutuhan air & rekomendasi
├── 2. Manajemen Stok Agroindustri
│   ├── 1. Lihat Semua Stok
│   ├── 2. Tambah Stok Baru
│   ├── 3. Update Stok
│   ├── 4. Hapus Stok
│   ├── 5. Cari Stok
│   ├── 6. Peringatan Stok Rendah
│   └── 0. Kembali
├── 3. Tentang SISTA
└── 0. Keluar
```

### Contoh Penggunaan

#### Rekomendasi Irigasi
```
Tanaman: Padi
Jenis Tanah: Lempung
Cuaca: Cerah
Luas Lahan: 1000 m²

Hasil:
- Kebutuhan Air per m²: 9.60 liter/hari
- Total Kebutuhan Air: 9,600.00 liter/hari
- Prioritas: Tinggi
- Rekomendasi: Lakukan irigasi lebih intensif karena cuaca panas.
```

#### Manajemen Stok
```
Produk: Pupuk Urea
Kategori: Pupuk
Jumlah: 100
Satuan: karung
Harga: 150000

Hasil:
- ID: STK0001
- Stok berhasil ditambahkan!
```

### Teknologi
- **Bahasa**: Python 3
- **Paradigma**: Prosedural
- **Interface**: Command Line Interface (CLI)

### Tim Pengembang
Kelompok 12 - Projek Algoritma

### Lisensi
Projek ini dikembangkan untuk keperluan akademik.