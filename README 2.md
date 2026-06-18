<table>
  <tr>
    <!-- <td align="left">
      <img src="./assets/logo.png" width="120">
    </td> -->
    <td>
      <h1>Git Workspace Sync</h1>
      <p>
        A powerful Python toolkit for managing, linking, and synchronizing multiple Git and GitHub repositories from a single workspace.
      </p>
    </td>
  </tr>
</table>

[![Version](https://img.shields.io/badge/version-1.0-orange?style=flat-square)](../../releases/latest)
[![Platform](https://img.shields.io/badge/platform-Cross--Platform-blue?style=flat-square)](.)
[![Language](https://img.shields.io/badge/language-Python-yellow?style=flat-square)](https://python.org)
[![Status](https://img.shields.io/badge/status-Active-success?style=flat-square)](.)
[![License](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)](./LICENSE)

---

# 📖 Table of Contents

* [About](#about)
* [Features](#-features)
* [What's Included](#-whats-included)
* [Use Cases](#-use-cases)
* [Project Structure](#-project-structure)
* [Requirements](#-requirements)
* [Installation](#-installation)
* [Usage](#-usage)
* [Git Update](#-git-update)
* [Git Link](#-git-link)
* [Roadmap](#-roadmap)
* [Built With](#️-built-with)
* [Support](#-support)
* [Contact](#-contact)
* [License](#-license)

---

# About

**Git Workspace Sync** is a Python-based command-line toolkit designed to simplify Git and GitHub repository management across multiple projects.

Built for **students, freelancers, indie developers, and open-source contributors**, it automates repetitive Git tasks and helps manage repositories more efficiently from a single workspace.

No repetitive commands. No repository hopping. Just sync.

---

# ✨ Features

### 🚀 Multi Repository Push Manager

* Automatic Git repository detection
* Push multiple repositories simultaneously
* Automatic staging (`git add .`)
* Automatic commits
* Automatic GitHub push
* Preview changed files before commit
* Pull-rebase conflict handling
* Interactive CLI workflow

### 🔗 Git Repository Linker

* Clone GitHub repositories
* Initialize and push local folders
* Link existing folders to GitHub repositories
* Workspace-wide repository scanning
* Detect missing remotes
* Detect non-Git folders

---

# 📦 What's Included

### 🚀 Git Update

A repository synchronization tool for:

* Scanning workspaces
* Detecting Git repositories
* Committing changes
* Pushing repositories
* Managing multiple projects simultaneously

---

### 🔗 Git Link

A repository connection manager for:

* Cloning repositories
* Initializing repositories
* Linking existing folders
* Configuring remotes
* Repository discovery and auditing

---

# 🎯 Use Cases

## 🎓 Students

Manage:

* Coding assignments
* University projects
* Learning repositories
* Portfolio projects

---

## 💼 Freelancers

Handle:

* Client repositories
* Website projects
* Automation tools
* Internal utilities

---

## 🎮 Indie Developers

Maintain:

* Applications
* Games
* Websites
* Experiments
* Side projects

---

## 🌍 Open Source Contributors

Quickly synchronize:

* Forks
* Contributions
* Personal repositories
* Organization repositories

---

# 📂 Project Structure

```text
Git Workspace Sync/
│
├── git_update.py
├── git_link.py
└── README.md
```

### Components

| File            | Description                   |
| --------------- | ----------------------------- |
| `git_update.py` | Multi Repository Push Manager |
| `git_link.py`   | Git Repository Linker         |
| `README.md`     | Project Documentation         |

---

# ⚙️ Requirements

### Software

* Python 3.8+
* Git installed and available in PATH

Verify installation:

```bash
git --version
```

Example:

```bash
git version 2.50.0
```

---

# 📥 Installation

## Clone Repository

```bash
git clone https://github.com/USERNAME/Git-Workspace-Sync.git
cd Git-Workspace-Sync
```

---

## Or Download ZIP

1. Download repository ZIP
2. Extract files
3. Open terminal in project folder

---

# 🚀 Usage

## Run Git Update

```bash
python git_update.py
```

---

## Run Git Link

```bash
python git_link.py
```

---

# 🚀 Git Update

Git Update allows you to commit and push multiple repositories at once.

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

├── Project A/
│   └── .git
│
├── Project B/
│   └── .git
│
├── Project C/
│   └── .git
│
└── Git Workspace Sync/
```

Git Update automatically detects repositories inside the selected workspace.

---

# 🔗 Git Link

Git Link helps connect local folders and GitHub repositories without remembering complicated Git commands.

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

## Clone Repository

```bash
python git_link.py --clone https://github.com/user/repository.git
```

---

## Initialize & Push

```bash
python git_link.py --init
```

Turns a local folder into a Git repository and pushes it to GitHub.

---

## Link Existing Folder

```bash
python git_link.py --link
```

Connects an existing local project with a GitHub repository.

---

## Scan Workspace

```bash
python git_link.py --scan
```

Automatically detects:

* Connected repositories
* Repositories without remotes
* Non-Git folders

---

# 🆚 Comparison

| Feature                   | Git Workspace Sync | Manual Git Workflow |
| ------------------------- | ------------------ | ------------------- |
| Auto Repository Detection | ✅ Yes              | ❌ No                |
| Multi Repository Push     | ✅ Yes              | ❌ No                |
| Automatic Staging         | ✅ Yes              | ❌ No                |
| Automatic Commit          | ✅ Yes              | ❌ No                |
| Automatic Push            | ✅ Yes              | ❌ No                |
| Repository Scanning       | ✅ Yes              | ❌ No                |
| Clone Manager             | ✅ Yes              | ⚠️ Manual           |
| Link Existing Folder      | ✅ Yes              | ⚠️ Manual           |
| Workspace Management      | ✅ Yes              | ❌ No                |
| Interactive CLI           | ✅ Yes              | ❌ No                |

---

# 🖼️ Preview

### Git Update

```text
Detected Repositories:

[1] Portfolio Website
[2] Naulex Translate
[3] Nausort Media

Select repositories to push:
```

---

### Git Link

```text
[1] Clone
[2] Init & Push
[3] Link
[4] Scan
[0] Exit
```

---

# 🚧 Roadmap

### Planned Features

* [ ] Repository Synchronization
* [ ] GitHub API Integration
* [ ] Branch Manager
* [ ] Release Manager
* [ ] Multi-Remote Support
* [ ] Automatic Repository Backup
* [ ] GUI Version
* [ ] Cross-Platform Package Distribution

---

# ⚙️ Built With

* **Python** — Core application
* **Git CLI** — Repository management
* **GitHub** — Remote hosting
* **Command Line Interface** — User interaction
* **Workspace Scanner** — Repository discovery engine

---

# 👨‍💻 Developer

<div align="left">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/NaufalKhalil">
          <img src="https://github.com/NaufalKhalil.png" width="80" alt="Naufal Khalil"><br>
          <strong>Naufal Khalil</strong>
        </a><br>
        <sub>Creator & Developer</sub>
      </td>
    </tr>
  </table>
</div>

---

# 📧 Contact

For bug reports, suggestions, or feature requests:

* GitHub Issues
* Instagram: https://www.instagram.com/khalil.naufal_/

---

# 💬 Support

If Git Workspace Sync improves your workflow:

* ⭐ Star the repository
* 🍴 Fork the project
* 🐞 Report bugs
* 💡 Suggest new features

Your support helps the project grow and motivates future development.

---

# 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](./LICENSE) file for details.