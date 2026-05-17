# ⚡ Arth Python IDE

### *A Minimal Yet Powerful Python Coding Environment*

A sleek, modern, and lightweight **Python IDE** built using **Tkinter + ttkbootstrap**, designed to provide an efficient coding workflow with built-in execution, syntax highlighting, and package management.

---

## ✨ Features

* 🎨 Modern UI with **dark/light themes**
* 🧠 Real-time **syntax highlighting**
* 📁 Full file management (New, Open, Save, Save As)
* ▶️ Run Python code in external terminal
* 📦 Built-in **pip package manager**
* 💡 Hover-based **built-in function tooltips**
* ⌨️ Keyboard shortcuts for faster workflow
* 🖥️ Cross-platform support (Windows/Linux)
* ⚡ Lightweight & fast startup

---

## 🚀 Download & Run

### 🔽 Download Project

[![Download](https://img.shields.io/badge/Download-ZIP-blue?style=for-the-badge&logo=github)][(https://github.com/Arth-Joshi1001/PYTHON-IDLE/archive/refs/heads/main.zip)]
---

### ▶️ Run Locally

```bash
# Clone the repository
git clone https://github.com/your-username/arth-python-ide.git

# Navigate into the folder
cd arth-python-ide

# Install dependencies
pip install ttkbootstrap

# Run the IDE
python main.py
```

---
## 🛠️ Tech Stack
Python
Tkinter – GUI framework
ttkbootstrap – Modern themed UI
subprocess – Code execution & package handling
re (Regex) – Syntax highlighting engine
---


## 📂 Project Structure

```bash
📦 arth-python-ide
 ┣ 📄 main.py
 ┣ 🖼️ p.png
 ┣ 🎯 p.ico
 ┣ 📄 README.md
```

---

## 🧠 How It Works

- Code is written inside a custom Tkinter text editor  
- Regex-based engine dynamically highlights:
  - Keywords  
  - Strings  
  - Comments  
  - Built-in functions  
  - Numbers & operators  
- Python scripts are executed using `subprocess`  
- Package manager integrates `pip` directly into the IDE  
- Tooltips fetch documentation from Python built-ins dynamically  

---

## ⌨️ Shortcuts

| Shortcut        | Action        |
|----------------|--------------|
| Ctrl + N       | New File     |
| Ctrl + O       | Open File    |
| Ctrl + S       | Save File    |
| Ctrl + Shift+S | Save As      |
| Ctrl + R       | Run Code     |
| Ctrl + T       | Toggle Theme |

---

## ⚙️ Build Executable (.exe)

Convert into a standalone application using PyInstaller:

```bash
pyinstaller --onefile --windowed --icon=p.ico main.py
```

### Include assets

```bash
pyinstaller --onefile --windowed \
--add-data "p.png;." \
--add-data "p.ico;." \
main.py
```

---

## ⚠️ Notes

- Regex-based highlighting (not full parser)  
- External terminal is used for execution  
- Large files may impact performance  

---

## 🚧 Future Improvements

- 🔍 Autocomplete (Jedi integration)  
- 📑 Multi-tab support  
- 🐞 Debugger integration  
- 📊 Integrated output console  
- 🔎 Find & Replace  
- 🎯 Smarter syntax engine  

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
