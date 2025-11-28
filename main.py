"""
SISTA - Sistem Rekomendasi Irigasi dan Stok Agroindustri

Program utama yang mengintegrasikan modul irigasi dan manajemen stok.
Projek Algoritma Kelompok 12
"""

import irigasi
import stok


def tampilkan_header():
    """Menampilkan header program."""
    print("\n" + "=" * 60)
    print("          ╔═══════════════════════════════════════╗")
    print("          ║            S I S T A                  ║")
    print("          ║  Sistem Rekomendasi Irigasi dan       ║")
    print("          ║        Stok Agroindustri              ║")
    print("          ╚═══════════════════════════════════════╝")
    print("          Projek Algoritma - Kelompok 12")
    print("=" * 60)


def tampilkan_menu_utama():
    """Menampilkan menu utama."""
    print("\n" + "-" * 40)
    print("              MENU UTAMA")
    print("-" * 40)
    print("1. Rekomendasi Irigasi")
    print("2. Manajemen Stok")
    print("3. Tentang Program")
    print("0. Keluar")
    print("-" * 40)


def tampilkan_menu_irigasi():
    """Menampilkan submenu irigasi."""
    print("\n" + "-" * 40)
    print("         MENU REKOMENDASI IRIGASI")
    print("-" * 40)
    print("1. Hitung Kebutuhan Air")
    print("2. Lihat Daftar Tanaman")
    print("3. Lihat Jenis Tanah")
    print("4. Lihat Kondisi Cuaca")
    print("0. Kembali ke Menu Utama")
    print("-" * 40)


def tampilkan_menu_stok():
    """Menampilkan submenu stok."""
    print("\n" + "-" * 40)
    print("           MENU MANAJEMEN STOK")
    print("-" * 40)
    print("1. Lihat Semua Stok")
    print("2. Lihat Stok per Kategori")
    print("3. Tambah Stok")
    print("4. Kurangi Stok")
    print("5. Cek Stok Minimum")
    print("6. Rekomendasi Pemesanan")
    print("0. Kembali ke Menu Utama")
    print("-" * 40)


def input_float(prompt):
    """Input angka dengan validasi."""
    while True:
        try:
            nilai = float(input(prompt))
            if nilai < 0:
                print("Nilai tidak boleh negatif. Silakan coba lagi.")
                continue
            return nilai
        except ValueError:
            print("Input tidak valid. Masukkan angka yang benar.")


def proses_irigasi():
    """Menangani submenu irigasi."""
    while True:
        tampilkan_menu_irigasi()
        pilihan = input("Pilih menu [0-4]: ").strip()
        
        if pilihan == "1":
            print("\n=== HITUNG KEBUTUHAN AIR IRIGASI ===")
            print("\nDaftar tanaman:", ", ".join(irigasi.get_daftar_tanaman()))
            jenis_tanaman = input("Masukkan jenis tanaman: ").strip().lower()
            
            luas_lahan = input_float("Masukkan luas lahan (m²): ")
            
            print("\nJenis tanah:", ", ".join(irigasi.get_daftar_jenis_tanah()))
            jenis_tanah = input("Masukkan jenis tanah: ").strip().lower()
            
            print("\nKondisi cuaca:", ", ".join(irigasi.get_daftar_kondisi_cuaca()))
            kondisi_cuaca = input("Masukkan kondisi cuaca: ").strip().lower()
            
            hasil = irigasi.tampilkan_rekomendasi_irigasi(
                jenis_tanaman, luas_lahan, jenis_tanah, kondisi_cuaca
            )
            print(hasil)
            
        elif pilihan == "2":
            print("\n=== DAFTAR TANAMAN YANG TERSEDIA ===")
            for i, tanaman in enumerate(irigasi.get_daftar_tanaman(), 1):
                kebutuhan = irigasi.KEBUTUHAN_AIR_TANAMAN[tanaman]
                print(f"{i}. {tanaman.capitalize():<15} - Kebutuhan air: {kebutuhan} liter/m²/hari")
            
        elif pilihan == "3":
            print("\n=== JENIS TANAH ===")
            for tanah, faktor in irigasi.FAKTOR_TANAH.items():
                keterangan = "normal" if faktor == 1.0 else "membutuhkan lebih banyak air" if faktor > 1.0 else "membutuhkan lebih sedikit air"
                print(f"- {tanah.capitalize():<12}: Faktor {faktor} ({keterangan})")
            
        elif pilihan == "4":
            print("\n=== KONDISI CUACA ===")
            for cuaca, faktor in irigasi.FAKTOR_CUACA.items():
                print(f"- {cuaca.replace('_', ' ').capitalize():<15}: Faktor {faktor}")
            
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid. Silakan pilih 0-4.")


