# To run project:
# Make sure you have downloaded the other 5 Python source files
# Run this file
# Can use ExpenseSheet1.csv or ExpenseSheet2.csv for imported data sample

import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import ReadFile
import Graphs
import Trees
import HelperFunctions
from Calendar import open_calendar

class PFM(tk.Tk):

    def __init__(self):
        super().__init__()

        self.backToMain = None
        self.title("Personal Finance Manager")
        self.geometry("1200x800")  # Increased size to fit the graph
        self.attributes("-topmost", True)  # Moves in front of other windows
        self.configure(bg="midnightblue")  # Can change, chose blue for now

        self.trees = {}
        self.data = None

        self.buttons = []
        self.buttonNames = [
            ("Add Expenses", self.addPage),
            ("Search/Remove Expenses", self.searchPage),
            ("View Expense Data", self.viewPage),
            ("Import Data", self.importDataButton)
        ]

        self.imported = False
        self.searchDisplay = None
        self.searchFrame = None
        self.deleteFrame = None
        self.pressedDataIn = False

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
        for text, command in self.buttonNames:
            if (command == self.searchPage or command == self.viewPage) and self.pressedDataIn is False:
                state='disabled'
            else:
                state='normal'
            btn = tk.Button(self, text=text, command=command, fg="midnightblue", bg="blue",
                            font=("Times New Roman", 20), width=20, height=3, state=state)
            btn.pack(side="top", pady=10)
            self.buttons.append(btn)

    def enableAllButtons(self): # Import data button needs this to enable all buttons, cannot do simply pressed boolean
        if self.pressedDataIn:
            for btn in self.buttons:
                btn.config(state='normal')

    def addPage(self):

        self.clear()
        self.pressedDataIn = True
        self.createReturnButton()

        def saveExpensesAndVals():
            expense_group = expenseGroupEntry.get()
            subcategory = expenseEntry.get()
            amount = float(amountEntry.get())
            dateEntry = date.get()

            expenseGroupEntry.delete(0, "end")
            expenseEntry.delete(0, "end")
            amountEntry.delete(0, "end")
            dateButton.config(text = "Date")

            if expense_group in self.trees:
                self.trees[expense_group].insert(expense_group, subcategory, dateEntry, amount)
            else:
                new_tree = Trees.Tree(expense_group)
                new_tree.insert(expense_group, subcategory, dateEntry, amount)
                self.trees[expense_group] = new_tree

        pageTitle = HelperFunctions.create_label(self, "Add Expenses\n----------------------------------")
        note = HelperFunctions.create_label(self, "*Note: To add an expense, do not leave any criteria blank.")

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
        date = tk.StringVar(value=None)
        dateButton = tk.Button(self, text="Date", command=lambda: open_calendar(dateButton, date), bg="midnightblue")
        dateButton.pack(side="top", pady=10)

        # ----- Submit Button -----
        enterButton = tk.Button(self, text="Submit Expense Data", font=("Times New Roman", 16),
                                command=saveExpensesAndVals)
        enterButton.pack(side="bottom", pady=20)

    def searchPage(self):

        self.clear()
        self.createReturnButton()

        def search():
            def deleteFunc():
                delete = delete_option.get()
                delete = delete.lstrip("(")
                delete = delete.rstrip(")")
                delete = delete.split(", ")
                group = delete[0].replace("'", "")
                group = group.replace('"', "")
                self.trees[group].remove(self.trees[group].root, delete[1], float(delete[2]))

                updated = HelperFunctions.create_label_B(self.deleteFrame, f"'{delete[1]}' was successfully deleted from '{self.trees[group].name}'", "red")

            if self.deleteFrame is not None:
                self.deleteFrame.destroy()

            if self.searchFrame is not None:
                self.searchFrame.destroy()

            self.searchFrame = tk.Frame(self, bg="midnightblue")
            self.searchFrame.pack(side="top", pady=10)

            self.deleteFrame = tk.Frame(self, bg="midnightblue")
            self.deleteFrame.pack(side="top", pady=10)

            group = selected_group.get()
            name = expenseEntry.get()
            amount = amountEntry.get()
            dateF = fromDate.get()
            dateT = toDate.get()

            if group == "":
                group = None
            if name == "":
                name = None
            if amount == "":
                amount = None
            if dateF == "":
                dateF = None
            if dateT == "":
                dateT = None
            nodes = []
            if amount is not None:
                amount = float(amount)

            # Store the search results as instance variable
            self.all_results = []
            if group:
                self.all_results = self.trees[group].newSearch(self.trees[group].root, group, name, dateF, dateT,
                                                               amount, nodes)
            else:
                for tree_group in self.trees:
                    results = self.trees[tree_group].newSearch(self.trees[tree_group].root, tree_group, name, dateF,
                                                               dateT, amount, nodes)
                    if results:
                        self.all_results.extend(results)

            # Initialize pagination variables
            self.current_page = 0
            self.items_per_page = 5

            def display_current_page():
                # Clear previous results
                for widget in self.searchFrame.winfo_children():
                    widget.destroy()

                start_idx = self.current_page * self.items_per_page
                end_idx = start_idx + self.items_per_page
                current_page_items = self.all_results[start_idx:end_idx]

                for item in current_page_items:
                    node = HelperFunctions.create_label_L(
                        self.searchFrame,
                        f"Expense Group: {item[0]}\n"
                        f"Expense Name: {item[1]}\n"
                        f"Expense Amount: {item[2]}\n"
                        f"Expense Date: {item[3]}",
                        "green"
                    )

            def next_page():
                if (self.current_page + 1) * self.items_per_page < len(self.all_results):
                    self.current_page += 1
                    display_current_page()
                    update_buttons()

            def prev_page():
                if self.current_page > 0:
                    self.current_page -= 1
                    display_current_page()
                    update_buttons()

            def update_buttons():
                if self.current_page == 0:
                    prev_button.config(state="disabled", bg="gray", text="<--")
                    return

                if (self.current_page + 1) * self.items_per_page > len(self.all_results):
                    next_button.config(state="disabled", bg="gray", text="-->")
                    return

                prev_button.config(state="normal", bg="midnightblue", text=f"{self.current_page} <--")
                next_button.config(state="normal", bg="midnightblue", text=f"--> {self.current_page + 1}")

            # Display initial page
            display_current_page()

            # Create navigation buttons
            prev_button = tk.Button(self.searchRemoveFrame, text="<--", command=prev_page,
                                    font=("Times New Roman", 16),
                                    bg="midnightblue")
            prev_button.place(x=0, y=340)

            next_button = tk.Button(self.searchRemoveFrame, text="--> 1", command=next_page,
                                    font=("Times New Roman", 16),
                                    bg="midnightblue")
            next_button.place(x=200, y=340)
            update_buttons()

            deleteLabel = HelperFunctions.create_label(self.deleteFrame, f"Select Expense to Delete:")
            delete_option = tk.StringVar()
            options = []
            for item in self.all_results:
                if item not in options:
                    options.append(item)
            deleteDropdown = tk.OptionMenu(self.deleteFrame, delete_option, *options)
            deleteDropdown.pack(side="top", pady=10)
            deleteButton = tk.Button(self.deleteFrame, text="Delete Expense",command=deleteFunc, font=("Times New Roman", 16), bg="midnightblue")
            deleteButton.pack(side="top", pady=10)

        self.searchRemoveFrame = tk.Frame(self, bg="midnightblue")
        self.searchRemoveFrame.pack(side="top", pady=10)
        self.pageTitle = HelperFunctions.create_label(self.searchRemoveFrame,
                                                      text="Search/Remove Expenses\n----------------------------------")

        expenseGroupLabel = HelperFunctions.create_label(self.searchRemoveFrame, "\nEnter the expense group:")

        selected_group = tk.StringVar()
        groupDropdown = tk.OptionMenu(self.searchRemoveFrame, selected_group, *self.trees.keys())
        groupDropdown.pack(side="top", pady=10)

        expenseLabel = HelperFunctions.create_label(self.searchRemoveFrame, "Search by Expense Name:")
        expenseEntry = HelperFunctions.create_entry(self.searchRemoveFrame)

        amountLabel = HelperFunctions.create_label(self.searchRemoveFrame, "Search by Amount:")
        amountEntry = HelperFunctions.create_entry(self.searchRemoveFrame)

        dateLabel = HelperFunctions.create_label(self.searchRemoveFrame, "Search by Date (mm/dd/yyyy):")

        self.dateFrame = tk.Frame(self.searchRemoveFrame, bg="midnightblue")
        self.dateFrame.pack(side="top")

        fromDate = tk.StringVar(value=None)
        fromButton = tk.Button(self.dateFrame, text="Search From:", command=lambda: open_calendar(fromButton, fromDate), bg = "midnightblue", font=("Times New Roman", 16))
        fromButton.pack(side="left", pady=10)

        toDate = tk.StringVar(value=None)
        toButton = tk.Button(self.dateFrame, text="Search To:", command=lambda: open_calendar(toButton, toDate), bg = "midnightblue", font=("Times New Roman", 16))
        toButton.pack(side="right", pady=10)

        self.searching = tk.Button(self.searchRemoveFrame, text="Search", font=("Times New Roman", 16), command=search)
        self.searching.pack(side="top")

    def viewPage(self):

        self.clear()
        self.createReturnButton()

        def displayGraph():
            graphChoice = selected_option1.get()
            graphGroupChoice = selected_option2.get()

            group = self.trees[graphGroupChoice].newSearch(self.trees[graphGroupChoice].root, self.trees[graphGroupChoice].name, None, None, None, None, [])

            global canvas
            fig = Figure(figsize=(10, 7), dpi=75)
            ax = fig.add_subplot(111)

            if graphChoice == "Pie Chart":

                if 'canvas' in globals():
                    canvas.get_tk_widget().destroy()  # Remove previous graph if exists

                values = []
                names_and_dates = []
                for item in group:
                    values.append(float(item[2]))
                    names_and_dates.append(str(item[1]) + ": " + str(item[3]))

                Graphs.make_pie_chart(fig, values, names_and_dates, 111, f"{graphGroupChoice} Expense Report")

            elif graphChoice == "Bar Chart":

                # Embed the figure in Tkinter window
                if 'canvas' in globals():
                    canvas.get_tk_widget().destroy()  # Remove previous graph if exists

                values = []
                names_and_dates = []
                for item in group:
                    values.append(float(item[2]))
                    names_and_dates.append(str(item[1]) + ": " + str(item[3]))

                Graphs.make_bar_graph(fig, values, names_and_dates, 111, f"{graphGroupChoice} Expense Report")

            elif graphChoice == "Timeline Chart":

                if 'canvas' in globals():
                    canvas.get_tk_widget().destroy()  # Remove previous graph if exists

                try:
                    values = []
                    dates = []
                    for item in group:
                        values.append(float(item[2]))
                        dates.append(item[3])
                    Graphs.make_line_graph(fig, values, dates, 111, "Timeline Expense Report")

                except ValueError:
                    self.errorLabel = tk.Label(self, text="\nError! Date improper format-- use mm/dd/yyyy",
                                               font=("Times New Roman", 20), width=40, bg="midnightblue")
                    self.errorLabel.pack(side="top", pady=10)

            ax.axis("off")
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.get_tk_widget().pack(side="top", pady=10)
            canvas.draw()

        self.pageTitle = tk.Label(self, text="View Expense Data\n----------------------------------", font=("Times New Roman", 22), bg="midnightblue")
        self.pageTitle.pack(side="top")

        selected_option1 = tk.StringVar()
        options1 = ["Pie Chart", "Bar Chart", "Timeline Chart"]
        dropdown1 = tk.OptionMenu(self, selected_option1, *options1)
        dropdown1.pack(side="top", pady=10)

        selected_option2 = tk.StringVar()
        dropdown2 = tk.OptionMenu(self, selected_option2, *self.trees.keys())
        dropdown2.pack(side="top", pady=10)

        enterButton = tk.Button(self, text="Submit Graph Choice", font=("Times New Roman", 16), command=displayGraph)
        enterButton.pack(side="top", pady=10)

    def importDataButton(self):
        self.data = ReadFile.open_file_dialog(self.trees, self)
        if self.data is None:
            successLabel = HelperFunctions.create_label(self, "Data Successfully Imported...")
            self.pressedDataIn = True
            self.enableAllButtons()
            self.imported = True
        else:
            successLabel = HelperFunctions.create_label(self, "Data Not Imported...")

if __name__ == "__main__":
    pfm = PFM()
    pfm.mainloop()
