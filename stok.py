"""
Modul Manajemen Stok untuk SISTA
(Sistem Rekomendasi Irigasi dan Stok Agroindustri)

Modul ini mengelola stok agroindustri dan memberikan rekomendasi:
- Manajemen data stok (tambah, kurang, lihat)
- Peringatan stok minimum
- Rekomendasi pemesanan ulang
"""

# Data stok (simulasi database)
stok_data = {}

# Batas minimum stok default (dalam kg)
BATAS_MINIMUM_DEFAULT = 50

# Kategori produk agroindustri
KATEGORI_PRODUK = {
    "benih": ["padi", "jagung", "kedelai", "tomat", "cabai", "kangkung", "bayam", "wortel", "kentang", "bawang"],
    "pupuk": ["urea", "npk", "za", "organik", "kompos"],
    "pestisida": ["insektisida", "herbisida", "fungisida"],
    "hasil_panen": ["gabah", "jagung_pipil", "kedelai_kering", "sayuran_segar", "buah_segar"]
}


def inisialisasi_stok():
    """Menginisialisasi data stok dengan nilai default."""
    global stok_data
    stok_data = {
        # Benih (kg)
        "benih_padi": {"jumlah": 100, "satuan": "kg", "batas_minimum": 50, "kategori": "benih"},
        "benih_jagung": {"jumlah": 80, "satuan": "kg", "batas_minimum": 40, "kategori": "benih"},
        "benih_kedelai": {"jumlah": 60, "satuan": "kg", "batas_minimum": 30, "kategori": "benih"},
        "benih_tomat": {"jumlah": 20, "satuan": "kg", "batas_minimum": 10, "kategori": "benih"},
        "benih_cabai": {"jumlah": 15, "satuan": "kg", "batas_minimum": 10, "kategori": "benih"},
        # Pupuk (kg)
        "pupuk_urea": {"jumlah": 500, "satuan": "kg", "batas_minimum": 100, "kategori": "pupuk"},
        "pupuk_npk": {"jumlah": 400, "satuan": "kg", "batas_minimum": 100, "kategori": "pupuk"},
        "pupuk_organik": {"jumlah": 300, "satuan": "kg", "batas_minimum": 80, "kategori": "pupuk"},
        # Pestisida (liter)
        "insektisida": {"jumlah": 50, "satuan": "liter", "batas_minimum": 20, "kategori": "pestisida"},
        "herbisida": {"jumlah": 40, "satuan": "liter", "batas_minimum": 15, "kategori": "pestisida"},
        "fungisida": {"jumlah": 30, "satuan": "liter", "batas_minimum": 10, "kategori": "pestisida"},
        # Hasil Panen (kg)
        "gabah": {"jumlah": 1000, "satuan": "kg", "batas_minimum": 200, "kategori": "hasil_panen"},
        "jagung_pipil": {"jumlah": 800, "satuan": "kg", "batas_minimum": 150, "kategori": "hasil_panen"},
    }


def get_semua_stok():
    """Mengembalikan seluruh data stok."""
    return stok_data.copy()


def get_stok(nama_produk):
    """
    Mendapatkan informasi stok produk tertentu.
    
    Args:
        nama_produk (str): Nama produk yang ingin dicari
    
    Returns:
        dict: Informasi stok atau None jika tidak ditemukan
    """
    nama_produk = nama_produk.lower().replace(" ", "_")
    return stok_data.get(nama_produk)


def tambah_stok(nama_produk, jumlah, satuan="kg", batas_minimum=None, kategori="lainnya"):
    """
    Menambah stok produk (baru atau existing).
    
    Args:
        nama_produk (str): Nama produk
        jumlah (float): Jumlah yang ditambahkan
        satuan (str): Satuan produk (kg, liter, dll)
        batas_minimum (float): Batas minimum stok
        kategori (str): Kategori produk
    
    Returns:
        tuple: (success: bool, message: str)
    """
    if jumlah < 0:
        return False, "Jumlah tidak boleh negatif."
    
    nama_produk = nama_produk.lower().replace(" ", "_")
    
    if nama_produk in stok_data:
        stok_data[nama_produk]["jumlah"] += jumlah
        return True, f"Berhasil menambah {jumlah} {stok_data[nama_produk]['satuan']} ke stok {nama_produk}. Total: {stok_data[nama_produk]['jumlah']} {stok_data[nama_produk]['satuan']}"
    else:
        if batas_minimum is None:
            batas_minimum = BATAS_MINIMUM_DEFAULT
        stok_data[nama_produk] = {
            "jumlah": jumlah,
            "satuan": satuan,
            "batas_minimum": batas_minimum,
            "kategori": kategori
        }
        return True, f"Berhasil menambah produk baru: {nama_produk} dengan stok {jumlah} {satuan}"


