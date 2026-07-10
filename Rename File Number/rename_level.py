"""
rename_level.py
===============
Menambahkan angka nol (zero-padding) pada nomor level di nama file
agar urutan file rapi secara alfabetis di GitHub, Explorer, dll.

Contoh hasil:
  L1-Variable.py          → L001-Variable.py
  L9-Pengurangan.py       → L009-Pengurangan.py
  L10-Perkalian.py        → L010-Perkalian.py
  L21-For Loop Dasar.py   → L021-For Loop Dasar.py
  L100-Sesuatu.py         → L100-Sesuatu.py  (tidak berubah, sudah 3 digit)

Cara pakai:
  1. Letakkan script ini di LUAR folder-folder berisi file .py
  2. Jalankan: python rename_level.py
  3. Pilih folder, lalu pilih mode (preview dulu atau langsung rename)
"""

import os
import re


def kumpulkan_folder(base_dir):
    folders = []
    for item in sorted(os.listdir(base_dir)):
        path = os.path.join(base_dir, item)
        if os.path.isdir(path):
            folders.append((item, path))
    return folders


def buat_nama_baru(nama_file, lebar=3):
    """
    Cari pola L<angka> di awal nama file, lalu zero-pad angkanya.
    Mengembalikan (nama_baru, sudah_berubah).
    """
    pola = re.match(r'^(L)(\d+)(-.+)$', nama_file, re.IGNORECASE)
    if not pola:
        return nama_file, False

    prefix  = pola.group(1)          # "L"
    angka   = pola.group(2)          # "1", "10", "100"
    sisanya = pola.group(3)          # "-Variable.py"

    angka_baru = angka.zfill(lebar)  # zero-pad ke `lebar` digit
    if angka_baru == angka:
        return nama_file, False      # tidak perlu diubah

    return f"{prefix}{angka_baru}{sisanya}", True


def scan_folder(folder_path, lebar=3):
    """Scan folder dan kembalikan list (nama_lama, nama_baru) yang perlu diubah."""
    perubahan = []
    tidak_berubah = []

    for nama in sorted(os.listdir(folder_path)):
        path = os.path.join(folder_path, nama)
        if not os.path.isfile(path):
            continue
        if not nama.endswith(".py"):
            continue

        nama_baru, berubah = buat_nama_baru(nama, lebar)
        if berubah:
            perubahan.append((nama, nama_baru))
        else:
            tidak_berubah.append(nama)

    return perubahan, tidak_berubah


def tampilkan_preview(perubahan, tidak_berubah):
    print(f"\n{'─' * 60}")
    print(f"  PREVIEW PERUBAHAN  ({len(perubahan)} file akan direname)")
    print(f"{'─' * 60}")
    if perubahan:
        for lama, baru in perubahan:
            print(f"  {lama:<45} →  {baru}")
    else:
        print("  (tidak ada file yang perlu direname)")

    if tidak_berubah:
        print(f"\n  File yang TIDAK berubah ({len(tidak_berubah)}):")
        for nama in tidak_berubah:
            print(f"    • {nama}")
    print(f"{'─' * 60}")


def lakukan_rename(folder_path, perubahan):
    berhasil = 0
    gagal    = 0
    for lama, baru in perubahan:
        path_lama = os.path.join(folder_path, lama)
        path_baru = os.path.join(folder_path, baru)
        try:
            os.rename(path_lama, path_baru)
            print(f"  ✅  {lama}  →  {baru}")
            berhasil += 1
        except Exception as e:
            print(f"  ❌  Gagal rename '{lama}': {e}")
            gagal += 1
    print(f"\n  Selesai: {berhasil} berhasil, {gagal} gagal.")


def tanya_lebar():
    """Tanya pengguna berapa digit yang dipakai."""
    print("\n  Berapa digit nomor level yang dipakai?")
    print("  [1]  3 digit  → L001, L010, L100  (cocok sampai 999 file)")
    print("  [2]  4 digit  → L0001, L0010, L0100 (cocok sampai 9999 file)")
    pilihan = input("\n  Pilih (default 1): ").strip()
    return 4 if pilihan == "2" else 3


def tampilkan_menu(folders):
    print("\n" + "=" * 60)
    print("  RENAME ZERO-PADDING – PILIH FOLDER")
    print("=" * 60)
    if not folders:
        print("  ❌  Tidak ada sub-folder di direktori ini.")
        return
    for i, (nama, path) in enumerate(folders, 1):
        jumlah = len([f for f in os.listdir(path)
                      if f.endswith(".py") and os.path.isfile(os.path.join(path, f))])
        print(f"  [{i}]  {nama}  ({jumlah} file .py)")
    print("  [0]  Keluar")
    print("=" * 60)


def main():
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
            print(f"\n⚠️   Pilihan tidak valid. Masukkan angka 1–{len(folders)} atau 0.")
            continue

        idx = int(pilihan) - 1
        nama_folder, folder_path = folders[idx]

        lebar = tanya_lebar()

        perubahan, tidak_berubah = scan_folder(folder_path, lebar)
        tampilkan_preview(perubahan, tidak_berubah)

        if not perubahan:
            input("\n  Tekan Enter untuk kembali ke menu...")
            continue

        print("\n  Pilih aksi:")
        print("  [1]  Lakukan rename sekarang")
        print("  [2]  Batal, kembali ke menu")
        aksi = input("\n  Pilih: ").strip()

        if aksi == "1":
            print(f"\n⏳  Merename file di '{nama_folder}'...\n")
            lakukan_rename(folder_path, perubahan)
        else:
            print("\n  Dibatalkan.")

        lagi = input("\nProses folder lain? (y/n): ").strip().lower()
        if lagi != "y":
            print("\nSelesai. Sampai jumpa! 👋")
            break


if __name__ == "__main__":
    main()
