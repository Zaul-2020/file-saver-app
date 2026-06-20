import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import shutil
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create main window
window = tk.Tk()
window.title("Data explorer")
window.geometry("900x600")
window.configure(bg="#f4f4f4")

# Current directory label
current_dir_label = tk.Label(window, text="Current Directory:", font=("Arial", 12), bg="#f4f4f4")
current_dir_label.pack(pady=5)

# File listbox
file_listbox = tk.Listbox(window, width=100, height=15, font=("Courier", 10))
file_listbox.pack(pady=10)

# File size label
file_size_label = tk.Label(window, text="", font=("Arial", 12), fg="green", bg="#f4f4f4")
file_size_label.pack(pady=5)

# Button frame
btn_frame = tk.Frame(window, bg="#f4f4f4")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Browse", width=12, command=lambda: browse_directory()).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Open", width=12, command=lambda: open_file()).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", width=12, command=lambda: delete_file()).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="New Folder", width=12, command=lambda: create_folder()).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Go Back", width=12, command=lambda: go_back()).grid(row=0, column=4, padx=5)

# Matplotlib chart setup
fig, ax = plt.subplots(figsize=(4, 3))
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(pady=10)

# Load files into listbox
def load_files(path):
    file_listbox.delete(0, tk.END)
    current_dir_label.config(text=f"Current Directory: {path}")
    try:
        for item in os.listdir(path):
            file_listbox.insert(tk.END, item)
        update_chart()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Update memory chart
def update_chart():
    mem = psutil.virtual_memory()
    labels = ['Used', 'Free']
    sizes = [mem.used, mem.available]
    ax.clear()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['red', 'green'])
    ax.set_title("Memory Usage")
    canvas.draw()

# Show file size
def show_file_size(event=None):
    selected = file_listbox.get(tk.ACTIVE)
    path = os.path.join(current_dir_label.cget("text").replace("Current Directory: ", ""), selected)
    if os.path.isfile(path):
        size = os.path.getsize(path)
        file_size_label.config(text=f"Selected File Size: {size // 1024} KB")
    else:
        file_size_label.config(text="Selected item is a folder.")

# Browse directory
def browse_directory():
    folder = filedialog.askdirectory()
    if folder:
        load_files(folder)

# Open file
def open_file():
    selected = file_listbox.get(tk.ACTIVE)
    path = os.path.join(current_dir_label.cget("text").replace("Current Directory: ", ""), selected)
    try:
        os.startfile(path)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Delete file
def delete_file():
    selected = file_listbox.get(tk.ACTIVE)
    path = os.path.join(current_dir_label.cget("text").replace("Current Directory: ", ""), selected)
    try:
        os.remove(path)
        load_files(os.path.dirname(path))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create new folder
def create_folder():
    path = filedialog.askdirectory()
    if path:
        folder_name = simpledialog.askstring("Folder Name", "Enter new folder name:")
        if folder_name:
            new_path = os.path.join(path, folder_name)
            try:
                os.mkdir(new_path)
                load_files(path)
            except Exception as e:
                messagebox.showerror("Error", str(e))

# Go back to parent folder
def go_back():
    current_path = current_dir_label.cget("text").replace("Current Directory: ", "")
    parent_path = os.path.dirname(current_path)
    if os.path.exists(parent_path):
        load_files(parent_path)

# Bind selection to show file size
file_listbox.bind("<<ListboxSelect>>", show_file_size)

# Start with home directory
load_files(os.path.expanduser("~"))

window.mainloop()
