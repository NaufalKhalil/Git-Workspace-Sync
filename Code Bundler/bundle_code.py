"""
gabung_py.py
============
Menggabungkan semua file .py dalam folder pilihan menjadi satu file
dokumentasi teks agar mudah dikirim ke AI.

Cara pakai:
  1. Letakkan script ini di LUAR folder-folder yang berisi file .py kamu.
     Contoh struktur:
       📁 Proyek/
         📄 gabung_py.py        ← script ini
         📁 Python Sesi 1/      ← folder berisi file .py
         📁 Python Sesi 2/      ← folder berisi file .py
         📁 Latihan Lain/       ← dst.

  2. Jalankan:  python gabung_py.py
  3. Pilih nomor folder yang ingin digabung
  4. File hasil .txt akan muncul di samping script ini
"""

import os
import datetime


def kumpulkan_folder(base_dir):
    """Mengumpulkan semua sub-folder di direktori yang sama dengan script."""
    folders = []
    for item in sorted(os.listdir(base_dir)):
        path = os.path.join(base_dir, item)
        if os.path.isdir(path):
            folders.append((item, path))
    return folders


def kumpulkan_file_py(folder):
    """Mengumpulkan semua file .py dalam folder, diurutkan alfabetis."""
    hasil = []
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        if os.path.isfile(path) and f.endswith(".py"):
            hasil.append(path)
    hasil.sort(key=lambda p: os.path.basename(p).lower())
    return hasil


def buat_dokumentasi(nama_folder, folder_path, output_path):
    file_list = kumpulkan_file_py(folder_path)

    if not file_list:
        print(f"\n❌  Tidak ada file .py di folder '{nama_folder}'.")
        return

    waktu_sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_path, "w", encoding="utf-8") as out:
        # Header utama
        out.write("=" * 70 + "\n")
        out.write(f"  DOKUMENTASI KODE PYTHON – {nama_folder.upper()}\n")
        out.write(f"  Dibuat  : {waktu_sekarang}\n")
        out.write(f"  Folder  : {folder_path}\n")
        out.write(f"  Total   : {len(file_list)} file\n")
        out.write("=" * 70 + "\n\n")

        # Peraturan untuk AI
        out.write("=" * 70 + "\n")
        out.write("  KONTEKS & PERATURAN UNTUK AI – BACA INI DULU\n")
        out.write("=" * 70 + "\n\n")
        out.write(
            "Halo AI! Ini adalah sesi lanjutan belajar Python seorang pemula.\n"
            "Obrolan sebelumnya sudah mencapai batas token sehingga chat dibuka ulang.\n"
            "File ini berisi seluruh kode yang sudah pernah dibuat sebagai bukti progres belajar.\n\n"

            "Tugasmu adalah menjadi tutor/mentor Python interaktif dengan aturan berikut:\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            " ATURAN PEMBERIAN SOAL\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            " 1. JANGAN beri jawaban kode lengkap sebelum pengguna mengatakan\n"
            "    kata 'menyerah'. Sebelum itu, hanya boleh memberi clue/petunjuk.\n\n"

            " 2. Jika pengguna mengatakan 'menyerah', barulah tampilkan kode\n"
            "    jawaban lengkap beserta penjelasannya.\n\n"

            " 3. Jika kode yang dikirim pengguna SALAH atau belum lulus:\n"
            "    - Jangan langsung kasih jawaban.\n"
            "    - Berikan petunjuk/clue yang mengarahkan ke kesalahan.\n"
            "    - Tanyakan apakah mau coba lagi atau menyerah.\n\n"

            " 4. Soal level berikutnya HANYA boleh diberikan setelah kode\n"
            "    pengguna dinyatakan BENAR / LULUS oleh kamu.\n\n"

            " 5. Tingkat kesulitan soal harus disesuaikan dengan level:\n"
            "    - Level rendah  → soal sederhana, 1 konsep, cocok untuk pemula.\n"
            "    - Level tinggi  → soal lebih kompleks, bisa gabungan beberapa konsep.\n"
            "    - Naik level hanya jika sudah lulus soal sebelumnya.\n\n"

            " 6. Soal harus selalu bisa dipahami pemula:\n"
            "    - Gunakan bahasa yang mudah dan jelas.\n"
            "    - Sertakan contoh input/output yang diharapkan.\n"
            "    - Jangan gunakan library eksternal kecuali sudah di level lanjut.\n\n"

            " 7. Lihat daftar kode di bawah untuk mengetahui syntax dan topik\n"
            "    apa saja yang sudah pernah dipelajari. Gunakan ini sebagai\n"
            "    acuan level dan titik lanjut pembelajaran.\n\n"

            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            " CARA MEMULAI SESI INI\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            " Setelah membaca file ini, sambut pengguna dan tanyakan:\n"
            " 'Mau lanjut dari mana? Minta soal baru, atau ada topik tertentu?'\n\n"
        )
        out.write("=" * 70 + "\n\n")

        # Daftar isi
        out.write("DAFTAR ISI\n")
        out.write("-" * 40 + "\n")
        for i, path in enumerate(file_list, 1):
            out.write(f"  {i:>3}. {os.path.basename(path)}\n")
        out.write("\n" + "=" * 70 + "\n\n")

        # Isi tiap file
        for i, path in enumerate(file_list, 1):
            nama = os.path.basename(path)
            out.write("=" * 70 + "\n")
            out.write(f"  BAB {i} – {nama}\n")
            out.write("=" * 70 + "\n\n")

            try:
                with open(path, "r", encoding="utf-8") as f:
                    kode = f.read().strip()
            except UnicodeDecodeError:
                try:
                    with open(path, "r", encoding="latin-1") as f:
                        kode = f.read().strip()
                except Exception as e:
                    kode = f"# Gagal membaca file: {e}"
            except Exception as e:
                kode = f"# Gagal membaca file: {e}"

            out.write(kode if kode else "# (file kosong)")
            out.write("\n\n")

        # Footer
        out.write("=" * 70 + "\n")
        out.write("  AKHIR DOKUMENTASI\n")
        out.write("=" * 70 + "\n")

    ukuran_kb = os.path.getsize(output_path) / 1024
    print(f"\n✅  Selesai! {len(file_list)} file digabung.")
    print(f"📄  Hasil  : {output_path}")
    print(f"📦  Ukuran : {ukuran_kb:.1f} KB")


