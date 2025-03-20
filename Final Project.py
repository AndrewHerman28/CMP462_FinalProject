class ExpenseNode:
    def __init__(self, name):
        self.name = name
        self.amount = 0
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def calculate_total(self):
        if self.children:
            self.amount = sum(child.calculate_total() for child in self.children)
        return self.amount

    def display(self, level=0, income=None):
        indent = "  " * level
        percent = f" ({(self.amount / income * 100):.2f}%)" if income else ""
        print(f"{indent}{self.name}: ${self.amount:.2f}{percent}")
        for child in self.children:
            child.display(level + 1, income)

# Get income
income = float(input("Enter your monthly income: $"))
remaining_money = income

# Create root node
root = ExpenseNode("Expenses")

# Add expenses
while True:
    print(f"\nMoney remaining: ${remaining_money:.2f}")
    add_expense = input("Do you want to add an expense? (yes/no): ").lower()
    if add_expense != 'yes':
        break

    try:
        num_sub = int(input(f"How many subcategories do you want to add for '{exp_name}'? "))
    except ValueError:
        print("Invalid number. Skipping subcategories.")
        num_sub = 0
    total_expense = 0

        for _ in range(num_sub):
            sub_name = input("  Enter subcategory name: ")
            sub_amount = float(input(f"  Enter amount for {sub_name}: $"))
            total_expense += sub_amount
            sub_node = ExpenseNode(sub_name)
            sub_node.amount = sub_amount
            expense.add_child(sub_node)
    else:
        amount = float(input(f"Enter amount for {exp_name}: $"))
        total_expense = amount
        expense.amount = amount

    remaining_money -= total_expense
    if remaining_money < 0:
        print("Warning: You have spent more than your income!")
        remaining_money = 0

    root.add_child(expense)

# Add leftover to savings
if remaining_money > 0:
    savings = ExpenseNode("Savings")
    savings.amount = remaining_money
    root.add_child(savings)

# Final report
root.calculate_total()
print("\nYour Expense Report:")
root.display(income=income)

print(f"\nTotal Income: ${income:.2f}")
total_spent = income - remaining_money
print(f"Total Spent: ${total_spent:.2f}")
print(f"Remaining (Savings): ${remaining_money:.2f}")
percent_spent = (total_spent / income) * 100
print(f"Percent of Income Spent: {percent_spent:.2f}%")
