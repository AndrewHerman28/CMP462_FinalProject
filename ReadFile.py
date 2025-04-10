import csv
import os
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict
import TempTree  # Make sure TempTree.py is in the same directory

# GUI file picker and logic handler
def open_file_dialog():
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[
            ("CSV files", "*.csv"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
    )

    if file_path:
        print(f"Selected file: {file_path}")
        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.csv':
            parse_and_build_trees(file_path)
        elif ext == '.txt':
            parse_txt_and_build_trees(file_path)
        else:
            print("Unsupported file type")

# Function to parse and build trees from a CSV file
def parse_and_build_trees(file_path):
    data = defaultdict(list)

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            main_category = row['Tree Name']
            subcategory_info = {
                'Subcategory': row['Subcategory'],
                'Value': float(row['Value']),
                'Date': row['Date']
            }
            data[main_category].append(subcategory_info)

    build_trees(data)

# Function to parse and build trees from a TXT file (if same structure as CSV)
def parse_txt_and_build_trees(file_path):
    data = defaultdict(list)

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)  # This works if TXT is comma-delimited
        for row in reader:
            main_category = row['Tree Name']
            subcategory_info = {
                'Subcategory': row['Subcategory'],
                'Value': float(row['Value']),
                'Date': row['Date']
            }
            data[main_category].append(subcategory_info)

    build_trees(data)

# Shared logic for creating and populating TempTree trees
def build_trees(data):
    trees = set()

    for category in data:
        tree = TempTree.Tree(category)
        trees.add(tree)
        for entry in data[category]:
            subcategory = entry['Subcategory']
            value = entry['Value']
            date = entry['Date']
            print(category, subcategory, date, value)

            # Optionally insert into your tree here
            # tree.insert(subcategory, value, date)

# Set up the GUI window
root = tk.Tk()
root.title("CSV/TXT Expense Tree Loader")
root.geometry("300x100")

select_button = tk.Button(root, text="Choose File", command=open_file_dialog)
select_button.pack(pady=30)

root.mainloop()