def kurangi_stok(nama_produk, jumlah):
    """
    Mengurangi stok produk.
    
    Args:
        nama_produk (str): Nama produk
        jumlah (float): Jumlah yang dikurangi
    
    Returns:
        tuple: (success: bool, message: str)
    """
    if jumlah < 0:
        return False, "Jumlah tidak boleh negatif."
    
    nama_produk = nama_produk.lower().replace(" ", "_")
    
    if nama_produk not in stok_data:
        return False, f"Produk {nama_produk} tidak ditemukan."
    
    if stok_data[nama_produk]["jumlah"] < jumlah:
        return False, f"Stok tidak mencukupi. Stok saat ini: {stok_data[nama_produk]['jumlah']} {stok_data[nama_produk]['satuan']}"
    
    stok_data[nama_produk]["jumlah"] -= jumlah
    sisa = stok_data[nama_produk]["jumlah"]
    satuan = stok_data[nama_produk]["satuan"]
    
    pesan = f"Berhasil mengurangi {jumlah} {satuan} dari stok {nama_produk}. Sisa: {sisa} {satuan}"
    
    # Peringatan jika mendekati batas minimum
    if sisa <= stok_data[nama_produk]["batas_minimum"]:
        pesan += f"\n⚠️ PERINGATAN: Stok {nama_produk} sudah mencapai/di bawah batas minimum!"
    
    return True, pesan


def cek_stok_minimum():
    """
    Mengecek produk yang stoknya di bawah batas minimum.
    
    Returns:
        list: Daftar produk dengan stok rendah
    """
    produk_rendah = []
    for nama, data in stok_data.items():
        if data["jumlah"] <= data["batas_minimum"]:
            produk_rendah.append({
                "nama": nama,
                "jumlah": data["jumlah"],
                "batas_minimum": data["batas_minimum"],
                "satuan": data["satuan"],
                "kekurangan": data["batas_minimum"] - data["jumlah"]
            })
    return produk_rendah


def rekomendasi_pemesanan():
    """
    Memberikan rekomendasi pemesanan berdasarkan stok yang rendah.
    
    Returns:
        list: Daftar rekomendasi pemesanan
    """
    produk_rendah = cek_stok_minimum()
    rekomendasi = []
    
    for produk in produk_rendah:
        # Rekomendasi pesan 2x batas minimum
        jumlah_pesan = produk["batas_minimum"] * 2
        
        # Tentukan prioritas berdasarkan level stok
        if produk["jumlah"] == 0:
            prioritas = "TINGGI"
        elif produk["jumlah"] < produk["batas_minimum"] / 2:
            prioritas = "SEDANG"
        else:
            prioritas = "RENDAH"
        
        rekomendasi.append({
            "nama": produk["nama"],
            "stok_saat_ini": produk["jumlah"],
            "rekomendasi_pesan": jumlah_pesan,
            "satuan": produk["satuan"],
            "prioritas": prioritas
        })
    
    # Urutkan berdasarkan prioritas
    urutan_prioritas = {"TINGGI": 0, "SEDANG": 1, "RENDAH": 2}
    rekomendasi.sort(key=lambda x: urutan_prioritas[x["prioritas"]])
    
    return rekomendasi


