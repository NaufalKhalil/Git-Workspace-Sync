#!/usr/bin/env python3
"""
hitung_file.py

Program untuk menghitung jumlah file dan total ukuran per jenis ekstensi
di dalam sebuah folder (termasuk semua subfolder di dalamnya).

Cara pakai paling gampang (mode pilih folder):
    Taruh file ini sejajar dengan folder-folder yang mau dicek, lalu:
    python hitung_file.py

    Nanti akan muncul daftar folder bernomor, tinggal ketik nomornya.

Cara pakai lama (langsung kasih path, masih bisa dipakai):
    python hitung_file.py "D:\Path\Ke\Folder"
    python hitung_file.py "D:\Path\Ke\Folder" --no-subfolder
"""

import os
import sys
import argparse
from collections import defaultdict


def pilih_folder_interaktif(base_path: str) -> str:
    """
    Tampilkan daftar folder yang sejajar dengan script ini (di base_path),
    lalu minta user memilih salah satu dengan mengetik nomornya.
    Mengembalikan path folder yang dipilih.
    """
    subfolder = sorted(
        f for f in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, f))
    )

    if not subfolder:
        print(f"Tidak ada folder yang ditemukan di: {base_path}")
        sys.exit(1)

    print(f"\nFolder yang ditemukan di: {base_path}\n")
    for i, nama in enumerate(subfolder, start=1):
        print(f"  {i}. {nama}")
    print(f"  0. (Ketik path manual)")

    while True:
        pilihan = input("\nPilih nomor folder yang mau dihitung: ").strip()

        if pilihan == "0":
            path_manual = input("Ketik/paste path folder: ").strip().strip('"')
            if os.path.isdir(path_manual):
                return path_manual
            print("Path tidak valid, coba lagi.")
            continue

        if pilihan.isdigit() and 1 <= int(pilihan) <= len(subfolder):
            return os.path.join(base_path, subfolder[int(pilihan) - 1])

        print("Input tidak valid, ketik nomor yang ada di daftar.")


def format_ukuran(byte_size: float) -> str:
    """Ubah ukuran byte jadi format yang mudah dibaca (KB, MB, GB, TB)."""
    for satuan in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if byte_size < 1024:
            return f"{byte_size:.2f} {satuan}"
        byte_size /= 1024
    return f"{byte_size:.2f} EB"


def scan_folder(path: str, rekursif: bool = True):
    """
    Scan folder dan kembalikan dict:
    { ".ekstensi": {"jumlah": int, "total_byte": int} }
    """
    hasil = defaultdict(lambda: {"jumlah": 0, "total_byte": 0})

    if rekursif:
        walker = os.walk(path)
    else:
        # Hanya scan folder ini saja, tanpa masuk ke subfolder
        walker = [(path, [], [f for f in os.listdir(path)
                             if os.path.isfile(os.path.join(path, f))])]

    for root, _dirs, files in walker:
        for nama_file in files:
            full_path = os.path.join(root, nama_file)
            try:
                ukuran = os.path.getsize(full_path)
            except (OSError, FileNotFoundError):
                # Lewati file yang tidak bisa diakses (misal permission error)
                continue

            _, ext = os.path.splitext(nama_file)
            ext = ext.lower() if ext else "(tanpa ekstensi)"

            hasil[ext]["jumlah"] += 1
            hasil[ext]["total_byte"] += ukuran

    return hasil


def tampilkan_hasil(hasil: dict, path: str):
    if not hasil:
        print(f"Folder '{path}' kosong atau tidak ada file yang bisa dibaca.")
        return

    # Urutkan berdasarkan total ukuran, dari yang terbesar
    urutan = sorted(hasil.items(), key=lambda x: x[1]["total_byte"], reverse=True)

    total_file = sum(v["jumlah"] for v in hasil.values())
    total_byte = sum(v["total_byte"] for v in hasil.values())

    print(f"\nHasil scan folder: {path}\n")
    print(f"{'Ekstensi':<18}{'Jumlah File':<15}{'Total Ukuran':<15}")
    print("-" * 48)
    for ext, info in urutan:
        print(f"{ext:<18}{info['jumlah']:<15}{format_ukuran(info['total_byte']):<15}")
    print("-" * 48)
    print(f"{'TOTAL':<18}{total_file:<15}{format_ukuran(total_byte):<15}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Hitung jumlah file dan ukuran per ekstensi dalam sebuah folder."
    )
    parser.add_argument(
        "folder", nargs="?", default=None,
        help="Path folder yang ingin di-scan (kosongkan untuk mode pilih folder bernomor)",
    )
    parser.add_argument(
        "--no-subfolder",
        action="store_true",
        help="Jika diaktifkan, hanya scan folder ini saja (tidak masuk ke subfolder)",
    )

    args = parser.parse_args()

    if args.folder:
        # Mode lama: path dikasih langsung lewat argumen
        target_folder = args.folder
        if not os.path.isdir(target_folder):
            print(f"Error: folder '{target_folder}' tidak ditemukan.")
            sys.exit(1)
    else:
        # Mode baru: pilih folder bernomor, folder yang di-scan adalah
        # folder tempat script ini berada
        base_path = os.path.dirname(os.path.abspath(__file__))
        target_folder = pilih_folder_interaktif(base_path)

    hasil = scan_folder(target_folder, rekursif=not args.no_subfolder)
    tampilkan_hasil(hasil, target_folder)

    input("\nTekan ENTER untuk keluar...")


if __name__ == "__main__":
    main()
