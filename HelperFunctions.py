import tkinter as tk
from datetime import datetime

def create_label(self, text):
    label = tk.Label(self, text=text, font=("Times New Roman", 20), bg="midnightblue")
    label.pack(side="top")
    return label

def create_label_L(self, text, color):
    label = tk.Label(self, text=text, font=("Times New Roman", 18), bg=color)
    label.pack(side="left", pady=10, padx=10)
    return label

def convert_to_date(str):
    return datetime.strptime(str, "%m/%d/%Y")

def create_label_B(self, text):
    label = tk.Label(self, text=text, font=("Times New Roman", 18), bg="midnightblue")
    label.pack(side="bottom", pady=10)
    return label

def create_entry(self):
    entry = tk.Entry(self, width=20, justify="center")
    entry.pack(side="top")
    entry.focus_set()
    return entry
