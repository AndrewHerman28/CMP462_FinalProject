import tkinter as tk

def create_label(self, text):
    label = tk.Label(self, text=text, font=("Times New Roman", 20), bg="midnightblue")
    label.pack(side="top")
    return label

def create_label_L(self, text, color):
    label = tk.Label(self, text=text, font=("Times New Roman", 18), bg=color)
    label.pack(side="left", pady=10, padx=10)
    return label

def create_label_R(self, text, color):
    label = tk.Label(self, text=text, font=("Times New Roman", 18), bg=color)
    label.pack(side="right", pady=10, padx=10)
    return label

def create_label_B(self, text, color):
    label = tk.Label(self, text=text, font=("Times New Roman", 18), bg=color)
    label.pack(side="bottom", pady=10)
    return label

def create_entry(self):
    entry = tk.Entry(self, width=20, justify="center")
    entry.pack(side="top")
    entry.focus_set()
    return entry

def prev_page(self, page_expenses):
    if self.current_page > 0:
        self.current_page -= 1
        self.display_search_results(self, page_expenses)

def display_search_results(self, page_expenses):
    for item in page_expenses:
        node = create_label_L(
            self.searchFrame,
            f"Expense Group: {item[0]}\n"
            f"Expense Name: {item[1]}\n"
            f"Expense Amount: {item[2]}\n"
            f"Expense Date: {item[3]}",
            "green")

def next_page(self, page_expenses):
    if (self.current_page + 1) * self.results_per_page < len(self.expenses):
        self.current_page += 1
        self.display_search_results(self, page_expenses)
