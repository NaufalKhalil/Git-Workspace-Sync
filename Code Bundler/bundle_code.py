"""
gabung_file.py
==============
Menggabungkan SEMUA file (kode maupun teks — .py, .js, .html, .json,
.md, .txt, dsb) dalam folder pilihan menjadi SATU file dokumentasi
Markdown (.md) yang terstruktur secara hierarkis — lebih hemat token
dan lebih mudah dipahami AI dibanding menggabung manual satu-satu.

File biner (gambar, video, audio, executable, arsip, dll) dan folder
"sampah" umum (.git, node_modules, __pycache__, venv, dist, build, dll)
otomatis DILEWATI, supaya hasil gabungan tetap bersih & bisa dibaca.

Menu hanya menampilkan folder yang SEJAJAR dengan script ini (top-level
saja, tidak menampilkan sub-folder di menu). Begitu satu folder dipilih,
SELURUH isinya — termasuk semua sub-folder & sub-sub-folder di dalamnya —
otomatis ikut digabung, tanpa perlu memilih satu per satu.

Cara pakai:
  1. Letakkan script ini di LUAR folder-folder yang berisi file kamu.
     Contoh struktur:
       📁 Proyek/
         📄 gabung_file.py      ← script ini
         📁 Backend/            ← akan tampil di menu
           📁 routes/           ← otomatis ikut kalau "Backend" dipilih
           📁 models/
         📁 Frontend/           ← akan tampil di menu
         📁 Dokumen/            ← akan tampil di menu

  2. Jalankan:  python gabung_file.py
  3. Pilih nomor folder yang ingin digabung.
  4. Semua file di folder itu (termasuk seluruh sub-folder di dalamnya,
     minus file biner & folder sampah) akan langsung digabung.
  5. File hasil .md akan muncul di samping script ini
"""

import os
import re
import datetime


# ---------------------------------------------------------------------------
# Konfigurasi: apa yang DILEWATI / bagaimana file ditampilkan
# ---------------------------------------------------------------------------

FOLDER_DIABAIKAN = {
    ".git", ".svn", ".hg",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "node_modules", "venv", ".venv", "env", ".env",
    "dist", "build", "target", "out",
    ".idea", ".vscode", ".vs",
    "egg-info",
}

EKSTENSI_BINER = {
    # gambar
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp", ".tiff",
    # video / audio
    ".mp4", ".mov", ".avi", ".mkv", ".mp3", ".wav", ".flac", ".ogg",
    # font
    ".ttf", ".otf", ".woff", ".woff2", ".eot",
    # arsip / paket
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".whl",
    # binary / executable / compiled
    ".exe", ".dll", ".so", ".dylib", ".bin", ".pyc", ".pyo", ".class",
    ".jar", ".o", ".a", ".lib",
    # data biner / database
    ".db", ".sqlite", ".sqlite3", ".pkl", ".pickle", ".pdf",
}

# Mapping ekstensi -> bahasa untuk code fence Markdown (biar syntax highlight rapi)
BAHASA_FENCE = {
    ".py": "python", ".js": "javascript", ".jsx": "jsx",
    ".ts": "typescript", ".tsx": "tsx", ".json": "json",
    ".html": "html", ".htm": "html", ".css": "css", ".scss": "scss",
    ".md": "markdown", ".sh": "bash", ".bash": "bash",
    ".yml": "yaml", ".yaml": "yaml", ".sql": "sql",
    ".java": "java", ".c": "c", ".h": "c", ".cpp": "cpp", ".hpp": "cpp",
    ".go": "go", ".rb": "ruby", ".php": "php", ".rs": "rust",
    ".xml": "xml", ".toml": "toml", ".ini": "ini", ".cfg": "ini",
    ".txt": "", ".env": "",
}


def kumpulkan_folder(base_dir):
    """
    Mengumpulkan folder yang SEJAJAR (langsung di dalam base_dir saja,
    tanpa masuk ke sub-folder). Dikembalikan sebagai list tuple:
      (nama, path_absolut)
    """
    try:
        entries = sorted(
            e for e in os.listdir(base_dir)
            if os.path.isdir(os.path.join(base_dir, e))
            and not e.startswith(".")
        )
    except PermissionError:
        return []

    return [(nama, os.path.join(base_dir, nama)) for nama in entries]


def is_file_biner(path):
    """
    Deteksi file biner: cek ekstensi dulu (cepat), kalau ekstensinya
    tidak dikenal, cek byte null di awal file (heuristik umum).
    """
    ext = os.path.splitext(path)[1].lower()
    if ext in EKSTENSI_BINER:
        return True
    try:
        with open(path, "rb") as f:
            chunk = f.read(2048)
        return b"\x00" in chunk
    except Exception:
        return True  # kalau gagal dibaca sama sekali, anggap tidak bisa disertakan


def kumpulkan_file_rekursif(folder):
    """
    Mengambil SEMUA file (bukan biner) di dalam 'folder', termasuk yang
    ada di sub-folder & sub-sub-folder (rekursif, berapa pun level).
    Folder tersembunyi & folder "sampah" umum dilewati.
    """
    hasil = []
    for root, dirs, files in os.walk(folder):
        dirs[:] = sorted(
            d for d in dirs
            if not d.startswith(".") and d not in FOLDER_DIABAIKAN
        )
        for f in sorted(files):
            if f.startswith("."):
                continue
            path = os.path.join(root, f)
            if not is_file_biner(path):
                hasil.append(path)
    return hasil


def hitung_rekursif(folder):
    return len(kumpulkan_file_rekursif(folder))


