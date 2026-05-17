import tkinter as tk
import ttkbootstrap as tb
from tkinter import filedialog
from ttkbootstrap.dialogs import Messagebox, Querybox
import subprocess
import tempfile
import builtins
import os
import re
import sys


# main
m = tb.Window(themename="superhero")
style = tb.Style()

m.title("Arth Python Idle")
m.geometry("1000x700")
m.minsize(900, 650)

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller onefile bundles."""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

try:
    icon_file = resource_path("p.ico")
    m.iconbitmap(icon_file)
except Exception:
    pass  # Icon file not found or failed to load, continue without it

logo_image = None
try:
    logo_image = tk.PhotoImage(file=resource_path("p.png"))
except Exception:
    logo_image = None

editor_frame = tb.Frame(m, bootstyle="secondary", padding=10)
# We will pack editor_frame later so toolbar sits on top

scrollbar = tb.Scrollbar(editor_frame, bootstyle="round")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))

te = tk.Text(editor_frame, bg="#020814", fg="#ffffff", insertbackground="#ffffff", font=("Cascadia Code", 12), undo=True, relief=tk.FLAT, bd=0, yscrollcommand=scrollbar.set)
te.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=te.yview)

# tags
te.tag_configure("keyword", foreground="#ff79c6")
te.tag_configure("string", foreground="#f1fa8c")
te.tag_configure("comment", foreground="#6272a4")
te.tag_configure("builtin", foreground="#8be9fd")
te.tag_configure("number", foreground="#bd93f9")
te.tag_configure("operator", foreground="#50fa7b")
te.tag_configure("function", foreground="#ffb86c")

THEMES = {
    "dark": {
        "bg": "#020814",
        "fg": "#ffffff",
        "insert": "#ffffff",
        "menu_bg": "#282a36",
        "menu_fg": "#f8f8f2",
        "result_bg": "#020814",
        "result_fg": "#ffffff",
        "keyword": "#ff79c6",
        "string": "#f1fa8c",
        "comment": "#6272a4",
        "builtin": "#8be9fd",
        "number": "#bd93f9",
        "operator": "#50fa7b",
        "function": "#ffb86c"
    },
    "light": {
        "bg": "#ffffff",
        "fg": "#000000",
        "insert": "#000000",
        "menu_bg": "#e0e0e0",
        "menu_fg": "#000000",
        "result_bg": "#f5f5f5",
        "result_fg": "#000000",
        "keyword": "#0000ff",
        "string": "#a31515",
        "comment": "#008000",
        "builtin": "#795e26",
        "number": "#098658",
        "operator": "#000000",
        "function": "#795e26"
    }
}

current_theme = "dark"

# result

## buttons interactive


# unused tool label removed

#file
cfile = None
# built-in functions
BUILTINS = dir(builtins)
keywords = {
    'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
    'def', 'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
    'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None',
    'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True', 'try',
    'while', 'with', 'yield'
}

def new_file():
    global cfile
    cfile = None
    te.delete(1.0, tk.END)
    m.title("Arth Python Idle - New File")
    statusbar.config(text="New file created")

def open_file():
    global cfile
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        cfile = file_path
        with open(cfile, "r") as f:
            code = f.read()
            te.delete(1.0, tk.END)
            te.insert(tk.END, code)
        m.title(f"Arth Python Idle - {os.path.basename(cfile)}")
        statusbar.config(text=f"Opened {os.path.basename(cfile)}")

def save_file():
    global cfile
    if cfile:
        with open(cfile, "w") as f:
            f.write(te.get(1.0, tk.END))
        m.title(f"Arth Python Idle - {os.path.basename(cfile)}")
        statusbar.config(text=f"Saved {os.path.basename(cfile)}")
    else:
        save_as_file()

def save_as_file():
    global cfile
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    if file_path:
        cfile = file_path
        with open(cfile, "w") as f:
            f.write(te.get(1.0, tk.END))
        m.title(f"Arth Python Idle - {os.path.basename(cfile)}")
        statusbar.config(text=f"Saved {os.path.basename(cfile)}")

def apply_theme(theme_name):
    global current_theme
    current_theme = theme_name
    theme = THEMES[theme_name]

    if theme_name == "dark":
        style.theme_use("darkly")
    else:
        style.theme_use("litera")

    # Editor
    te.configure(
        bg=theme["bg"],
        fg=theme["fg"],
        insertbackground=theme["insert"]
    )

    te.tag_configure("keyword", foreground=theme["keyword"])
    te.tag_configure("string", foreground=theme["string"])
    te.tag_configure("comment", foreground=theme["comment"])
    te.tag_configure("builtin", foreground=theme["builtin"])
    te.tag_configure("number", foreground=theme["number"])
    te.tag_configure("operator", foreground=theme["operator"])
    te.tag_configure("function", foreground=theme["function"])

    # Menu colors
    menu.configure(bg=theme["menu_bg"], fg=theme["menu_fg"])

def toggle_theme():
    if current_theme == "dark":
        apply_theme("light")
    else:
        apply_theme("dark")
# syntax

def syntax(event=None):
    code = te.get(1.0, tk.END)
    te.tag_remove("keyword", "1.0", tk.END)
    te.tag_remove("string", "1.0", tk.END)
    te.tag_remove("comment", "1.0", tk.END)
    te.tag_remove("builtin", "1.0", tk.END)
    te.tag_remove("number", "1.0", tk.END)
    te.tag_remove("operator", "1.0", tk.END)
    te.tag_remove("function", "1.0", tk.END)

    for match in re.finditer(r'\b(' + '|'.join(keywords) + r')\b', code):
        start = f"1.0+{match.start()}c"
        end = f"1.0+{match.end()}c"
        te.tag_add("keyword", start, end)

    for match in re.finditer(r'(\".*?\"|\'.*?\')', code):
        start = f"1.0+{match.start()}c"
        end = f"1.0+{match.end()}c"
        te.tag_add("string", start, end)

    for match in re.finditer(r'#.*', code):
        start = f"1.0+{match.start()}c"
        end = f"1.0+{match.end()}c"
        te.tag_add("comment", start, end)

    for match in re.finditer(r'\b(' + '|'.join(BUILTINS) + r')\b', code):
        start = f"1.0+{match.start()}c"
        end = f"1.0+{match.end()}c"
        te.tag_add("builtin", start, end)

    for match in re.finditer(r'\b\d+\b', code):
        start = f"1.0+{match.start()}c"
        end = f"1.0+{match.end()}c"
        te.tag_add("number", start, end)

    for match in re.finditer(r'[+\-*/%=<>!]+', code):
        start = f"1.0+{match.start()}c"
        end = f"1.0+{match.end()}c"
        te.tag_add("operator", start, end)

    for match in re.finditer(r'\bdef\s+(\w+)\b', code):
        start = f"1.0+{match.start(1)}c"
        end = f"1.0+{match.end(1)}c"
        te.tag_add("function", start, end)
te.bind("<KeyRelease>", syntax)

# hover
ht = None
def show_tooltip(event):
    global ht
    if ht:
        ht.destroy()
    try:
        word = te.get(f"@{event.x},{event.y} wordstart", f"@{event.x},{event.y} wordend")
        if word in BUILTINS:
            doc = getattr(builtins, word).__doc__
            if doc:
                doc = doc[:300] + "..." if len(doc) > 300 else doc
                ht = tb.Toplevel(m)
                ht.wm_overrideredirect(True)
                tooltip_label = tb.Label(ht, text=f"📚 {word}\n{doc}", font=("Consolas", 10), justify=tk.LEFT, wraplength=400, bootstyle="inverse-secondary")
                tooltip_label.pack(padx=8, pady=8)
                ht.geometry(f"+{event.x_root + 15}+{event.y_root + 15}")
    except tk.TclError:
        pass
def hide_tooltip(event):
    global ht
    if ht:
        ht.destroy()
        ht = None

te.bind("<Motion>", show_tooltip)
te.bind("<Leave>", hide_tooltip)


#run


def run_code():
    code = te.get(1.0, tk.END)

    if cfile:
        script_path = cfile
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as tmp:
            tmp.write(code)
            script_path = tmp.name

    if getattr(sys, 'frozen', False):
        python_executable = 'python'
    else:
        python_executable = sys.executable
        if os.path.basename(python_executable).lower() == "pythonw.exe":
            python_executable = os.path.join(os.path.dirname(python_executable), "python.exe")

    try:
        if os.name == "nt":  # Windows
            cmd_str = f'cmd.exe /k ""{python_executable}" "{script_path}""'
            subprocess.Popen(cmd_str, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:  # Linux / Mac
            subprocess.Popen(
                ["x-terminal-emulator", "-e", python_executable, script_path]
            )
        statusbar.config(text="Script launched")
    except Exception as e:
        statusbar.config(text="Failed to launch script")
        print("Error:", e)
# menubar
menu = tk.Menu(m , bg="#282a36", fg="#f8f8f2", font=("Consolas", 10))
m.config(menu=menu)
file_menu = tk.Menu(menu, tearoff=0, bg="#282a36", fg="#f8f8f2", font=("Consolas", 10))
menu.add_cascade(label="📁 File", menu=file_menu)

file_menu.add_command(label="✨ New", command=new_file)
file_menu.add_command(label="📂 Open", command=open_file)
file_menu.add_command(label="💾 Save", command=save_file)
file_menu.add_command(label="💾 Save As", command=save_as_file)
run_menu = tk.Menu(menu, tearoff=0, bg="#282a36", fg="#f8f8f2", font=("Consolas", 10))
menu.add_cascade(label="▶️ Run", menu=run_menu)
run_menu.add_command(label="▶️ Run Code", command=run_code)

#package manager

def install_package():
    package_name = Querybox.get_string("Enter package name:", "Install Package")
    if package_name:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            Messagebox.show_info(f"Package '{package_name}' installed successfully.", "Success")
        except subprocess.CalledProcessError as e:
            Messagebox.show_error(f"Failed to install package '{package_name}'.\n{e}", "Error")

def show_installed_packages():
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
        output = result.stdout
        Messagebox.show_info(output, "Installed Packages")
    except Exception as e:
        Messagebox.show_error(str(e), "Error")

package_menu = tk.Menu(menu, tearoff=0, bg="#282a36", fg="#f8f8f2", font=("Consolas", 10))
package_menu.add_command(label="⬇️ Install Package", command=install_package)
package_menu.add_command(label="📦 Show Installed Packages", command=show_installed_packages)
menu.add_cascade(label="📦 Packages", menu=package_menu)
view_menu = tk.Menu(menu, tearoff=0, bg="#282a36", fg="#f8f8f2", font=("Consolas", 10))
menu.add_cascade(label="👁️ View", menu=view_menu)

view_menu.add_command(label="🎨 Toggle Theme", command=toggle_theme)

toolbar = tb.Frame(m, bootstyle="light")

button_specs = [
    ("✨ New", new_file, "primary"),
    ("📂 Open", open_file, "secondary"),
    ("💾 Save", save_file, "success"),
    ("▶️ Run", run_code, "info"),
    ("🎨 Theme", toggle_theme, "warning")
]
for text, command, style_name in button_specs:
    tb.Button(toolbar, text=text, command=command, bootstyle=f"{style_name}").pack(side=tk.LEFT, padx=(0, 8))

statusbar = tb.Label(m, text="Ready", anchor=tk.W, bootstyle="inverse-secondary", padding=4)

# Pack everything in the correct order
statusbar.pack(side=tk.BOTTOM, fill=tk.X)
toolbar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))
editor_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

# SHORTCUTS
m.bind("<Control-n>", lambda e: new_file())
m.bind("<Control-o>", lambda e: open_file())
m.bind("<Control-s>", lambda e: save_file())
m.bind("<Control-S>", lambda e: save_as_file())
m.bind("<Control-r>", lambda e: run_code())
m.bind("<Control-t>", lambda e: toggle_theme())

apply_theme("dark")

# Force window to render before closing splash
m.update() 

# Close the PyInstaller splash screen if it's running
try:
    import pyi_splash
    pyi_splash.close()
except ImportError:
    pass

m.mainloop()
