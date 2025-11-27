"""
SISTA - Sistem Rekomendasi Irigasi dan Stok Agroindustri
(Irrigation and Agroindustry Stock Recommendation System)

Kelompok 12 - Projek Algoritma
"""

import os
from datetime import datetime

# ==================== DATA CONSTANTS ====================

# Data tanaman dan kebutuhan airnya (liter/m²/hari)
CROP_WATER_REQUIREMENTS = {
    "padi": {"base": 8, "name": "Padi", "kategori": "Pangan"},
    "jagung": {"base": 5, "name": "Jagung", "kategori": "Pangan"},
    "kedelai": {"base": 4, "name": "Kedelai", "kategori": "Pangan"},
    "cabai": {"base": 6, "name": "Cabai", "kategori": "Hortikultura"},
    "tomat": {"base": 5, "name": "Tomat", "kategori": "Hortikultura"},
    "bawang": {"base": 4, "name": "Bawang", "kategori": "Hortikultura"},
    "tebu": {"base": 7, "name": "Tebu", "kategori": "Perkebunan"},
    "kelapa_sawit": {"base": 6, "name": "Kelapa Sawit", "kategori": "Perkebunan"},
}

# Faktor jenis tanah terhadap kebutuhan air
SOIL_FACTORS = {
    "lempung": {"factor": 1.0, "name": "Lempung", "desc": "Tanah ideal untuk pertanian"},
    "berpasir": {"factor": 1.3, "name": "Berpasir", "desc": "Membutuhkan air lebih banyak"},
    "liat": {"factor": 0.8, "name": "Liat", "desc": "Menahan air dengan baik"},
    "gambut": {"factor": 0.9, "name": "Gambut", "desc": "Kapasitas air tinggi"},
}

# Faktor cuaca terhadap kebutuhan air
WEATHER_FACTORS = {
    "cerah": {"factor": 1.2, "name": "Cerah", "desc": "Evaporasi tinggi"},
    "berawan": {"factor": 1.0, "name": "Berawan", "desc": "Kondisi normal"},
    "hujan_ringan": {"factor": 0.5, "name": "Hujan Ringan", "desc": "Kebutuhan air berkurang"},
    "hujan_deras": {"factor": 0.2, "name": "Hujan Deras", "desc": "Hampir tidak perlu irigasi"},
}

# ==================== UTILITY FUNCTIONS ====================

