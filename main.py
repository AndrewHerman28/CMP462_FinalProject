import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ReadFile
import Graphs
import Trees
import HelperFunctions


class PFM(tk.Tk):

    def __init__(self):
        super().__init__()

        self.backToMain = None
        self.title("Personal Finance Manager")
        self.geometry("800x700")  # Increased size to fit the graph
        self.attributes("-topmost", True)  # Moves in front of other windows
        self.configure(bg="midnightblue")  # Can change, chose blue for now

        self.expenseGroups = []
        self.expenses = []
        self.expensesVals = []
        self.dates = []
        self.trees = {}

        self.buttons = [
            ("Add Expenses", self.addPage),
            ("Search/Remove Expenses", self.searchPage),
            ("View Expense Data", self.viewPage),
            ("Import Data", self.importDataButton)
        ]

        self.homePage()

    def clear(self):
        if self.winfo_children() != "":
            for item in self.winfo_children():
                if item != self.backToMain:
                    item.destroy()

    def createReturnButton(self):
        self.backToMain = tk.Button(self, text="Return to Main Menu", fg="midnightblue", bg="midnightblue",
                                    font=("Times New Roman", 16), width=15, command=self.homePage)
        self.backToMain.place(x=10, y=10)

    def homePage(self):
        self.clear()  # clear when returning back to home from other page
        if self.backToMain is not None: self.backToMain.destroy()
        # remove "back to main menu" button from main page; clear function does not remove it because is needed for other 3 pages

        self.introFrame = tk.Frame(self)
        self.greetLabel = HelperFunctions.create_label(self, "Welcome to Your Personal Finance Manager!")
        self.greetLabel2 = HelperFunctions.create_label(self,
                                                        "Let's get started...\n------------------------------------------------------------------------------------------------------")
        self.menuName = HelperFunctions.create_label(self, "\nHome Menu")

        self.buttonFrame = tk.Frame(self)
        for text, command in self.buttons:
            btn = tk.Button(self, text=text, command=command, fg="midnightblue", bg="blue",
                            font=("Times New Roman", 20), width=20, height=3)
            btn.pack(side="top", pady=10)

    def addPage(self):

        self.clear()
        self.createReturnButton()

        def saveExpensesAndVals():
            expense_group = expenseGroupEntry.get()
            subcategory = expenseEntry.get()
            amount = float(amountEntry.get())
            date = dateEntry.get()

            self.expenseGroups.append(expense_group)
            self.expenses.append(subcategory)
            self.expensesVals.append(amount)
            self.dates.append(date)

            expenseGroupEntry.delete(0, "end")
            expenseEntry.delete(0, "end")
            amountEntry.delete(0, "end")
            dateEntry.delete(0, "end")

            if expense_group in self.trees:
                self.trees[expense_group].insert(expense_group, subcategory, date, amount)
            else:
                new_tree = Trees.Tree(expense_group)
                new_tree.insert(expense_group, subcategory, date, amount)
                self.trees[expense_group] = new_tree

        pageTitle = HelperFunctions.create_label(self, "Add Expenses\n----------------------------------")

        # ----- Expense -----
        expenseGroupLabel = HelperFunctions.create_label(self, "\nEnter the expense group:")
        expenseGroupEntry = HelperFunctions.create_entry(self)

        # ----- Subcategory -----
        expenseLabel = HelperFunctions.create_label(self, "\nEnter an sub-expense of the expense group:")
        expenseEntry = HelperFunctions.create_entry(self)

        # ----- Value of expense -----
        amountLabel = HelperFunctions.create_label(self, "Enter the expense amount:")
        amountEntry = HelperFunctions.create_entry(self)

        # ----- Date of expense -----
        dateLabel = HelperFunctions.create_label(self, "\nEnter the date for this expense (mm/dd/yyyy):")
        dateEntry = HelperFunctions.create_entry(self)

        # ----- Submit Button -----
        enterButton = tk.Button(self, text="Submit Expense Data", font=("Times New Roman", 16),
                                command=saveExpensesAndVals)
        enterButton.pack(side="bottom", pady=20)

    def searchPage(self):

        self.clear()
        self.createReturnButton()

        def search():
            value = float(self.expenseVal.get())
            date = self.expenseDate.get()
            name = self.expense.get()

        def remove():
            value = float(self.expenseVal.get())
            date = self.expenseDate.get()
            name = self.expense.get()

        self.pageTitle = tk.Label(self, text="Search/Remove Expenses\n----------------------------------",
                                  font=("Times New Roman", 22), bg="midnightblue")
        self.pageTitle.pack(side="top")

        self.expenseLabel = tk.Label(self, text="Enter an expense name:", font=("Times New Roman", 20), width=40,
                                     bg="midnightblue")
        self.expenseLabel.pack(side="top")
        self.expense = tk.Entry(self, width=20, justify="center")
        self.expense.pack(side="top", pady=10)
        self.expense.focus_set()

        self.expenseValLabel = tk.Label(self, text="\nEnter an expense value (300):", font=("Times New Roman", 20),
                                        width=40, bg="midnightblue")
        self.expenseValLabel.pack(side="top")
        self.expenseVal = tk.Entry(self, width=20, justify="center")
        self.expenseVal.pack(side="top", pady=10)
        self.expenseVal.focus_set()

        self.expenseDateLabel = tk.Label(self, text="\nEnter an expense date (mm/dd/yyyy):",
                                         font=("Times New Roman", 20), width=40, bg="midnightblue")
        self.expenseDateLabel.pack(side="top")
        self.expenseDate = tk.Entry(self, width=20, justify="center")
        self.expenseDate.pack(side="top", pady=10)
        self.expenseDate.focus_set()

        self.searchOrRemove = tk.Label(self, text="Would you like to search or remove this expense?",
                                       font=("Times New Roman", 20), width=40, bg="midnightblue")
        self.searchOrRemove.pack(side="top", pady=10)
        self.search = tk.Button(self, text="Search", font=("Times New Roman", 16), command=search)
        self.search.pack(side="top", pady=10)
        self.remove = tk.Button(self, text="Remove", font=("Times New Roman", 16), command=remove)
        self.remove.pack(side="top", pady=10)

    def viewPage(self):

        self.clear()
        self.createReturnButton()

        def displayGraph():
            graphChoice = selected_option1.get()
            graphGroupChoice = selected_option2.get()

            global canvas

            fig = Figure(figsize=(7, 5), dpi=100)
            ax = fig.add_subplot(111)

            if graphChoice == "Pie Chart":

                if 'canvas' in globals():
                    canvas.get_tk_widget().destroy()  # Remove previous graph if exists

                values = []
                names_and_dates = []
                for item in options2dict[graphGroupChoice]:
                    values.append(float(item[2]))
                    names_and_dates.append(str(item[0]) + ": " + str(item[1]))

                Graphs.make_pie_chart(fig, values, names_and_dates, 111, f"{graphGroupChoice} Expense Report")

            elif graphChoice == "Bar Chart":

                # Embed the figure in Tkinter window
                if 'canvas' in globals():
                    canvas.get_tk_widget().destroy()  # Remove previous graph if exists

                values = []
                names_and_dates = []
                for item in options2dict[graphGroupChoice]:
                    values.append(float(item[2]))
                    names_and_dates.append(str(item[0]) + ": " + str(item[1]))

                Graphs.make_bar_graph(fig, values, names_and_dates, 111, f"{graphGroupChoice} Expense Report")

            elif graphChoice == "Timeline Chart":

                if 'canvas' in globals():
                    canvas.get_tk_widget().destroy()  # Remove previous graph if exists

                try:
                    values = []
                    names = []
                    dates = []
                    for item in options2dict[graphGroupChoice]:
                        values.append(float(item[2]))
                        dates.append(item[1])
                        names.append(item[0])
                    Graphs.make_line_graph(fig, values, dates, 111, "Monthly Expense Report")

                except ValueError:
                    self.errorLabel = tk.Label(self, text="\nError! Date improper format-- use mm/dd/yyyy",
                                               font=("Times New Roman", 20), width=40, bg="midnightblue")
                    self.errorLabel.pack(side="top", pady=10)

            ax.axis("off")
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.get_tk_widget().pack(side="top", pady=10)
            canvas.draw()

        def convertDatatoDictionary():
            for item in range(len(self.displayData[0])):
                key = self.displayData[0][item]
                value = self.displayData[1][item]
                date = self.displayData[2][item]
                amount = self.displayData[3][item]
                if key not in options2dict:
                    options2dict[key] = [[value, date, amount]]
                else:
                    options2dict[key].append([value, date, amount])
            options2dict["All Expenses"] = self.displayData[1]

        self.pageTitle = tk.Label(self, text="View Expense Data\n----------------------------------",
                                  font=("Times New Roman", 22), bg="midnightblue")
        self.pageTitle.pack(side="top")

        selected_option1 = tk.StringVar()
        options1 = ["Pie Chart", "Bar Chart", "Timeline Chart"]
        dropdown1 = tk.OptionMenu(self, selected_option1, *options1)
        dropdown1.pack(side="top", pady=10)

        selected_option2 = tk.StringVar()
        options2dict = {}

        convertDatatoDictionary()

        dropdown2 = tk.OptionMenu(self, selected_option2, *options2dict.keys())
        dropdown2.pack(side="top", pady=10)

        enterButton = tk.Button(self, text="Submit Graph Choice", font=("Times New Roman", 16), command=displayGraph)
        enterButton.pack(side="top", pady=10)

    def importDataButton(self):
        self.displayData = ReadFile.open_file_dialog(self.trees, self)
        successLabel = HelperFunctions.create_label(self, "Data Successfully Imported...")
        for tree in self.trees:
            print(self.trees[tree].root.right)


if __name__ == "__main__":
    pfm = PFM()
    pfm.mainloop()