def tampilkan_menu(folders):
    print("\n" + "=" * 70)
    print("  GABUNG FILE .PY – PILIH FOLDER")
    print("=" * 70)
    if not folders:
        print("  ❌  Tidak ada sub-folder yang ditemukan di direktori ini.")
        return
    for i, (nama, path) in enumerate(folders, 1):
        # Hitung jumlah file .py di dalamnya sebagai info tambahan
        jumlah = len([f for f in os.listdir(path) if f.endswith(".py")])
        print(f"  [{i}]  {nama}  ({jumlah} file .py)")
    print("  [0]  Keluar")
    print("=" * 70)


def main():
    # Direktori tempat script ini berada
    base_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        folders = kumpulkan_folder(base_dir)
        tampilkan_menu(folders)

        if not folders:
            break

        try:
            pilihan = input("\nMasukkan nomor folder: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nProgram dihentikan.")
            break

        if pilihan == "0":
            print("\nKeluar. Sampai jumpa! 👋")
            break

        if not pilihan.isdigit() or not (1 <= int(pilihan) <= len(folders)):
            print(f"\n⚠️   Pilihan tidak valid. Masukkan angka 1–{len(folders)} atau 0 untuk keluar.")
            continue

        idx = int(pilihan) - 1
        nama_folder, folder_path = folders[idx]

        # Nama file output: dokumentasi_<nama folder>.txt
        nama_output = f"dokumentasi_{nama_folder.replace(' ', '_')}.txt"
        output_path = os.path.join(base_dir, nama_output)

        print(f"\n⏳  Menggabungkan file dari '{nama_folder}'...")
        buat_dokumentasi(nama_folder, folder_path, output_path)

        lagi = input("\nGabung folder lain? (y/n): ").strip().lower()
        if lagi != "y":
            print("\nSelesai. Sampai jumpa! 👋")
            break


if __name__ == "__main__":
    main()
