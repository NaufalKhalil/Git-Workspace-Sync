# 🚀 Git Workspace Sync

> **One Workspace. Multiple Repositories. Zero Hassle.**

Git Workspace Sync adalah toolkit CLI berbasis Python yang membantu mengelola banyak repository Git dalam satu workspace dengan lebih cepat dan mudah.

Dirancang untuk developer, mahasiswa, freelancer, maupun tim kecil yang sering bekerja dengan banyak project sekaligus.

---

## ✨ Fitur Utama

### 🚀 Multi Repository Push
Kelola dan push banyak repository sekaligus.

- Deteksi semua repository dalam satu folder
- Pilih repository tertentu atau push semuanya
- Auto stage (`git add .`)
- Auto commit
- Auto push
- Menampilkan file yang berubah
- Menangani konflik push sederhana dengan pull-rebase otomatis

---

### 🔗 Git Repository Linker

Hubungkan folder lokal dengan GitHub tanpa harus menghafal banyak command Git.

#### 📥 Clone Repository
Unduh repository GitHub ke folder lokal.

#### 📤 Init & Push
Ubah folder biasa menjadi repository Git lalu push ke GitHub.

#### 🔄 Link Existing Folder
Hubungkan folder yang sudah ada ke repository GitHub.

#### 🔍 Auto Scan
Mendeteksi status seluruh folder dalam workspace:

- Sudah terhubung ke GitHub
- Repository lokal tanpa remote
- Folder yang belum menjadi repository

---

## 📦 Struktur Project

```text
Git Workspace Sync/
│
├── git_update.py   # Multi Repo Push Manager
├── git_link.py     # Git Repo Linker
└── README.md
```

---

## ⚙️ Requirements

- Python 3.8+
- Git terinstall dan tersedia di PATH

Cek instalasi Git:

```bash
git --version
```

---

## 🚀 Instalasi

Clone repository:

```bash
git clone https://github.com/USERNAME/Git-Workspace-Sync.git
cd Git-Workspace-Sync
```

Atau download ZIP dan ekstrak.

---

# 📤 Git Update

Tool untuk commit dan push banyak repository sekaligus.

## Menjalankan

```bash
python git_update.py
```

---

### Push Semua Repository

```bash
python git_update.py --all
```

atau

```bash
python git_update.py -a
```

---

### Commit Message Otomatis

```bash
python git_update.py --all -m "Update project"
```

---

### Folder Workspace Custom

```bash
python git_update.py -p "D:/Projects"
```

---

## Contoh Workspace

```text
D:/Projects/

├── Nausort Media/
│   └── .git
│
├── Naulex Translate/
│   └── .git
│
├── Website Portfolio/
│   └── .git
│
└── git_update.py
```

Tool akan mendeteksi semua repository secara otomatis.

---

# 🔗 Git Link

Tool interaktif untuk menghubungkan folder dan GitHub.

## Menjalankan

```bash
python git_link.py
```

---

## Menu

```text
[1] Clone
[2] Init & Push
[3] Link
[4] Scan
[0] Exit
```

---

## Clone Repository

```bash
python git_link.py --clone https://github.com/user/repo.git
```

---

## Init Folder Menjadi Repository

```bash
python git_link.py --init
```

---

## Hubungkan Folder ke Repository Existing

```bash
python git_link.py --link
```

---

## Scan Workspace

```bash
python git_link.py --scan
```

---

# 💡 Use Cases

### Mahasiswa

Mengelola tugas coding dari berbagai mata kuliah.

### Freelancer

Mengelola banyak project client sekaligus.

### Indie Developer

Mengelola aplikasi, website, dan tools pribadi dalam satu workspace.

### Open Source Contributor

Memudahkan sinkronisasi banyak repository GitHub.

---

# 🛠️ Dibangun Dengan

- Python
- Git CLI
- GitHub

---

# 📈 Roadmap

- [ ] Repository synchronization
- [ ] GitHub API integration
- [ ] Release creator
- [ ] Branch manager
- [ ] Multi-remote support
- [ ] Auto backup repository
- [ ] GUI Version
- [ ] Cross-platform package

---

# 🤝 Contributing

Pull Request dan Issue sangat diterima.

Jika menemukan bug atau memiliki ide fitur baru, silakan buat Issue.

---

# 📄 License

MIT License

---

## ⭐ Support

Jika project ini membantu workflow Git Anda, jangan lupa berikan ⭐ pada repository ini.