def clear_screen():
    """Membersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_datetime():
    """Mendapatkan tanggal dan waktu saat ini."""
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def display_header(title):
    """Menampilkan header dengan judul."""
    print("=" * 60)
    print(f"{'SISTA':^60}")
    print(f"{'Sistem Rekomendasi Irigasi dan Stok Agroindustri':^60}")
    print("=" * 60)
    print(f"[{title}]")
    print("-" * 60)

def get_valid_input(prompt, valid_options):
    """Mendapatkan input yang valid dari pengguna."""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        print(f"Input tidak valid. Pilihan: {', '.join(valid_options)}")

def get_positive_number(prompt):
    """Mendapatkan input angka positif dari pengguna."""
    while True:
        try:
            value = float(input(prompt).strip())
            if value > 0:
                return value
            print("Nilai harus lebih dari 0.")
        except ValueError:
            print("Input tidak valid. Masukkan angka yang benar.")

def get_integer(prompt, min_val=None, max_val=None):
    """Mendapatkan input integer dari pengguna."""
    while True:
        try:
            value = int(input(prompt).strip())
            if min_val is not None and value < min_val:
                print(f"Nilai minimal adalah {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Nilai maksimal adalah {max_val}.")
                continue
            return value
        except ValueError:
            print("Input tidak valid. Masukkan angka bulat.")

# ==================== IRRIGATION RECOMMENDATION ====================

def display_crop_options():
    """Menampilkan pilihan tanaman."""
    print("\nDaftar Tanaman:")
    for i, (key, data) in enumerate(CROP_WATER_REQUIREMENTS.items(), 1):
        print(f"  {i}. {data['name']} ({data['kategori']})")
    return list(CROP_WATER_REQUIREMENTS.keys())

def display_soil_options():
    """Menampilkan pilihan jenis tanah."""
    print("\nJenis Tanah:")
    for i, (key, data) in enumerate(SOIL_FACTORS.items(), 1):
        print(f"  {i}. {data['name']} - {data['desc']}")
    return list(SOIL_FACTORS.keys())

def display_weather_options():
    """Menampilkan pilihan kondisi cuaca."""
    print("\nKondisi Cuaca:")
    for i, (key, data) in enumerate(WEATHER_FACTORS.items(), 1):
        print(f"  {i}. {data['name']} - {data['desc']}")
    return list(WEATHER_FACTORS.keys())

def calculate_irrigation(crop_type, soil_type, weather, area):
    """
    Menghitung kebutuhan irigasi berdasarkan berbagai faktor.
    
    Args:
        crop_type: Jenis tanaman
        soil_type: Jenis tanah
        weather: Kondisi cuaca
        area: Luas lahan (m²)
    
    Returns:
        dict: Dictionary containing water requirements and recommendations
    """
    base_water = CROP_WATER_REQUIREMENTS[crop_type]["base"]
    soil_factor = SOIL_FACTORS[soil_type]["factor"]
    weather_factor = WEATHER_FACTORS[weather]["factor"]
    
    # Hitung kebutuhan air per m² per hari
    water_per_sqm = base_water * soil_factor * weather_factor
    
    # Hitung total kebutuhan air
    total_water = water_per_sqm * area
    
    # Buat rekomendasi
    if weather_factor <= 0.3:
        recommendation = "Tidak perlu irigasi hari ini karena curah hujan tinggi."
        priority = "Rendah"
    elif weather_factor <= 0.6:
        recommendation = "Lakukan irigasi ringan untuk melengkapi air hujan."
        priority = "Sedang"
    elif weather_factor <= 1.0:
        recommendation = "Lakukan irigasi normal sesuai jadwal."
        priority = "Normal"
    else:
        recommendation = "Lakukan irigasi lebih intensif karena cuaca panas."
        priority = "Tinggi"
    
    return {
        "water_per_sqm": water_per_sqm,
        "total_water": total_water,
        "recommendation": recommendation,
        "priority": priority,
        "crop_name": CROP_WATER_REQUIREMENTS[crop_type]["name"],
        "soil_name": SOIL_FACTORS[soil_type]["name"],
        "weather_name": WEATHER_FACTORS[weather]["name"]
    }

def irrigation_menu():
    """Menu untuk rekomendasi irigasi."""
    clear_screen()
    display_header("Rekomendasi Irigasi")
    
    # Pilih tanaman
    crop_keys = display_crop_options()
    crop_idx = get_integer("\nPilih nomor tanaman: ", 1, len(crop_keys)) - 1
    crop_type = crop_keys[crop_idx]
    
    # Pilih jenis tanah
    soil_keys = display_soil_options()
    soil_idx = get_integer("\nPilih nomor jenis tanah: ", 1, len(soil_keys)) - 1
    soil_type = soil_keys[soil_idx]
    
    # Pilih cuaca
    weather_keys = display_weather_options()
    weather_idx = get_integer("\nPilih nomor kondisi cuaca: ", 1, len(weather_keys)) - 1
    weather = weather_keys[weather_idx]
    
    # Input luas lahan
    area = get_positive_number("\nMasukkan luas lahan (m²): ")
    
    # Hitung dan tampilkan hasil
    result = calculate_irrigation(crop_type, soil_type, weather, area)
    
    print("\n" + "=" * 60)
    print("HASIL REKOMENDASI IRIGASI")
    print("=" * 60)
    print(f"Tanaman      : {result['crop_name']}")
    print(f"Jenis Tanah  : {result['soil_name']}")
    print(f"Cuaca        : {result['weather_name']}")
    print(f"Luas Lahan   : {area:,.0f} m²")
    print("-" * 60)
    print(f"Kebutuhan Air per m² : {result['water_per_sqm']:.2f} liter/hari")
    print(f"Total Kebutuhan Air  : {result['total_water']:,.2f} liter/hari")
    print(f"Prioritas Irigasi    : {result['priority']}")
    print("-" * 60)
    print(f"Rekomendasi: {result['recommendation']}")
    print("=" * 60)
    
    input("\nTekan Enter untuk kembali ke menu utama...")

# ==================== STOCK MANAGEMENT ====================

# Data stok (menggunakan list sebagai database sederhana)
stock_data = []
_stock_id_counter = 0  # Counter untuk ID stok

def generate_stock_id():
    """Menghasilkan ID stok baru."""
    global _stock_id_counter
    _stock_id_counter += 1
    return f"STK{_stock_id_counter:04d}"

def reset_stock_id_counter():
    """Reset counter untuk keperluan testing."""
    global _stock_id_counter
    _stock_id_counter = 0

def add_stock():
    """Menambahkan stok baru."""
    clear_screen()
    display_header("Tambah Stok Baru")
    
    name = input("Nama produk: ").strip()
    if not name:
        print("Nama produk tidak boleh kosong.")
        input("\nTekan Enter untuk kembali...")
        return
    
    category = input("Kategori (Pupuk/Pestisida/Benih/Alat/Hasil Panen): ").strip()
    quantity = get_positive_number("Jumlah: ")
    unit = input("Satuan (kg/liter/pcs/karung): ").strip()
    price = get_positive_number("Harga per satuan (Rp): ")
    
    stock_item = {
        "id": generate_stock_id(),
        "name": name,
        "category": category,
        "quantity": quantity,
        "unit": unit,
        "price": price,
        "date_added": get_current_datetime()
    }
    
    stock_data.append(stock_item)
    
    print("\n" + "=" * 60)
    print("Stok berhasil ditambahkan!")
    print(f"ID: {stock_item['id']}")
    print(f"Produk: {name}")
    print(f"Jumlah: {quantity} {unit}")
    print("=" * 60)
    
    input("\nTekan Enter untuk kembali...")

def view_stock():
    """Menampilkan semua stok."""
    clear_screen()
    display_header("Daftar Stok")
    
    if not stock_data:
        print("\nBelum ada data stok.")
        input("\nTekan Enter untuk kembali...")
        return
    
    print(f"\n{'ID':<10} {'Nama':<20} {'Kategori':<15} {'Jumlah':<12} {'Harga':<15}")
    print("-" * 72)
    
    total_value = 0
    for item in stock_data:
        value = item['quantity'] * item['price']
        total_value += value
        print(f"{item['id']:<10} {item['name'][:18]:<20} {item['category'][:13]:<15} "
              f"{item['quantity']:.0f} {item['unit']:<6} Rp {item['price']:>10,.0f}")
    
    print("-" * 72)
    print(f"Total item: {len(stock_data)}")
    print(f"Total nilai stok: Rp {total_value:,.0f}")
    
    input("\nTekan Enter untuk kembali...")

def update_stock():
    """Memperbarui jumlah stok."""
    clear_screen()
    display_header("Update Stok")
    
    if not stock_data:
        print("\nBelum ada data stok.")
        input("\nTekan Enter untuk kembali...")
        return
    
    # Tampilkan daftar stok
    print("\nDaftar Stok:")
    for i, item in enumerate(stock_data, 1):
        print(f"  {i}. [{item['id']}] {item['name']} - {item['quantity']} {item['unit']}")
    
    idx = get_integer("\nPilih nomor stok yang akan diupdate: ", 1, len(stock_data)) - 1
    item = stock_data[idx]
    
    print(f"\nStok saat ini: {item['quantity']} {item['unit']}")
    print("1. Tambah stok")
    print("2. Kurangi stok")
    
    action = get_integer("Pilih aksi: ", 1, 2)
    amount = get_positive_number("Jumlah: ")
    
    if action == 1:
        item['quantity'] += amount
        print(f"\nStok {item['name']} ditambah {amount} {item['unit']}.")
    else:
        if amount > item['quantity']:
            print(f"\nError: Jumlah pengurangan melebihi stok yang ada.")
        else:
            item['quantity'] -= amount
            print(f"\nStok {item['name']} dikurangi {amount} {item['unit']}.")
    
    print(f"Stok sekarang: {item['quantity']} {item['unit']}")
    
    input("\nTekan Enter untuk kembali...")

def delete_stock():
    """Menghapus stok."""
    clear_screen()
    display_header("Hapus Stok")
    
    if not stock_data:
        print("\nBelum ada data stok.")
        input("\nTekan Enter untuk kembali...")
        return
    
    # Tampilkan daftar stok
    print("\nDaftar Stok:")
    for i, item in enumerate(stock_data, 1):
        print(f"  {i}. [{item['id']}] {item['name']} - {item['quantity']} {item['unit']}")
    
    idx = get_integer("\nPilih nomor stok yang akan dihapus: ", 1, len(stock_data)) - 1
    item = stock_data[idx]
    
    confirm = input(f"\nYakin hapus '{item['name']}'? (y/n): ").strip().lower()
    if confirm == 'y':
        stock_data.pop(idx)
        print("Stok berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")
    
    input("\nTekan Enter untuk kembali...")

def search_stock():
    """Mencari stok berdasarkan nama atau kategori."""
    clear_screen()
    display_header("Cari Stok")
    
    if not stock_data:
        print("\nBelum ada data stok.")
        input("\nTekan Enter untuk kembali...")
        return
    
    keyword = input("Masukkan kata kunci pencarian: ").strip().lower()
    
    results = [item for item in stock_data 
               if keyword in item['name'].lower() or keyword in item['category'].lower()]
    
    if not results:
        print(f"\nTidak ditemukan stok dengan kata kunci '{keyword}'.")
    else:
        print(f"\nDitemukan {len(results)} hasil:")
        print(f"\n{'ID':<10} {'Nama':<20} {'Kategori':<15} {'Jumlah':<12} {'Harga':<15}")
        print("-" * 72)
        
        for item in results:
            print(f"{item['id']:<10} {item['name'][:18]:<20} {item['category'][:13]:<15} "
                  f"{item['quantity']:.0f} {item['unit']:<6} Rp {item['price']:>10,.0f}")
    
    input("\nTekan Enter untuk kembali...")

def low_stock_alert():
    """Menampilkan stok yang hampir habis."""
    clear_screen()
    display_header("Peringatan Stok Rendah")
    
    if not stock_data:
        print("\nBelum ada data stok.")
        input("\nTekan Enter untuk kembali...")
        return
    
    threshold = get_positive_number("Masukkan batas minimum stok: ")
    
    low_items = [item for item in stock_data if item['quantity'] <= threshold]
    
    if not low_items:
        print(f"\nTidak ada stok dengan jumlah di bawah {threshold}.")
    else:
        print(f"\n⚠️  PERINGATAN: {len(low_items)} item dengan stok rendah:")
        print(f"\n{'ID':<10} {'Nama':<25} {'Jumlah':<15} {'Status'}")
        print("-" * 60)
        
        for item in low_items:
            status = "HABIS" if item['quantity'] == 0 else "RENDAH"
            print(f"{item['id']:<10} {item['name'][:23]:<25} "
                  f"{item['quantity']:.0f} {item['unit']:<8} {status}")
    
    input("\nTekan Enter untuk kembali...")

def stock_menu():
    """Menu untuk manajemen stok."""
    while True:
        clear_screen()
        display_header("Manajemen Stok Agroindustri")
        
        print("\nPilih Menu:")
        print("1. Lihat Semua Stok")
        print("2. Tambah Stok Baru")
        print("3. Update Stok")
        print("4. Hapus Stok")
        print("5. Cari Stok")
        print("6. Peringatan Stok Rendah")
        print("0. Kembali ke Menu Utama")
        
        choice = get_integer("\nPilihan Anda: ", 0, 6)
        
        if choice == 0:
            break
        elif choice == 1:
            view_stock()
        elif choice == 2:
            add_stock()
        elif choice == 3:
            update_stock()
        elif choice == 4:
            delete_stock()
        elif choice == 5:
            search_stock()
        elif choice == 6:
            low_stock_alert()

# ==================== MAIN MENU ====================

def main_menu():
    """Menu utama aplikasi SISTA."""
    while True:
        clear_screen()
        display_header("Menu Utama")
        
        print(f"\nTanggal/Waktu: {get_current_datetime()}")
        print("\nSelamat datang di SISTA!")
        print("Sistem Rekomendasi Irigasi dan Stok Agroindustri\n")
        
        print("Pilih Menu:")
        print("1. Rekomendasi Irigasi")
        print("2. Manajemen Stok Agroindustri")
        print("3. Tentang SISTA")
        print("0. Keluar")
        
        choice = get_integer("\nPilihan Anda: ", 0, 3)
        
        if choice == 0:
            print("\nTerima kasih telah menggunakan SISTA!")
            print("Sampai jumpa!\n")
            break
        elif choice == 1:
            irrigation_menu()
        elif choice == 2:
            stock_menu()
        elif choice == 3:
            about_menu()

def about_menu():
    """Menampilkan informasi tentang SISTA."""
    clear_screen()
    display_header("Tentang SISTA")
    
    print("""
    SISTA - Sistem Rekomendasi Irigasi dan Stok Agroindustri
    
    Deskripsi:
    SISTA adalah aplikasi yang dirancang untuk membantu petani
    dan pelaku agroindustri dalam:
    
    1. Menghitung kebutuhan irigasi berdasarkan:
       - Jenis tanaman yang ditanam
       - Jenis tanah
       - Kondisi cuaca
       - Luas lahan
    
    2. Mengelola stok agroindustri:
       - Menambah dan menghapus stok
       - Memperbarui jumlah stok
       - Mencari stok
       - Memantau stok yang rendah
    
    Dikembangkan oleh:
    Kelompok 12 - Projek Algoritma
    
    Versi: 1.0.0
    """)
    
    input("\nTekan Enter untuk kembali...")

# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    main_menu()
