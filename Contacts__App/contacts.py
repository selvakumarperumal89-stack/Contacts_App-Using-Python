# ===============================
# CONTACTS APP USING PYTHON + TKINTER + SQLITE
# ===============================

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# -------------------------------
# DATABASE SETUP
# -------------------------------
conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
)
""")

conn.commit()


# -------------------------------
# SAVE CONTACT FUNCTION
# -------------------------------
def save_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()

    if name == "" or phone == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    if not phone.isdigit():
        messagebox.showerror("Error", "Phone number must contain only digits")
        return

    cursor.execute(
        "INSERT INTO contacts (name, phone) VALUES (?, ?)",
        (name, phone)
    )
    conn.commit()

    messagebox.showinfo("Success", "Contact Saved Successfully")

    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

    load_contacts()


# -------------------------------
# LOAD CONTACTS FUNCTION
# -------------------------------
def load_contacts():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=(row[1], row[2]))


# -------------------------------
# MAIN WINDOW
# -------------------------------
root = tk.Tk()
root.title("Modern Contacts App")
root.geometry("700x500")
root.config(bg="#0F172A")
root.resizable(False, False)

# -------------------------------
# STYLE
# -------------------------------
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="#1E293B",
    foreground="white",
    rowheight=30,
    fieldbackground="#1E293B",
    font=("Segoe UI", 11)
)

style.configure(
    "Treeview.Heading",
    background="#2563EB",
    foreground="white",
    font=("Segoe UI", 11, "bold")
)

style.map("Treeview", background=[("selected", "#3B82F6")])

# -------------------------------
# HEADER
# -------------------------------
header = tk.Label(
    root,
    text="📱 CONTACTS MANAGER",
    bg="#0F172A",
    fg="white",
    font=("Segoe UI", 24, "bold")
)
header.pack(pady=20)

# -------------------------------
# FORM FRAME
# -------------------------------
form_frame = tk.Frame(root, bg="#1E293B", bd=0)
form_frame.pack(padx=20, pady=10, fill="x")

# Name
name_label = tk.Label(
    form_frame,
    text="Name",
    bg="#1E293B",
    fg="white",
    font=("Segoe UI", 12)
)
name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

name_entry = tk.Entry(
    form_frame,
    font=("Segoe UI", 12),
    bg="#334155",
    fg="white",
    insertbackground="white",
    relief="flat",
    width=30
)
name_entry.grid(row=1, column=0, padx=10, pady=5)

# Phone
phone_label = tk.Label(
    form_frame,
    text="Phone Number",
    bg="#1E293B",
    fg="white",
    font=("Segoe UI", 12)
)
phone_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

phone_entry = tk.Entry(
    form_frame,
    font=("Segoe UI", 12),
    bg="#334155",
    fg="white",
    insertbackground="white",
    relief="flat",
    width=30
)
phone_entry.grid(row=1, column=1, padx=10, pady=5)

# -------------------------------
# SAVE BUTTON
# -------------------------------
save_btn = tk.Button(
    root,
    text="SAVE CONTACT",
    bg="#2563EB",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2",
    command=save_contact
)

save_btn.pack(pady=20)

# Hover effect
def on_enter(e):
    save_btn["bg"] = "#1D4ED8"

def on_leave(e):
    save_btn["bg"] = "#2563EB"

save_btn.bind("<Enter>", on_enter)
save_btn.bind("<Leave>", on_leave)

# -------------------------------
# CONTACT LIST
# -------------------------------
table_frame = tk.Frame(root, bg="#0F172A")
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

tree = ttk.Treeview(
    table_frame,
    columns=("Name", "Phone"),
    show="headings",
    height=10
)

tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone Number")

tree.column("Name", width=300)
tree.column("Phone", width=300)

tree.pack(fill="both", expand=True)

# -------------------------------
# LOAD DATA
# -------------------------------
load_contacts()

# -------------------------------
# RUN APP
# -------------------------------
root.mainloop()

# -------------------------------
# CLOSE DATABASE CONNECTION
# -------------------------------
conn.close()