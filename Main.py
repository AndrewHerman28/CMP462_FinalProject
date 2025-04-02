import tkinter as tk
import Tree
import ViewData

tree = Tree.Tree("Rent")

tree.insert(25, "AC", "1/2/3")
tree.insert(35, "Electricity", "5/2/3")
tree.insert(45, "Rent", "1/5/3")
tree.insert(55, "Utility", "6/2/3")
tree.insert(65, "Water", "1/2/6")
tree.insert(75, "Lawn Services", "2/2/2")


# Build Window
window = tk.Tk()
window.title("Personal Finance Manager")
window.geometry("1600x1000")  # Increased size to fit the graph
window.attributes("-topmost", 1)

ViewData.expenseReport(tree.convert_to_list(tree.root), window)
window.mainloop()