def proses_stok():
    """Menangani submenu stok."""
    while True:
        tampilkan_menu_stok()
        pilihan = input("Pilih menu [0-6]: ").strip()
        
        if pilihan == "1":
            print(stok.tampilkan_stok_lengkap())
            
        elif pilihan == "2":
            print("\nKategori tersedia: benih, pupuk, pestisida, hasil_panen")
            kategori = input("Masukkan kategori: ").strip().lower()
            print(stok.tampilkan_stok_per_kategori(kategori))
            
        elif pilihan == "3":
            print("\n=== TAMBAH STOK ===")
            nama_produk = input("Nama produk: ").strip()
            
            # Cek apakah produk sudah ada
            produk_existing = stok.get_stok(nama_produk)
            if produk_existing:
                jumlah = input_float(f"Jumlah yang ditambahkan ({produk_existing['satuan']}): ")
                success, pesan = stok.tambah_stok(nama_produk, jumlah)
            else:
                print("\nProduk baru! Mohon lengkapi informasi:")
                jumlah = input_float("Jumlah stok awal: ")
                satuan = input("Satuan (kg/liter/unit): ").strip() or "kg"
                batas_min = input_float("Batas minimum stok: ")
                print("Kategori: benih, pupuk, pestisida, hasil_panen, lainnya")
                kategori = input("Kategori: ").strip() or "lainnya"
                success, pesan = stok.tambah_stok(nama_produk, jumlah, satuan, batas_min, kategori)
            
            print("\n" + pesan)
            
        elif pilihan == "4":
            print("\n=== KURANGI STOK ===")
            nama_produk = input("Nama produk: ").strip()
            produk = stok.get_stok(nama_produk)
            
            if produk:
                print(f"Stok saat ini: {produk['jumlah']} {produk['satuan']}")
                jumlah = input_float(f"Jumlah yang dikurangi ({produk['satuan']}): ")
                success, pesan = stok.kurangi_stok(nama_produk, jumlah)
                print("\n" + pesan)
            else:
                print(f"Produk '{nama_produk}' tidak ditemukan.")
            
        elif pilihan == "5":
            print("\n=== CEK STOK MINIMUM ===")
            produk_rendah = stok.cek_stok_minimum()
            if produk_rendah:
                print("\nProduk dengan stok rendah atau habis:")
                for p in produk_rendah:
                    status = "HABIS" if p['jumlah'] == 0 else "RENDAH"
                    print(f"⚠ {p['nama']}: {p['jumlah']} {p['satuan']} (min: {p['batas_minimum']}) - {status}")
            else:
                print("✓ Semua stok dalam kondisi aman!")
            
        elif pilihan == "6":
            print(stok.tampilkan_rekomendasi_pemesanan())
            
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid. Silakan pilih 0-6.")


def tampilkan_tentang():
    """Menampilkan informasi tentang program."""
    print("\n" + "=" * 60)
    print("                   TENTANG SISTA")
    print("=" * 60)
    print("""
SISTA (Sistem Rekomendasi Irigasi dan Stok Agroindustri) adalah
aplikasi yang dirancang untuk membantu petani dan pelaku usaha
agroindustri dalam:

1. REKOMENDASI IRIGASI
   - Menghitung kebutuhan air berdasarkan jenis tanaman
   - Menyesuaikan dengan kondisi tanah dan cuaca
   - Memberikan jadwal irigasi yang optimal

2. MANAJEMEN STOK
   - Mengelola data stok benih, pupuk, pestisida, dan hasil panen
   - Memberikan peringatan saat stok mendekati batas minimum
   - Memberikan rekomendasi pemesanan ulang

FITUR UTAMA:
✓ Perhitungan kebutuhan air otomatis
✓ Rekomendasi jadwal irigasi
✓ Manajemen stok terintegrasi
✓ Sistem peringatan stok minimum
✓ Rekomendasi pemesanan dengan prioritas

""")
    print("=" * 60)
    print("         Projek Algoritma - Kelompok 12")
    print("=" * 60)


def main():
    """Fungsi utama program."""
    tampilkan_header()
    
    while True:
        tampilkan_menu_utama()
        pilihan = input("Pilih menu [0-3]: ").strip()
        
        if pilihan == "1":
            proses_irigasi()
        elif pilihan == "2":
            proses_stok()
        elif pilihan == "3":
            tampilkan_tentang()
        elif pilihan == "0":
            print("\n" + "=" * 60)
            print("     Terima kasih telah menggunakan SISTA!")
            print("      Sampai jumpa dan sukses selalu! 🌾")
            print("=" * 60 + "\n")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih 0-3.")


if __name__ == "__main__":
    main()
