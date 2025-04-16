import csv
import os
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict
import tree  # Trees.py in repo

# GUI file picker and logic handler
def open_file_dialog(window):
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[
            ("CSV files", "*.csv"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ],
        parent = window
    )

    if file_path:
        print(f"Selected file: {file_path}")
        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.csv' or ext == '.txt':
            data = parse_and_build_trees(file_path)
            return data  # return for displayData
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

    lists = build_trees(data)
    return(lists)

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

    data = build_trees(data)
    return data

# Shared logic for creating and populating TempTree trees
def build_trees(data):
    trees = list()
    # lists so can be used on view page; view page uses matplotlib which requires lists to display data
    categories = list()
    subcategories = list()
    dates = list()
    values = list()

    for category in data:
        dataTree = tree.Tree(category)
        if dataTree not in trees:
            trees.append(dataTree)
        for entry in data[category]:
            categories.append(category)
            subcategory = entry['Subcategory']
            subcategories.append(subcategory)
            value = entry['Value']
            values.append(value)
            date = entry['Date']
            dates.append(date)
            dataTree.insert(category, subcategory, date, value)

    for item in trees:
        item.display(item.root)

    return categories, subcategories, dates, values, trees