def tampilkan_stok_lengkap():
    """
    Menampilkan seluruh stok dalam format yang rapi.
    
    Returns:
        str: Tabel stok dalam format string
    """
    hasil = []
    hasil.append("\n" + "=" * 70)
    hasil.append("                    DAFTAR STOK AGROINDUSTRI")
    hasil.append("=" * 70)
    hasil.append(f"{'No':<4} {'Nama Produk':<20} {'Jumlah':<12} {'Satuan':<10} {'Status':<15}")
    hasil.append("-" * 70)
    
    no = 1
    for nama, data in sorted(stok_data.items()):
        status = "✓ Aman" if data["jumlah"] > data["batas_minimum"] else "⚠ Rendah" if data["jumlah"] > 0 else "❌ Habis"
        hasil.append(f"{no:<4} {nama:<20} {data['jumlah']:<12} {data['satuan']:<10} {status:<15}")
        no += 1
    
    hasil.append("=" * 70)
    hasil.append(f"Total produk: {len(stok_data)}")
    hasil.append("=" * 70 + "\n")
    
    return "\n".join(hasil)


def tampilkan_rekomendasi_pemesanan():
    """
    Menampilkan rekomendasi pemesanan dalam format yang rapi.
    
    Returns:
        str: Rekomendasi pemesanan dalam format string
    """
    rekomendasi = rekomendasi_pemesanan()
    
    hasil = []
    hasil.append("\n" + "=" * 70)
    hasil.append("                 REKOMENDASI PEMESANAN STOK")
    hasil.append("=" * 70)
    
    if not rekomendasi:
        hasil.append("Semua stok dalam kondisi aman. Tidak ada rekomendasi pemesanan.")
    else:
        hasil.append(f"{'No':<4} {'Nama Produk':<20} {'Stok':<10} {'Pesan':<12} {'Prioritas':<12}")
        hasil.append("-" * 70)
        
        no = 1
        for r in rekomendasi:
            stok_str = f"{r['stok_saat_ini']} {r['satuan']}"
            pesan_str = f"{r['rekomendasi_pesan']} {r['satuan']}"
            hasil.append(f"{no:<4} {r['nama']:<20} {stok_str:<10} {pesan_str:<12} {r['prioritas']:<12}")
            no += 1
    
    hasil.append("=" * 70 + "\n")
    
    return "\n".join(hasil)


def tampilkan_stok_per_kategori(kategori):
    """
    Menampilkan stok berdasarkan kategori.
    
    Args:
        kategori (str): Kategori produk (benih, pupuk, pestisida, hasil_panen)
    
    Returns:
        str: Stok per kategori dalam format string
    """
    kategori = kategori.lower()
    
    hasil = []
    hasil.append("\n" + "=" * 60)
    hasil.append(f"          STOK KATEGORI: {kategori.upper()}")
    hasil.append("=" * 60)
    
    produk_kategori = {k: v for k, v in stok_data.items() if v.get("kategori") == kategori}
    
    if not produk_kategori:
        hasil.append(f"Tidak ada produk dalam kategori {kategori}.")
    else:
        hasil.append(f"{'No':<4} {'Nama Produk':<25} {'Jumlah':<12} {'Status':<15}")
        hasil.append("-" * 60)
        
        no = 1
        for nama, data in sorted(produk_kategori.items()):
            status = "✓ Aman" if data["jumlah"] > data["batas_minimum"] else "⚠ Rendah" if data["jumlah"] > 0 else "❌ Habis"
            hasil.append(f"{no:<4} {nama:<25} {data['jumlah']} {data['satuan']:<5} {status:<15}")
            no += 1
    
    hasil.append("=" * 60 + "\n")
    
    return "\n".join(hasil)


# Inisialisasi stok saat modul dimuat
inisialisasi_stok()


# Fungsi untuk penggunaan modul secara mandiri
if __name__ == "__main__":
    print("=== Demo Modul Stok SISTA ===\n")
    
    # Tampilkan stok lengkap
    print(tampilkan_stok_lengkap())
    
    # Contoh operasi stok
    print("Mengurangi stok benih_cabai sebanyak 10 kg...")
    success, msg = kurangi_stok("benih_cabai", 10)
    print(msg)
    
    print("\nMenambah stok pupuk_urea sebanyak 200 kg...")
    success, msg = tambah_stok("pupuk_urea", 200)
    print(msg)
    
    # Tampilkan rekomendasi pemesanan
    print(tampilkan_rekomendasi_pemesanan())
    
    # Tampilkan stok per kategori
    print(tampilkan_stok_per_kategori("pupuk"))
