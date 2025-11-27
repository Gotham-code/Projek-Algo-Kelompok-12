"""
Modul Rekomendasi Irigasi untuk SISTA
(Sistem Rekomendasi Irigasi dan Stok Agroindustri)

Modul ini memberikan rekomendasi irigasi berdasarkan:
- Jenis tanaman
- Kondisi tanah
- Kondisi cuaca
"""

# Konstanta kebutuhan air tanaman (liter/m2/hari)
KEBUTUHAN_AIR_TANAMAN = {
    "padi": 8.0,
    "jagung": 5.0,
    "kedelai": 4.5,
    "tomat": 4.0,
    "cabai": 3.5,
    "kangkung": 6.0,
    "bayam": 5.5,
    "wortel": 4.0,
    "kentang": 5.5,
    "bawang": 3.0
}

# Faktor koreksi berdasarkan kondisi tanah
FAKTOR_TANAH = {
    "berpasir": 1.3,    # Tanah berpasir membutuhkan lebih banyak air
    "lempung": 1.0,     # Tanah lempung normal
    "liat": 0.8,        # Tanah liat menahan air lebih baik
    "gambut": 0.9       # Tanah gambut
}

# Faktor koreksi berdasarkan cuaca
FAKTOR_CUACA = {
    "cerah": 1.2,       # Cuaca cerah/panas butuh lebih banyak air
    "berawan": 1.0,     # Cuaca berawan normal
    "hujan_ringan": 0.5,  # Hujan ringan mengurangi kebutuhan irigasi
    "hujan_lebat": 0.0  # Hujan lebat tidak perlu irigasi
}


def get_daftar_tanaman():
    """Mengembalikan daftar tanaman yang tersedia."""
    return list(KEBUTUHAN_AIR_TANAMAN.keys())


def get_daftar_jenis_tanah():
    """Mengembalikan daftar jenis tanah yang tersedia."""
    return list(FAKTOR_TANAH.keys())


def get_daftar_kondisi_cuaca():
    """Mengembalikan daftar kondisi cuaca yang tersedia."""
    return list(FAKTOR_CUACA.keys())


def hitung_kebutuhan_air(jenis_tanaman, luas_lahan, jenis_tanah, kondisi_cuaca):
    """
    Menghitung kebutuhan air irigasi harian.
    
    Args:
        jenis_tanaman (str): Jenis tanaman yang ditanam
        luas_lahan (float): Luas lahan dalam meter persegi
        jenis_tanah (str): Jenis tanah lahan
        kondisi_cuaca (str): Kondisi cuaca saat ini
    
    Returns:
        float: Kebutuhan air dalam liter per hari, atau -1 jika input tidak valid
    """
    jenis_tanaman = jenis_tanaman.lower()
    jenis_tanah = jenis_tanah.lower()
    kondisi_cuaca = kondisi_cuaca.lower()
    
    if jenis_tanaman not in KEBUTUHAN_AIR_TANAMAN:
        return -1
    if jenis_tanah not in FAKTOR_TANAH:
        return -1
    if kondisi_cuaca not in FAKTOR_CUACA:
        return -1
    
    kebutuhan_dasar = KEBUTUHAN_AIR_TANAMAN[jenis_tanaman]
    faktor_tanah = FAKTOR_TANAH[jenis_tanah]
    faktor_cuaca = FAKTOR_CUACA[kondisi_cuaca]
    
    kebutuhan_air = kebutuhan_dasar * luas_lahan * faktor_tanah * faktor_cuaca
    return round(kebutuhan_air, 2)


