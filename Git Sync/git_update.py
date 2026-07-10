#!/usr/bin/env python3
"""
git_push.py — Multi Repo Auto Push
====================================
Taruh di folder INDUK yang berisi banyak repo git.

  📁 D:/Project/Coding/
      📁 Nausort Media/   (.git)
      📁 Naulex Translate/ (.git)
      git_push.py          ← di sini

Cara pakai:
  python git_push.py              # interaktif, pilih repo
  python git_push.py --all        # push semua repo sekaligus
"""

import os
import sys
import subprocess
import argparse
import fnmatch
from pathlib import Path
from datetime import datetime


# ══════════════════════════════════════════
# WARNA
# ══════════════════════════════════════════
R="\033[91m"; G="\033[92m"; Y="\033[93m"
C="\033[96m"; B="\033[1m";  D="\033[2m"; X="\033[0m"
def red(t):   return f"{R}{t}{X}"
def green(t): return f"{G}{t}{X}"
def cyan(t):  return f"{C}{t}{X}"
def bold(t):  return f"{B}{t}{X}"
def dim(t):   return f"{D}{t}{X}"
def yellow(t):return f"{Y}{t}{X}"


# ══════════════════════════════════════════
# GIT
# ══════════════════════════════════════════
def git(args, cwd):
    """Jalankan git command, return (ok, output)."""
    r = subprocess.run(
        ["git"] + args, cwd=str(cwd),
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    out = (r.stdout + r.stderr).strip()
    return r.returncode == 0, out


def is_repo(path):
    ok, _ = git(["rev-parse", "--git-dir"], path)
    return ok


def branch(repo):
    ok, out = git(["branch", "--show-current"], repo)
    return out.strip() or "main"


def remote(repo):
    ok, out = git(["remote", "get-url", "origin"], repo)
    return out.strip() if ok else "(no remote)"


def has_changes(repo):
    """True jika ada file yang berubah (tracked maupun untracked)."""
    ok, out = git(["status", "--short"], repo)
    return bool(out.strip())


def count_changes(repo):
    ok, out = git(["status", "--short"], repo)
    return len([l for l in out.strip().splitlines() if l.strip()])


def show_changes(repo, patterns=None):
    """Tampilkan daftar file berubah pakai git status --short.
    File yang cocok .pushignore ditandai 🔒 SKIP dan diberi warna dim."""
    patterns = patterns or []
    for code, name in changed_files(repo):
        icons = {"M":"~","A":"+","D":"-","R":"→","?":"*","U":"!"}
        icon = icons.get(code[0] if code else "?", "•")
        if is_ignored_file(name, patterns):
            print(f"      {dim('🔒 SKIP')} {dim(name)}")
            continue
        color = yellow if code.startswith("M") else (
                green  if code in ("A","??") else (
                red    if code.startswith("D") else cyan))
        print(f"      {color(icon)} {name}")


def has_upstream(repo, br):
    ok, _ = git(["rev-parse", "--abbrev-ref", f"{br}@{{upstream}}"], repo)
    return ok


def load_pushignore(repo):
    """Baca daftar pattern dari .pushignore di root repo (kalau ada)."""
    f = repo / ".pushignore"
    if not f.exists():
        return []
    patterns = []
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)
    return patterns


def is_ignored_file(path, patterns):
    """Cek apakah path (relatif ke repo) cocok salah satu pattern .pushignore."""
    path = path.strip().strip('"')
    base = os.path.basename(path)
    for pat in patterns:
        if fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(base, pat):
            return True
        # dukung pattern folder, misal "secrets/" atau "secrets"
        if pat.rstrip("/") and (path == pat.rstrip("/") or path.startswith(pat.rstrip("/") + "/")):
            return True
    return False


def changed_files(repo):
    ok, out = git(["status", "--porcelain=v1"], repo)
    result = []

    for line in out.splitlines():
        if len(line) < 4:
            continue

        code = line[:2]          # jangan di-strip dulu
        name = line[3:]          # nama selalu mulai index 3

        # rename
        if " -> " in name:
            name = name.split(" -> ", 1)[1]

        name = name.strip().strip('"')

        result.append((code.strip(), name))

    return result


def find_repos(start):
    repos = []
    for item in sorted(start.iterdir()):
        if item.is_dir() and (item / ".git").exists():
            repos.append(item)
    return repos


