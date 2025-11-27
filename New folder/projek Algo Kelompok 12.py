import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_ADMIN_DIR = os.path.join(BASE_DIR, "data_admin")
os.makedirs(DATA_ADMIN_DIR, exist_ok=True)

def admin_file(name):

    return os.path.join(DATA_ADMIN_DIR, name)

def file_in_dirs(name, prefer_dirs=None):
   
    dirs = prefer_dirs or [DATA_ADMIN_DIR]
    for d in dirs:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return os.path.join(DATA_ADMIN_DIR, name)

# Gunakan file_in_dirs untuk menentukan path yang dipakai program
PENGGUNA_FILE = file_in_dirs('pengguna.csv')
TRANSAKSI_FILE = file_in_dirs('transaksi.csv')
produk_path = file_in_dirs('produk.csv')
# ---- selesai perubahan ----
def ensure_user_file(path=PENGGUNA_FILE):  
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password', 'role'])
 
def read_all_users(path=PENGGUNA_FILE):
    ensure_user_file(path)
    users = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if not r.get('username'):
                continue
            users[r['username']] = {'password': r.get('password',''), 'role': r.get('role','user')}
    return users

def append_user(username, password, role, path=PENGGUNA_FILE):
    ensure_user_file(path)
    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([username, password, role])

def write_all_users(users, path=PENGGUNA_FILE):
    ensure_user_file(path)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['username','password','role'])
        for usn, meta in users.items():
            writer.writerow([usn, meta.get('password',''), meta.get('role','user')])

def delete_user_account(username, path=PENGGUNA_FILE):
    users = read_all_users(path)
    if username not in users:
        return False, "User tidak ditemukan."
    if username == pengguna_sekarang:
        return False, "Tidak boleh menghapus account yang sedang login."
    role = users[username].get('role','user')
    if role == 'admin':
        confirm = input(f"'{username}' berperan ADMIN. Ketik 'DELETE-ADMIN' untuk konfirmasi penghapusan: ").strip()
        if confirm != 'DELETE-ADMIN':
            return False, "Konfirmasi penghapusan admin dibatalkan."
    del users[username]
    write_all_users(users, path)
    return True, f"User '{username}' berhasil dihapus."



pengguna_sekarang = None
peran_sekarang = None

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def ensure_csv(path, headers):
    """Buat file CSV dengan header bila belum ada atau kosong."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
title = r"""
███████╗██╗███████╗████████╗ █████╗ 
██╔════╝██║██╔════╝╚══██╔══╝██╔══██╗
███████╗██║███████╗   ██║   ███████║
╚════██║██║╚════██║   ██║   ██╔══██║
███████║██║███████║   ██║   ██║  ██║
╚══════╝╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝
                  
