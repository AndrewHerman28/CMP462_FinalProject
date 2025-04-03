# GUI Display
# Test 3 -- Created multiple pages (each page as function) in 1 GUI class

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PFM(tk.Tk):
    def __init__(self):
        super().__init__()

        self.backToMain = None
        self.title("Personal Finance Manager")
        self.geometry("750x600")  # Increased size to fit the graph
        self.attributes("-topmost", True) # Moves in front of other windows
        self.configure(bg = "midnightblue") # Can change, chose blue for now

        self.homePage()

    def clear(self):
        if self.winfo_children() != "":
            for item in self.winfo_children():
                if item != self.backToMain:
                    item.destroy()

    def createReturnButton(self):
        self.backToMain = tk.Button(self, text="Return to Main Menu", fg="midnightblue", bg="midnightblue", font=("Times New Roman", 16), width=15, command=self.homePage)
        self.backToMain.place(x=10, y=10)

    def homePage(self):
        self.clear() # clear when returning back to home from other page
        if self.backToMain is not None: self.backToMain.destroy()
        # remove "back to main menu" button from main page; clear function does not remove it because is needed for other 3 pages

        self.introFrame = tk.Frame(self)
        self.greetLabel = tk.Label(self, text = "Welcome to Your Personal Finance Manager!", font = ("Times New Roman", 24), bg = "midnightblue")
        self.greetLabel.pack(side = "top")
        self.greetLabel2 = tk.Label(self, text = "Let's get started...", font = ("Times New Roman", 20), bg = "midnightblue")
        self.greetLabel2.pack(side = "top")
        self.menuName = tk.Label(self, text = "\nHome Menu", font = ("Times New Roman", 20), bg = "midnightblue")
        self.menuName.pack(side = "top")

        self.buttonFrame = tk.Frame(self)
        self.addButton = tk.Button(self, text = "Add Expenses", fg = "midnightblue", bg = "blue", font = ("Times New Roman", 20), width = 20, height = 3, command = self.addPage)
        self.addButton.pack(side = "top", pady = 10)
        self.searchButton = tk.Button(self, text = "Search/Remove Expenses", fg = "midnightblue", font = ("Times New Roman", 20), width = 20, height = 3, command = self.searchPage)
        self.searchButton.pack(side = "top", pady = 10)
        self.viewButton = tk.Button(self, text = "View Expense Data", fg = "midnightblue", font = ("Times New Roman", 20), width = 20, height = 3, command = self.viewPage)
        self.viewButton.pack(side = 'top', pady = 10)

    def addPage(self):

        def subEx():
            self.subLabel = tk.Label(self, text = "\nEnter sub-expenses (Light Bill, Gas Bill, Water Bill, etc.):", font = ("Times New Roman", 18), width = 55, bg = "midnightblue")
            self.subLabel.pack(side = "top", pady = 10)
            self.subExp = tk.Text(self, width = 20, height = 4)
            self.subExp.pack(side = "top", pady = 0)
            self.subYes.config(state = "disabled")
            self.subNo.config(state = "disabled")

        def subExNo():
            self.subLabel = tk.Label(self, text = "\nPress Submit Data...", font = ("Times New Roman", 18), width = 40, bg = "midnightblue")
            self.subLabel.pack(side = "top", pady = 10)
            self.subYes.config(state = "disabled")
            self.subNo.config(state = "disabled")

        self.clear()

        self.pageTitle = tk.Label(self, text="Add Expenses\n----------------------------------", font=("Times New Roman", 22), bg="midnightblue")
        self.pageTitle.pack(side="top")

        self.expenseLabel = tk.Label(self, text = "\nEnter an expense:", font = ("Times New Roman", 20), width = 40, bg = "midnightblue")
        self.expenseLabel.pack(side = "top")
        self.expense = tk.Entry(self, width = 20, justify = "center")
        self.expense.pack(side = "top", pady = 10)
        self.expense.focus_set()

        self.amountLabel = tk.Label(self, text = "Enter the expense amount:", font = ("Times New Roman", 20), width = 40, bg = "midnightblue")
        self.amountLabel.pack(side = "top", pady = 10)
        self.amountCategories = tk.Entry(self, width = 20, justify = "center")
        self.amountCategories.pack(side = "top", pady = 10)

        self.subexpensesLabel = tk.Label(self, text = "Does this expense have subcategories?", font = ("Times New Roman", 20), width = 40, bg = "midnightblue")
        self.subexpensesLabel.pack(side = "top", pady = 10)
        self.subYes = tk.Button(self, text = "Yes", font = ("Times New Roman", 16), command = subEx)
        self.subYes.pack(side = "top", pady = 10)
        self.subNo = tk.Button(self, text = "No", font = ("Times New Roman", 16), command = subExNo)
        self.subNo.pack(side = "top", pady = 10)

        enterButton = tk.Button(self, text = "Submit Expense Data", font = ("Times New Roman", 16),)
        enterButton.pack(side = "bottom", pady = 20)

        self.createReturnButton()

    def searchPage(self):
        self.clear()

        self.pageTitle = tk.Label(self, text = "Search/Remove Expenses\n----------------------------------", font = ("Times New Roman", 22), bg = "midnightblue")
        self.pageTitle.pack(side = "top")

        self.expenseDateLabel = tk.Label(self, text = "\nEnter an expense date (mm/dd/yyy):", font = ("Times New Roman", 20), width = 40, bg = "midnightblue")
        self.expenseDateLabel.pack(side = "top")
        self.expenseDate = tk.Entry(self, width = 20, justify = "center")
        self.expenseDate.pack(side = "top", pady = 10)
        self.expenseDate.focus_set()

        self.expenseValLabel = tk.Label(self, text = "\nEnter an expense value (300):", font = ("Times New Roman", 20), width = 40, bg = "midnightblue")
        self.expenseValLabel.pack(side = "top")
        self.expenseVal = tk.Entry(self, width = 20, justify = "center")
        self.expenseVal.pack(side = "top", pady = 10)
        self.expenseVal.focus_set()

        enterButton = tk.Button(self, text = "Submit Expense Data", font = ("Times New Roman", 16), )
        enterButton.pack(side = "bottom", pady = 20)

        self.createReturnButton()

    def viewPage(self):

        def displayGraph():
            graphChoice = selected_option.get()
            global canvas
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)

            if graphChoice == "Pie Chart":
                ax.pie([300,1500,500], labels=["Grocery", "Rent", "Bills"], autopct='%1.1f%%')
                ax.set_title("Monthly Expense Report")

                # Embed the figure in Tkinter window
                if 'canvas' in globals():
                    canvas.get_tk_widget().destroy()  # Remove previous graph if exists

                canvas = FigureCanvasTkAgg(fig, master=self)
                canvas.get_tk_widget().pack(side="top", pady = 10)
                canvas.draw()

            elif graphChoice == "Bar Chart":
                ax.bar(["Grocery", "Rent", "Bills"], [300, 1500, 500])
                ax.set_title("Monthly Expense Report")

                # Embed the figure in Tkinter window
                if 'canvas' in globals():
                    canvas.get_tk_widget().destroy()  # Remove previous graph if exists

                canvas = FigureCanvasTkAgg(fig, master=self)
                canvas.get_tk_widget().pack(side="top", pady=10)
                canvas.draw()

            elif graphChoice == "Timeline Chart":
                x=1

        self.clear()

        self.pageTitle = tk.Label(self, text="View Expense Data\n----------------------------------", font=("Times New Roman", 22), bg="midnightblue")
        self.pageTitle.pack(side="top")

        selected_option = tk.StringVar()
        options = ["Pie Chart", "Bar Chart", "Timeline Chart"]
        dropdown = tk.OptionMenu(self, selected_option, *options)
        dropdown.pack(side = "top", pady = 10)

        enterButton = tk.Button(self, text = "Submit Graph Choice", font = ("Times New Roman", 16), command = displayGraph)
        enterButton.pack(side = "top", pady = 10)

        self.createReturnButton()

