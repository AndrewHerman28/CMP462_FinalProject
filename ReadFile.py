import csv
import os
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict
import Trees  # Trees.py in repo


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
            data = parse_and_build_trees(file_path, all_trees)
            return data  # return for displayData
        else:
            print("Unsupported file type")


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

    lists = build_trees(data, all_trees)
    return (lists)  # return for displayData


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

    data = build_trees(data, all_trees)
    return data  # return for displayData


# Shared logic for creating and populating TempTree trees
def build_trees(data, all_trees):
    trees = set()
    # lists so can be used on view page; view page uses matplotlib which requires lists to display data
    categories = list()
    subcategories = list()
    dates = list()
    values = list()

    for category in data:
        for entry in data[category]:
            subcategory = entry['Subcategory']
            value = entry['Value']
            date = entry['Date']

            if category in all_trees is not None:
                all_trees[category].insert(category, subcategory, date, value)
                print(f"Added {subcategory} to {category} from existing tree")
            else:
                new_tree = Trees.Tree(category)
                new_tree.insert(category, subcategory, date, value)
                all_trees[category] = new_tree
                print(f"Added {subcategory} to {category} creating new tree")



    return categories, subcategories, dates, values  # return for displayData
