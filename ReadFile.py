import csv
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict
import TempTree  # Make sure your TempTree.py is in the same folder or in PYTHONPATH


def open_file_dialog():
    file_path = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV files", "*.csv")]
    )

    if file_path:
        print(f"Selected file: {file_path}")
        parse_and_build_trees(file_path)


def parse_and_build_trees(file_path):
    data = defaultdict(list)

    # Read the CSV file
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

    # Create trees and populate them
    trees = set()
    for category in data:
        tree = TempTree.Tree(category)
        trees.add(tree)
        for entry in data[category]:
            subcategory = entry['Subcategory']
            value = entry['Value']
            date = entry['Date']
            print(category, subcategory, date, value)
            # You can insert into your tree here if Tree class supports it
            # e.g., tree.insert(subcategory, value, date)


# Set up GUI
root = tk.Tk()
root.title("CSV Expense Tree Loader")
root.geometry("300x100")

select_button = tk.Button(root, text="Choose CSV File", command=open_file_dialog)
select_button.pack(pady=30)

root.mainloop()