if __name__ == "__main__":
    pfm = PFM()
    pfm.mainloop()

""" 
Note: Current GUI is NOT using this function
This is from the previous testing; keeping this function as a comment in case needed later.

def expenseReport():
    categories = []
    categoriesVals = []

    monthIn = float(monthlyIncome.get())
    expenses = expensesCategories.get("1.0", tk.END).strip()
    values = expensesValues.get("1.0", tk.END).strip()

    if "," in expenses:
        expenses = expenses.split(",")
    elif "\n" in expenses:
        expenses = expenses.split("\n")
    for expense in expenses:
        categories.append(expense.strip())

    if "," in values:
        values = values.split(",")
    elif "\n" in values:
        values = values.split("\n")
    for value in values:
        if value.strip():  # Ensure no empty strings
            categoriesVals.append(float(value.strip()))

    total = sum(categoriesVals)
    savings = float(monthIn) - total
    categoriesVals.append(savings)
    categories.append("Savings")

    # Create a figure and pie chart
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(categoriesVals, labels=categories, autopct='%1.1f%%')
    ax.set_title("Monthly Expense Report")

    # Embed the figure in Tkinter window
    global canvas
    if 'canvas' in globals():
        canvas.get_tk_widget().destroy()  # Remove previous graph if exists

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().place(x=300, y=100)
    canvas.draw()
"""