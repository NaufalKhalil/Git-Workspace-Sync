#!/usr/bin/env python3
"""
git_link.py — Git Repo Linker
================================
Hubungkan folder lokal ↔ repo GitHub dengan mudah.

Fitur:
  1. Clone repo GitHub ke folder lokal
  2. Init folder lokal → repo baru → push ke GitHub
  3. Hubungkan folder existing ke repo GitHub (set remote)
  4. Auto-detect status folder

Cara pakai:
  python git_link.py
  python git_link.py --path "D:/Project/MyApp"
  python git_link.py --clone https://github.com/user/repo.git
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


# ══════════════════════════════════════════
# WARNA
# ══════════════════════════════════════════
R="\033[91m"; G="\033[92m"; Y="\033[93m"
C="\033[96m"; B="\033[1m";  D="\033[2m"; X="\033[0m"
M="\033[95m"
def red(t):    return f"{R}{t}{X}"
def green(t):  return f"{G}{t}{X}"
def cyan(t):   return f"{C}{t}{X}"
def bold(t):   return f"{B}{t}{X}"
def dim(t):    return f"{D}{t}{X}"
def yellow(t): return f"{Y}{t}{X}"
def magenta(t):return f"{M}{t}{X}"


# ══════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════
def git(args, cwd=None):
    """Jalankan git command, return (ok, output)."""
    r = subprocess.run(
        ["git"] + args,
        cwd=str(cwd) if cwd else None,
        capture_output=True, text=True,
        encoding="utf-8", errors="replace"
    )
    out = (r.stdout + r.stderr).strip()
    return r.returncode == 0, out


def header(title):
    print(f"\n  {bold('═'*54)}")
    print(f"  {bold(title)}")
    print(f"  {bold('═'*54)}\n")


def ask(prompt, default=None):
    """Input dengan default value."""
    hint = f" {dim(f'(Enter = {default})')}" if default else ""
    val = input(f"  {prompt}{hint}\n  > ").strip()
    return val or default or ""


def confirm(prompt, default="y"):
    hint = "Y/n" if default == "y" else "y/N"
    ans = input(f"  {prompt} {dim(f'({hint})')}: ").strip().lower()
    if not ans:
        return default == "y"
    return ans == "y"


def separator():
    print(f"\n  {dim('─'*54)}\n")


# ══════════════════════════════════════════
# DETEKSI STATUS FOLDER
# ══════════════════════════════════════════
class FolderStatus:
    def __init__(self, path: Path):
        self.path = path
        self.exists       = path.exists()
        self.is_repo      = False
        self.has_remote   = False
        self.remote_url   = ""
        self.branch       = ""
        self.has_commits  = False
        self.dirty        = False

        if self.exists:
            ok, _ = git(["rev-parse", "--git-dir"], path)
            self.is_repo = ok

        if self.is_repo:
            ok, url = git(["remote", "get-url", "origin"], path)
            self.has_remote = ok
            self.remote_url = url if ok else ""

            ok, br = git(["branch", "--show-current"], path)
            self.branch = br.strip() if ok else "main"

            ok, _ = git(["log", "-1", "--oneline"], path)
            self.has_commits = ok

            ok, st = git(["status", "--short"], path)
            self.dirty = bool(st.strip())

    def describe(self):
        if not self.exists:
            return yellow("✦ Folder belum ada")
        if not self.is_repo:
            return yellow("✦ Folder ada, belum jadi git repo")
        if not self.has_commits:
            return cyan("◈ Repo baru (belum ada commit)")
        if not self.has_remote:
            return cyan("◈ Repo lokal, belum ada remote")
        label = green("✓ Repo terhubung")
        if self.dirty:
            label += yellow("  △ ada perubahan")
        return label


def print_status(path: Path):
    s = FolderStatus(path)
    print(f"  {bold('Folder')}  : {cyan(str(path))}")
    print(f"  {bold('Status')}  : {s.describe()}")
    if s.is_repo and s.has_remote:
        print(f"  {bold('Remote')}  : {dim(s.remote_url)}")
    if s.is_repo:
        print(f"  {bold('Branch')}  : {green(s.branch)}")
    print()
    return s


# ══════════════════════════════════════════
# FITUR 1 — CLONE
# ══════════════════════════════════════════
def do_clone(repo_url=None, target_path=None):
    header("🔽  Clone Repo GitHub → Folder Lokal")

    if not repo_url:
        print(f"  Masukkan URL repo GitHub:")
        print(f"  {dim('Contoh: https://github.com/user/repo.git')}")
        repo_url = ask("URL").strip()
        if not repo_url:
            print(red("  ✗ URL tidak boleh kosong."))
            return False

    # Tebak nama folder dari URL
    default_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    default_dest = str(Path.cwd() / default_name)

    if not target_path:
        target_path = ask("Folder tujuan", default_dest)

    dest = Path(target_path)

    if dest.exists() and any(dest.iterdir()):
        print(yellow(f"\n  ⚠ Folder '{dest.name}' sudah ada dan tidak kosong."))
        if not confirm("Lanjut clone ke sini?", "n"):
            print(dim("  Dibatalkan."))
            return False

    print(f"\n  {bold('Cloning...')}")
    print(f"  {dim(repo_url)} → {dim(str(dest))}\n")

    ok, out = git(["clone", repo_url, str(dest)])
    if not ok:
        print(red(f"\n  ✗ Clone gagal:\n  {out}"))
        return False

    print(green(f"\n  ✓ Clone berhasil!"))
    print(f"  Folder : {cyan(str(dest))}")

    s = FolderStatus(dest)
    print(f"  Branch : {green(s.branch)}")
    print(f"  Remote : {dim(s.remote_url)}")
    return True


# ══════════════════════════════════════════
# FITUR 2 — INIT + PUSH KE REPO BARU
# ══════════════════════════════════════════
def do_init_push(folder_path=None):
    header("🚀  Init Folder → Repo Baru di GitHub")

    if not folder_path:
        folder_path = ask("Path folder lokal", str(Path.cwd()))
    path = Path(folder_path).resolve()

    if not path.exists():
        print(yellow(f"\n  Folder '{path}' belum ada."))
        if confirm("Buat folder baru?"):
            path.mkdir(parents=True)
            print(green(f"  ✓ Folder dibuat: {path}"))
        else:
            print(dim("  Dibatalkan."))
            return False

    s = FolderStatus(path)
    print_status(path)

    # Sudah jadi repo?
    if not s.is_repo:
        print(f"  {bold('Inisialisasi git repo...')}")
        ok, out = git(["init"], path)
        if not ok:
            print(red(f"  ✗ git init gagal: {out}"))
            return False

        # Tanya branch default
        br = ask("Nama branch utama", "main")
        git(["checkout", "-b", br], path)
        print(green(f"  ✓ Repo diinisialisasi (branch: {br})"))
    else:
        br = s.branch
        print(green(f"  ✓ Sudah jadi repo (branch: {br})"))

    separator()

    # Tanya URL remote
    if s.has_remote:
        print(f"  Remote sudah ada: {dim(s.remote_url)}")
        if not confirm("Ganti remote URL?", "n"):
            remote_url = s.remote_url
        else:
            remote_url = ask("URL repo GitHub baru")
            git(["remote", "set-url", "origin", remote_url], path)
            print(green(f"  ✓ Remote diperbarui."))
    else:
        print(f"  Masukkan URL repo GitHub (harus sudah dibuat di github.com):")
        print(f"  {dim('Contoh: https://github.com/user/nama-repo.git')}")
        remote_url = ask("URL").strip()
        if not remote_url:
            print(red("  ✗ URL tidak boleh kosong."))
            return False
        ok, out = git(["remote", "add", "origin", remote_url], path)
        if not ok:
            print(red(f"  ✗ Gagal set remote: {out}"))
            return False
        print(green(f"  ✓ Remote ditambahkan."))

    separator()

    # Buat README jika folder kosong
    files = [f for f in path.iterdir() if f.name != ".git"]
    if not files:
        print(yellow("  ⚠ Folder kosong."))
        if confirm("Buat README.md otomatis?"):
            readme = path / "README.md"
            repo_name = remote_url.rstrip("/").split("/")[-1].replace(".git","")
            readme.write_text(f"# {repo_name}\n\nDibuat dengan git_link.py\n", encoding="utf-8")
            print(green("  ✓ README.md dibuat."))

    # git add + commit + push
    print(f"\n  {bold('Staging semua file...')}")
    git(["add", "."], path)

    ok, st = git(["status", "--short"], path)
    if not st.strip():
        print(yellow("  ⚠ Tidak ada file baru untuk di-commit."))
    else:
        commit_msg = ask("Commit message", "initial commit")
        ok, out = git(["commit", "-m", commit_msg], path)
        if not ok and "nothing to commit" not in out:
            print(red(f"  ✗ Commit gagal: {out}"))
            return False
        print(green(f'  ✓ Commit: "{commit_msg}"'))

    print(f"\n  {bold('Pushing ke remote...')}")
    ok, out = git(["push", "--set-upstream", "origin", br], path)
    if not ok:
        # Coba pull rebase dulu kalau rejected
        if "rejected" in out or "fetch first" in out or "non-fast-forward" in out:
            print(yellow("  ⚠ Remote punya konten. Pull dulu..."))
            ok2, out2 = git(["pull", "--rebase", "origin", br], path)
            if ok2:
                ok3, out3 = git(["push", "--set-upstream", "origin", br], path)
                if ok3:
                    print(green(f"  ✓ Push berhasil → origin/{br}"))
                    return True
            print(red(f"  ✗ Masih gagal: {out2}"))
        else:
            print(red(f"  ✗ Push gagal: {out}"))
        return False

    print(green(f"  ✓ Push berhasil → origin/{br}"))
    print(f"  Remote : {dim(remote_url)}")
    return True


# ══════════════════════════════════════════
# FITUR 3 — HUBUNGKAN FOLDER KE REPO EXISTING
# ══════════════════════════════════════════
def do_link(folder_path=None):
    header("🔗  Hubungkan Folder → Repo GitHub Existing")

    if not folder_path:
        folder_path = ask("Path folder lokal", str(Path.cwd()))
    path = Path(folder_path).resolve()

    if not path.exists():
        print(red(f"  ✗ Folder tidak ditemukan: {path}"))
        return False

    s = print_status(path)

    # Init jika belum jadi repo
    if not s.is_repo:
        if not confirm("Folder belum jadi repo. Init git sekarang?"):
            print(dim("  Dibatalkan."))
            return False
        br = ask("Nama branch", "main")
        git(["init"], path)
        git(["checkout", "-b", br], path)
        print(green(f"  ✓ Repo diinisialisasi."))
        s = FolderStatus(path)
    else:
        br = s.branch

    separator()

    # Set / ganti remote
    print(f"  Masukkan URL repo GitHub yang ingin dihubungkan:")
    print(f"  {dim('Contoh: https://github.com/user/repo.git')}")
    remote_url = ask("URL").strip()
    if not remote_url:
        print(red("  ✗ URL tidak boleh kosong."))
        return False

    if s.has_remote:
        print(yellow(f"  Remote lama: {dim(s.remote_url)}"))
        if confirm("Ganti dengan URL baru?"):
            ok, out = git(["remote", "set-url", "origin", remote_url], path)
        else:
            remote_url = s.remote_url
            print(dim("  Remote tidak diubah."))
            ok = True
    else:
        ok, out = git(["remote", "add", "origin", remote_url], path)

    if not ok:
        print(red(f"  ✗ Gagal set remote: {out}"))
        return False
    print(green(f"  ✓ Remote: {dim(remote_url)}"))

    separator()

    # Pilih aksi lanjutan
    print(f"  {bold('Apa yang ingin dilakukan selanjutnya?')}")
    print(f"  {dim('[1]')} Pull dari remote (ambil isi repo GitHub)")
    print(f"  {dim('[2]')} Push ke remote (kirim isi folder ke GitHub)")
    print(f"  {dim('[3]')} Hanya set remote, tidak ada aksi lain")
    choice = input("  > ").strip()

    if choice == "1":
        print(f"\n  {bold('Pulling...')}")
        ok, out = git(["pull", "origin", br, "--allow-unrelated-histories"], path)
        if ok:
            print(green(f"  ✓ Pull berhasil dari origin/{br}"))
        else:
            print(red(f"  ✗ Pull gagal: {out}"))
            return False

    elif choice == "2":
        print(f"\n  {bold('Staging dan push...')}")
        git(["add", "."], path)
        ok, st = git(["status", "--short"], path)
        if st.strip():
            msg = ask("Commit message", "link: connect folder to repo")
            ok, out = git(["commit", "-m", msg], path)
            if not ok and "nothing to commit" not in out:
                print(red(f"  ✗ Commit gagal: {out}"))
                return False
            print(green(f'  ✓ Commit: "{msg}"'))

        ok, out = git(["push", "--set-upstream", "origin", br], path)
        if not ok:
            if "rejected" in out or "fetch first" in out or "non-fast-forward" in out:
                print(yellow("  ⚠ Remote punya konten. Pull dulu..."))
                ok2, out2 = git(["pull", "--rebase", "--allow-unrelated-histories", "origin", br], path)
                if ok2:
                    ok3, out3 = git(["push", "--set-upstream", "origin", br], path)
                    if ok3:
                        print(green(f"  ✓ Push berhasil → origin/{br}"))
                        return True
                print(red(f"  ✗ Masih gagal: {out2}"))
                return False
            else:
                print(red(f"  ✗ Push gagal: {out}"))
                return False
        print(green(f"  ✓ Push berhasil → origin/{br}"))

    else:
        print(green("  ✓ Remote berhasil diset. Tidak ada aksi lain."))

    return True


# ══════════════════════════════════════════
# FITUR 4 — AUTO-DETECT & SCAN FOLDER
# ══════════════════════════════════════════
def do_scan(scan_path=None):
    header("🔍  Scan & Auto-Detect Status Folder")

    if not scan_path:
        scan_path = ask("Path folder yang ingin di-scan", str(Path.cwd()))
    root = Path(scan_path).resolve()

    if not root.exists():
        print(red(f"  ✗ Path tidak ditemukan: {root}"))
        return

    print(f"  Scanning: {dim(str(root))}\n")

    # Cek apakah root sendiri adalah repo
    items = []
    root_status = FolderStatus(root)
    if root_status.is_repo:
        items.append(root)
    else:
        # Scan subfolder
        try:
            for item in sorted(root.iterdir()):
                if item.is_dir() and not item.name.startswith("."):
                    items.append(item)
        except PermissionError:
            pass

    if not items:
        print(yellow("  Tidak ada folder ditemukan."))
        return

    # Tampilkan status tiap folder
    categories = {"repo_linked": [], "repo_no_remote": [], "not_repo": []}
    for p in items:
        s = FolderStatus(p)
        if s.is_repo and s.has_remote:
            categories["repo_linked"].append((p, s))
        elif s.is_repo:
            categories["repo_no_remote"].append((p, s))
        else:
            categories["not_repo"].append((p, s))

    if categories["repo_linked"]:
        n = len(categories["repo_linked"])
        print(f"  {green(bold(f'✓ Terhubung ke remote ({n}):'))}")
        for p, s in categories["repo_linked"]:
            dirty = yellow(" △") if s.dirty else ""
            print(f"    {green('•')} {cyan(p.name):<30} {dim(s.branch):<12} {dim(s.remote_url)}{dirty}")
        print()

    if categories["repo_no_remote"]:
        n = len(categories["repo_no_remote"])
        print(f"  {yellow(bold(f'◈ Repo lokal, belum ada remote ({n}):'))}")
        for p, s in categories["repo_no_remote"]:
            print(f"    {yellow('•')} {cyan(p.name):<30} {dim(s.branch)}")
        print()

    if categories["not_repo"]:
        n = len(categories["not_repo"])
        print(f"  {dim(bold(f'✦ Belum jadi repo ({n}):'))}")
        for p, s in categories["not_repo"]:
            print(f"    {dim('•')} {p.name}")
        print()

    # Tawarkan aksi untuk yang belum terhubung
    needs_action = categories["repo_no_remote"] + categories["not_repo"]
    if needs_action:
        separator()
        n = len(needs_action)
        print(f"  {bold(f'{n} folder belum terhubung ke GitHub.')}")
        if confirm("Proses sekarang satu per satu?"):
            for p, s in needs_action:
                print(f"\n  {bold('━'*50)}")
                print(f"  Folder: {cyan(p.name)}")
                if not s.is_repo:
                    print(f"  {dim('Belum jadi repo')}")
                else:
                    print(f"  {dim('Sudah repo, belum ada remote')}")
                if confirm(f"  Hubungkan '{p.name}' ke GitHub?"):
                    do_link(str(p))


# ══════════════════════════════════════════
# MENU UTAMA
# ══════════════════════════════════════════
def main_menu(default_path=None):
    while True:
        header("🔗  Git Repo Linker")

        if default_path:
            print(f"  {dim('Path aktif:')} {cyan(default_path)}\n")

        print(f"  {dim('[1]')}  {bold('Clone')}       — Unduh repo GitHub ke folder lokal")
        print(f"  {dim('[2]')}  {bold('Init & Push')} — Jadikan folder baru sebagai repo GitHub")
        print(f"  {dim('[3]')}  {bold('Link')}        — Hubungkan folder existing ke repo GitHub")
        print(f"  {dim('[4]')}  {bold('Scan')}        — Deteksi status semua folder di direktori")
        print(f"  {dim('[0]')}  {bold('Keluar')}")

        choice = input(f"\n  Pilih menu: ").strip()

        if choice == "1":
            do_clone(target_path=default_path)
        elif choice == "2":
            do_init_push(folder_path=default_path)
        elif choice == "3":
            do_link(folder_path=default_path)
        elif choice == "4":
            do_scan(scan_path=default_path)
        elif choice == "0":
            print(f"\n  {dim('Sampai jumpa!')}\n")
            break
        else:
            print(yellow("  Input tidak valid. Pilih 0-4."))

        input(f"\n  {dim('Tekan Enter untuk kembali ke menu...')}")


# ══════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="Git Repo Linker")
    parser.add_argument("--path",  "-p", default=None, help="Path folder target")
    parser.add_argument("--clone", "-c", default=None, help="Langsung clone dari URL")
    parser.add_argument("--init",  "-i", action="store_true", help="Langsung init & push")
    parser.add_argument("--link",  "-l", action="store_true", help="Langsung link folder")
    parser.add_argument("--scan",  "-s", action="store_true", help="Langsung scan folder")
    args = parser.parse_args()

    # Mode langsung (non-interaktif)
    if args.clone:
        do_clone(repo_url=args.clone, target_path=args.path)
    elif args.init:
        do_init_push(folder_path=args.path)
    elif args.link:
        do_link(folder_path=args.path)
    elif args.scan:
        do_scan(scan_path=args.path)
    else:
        main_menu(default_path=args.path)


if __name__ == "__main__":
    main()
