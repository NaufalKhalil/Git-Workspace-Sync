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


def show_changes(repo):
    """Tampilkan daftar file berubah pakai git status --short."""
    ok, out = git(["status", "--short"], repo)
    if not out.strip():
        return
    for line in out.strip().splitlines():
        if len(line) >= 3:
            code = line[:2].strip()
            name = line[3:] if len(line) > 3 else line[2:]
            icons = {"M":"~","A":"+","D":"-","R":"→","?":"*","U":"!"}
            icon = icons.get(code[0] if code else "?", "•")
            color = yellow if code.startswith("M") else (
                    green  if code in ("A","??") else (
                    red    if code.startswith("D") else cyan))
            print(f"      {color(icon)} {name.strip()}")


def has_upstream(repo, br):
    ok, _ = git(["rev-parse", "--abbrev-ref", f"{br}@{{upstream}}"], repo)
    return ok


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

    n = count_changes(repo)
    print(f"\n  {bold(f'{n} file berubah:')}\n")
    show_changes(repo)

    # git add .
    ok, out = git(["add", "."], repo)
    if not ok:
        print(red(f"\n  ✗ git add gagal: {out}"))
        return False
    print(f"\n  {green('✓')} Semua file di-stage.")

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

    # git push
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
