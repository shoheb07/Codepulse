import tkinter as tk
from tkinter import filedialog, messagebox
import ast
import os

BG = "#f7f8fa"
ACCENT = "#090a0a"
TEXT = "white"

# ---------------- MAIN APP ----------------
root = tk.Tk()
root.title("CodePulse")
root.geometry("700x500")
root.config(bg=BG)

file_path = None

# ---------------- ANALYSIS LOGIC ----------------
def analyze_code(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_lines = len(lines)
    blank_lines = sum(1 for l in lines if not l.strip())
    comment_lines = sum(1 for l in lines if l.strip().startswith("#"))
    code_lines = total_lines - blank_lines - comment_lines

    with open(path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    functions = sum(isinstance(n, ast.FunctionDef) for n in ast.walk(tree))
    classes = sum(isinstance(n, ast.ClassDef) for n in ast.walk(tree))

    return {
        "File": os.path.basename(path),
        "Total Lines": total_lines,
        "Code Lines": code_lines,
        "Comment Lines": comment_lines,
        "Blank Lines": blank_lines,
        "Functions": functions,
        "Classes": classes
    }

# ---------------- FILE SELECT ----------------
def open_file():
    global file_path
    path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if not path:
        return
    file_path = path
    file_label.config(text=os.path.basename(path))
    analyze_and_display()

# ---------------- DISPLAY RESULTS ----------------
def analyze_and_display():
    if not file_path:
        messagebox.showwarning("No file", "Please select a Python file")
        return

    for w in result_frame.winfo_children():
        w.destroy()

    results = analyze_code(file_path)

    for key, value in results.items():
        row = tk.Frame(result_frame, bg=BG)
        row.pack(fill="x", pady=3)

        tk.Label(
            row,
            text=key,
            fg=ACCENT,
            bg=BG,
            font=("Arial", 11, "bold"),
            width=15,
            anchor="w"
        ).pack(side="left")

        tk.Label(
            row,
            text=value,
            fg=TEXT,
            bg=BG,
            font=("Arial", 11),
            anchor="w"
        ).pack(side="left")

# ---------------- UI ----------------
tk.Label(
    root,
    text="CodePulse ⚡",
    fg=ACCENT,
    bg=BG,
    font=("Arial", 22, "bold")
).pack(pady=15)

tk.Button(
    root,
    text="Open Python File",
    command=open_file,
    bg=ACCENT,
    fg="white",
    font=("Arial", 11, "bold"),
    width=20
).pack(pady=5)

file_label = tk.Label(
    root,
    text="No file selected",
    fg="gray",
    bg=BG
)
file_label.pack(pady=5)

result_frame = tk.Frame(root, bg=BG)
result_frame.pack(fill="both", expand=True, padx=20, pady=20)

root.mainloop()