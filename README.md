# 🚀 Git Workspace Sync

> **One Workspace. Multiple Repositories. Zero Hassle.**

Git Workspace Sync is a Python-based CLI toolkit designed to simplify Git and GitHub repository management across multiple projects.

Whether you're a student, freelancer, indie developer, or open-source contributor, Git Workspace Sync helps you automate repetitive Git tasks and manage repositories more efficiently.

---

# ✨ Features

## 🚀 Multi Repository Push Manager

Manage and synchronize multiple Git repositories from a single workspace.

### Features

- Automatically detect Git repositories
- Push one or multiple repositories at once
- Automatic staging (`git add .`)
- Automatic commits
- Automatic push to GitHub
- View changed files before committing
- Basic push conflict handling with pull-rebase support
- Interactive terminal interface

---

## 🔗 Git Repository Linker

Connect local folders and GitHub repositories without memorizing complex Git commands.

### 📥 Clone Repository

Clone GitHub repositories directly into local folders.

### 📤 Init & Push

Turn any local folder into a Git repository and push it to GitHub.

### 🔄 Link Existing Folder

Connect an existing project folder to a GitHub repository.

### 🔍 Auto Scan

Scan an entire workspace and automatically detect:

- Connected GitHub repositories
- Local repositories without remotes
- Folders that are not Git repositories

---

# 📦 Project Structure

```text
Git Workspace Sync/
│
├── git_update.py   # Multi Repository Push Manager
├── git_link.py     # Git Repository Linker
└── README.md
```

---

# ⚙️ Requirements

- Python 3.8+
- Git installed and available in PATH

Verify Git installation:

```bash
git --version
```

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/USERNAME/Git-Workspace-Sync.git
cd Git-Workspace-Sync
```

Or download the ZIP file and extract it.

---

# 🚀 Git Update

A tool for committing and pushing multiple repositories at once.

## Run

```bash
python git_update.py
```

---

## Push All Repositories

```bash
python git_update.py --all
```

or

```bash
python git_update.py -a
```

---

## Custom Commit Message

```bash
python git_update.py --all -m "Update project"
```

---

## Custom Workspace Path

```bash
python git_update.py -p "D:/Projects"
```

---

## Example Workspace

```text
D:/Projects/

├── Nausort Media/
│   └── .git
│
├── Naulex Translate/
│   └── .git
│
├── Portfolio Website/
│   └── .git
│
└── git_update.py
```

Git Workspace Sync will automatically detect all repositories inside the workspace.

---

# 🔗 Git Link

An interactive tool for connecting local folders with GitHub repositories.

## Run

```bash
python git_link.py
```

---

## Main Menu

```text
[1] Clone
[2] Init & Push
[3] Link
[4] Scan
[0] Exit
```

---

## Clone a Repository

```bash
python git_link.py --clone https://github.com/user/repository.git
```

---

## Initialize a Folder as a Repository

```bash
python git_link.py --init
```

---

## Connect a Folder to an Existing Repository

```bash
python git_link.py --link
```

---

## Scan a Workspace

```bash
python git_link.py --scan
```

---

# 💡 Use Cases

## 🎓 Students

Manage coding assignments and personal projects across multiple repositories.

## 💼 Freelancers

Handle client projects more efficiently from a single workspace.

## 🎮 Indie Developers

Manage applications, websites, tools, and experiments in one place.

## 🌍 Open Source Contributors

Quickly synchronize and maintain multiple GitHub repositories.

---

# 🛠 Built With

- Python
- Git CLI
- GitHub

---

# 📈 Roadmap

- [ ] Repository synchronization
- [ ] GitHub API integration
- [ ] Release manager
- [ ] Branch manager
- [ ] Multi-remote support
- [ ] Automatic repository backup
- [ ] GUI version
- [ ] Cross-platform package

---

# 🤝 Contributing

Contributions, issues, and feature requests are welcome.

Feel free to open an issue or submit a pull request.

---

# 📄 License

MIT License

---

# ⭐ Support

If Git Workspace Sync improves your workflow, consider giving the repository a ⭐ on GitHub.

It helps the project grow and motivates future development.