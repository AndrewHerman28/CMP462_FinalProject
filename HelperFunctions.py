import tkinter as tk

def create_label(self, text):
    label = tk.Label(self, text=text, font=("Times New Roman", 20), bg="midnightblue")
    label.pack(side="top", pady=10)
    return label

def create_entry(self):
    entry = tk.Entry(self, width=20, justify="center")
    entry.pack(side="top", pady=10)
    entry.focus_set()
    return entry