def rekomendasi_jadwal_irigasi(jenis_tanaman, kondisi_cuaca):
    """
    Memberikan rekomendasi jadwal waktu irigasi.
    
    Args:
        jenis_tanaman (str): Jenis tanaman yang ditanam
        kondisi_cuaca (str): Kondisi cuaca saat ini
    
    Returns:
        dict: Rekomendasi jadwal irigasi atau None jika input tidak valid
    """
    jenis_tanaman = jenis_tanaman.lower()
    kondisi_cuaca = kondisi_cuaca.lower()
    
    if jenis_tanaman not in KEBUTUHAN_AIR_TANAMAN:
        return None
    if kondisi_cuaca not in FAKTOR_CUACA:
        return None
    
    # Rekomendasi dasar
    rekomendasi = {
        "waktu_pagi": "06:00 - 08:00",
        "waktu_sore": "16:00 - 18:00",
        "frekuensi": "2x sehari",
        "catatan": ""
    }
    
    # Penyesuaian berdasarkan cuaca
    if kondisi_cuaca == "hujan_lebat":
        rekomendasi["frekuensi"] = "Tidak perlu irigasi"
        rekomendasi["catatan"] = "Cuaca hujan lebat, irigasi tidak diperlukan hari ini."
    elif kondisi_cuaca == "hujan_ringan":
        rekomendasi["frekuensi"] = "1x sehari (sore)"
        rekomendasi["catatan"] = "Cuaca hujan ringan, cukup irigasi sore hari saja."
    elif kondisi_cuaca == "cerah":
        rekomendasi["catatan"] = "Cuaca cerah, pastikan irigasi pagi dan sore tepat waktu."
    else:
        rekomendasi["catatan"] = "Cuaca berawan, irigasi normal sesuai jadwal."
    
    # Penyesuaian berdasarkan jenis tanaman
    if jenis_tanaman == "padi":
        rekomendasi["catatan"] += " Padi membutuhkan genangan air, pastikan lahan tergenang."
    elif jenis_tanaman in ["cabai", "tomat"]:
        rekomendasi["catatan"] += " Hindari menyiram bagian daun untuk mencegah penyakit."
    
    return rekomendasi


def tampilkan_rekomendasi_irigasi(jenis_tanaman, luas_lahan, jenis_tanah, kondisi_cuaca):
    """
    Menampilkan rekomendasi irigasi lengkap.
    
    Args:
        jenis_tanaman (str): Jenis tanaman yang ditanam
        luas_lahan (float): Luas lahan dalam meter persegi
        jenis_tanah (str): Jenis tanah lahan
        kondisi_cuaca (str): Kondisi cuaca saat ini
    
    Returns:
        str: Rekomendasi irigasi dalam format string
    """
    kebutuhan_air = hitung_kebutuhan_air(jenis_tanaman, luas_lahan, jenis_tanah, kondisi_cuaca)
    jadwal = rekomendasi_jadwal_irigasi(jenis_tanaman, kondisi_cuaca)
    
    if kebutuhan_air == -1 or jadwal is None:
        return "Error: Input tidak valid. Silakan periksa jenis tanaman, tanah, atau cuaca."
    
    hasil = []
    hasil.append("\n" + "=" * 50)
    hasil.append("      REKOMENDASI IRIGASI SISTA")
    hasil.append("=" * 50)
    hasil.append(f"Jenis Tanaman  : {jenis_tanaman.capitalize()}")
    hasil.append(f"Luas Lahan     : {luas_lahan} m²")
    hasil.append(f"Jenis Tanah    : {jenis_tanah.capitalize()}")
    hasil.append(f"Kondisi Cuaca  : {kondisi_cuaca.replace('_', ' ').capitalize()}")
    hasil.append("-" * 50)
    hasil.append(f"Kebutuhan Air  : {kebutuhan_air} liter/hari")
    hasil.append(f"Jadwal Pagi    : {jadwal['waktu_pagi']}")
    hasil.append(f"Jadwal Sore    : {jadwal['waktu_sore']}")
    hasil.append(f"Frekuensi      : {jadwal['frekuensi']}")
    hasil.append("-" * 50)
    hasil.append(f"Catatan: {jadwal['catatan']}")
    hasil.append("=" * 50 + "\n")
    
    return "\n".join(hasil)


# Fungsi untuk penggunaan modul secara mandiri
if __name__ == "__main__":
    print("=== Demo Modul Irigasi SISTA ===\n")
    
    # Contoh penggunaan
    print("Daftar tanaman tersedia:", get_daftar_tanaman())
    print("Jenis tanah tersedia:", get_daftar_jenis_tanah())
    print("Kondisi cuaca tersedia:", get_daftar_kondisi_cuaca())
    
    # Contoh rekomendasi
    print(tampilkan_rekomendasi_irigasi("padi", 100, "lempung", "cerah"))
    print(tampilkan_rekomendasi_irigasi("tomat", 50, "berpasir", "hujan_ringan"))