# ══════════════════════════════════════════
# PROSES SATU REPO
# ══════════════════════════════════════════
def push_repo(repo, commit_msg=None):
    br  = branch(repo)
    rem = remote(repo)

    print(f"\n  {'═'*50}")
    print(f"  {bold('📁 ' + repo.name)}")
    print(f"  {dim('branch')} {green(br)}  {dim('→')}  {dim(rem)}")
    print(f"  {'═'*50}")

    if not has_changes(repo):
        print(f"  {green('✓')} Tidak ada perubahan.")
        return True

    patterns = load_pushignore(repo)
    files = changed_files(repo)
    n = len(files)
    print(f"\n  {bold(f'{n} file berubah:')}\n")
    show_changes(repo, patterns)

    to_add    = [name for code, name in files if not is_ignored_file(name, patterns)]
    skipped   = [name for code, name in files if is_ignored_file(name, patterns)]

    if skipped:
        print(f"\n  {dim(f'🔒 {len(skipped)} file di-skip (.pushignore)')}")

    if not to_add:
        print(f"\n  {yellow('⚠ Semua file berubah masuk .pushignore, tidak ada yang di-push.')}")
        return True

    # stage SEMUA perubahan dulu (aman untuk file baru, terhapus, rename, dll)
    ok, out = git(["add", "-A"], repo)
    if not ok:
        print(red(f"\n  ✗ git add gagal: {out}"))
        return False

    # lalu unstage file yang cocok .pushignore
    for name in skipped:
        ok_u, out_u = git(["restore", "--staged", "--", name], repo)
        if not ok_u:
            # fallback untuk git versi lama yang belum punya `git restore`
            git(["reset", "HEAD", "--", name], repo)

    print(f"\n  {green('✓')} {len(to_add)} file di-stage.")

    # commit message
    if commit_msg:
        msg = commit_msg
    else:
        default = f"update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        print(f"\n  {bold('Commit message')} {dim(f'(Enter = {default})')}")
        msg = input("  > ").strip() or default

        print(f"  {bold('Description')} {dim('(Enter = kosong)')}")
        desc = input("  > ").strip()
        if desc:
            msg = f"{msg}\n\n{desc}"

    # git commit
    ok, out = git(["commit", "-m", msg], repo)
    if not ok:
        if "nothing to commit" in out:
            print(yellow("  ⚠ Sudah ter-commit sebelumnya."))
        else:
            print(red(f"  ✗ Commit gagal: {out}"))
            return False
    else:
        first_line = msg.splitlines()[0]
        print(green(f'  ✓ Commit: "{first_line}"'))

    # git pusha
    push_args = ["push"]
    if not has_upstream(repo, br):
        push_args += ["--set-upstream", "origin", br]

    ok, out = git(push_args, repo)
    if not ok:
        print(red(f"  ✗ Push gagal: {out}"))
        if "rejected" in out or "fetch first" in out:
            print(yellow("  💡 Ada perubahan di remote. Pull dulu?"))
            ans = input("  Pull sekarang? (y/N): ").strip().lower()
            if ans == "y":
                ok2, out2 = git(["pull", "--rebase", "origin", br], repo)
                if ok2:
                    ok3, out3 = git(push_args, repo)
                    if ok3:
                        print(green(f"  ✓ Push berhasil → origin/{br}"))
                        return True
                print(red(f"  ✗ Masih gagal: {out2}"))
        return False

    print(green(f"  ✓ Push berhasil → origin/{br}"))
    return True


# ══════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="Multi Repo Git Push")
    parser.add_argument("--path", "-p", default=None)
    parser.add_argument("--all",  "-a", action="store_true")
    parser.add_argument("--message", "-m", default=None)
    args = parser.parse_args()

    start = Path(args.path).resolve() if args.path else Path(__file__).parent.resolve()

    print(bold(f"\n{'═'*54}"))
    print(bold(f"  🚀 Git Push — Multi Repo"))
    print(bold(f"{'═'*54}"))
    print(f"  {dim(str(start))}\n")

    repos = find_repos(start)
    if not repos:
        print(red("  ✗ Tidak ada git repository ditemukan."))
        sys.exit(1)

    # Tampilkan semua repo + status
    for i, r in enumerate(repos, 1):
        n      = count_changes(r)
        br     = branch(r)
        status = yellow(f"△ {n} changes") if n else green("✓ clean")
        print(f"  {dim(f'[{i}]')} {cyan(r.name):<35} {dim(br):<15} {status}")

    # Pilih repo
    if not args.all:
        print(f"\n  {bold('Proses repo mana?')} {dim('(Enter = semua | nomor: 1,2,3)')}")
        choice = input("  > ").strip()
        if choice:
            try:
                indices = [int(x.strip())-1 for x in choice.split(",")]
                repos   = [repos[i] for i in indices if 0 <= i < len(repos)]
            except ValueError:
                print(red("  Input tidak valid."))
                sys.exit(1)

    # Push
    ok_count = fail_count = 0
    for repo in repos:
        ok = push_repo(repo, commit_msg=args.message)
        if ok: ok_count += 1
        else:  fail_count += 1

    # Ringkasan
    print(f"\n  {'═'*54}")
    print(bold("  Selesai!"))
    print(f"    {green(f'✓ Berhasil : {ok_count} repo')}")
    if fail_count:
        print(f"    {red(f'✗ Gagal    : {fail_count} repo')}")
    print(f"  {'═'*54}\n")


if __name__ == "__main__":
    main()