# ---------------------------------------------------------------------------
# Utilitas untuk membangun struktur pohon (tree) & Markdown
# ---------------------------------------------------------------------------

def bangun_tree(rel_paths):
    """Mengubah list path relatif (pakai '/') jadi struktur dict bertingkat."""
    tree = {}
    for rel in rel_paths:
        parts = rel.replace(os.sep, "/").split("/")
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node.setdefault("__files__", []).append(parts[-1])
    return tree


def render_tree(tree, prefix=""):
    """Merender dict tree jadi baris-baris ASCII tree (gaya perintah `tree`)."""
    lines = []
    folders = sorted(k for k in tree.keys() if k != "__files__")
    files = sorted(tree.get("__files__", []))
    entries = sorted(folders + files, key=str.lower)

    for i, nama in enumerate(entries):
        is_last = (i == len(entries) - 1)
        cabang = "└── " if is_last else "├── "
        if nama in folders:
            lines.append(f"{prefix}{cabang}{nama}/")
            ext = "    " if is_last else "│   "
            lines.extend(render_tree(tree[nama], prefix + ext))
        else:
            lines.append(f"{prefix}{cabang}{nama}")
    return lines


def slug(rel_path):
    """Slug sederhana gaya GitHub untuk anchor link Markdown."""
    s = rel_path.lower()
    s = re.sub(r"[^a-z0-9\-_ /]", "", s)
    s = s.replace("/", "-").replace(" ", "-").replace(".", "")
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def buat_dokumentasi(nama_folder, folder_path, output_path):
    """
    Mengambil SEMUA file (non-biner) di dalam folder_path (rekursif,
    termasuk seluruh sub-folder) lalu menulisnya sebagai satu Markdown
    terstruktur.
    """
    file_list = kumpulkan_file_rekursif(folder_path)

    if not file_list:
        print(f"\n❌  Tidak ada file yang bisa digabung dari folder '{nama_folder}'.")
        return

    rel_list = [os.path.relpath(p, folder_path).replace(os.sep, "/") for p in file_list]
    waktu_sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    jumlah_subfolder = len({os.path.dirname(r) for r in rel_list if os.path.dirname(r)})

    with open(output_path, "w", encoding="utf-8") as out:
        # Header + metadata ringkas (front-matter gaya YAML, hemat token, tetap terbaca AI)
        out.write(f"# {nama_folder}\n\n")
        out.write(f"- **Dibuat:** {waktu_sekarang}\n")
        out.write(f"- **Sumber:** `{folder_path}`\n")
        out.write(f"- **Total file:** {len(file_list)} ({jumlah_subfolder} sub-folder disertakan)\n\n")

        # Struktur folder sebagai tree ringkas — memberi AI peta hierarki
        # dalam beberapa baris saja, tanpa perlu membaca ulang tiap file.
        out.write("## Struktur\n\n```\n")
        out.write(f"{nama_folder}/\n")
        tree = bangun_tree(rel_list)
        out.write("\n".join(render_tree(tree)))
        out.write("\n```\n\n")

        # Daftar isi dengan anchor link ke tiap file
        out.write("## Daftar Isi\n\n")
        for rel in rel_list:
            out.write(f"- [{rel}](#{slug(rel)})\n")
        out.write("\n")

        # Isi tiap file — heading per file, code fence menyesuaikan bahasa
        out.write("## File\n\n")
        for rel, path in zip(rel_list, file_list):
            out.write(f"### `{rel}`\n\n")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    isi = f.read().strip()
            except UnicodeDecodeError:
                try:
                    with open(path, "r", encoding="latin-1") as f:
                        isi = f.read().strip()
                except Exception as e:
                    isi = f"# Gagal membaca file: {e}"
            except Exception as e:
                isi = f"# Gagal membaca file: {e}"

            ext = os.path.splitext(path)[1].lower()
            bahasa = BAHASA_FENCE.get(ext, ext.lstrip("."))
            out.write(f"```{bahasa}\n")
            out.write(isi if isi else "# (file kosong)")
            out.write("\n```\n\n")

    ukuran_kb = os.path.getsize(output_path) / 1024
    print(f"\n✅  Selesai! {len(file_list)} file digabung "
          f"({jumlah_subfolder} sub-folder disertakan).")
    print(f"📄  Hasil  : {output_path}")
    print(f"📦  Ukuran : {ukuran_kb:.1f} KB")


def tampilkan_menu(folders):
    print("\n" + "=" * 70)
    print("  GABUNG FILE – PILIH FOLDER")
    print("=" * 70)
    if not folders:
        print("  ❌  Tidak ada folder yang ditemukan di direktori ini.")
        return
    for i, (nama, path) in enumerate(folders, 1):
        total = hitung_rekursif(path)
        print(f"  [{i:>3}]  {nama}  ({total} file termasuk sub-folder)")
    print("  [  0]  Keluar")
    print("=" * 70)


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
            print(f"\n⚠️   Pilihan tidak valid. Masukkan angka 1–{len(folders)} atau 0 untuk keluar.")
            continue

        idx = int(pilihan) - 1
        nama_folder, folder_path = folders[idx]

        nama_output = f"dokumentasi_{nama_folder.replace(' ', '_')}.md"
        output_path = os.path.join(base_dir, nama_output)

        print(f"\n⏳  Menggabungkan seluruh isi folder '{nama_folder}' "
              f"(termasuk semua sub-folder)...")
        buat_dokumentasi(nama_folder, folder_path, output_path)

        lagi = input("\nGabung folder lain? (y/n): ").strip().lower()
        if lagi != "y":
            print("\nSelesai. Sampai jumpa! 👋")
            break


if __name__ == "__main__":
    main()
