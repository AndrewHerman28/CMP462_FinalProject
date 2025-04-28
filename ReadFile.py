import csv
import os
from tkinter import filedialog
from collections import defaultdict
import Trees

# GUI file picker and logic handler
def open_file_dialog(all_trees, root):
    file_path = filedialog.askopenfilename(
        parent=root,
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

        if ext == '.csv' or ext == '.txt':
            parse_and_build_trees(file_path, all_trees)
        else:
            print("Unsupported file type")

    if not file_path:
        return "f"


# Function to parse and build trees from a CSV file
def parse_and_build_trees(file_path, all_trees):
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

    build_trees(data, all_trees)


# Function to parse and build trees from a TXT file (if same structure as CSV)
def parse_txt_and_build_trees(file_path, all_trees):
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

    build_trees(data, all_trees)


# Shared logic for creating and populating TempTree trees
def build_trees(data, all_trees):

    for category in data:
        for entry in data[category]:
            subcategory = entry['Subcategory']
            value = entry['Value']
            date = entry['Date']

            if category in all_trees is not None:
                all_trees[category].insert(category, subcategory, date, value)
            else:
                new_tree = Trees.Tree(category)
                new_tree.insert(category, subcategory, date, value)
                all_trees[category] = new_tree