# GUI for expense tracker
# Test 1

import tkinter as tk
import matplotlib.pyplot as plt

def expenseReport():

    categories = []
    categoriesVals = []

    monthIn = float(monthlyIncome.get())
    expenses = expensesCategories.get("1.0", tk.END)
    values = expensesValues.get("1.0", tk.END)
    expenses = expenses.rstrip("\n")
    values = values.rstrip("\n")

    if "," in expenses:
        expenses = expenses.split(",")
    elif "\n" in expenses:
        expenses = expenses.split("\n")
    for expense in expenses:
        categories.append(expense)

    if "," in values:
        values = values.split(",")
    elif "\n" in values:
        values = values.split("\n")
    for value in values:
        categoriesVals.append(value)

    total = 0
    for item in categoriesVals:
        total += float(item)

    savings = float(monthIn) - float(total)
    categoriesVals.append(savings)
    categories.append("Savings")

    plt.pie(categoriesVals, labels = categories, autopct = '%1.1f%%')
    plt.title("Monthly Expense Report")
    plt.show()

# Build Window
window = tk.Tk()
window.title("Personal Finance Manager")
window.geometry("600x500")
window.attributes("-topmost", 1)

# Introduction
greetLabel = tk.Label(window, text="Welcome to Your Personal Finance Manager!", font=("Times New Roman", 20))
greetLabel.pack()
greetLabel2 = tk.Label(window, text="Let's get started...", font=("Times New Roman", 16))
greetLabel2.pack()

# User input
monthlyIncomeLabel = tk.Label(window, text="Monthly Income: ", font=("Times New Roman", 14))
monthlyIncomeLabel.place(x=15, y=100)
monthlyIncome = tk.Entry(window, width=15)
monthlyIncome.place(x=15, y=125)

expensesLabel = tk.Label(window, text="Enter expenses (Bills,Rent,Grocery,etc.): ", font=("Times New Roman", 14))
expensesLabel.place(x=15, y=150)
expensesCategories = tk.Text(window, height=5, width=25)
expensesCategories.place(x=15, y=175)

expensesValuesLabel = tk.Label(window, text="Enter expenses amounts (300,2000,500,etc.): ", font=("Times New Roman", 14))
expensesValuesLabel.place(x=15, y=250)
expensesValues = tk.Text(window, height=5, width=25)
expensesValues.place(x=15, y=275)

# Button
enterButton = tk.Button(window, text="Enter Data", font=("Times New Roman", 14), command= expenseReport)
enterButton.place(x=15, y=350)

window.mainloop()