Sistem Rekomendasi Irigasi & Stock Agroindustri
"""
def halaman_utama():
    WIDTH = 66
    def hr_top():
        print("╔" + "═" * WIDTH + "╗")
    def hr_bottom():
        print("╚" + "═" * WIDTH + "╝")
    def empty_line():
        print("║" + " " * WIDTH + "║")

    while True:
        clear_screen()
        print(title)
        hr_top()
        empty_line()
        print("║" + "".center(WIDTH) + "║")
        print("║" + "SISTEM IRIGASI & STOCK AGROINDUSTRI".center(WIDTH) + "║")
        empty_line()
        print("║" + "Selamat datang, petani dan pegiat pertanian digital".center(WIDTH) + "║")
        print("║" + "Kelola akun, produk, transaksi, dan rekomendasi irigasi".center(WIDTH) + "║")
        empty_line()
        print("║" + "PILIH MENU".center(WIDTH) + "║")
        empty_line()
        menu = ["1. Daftarkan Akun", "2. Login", "3. Keluar Program"]
        for item in menu:
            print("║" + item.center(WIDTH) + "║")
        empty_line()
        hr_bottom()

        command = input("Pilih menu (1/2/3): ").strip()
        if command == '1':
            daftarkan_akun()
        elif command == '2':
            if login():
                if peran_sekarang == 'admin':
                    admin_menu()
                else:
                    user_menu()
        elif command == '3':
            print("Keluar dari Program")
            break
        else:
            print("Masukkan pilihan yang valid (1-3).")
            input("Tekan Enter untuk melanjutkan...")

def load_products(path=produk_path):
   
    ensure_csv(path, ['id','nama_produk','harga','stok', ])

    products = []
    if not os.path.exists(path):
        print("File produk.csv tidak ditemukan:", path)
        return products

    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
           
            pid = (r.get('id') or '').strip()
            nama = (r.get('nama_produk') or r.get('nama') or '').strip()
         
            try:
                harga = int((r.get('harga') or r.get('price') or 0))
            except Exception:
                harga = 0
            try:
                stok = int((r.get('stok') or r.get('stock') or 0))
            except Exception:
                stok = 0

            prod = {
                'id': pid,
                'nama': nama,
                'harga': harga,
                'stok': stok,
            }
            products.append(prod)


    if not products:
        print("Belum ada produk terdaftar di produk.csv.")
    else:
        print("Daftar Produk:")
        for p in products:
            line = f"- ID:{p['id']}  {p['nama']}  (Rp{p['harga']:,})  Stok:{p['stok']}"
            print(line)

    return products



def user_menu():
    while True:
        clear_screen()
        print('='*6, f"User Menu - {pengguna_sekarang}", '='*6)
        print("1. Lihat Produk")
        print("2. Transaksi")
        print("3. Riwayat Transaksi")
        print("4. Logout")
        cmd = input("Pilih: ").strip()
        if cmd == '1':
            load_products()
            input("Tekan Enter untuk kembali...")
        elif cmd == '2':
            transaksi()
            input("Tekan Enter untuk kembali...")
        elif cmd == '3':
            riwayat_transaksi()
            input("Tekan Enter untuk kembali...")
        elif cmd == '4':
            logout()
            return 
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk mencoba lagi...")

def admin_menu():
    while True:
        clear_screen()
        print('='*10, "Menu Admin", '='*10)
        print("""
                1. Lihat Semua Pengguna
                2. Hapus Pengguna Tertentu
                3. Tambahkan Produk
                4. Daftar Produk
                5. Hapus Produk
                6. Modifikasi Produk
                7. Penjadwalan Irigasi
                8. Logout
                9. Hapus Semua Data
              """)
        cmd = input("Pilih: ").strip()
        if cmd == '1':
            users = read_all_users()
            print("Daftar pengguna:")
            for u, v in users.items():
                print("-", u, "(", v.get('role','user'), ")")
            input("Tekan Enter untuk kembali...")
        elif cmd == '2':
            username = input("Masukkan username yang akan dihapus: ").strip()
            success, message = delete_user_account(username)
            print(message)
            input("Tekan Enter untuk kembali...")
        elif cmd == '3':
            tambahkan_produk()
            input("Tekan Enter untuk kembali...")
        elif cmd == '4':
            load_products()
            input("Tekan Enter untuk kembali...")
        elif cmd == '5':
            hapus_produk()
            input("Tekan Enter untuk kembali...")
        elif cmd == '6':
            modifikasi_produk()
            input("Tekan Enter untuk kembali...")
        elif cmd == '7':
            irrigation_menu()
            input("Tekan Enter untuk kembali...")
        elif cmd == '8':
            logout()
            return  
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk mencoba lagi...")

def daftarkan_akun():
    print('='*10, "Masukkan", '='*10)
    ensure_user_file(PENGGUNA_FILE)

  
    existing = read_all_users()


    while True:
        username = input("Masukkan Username: ").strip()
        if not username:
            print("⚠️ Username tidak boleh kosong.")
            continue
        if username in existing:
            print("⚠️ Username sudah terdaftar. Silakan pilih username lain.")
            continue
        break


    while True:
        password = input("Masukkan Password: ").strip()
        if not password:
            print("⚠️ Password tidak boleh kosong.")
            continue
        break

    role = input("Masukkan Role (admin/user) [default:user]: ").strip() or 'user'

    append_user(username, password, role, PENGGUNA_FILE)
    print("Akun berhasil didaftarkan.")

def login():
    global pengguna_sekarang, peran_sekarang
    print('='*6, "Login", '='*6)
    users = read_all_users()
    usernameget = input("Masukkan Username: ").strip()
    passwordget = input("Masukkan Password: ").strip()
    user = users.get(usernameget)
    if user is None:
        print("Username tidak ditemukan.")
        return False
    if user['password'] == passwordget:
        pengguna_sekarang = usernameget
        peran_sekarang = user.get('role', 'user')
        print(f"Berhasil login: {pengguna_sekarang} ({peran_sekarang})")
        return True
    else:
        print("Password salah.")
        return False

def logout():
    global pengguna_sekarang, peran_sekarang
    pengguna_sekarang = None
    peran_sekarang = None
    print("Anda telah logout. Kembali ke menu utama.")

def riwayat_transaksi():
    ensure_csv(TRANSAKSI_FILE, ['waktu','username','id','nama','stok','harga','total' ])
    print("Riwayat Transaksi:")
    with open(TRANSAKSI_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        found = False
        for row in reader:
            if pengguna_sekarang and row.get('username') != pengguna_sekarang:
                continue  
            found = True
            print(f"- Waktu: {row.get('waktu','')}  Produk: {row.get('nama','')} x{row.get('stok','')}  Harga: Rp{row.get('harga','')}  Total: Rp{row.get('total','')} ")
        if not found:
            print("Belum ada riwayat transaksi.")
    
def transaksi():
    ensure_csv(produk_path, ['id','nama_produk','harga','stok', ])
    if not os.path.exists(produk_path):
        print("File produk.csv tidak ditemukan.")
        return

    prods = []
    with open(produk_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                stok = int(r.get('stok') or r.get('stock') or 0)
            except ValueError:
                stok = 0
            try:
                harga = int(r.get('harga') or r.get('price') or 0)
            except ValueError:
                harga = 0
            prods.append({
                'id': (r.get('id') or '').strip(),
                'nama': (r.get('nama_produk') or r.get('name') or '').strip(),
                'harga': harga,
                'stok': stok,
            })

    if not prods:
        print("Tidak ada produk terdaftar di produk.csv.")
        return

    load_products(produk_path)

    nama = input("Masukkan nama produk (atau id): ").strip()
    produk = None
    for p in prods:
        if (p['id'] and p['id'] == nama) or (p['nama'] and p['nama'].lower() == nama.lower()):
            produk = p
            break

    if not produk:
        print("Produk tidak ditemukan.")
        return

    try:
        stok = int(input("Masukkan jumlah: ").strip())
    except ValueError:
        print("Jumlah harus berupa angka.")
        return

    if stok <= 0:
        print("Jumlah harus > 0.")
        return

    if produk['stok'] < stok:
        print(f"Stok tidak cukup. Stok saat ini: {produk['stok']}")
        return

    total = produk['harga'] * stok
    print(f"Anda membeli: {produk['nama']} x{stok}  Harga satuan: Rp{produk['harga']}  Total: Rp{total}")


    konf = input("Konfirmasi bayar? (ya/tidak): ").strip().lower()
    if konf != 'ya':
        print("Transaksi dibatalkan.")
        return

    ensure_csv(TRANSAKSI_FILE, ['waktu','username','id','nama','stok','harga','total'])
    with open(TRANSAKSI_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        username = pengguna_sekarang or ''
        writer.writerow([waktu, username, produk['id'], produk['nama'], stok, produk['harga'], total])



    with open(produk_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['id','nama_produk','harga','stok', ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in prods:
            writer.writerow({
                'id': p.get('id',''),
                'nama_produk': p.get('nama',''),
                'harga': p.get('harga',0),
                'stok': p.get('stok',0)

            })

    print("Transaksi berhasil.")

def tambahkan_produk():
    ensure_csv(produk_path, ['id','nama_produk','harga','stok', ])
    with open(produk_path, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['id','nama_produk','harga','stok', ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        try:
            id_produk = int(input("Masukkan ID produk: ").strip())
        except ValueError:
            print("ID produk harus berupa angka.")
            return
        nama_produk = input("Masukkan nama produk: ").strip()
        harga_produk = input("Masukkan harga produk: ").strip()
        stok_produk = input("Masukkan stok produk: ").strip()
        # validasi sederhana angka
        try:
            harga_v = int(harga_produk)
            stok_v = int(stok_produk)
        except ValueError:
            print("Harga dan stok harus angka.")
            return
        writer.writerow({
            'id': id_produk,
            'nama_produk': nama_produk,
            'harga': harga_v,
            'stok': stok_v,
        })
    print("Produk berhasil ditambahkan.")


def modifikasi_produk(path=produk_path):
    """
    Edit produk di produk.csv.
    - Pilih produk berdasarkan ID atau nama
    - Kosongkan input untuk mempertahankan nilai lama
    - Validasi sederhana untuk harga & stok
    """
    ensure_csv(path, ['id','nama_produk','harga','stok', ])
    prods = []
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                try:
                    harga = int(r.get('harga') or 0)
                except Exception:
                    harga = 0
                try:
                    stok = int(r.get('stok') or 0)
                except Exception:
                    stok = 0
                prods.append({
                    'id': (r.get('id') or '').strip(),
                    'nama_produk': (r.get('nama_produk') or r.get('nama') or '').strip(),
                    'harga': harga,
                    'stok': stok,
                })
    except FileNotFoundError:
        print("produk.csv tidak ditemukan.")
        return

    if not prods:
        print("Tidak ada produk untuk dimodifikasi.")
        return

    print("Daftar produk:")
    for p in prods:
        print(f"- ID:{p['id']}  {p['nama_produk']}  (Rp{p['harga']:,})  Stok:{p['stok']} ")

    key = input("Masukkan ID atau nama produk yang ingin dimodifikasi: ").strip()
    target = None
    for p in prods:
        if p['id'] and p['id'] == key:
            target = p
            break
        if p['nama_produk'] and p['nama_produk'].lower() == key.lower():
            target = p
            break

    if not target:
        print("Produk tidak ditemukan.")
        return

    print("Kosongkan input untuk menjaga nilai lama.")
    nama_baru = input(f"Nama [{target['nama_produk']}]: ").strip()
    harga_baru = input(f"Harga [{target['harga']}]: ").strip()
    stok_baru = input(f"Stok [{target['stok']}]: ").strip()

    if nama_baru:
        target['nama_produk'] = nama_baru
    if harga_baru:
        try:
            target['harga'] = int(harga_baru)
        except ValueError:
            print("Harga tidak valid, perubahan harga diabaikan.")
    if stok_baru:
        try:
            target['stok'] = int(stok_baru)
        except ValueError:
            print("Stok tidak valid, perubahan stok diabaikan.")

    with open(path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['id','nama_produk','harga','stok', ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in prods:
            writer.writerow({
                'id': p.get('id',''),
                'nama_produk': p.get('nama_produk',''),
                'harga': p.get('harga',0),
                'stok': p.get('stok',0)
            })

    print(f"Produk '{target.get('nama_produk')}' (ID:{target.get('id')}) berhasil diperbarui.")

def hapus_produk(path=produk_path):
    """Hapus produk tertentu berdasarkan ID atau nama dari produk.csv."""
    ensure_csv(path, ['id','nama_produk','harga','stok', ])

    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    if not rows:
        print("Belum ada produk untuk dihapus.")
        return

    print("Daftar produk:")
    for r in rows:
        print(f"- ID:{r.get('id','')}  {r.get('nama_produk','')}  Stok:{r.get('stok','')}  Harga:{r.get('harga','')}")

    key = input("Masukkan ID atau nama produk yang ingin dihapus: ").strip()
    idx = None
    for i, r in enumerate(rows):
        if (r.get('id') and r.get('id') == key) or (r.get('nama_produk') and r.get('nama_produk').lower() == key.lower()):
            idx = i
            break

    if idx is None:
        print("Produk tidak ditemukan.")
        return

    target = rows[idx]
    konf = input(f"Yakin ingin menghapus produk '{target.get('nama_produk','')}' (ID:{target.get('id','')})? (ya/tidak): ").strip().lower()
    if konf != 'ya':
        print("Penghapusan dibatalkan.")
        return

    del rows[idx]
    with open(path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['id','nama_produk','harga','stok', ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                'id': r.get('id',''),
                'nama_produk': r.get('nama_produk',''),
                'harga': r.get('harga',''),
                'stok': r.get('stok',''),

            })
    print("Produk berhasil dihapus.")

def cek_kelembaban_dan_cuaca():
    
    print("--- Input Manual Data Irigasi ---")

    while True:
        try:
            kelembaban = int(input("Masukkan tingkat kelembaban tanah (0-100, di mana 0 sangat kering): "))
            if 0 <= kelembaban <= 100:
                break
            else:
                print("⚠️ Kelembaban harus di antara 0 dan 100.")
        except ValueError:
            print("⚠️ Masukkan angka yang valid.")


    while True:
        cuaca_input = input("Apakah hari ini turun hujan? (ya/tidak): ").lower()
        if cuaca_input in ['ya', 'tidak']:
            cuaca_hujan = (cuaca_input == 'ya')
            break
        else:
            print("⚠️ Masukkan 'ya' atau 'tidak'.")

    return kelembaban, cuaca_hujan

def tentukan_irigasi(kelembaban, hujan):
    """Menentukan rekomendasi irigasi berdasarkan input."""
    
    BATAS_KERING = 40

    print("\n--- Analisis dan Rekomendasi ---")

    if hujan:
        print("✅ Hari ini turun hujan. Irigasi TIDAK DIPERLUKAN saat ini.")
    elif kelembaban < BATAS_KERING:
        print(f"🔴 Kelembaban tanah ({kelembaban}%) di bawah batas kritis ({BATAS_KERING}%).")
        print("💧 Rekomendasi: AKTIFKAN SISTEM IRIGASI atau berikan air.")
    else:
        print(f"🟢 Kelembaban tanah ({kelembaban}%) cukup baik.")
        print("🛑 Rekomendasi: TIDAK PERLU IRIGASI saat ini. Periksa lagi nanti.")

def irrigation_menu():
    """Menu sederhana untuk menjalankan cek irigasi manual (integrasi ke admin_menu)."""
    while True:
        clear_screen()
        print("=== Menu Irigasi Manual Sederhana ===")
        print("1. Cek kelembaban & cuaca (manual)")
        print("2. Kembali")
        cmd = input("Pilih: ").strip()
        if cmd == '1':
            kelembaban, hujan = cek_kelembaban_dan_cuaca()
            tentukan_irigasi(kelembaban, hujan)
            input("\nTekan Enter untuk kembali ke menu irigasi...")
        elif cmd == '2':
            return
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk mencoba lagi...")

if __name__ == "__main__":
    halaman_utama()

