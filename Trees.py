class Node:
    def __init__(self, name, date, amount=0):
        self.name = name
        self.amount = amount
        self.date = date
        self.left = None
        self.right = None

class Tree:
    def __init__(self, name):
        self.root = None
        self.name = name
        self.total_amount = 0

    def insert(self, name, date, amount):
        # inserts a node into the tree
        new_node = Node(name, date, amount)
        self.total_amount += amount

        if self.root is None:
            self.root = new_node  # first subcategory becomes root
        else:
            current = self.root
            while True:
                if amount < current.amount:
                    if current.left is None:
                        current.left = new_node
                        break
                    current = current.left
                else:
                    if current.right is None:
                        current.right = new_node
                        break
                    current = current.right

    def display(self, node, level=0, total_spent=1):
        # displays expenses in tree format
        if node is not None:
            self.display(node.left, level + 1, total_spent)
            percent_of_total = (node.amount / total_spent) * 100 if total_spent > 0 else 0
            print("  " * level + f"{node.name}: ${node.amount:.2f} ({percent_of_total:.2f}% of total)")
            self.display(node.right, level + 1, total_spent)


# stores all expense trees
expense_trees = []
total_spent = 0

# loop to add expenses
while True:
    has_expense = input("Do you have an expense to add? (yes/no): ").lower()
    if has_expense != 'yes':
        break

    exp_name = input("Enter expense name: ")
    expense_tree = Tree(exp_name)
    exp_amount = 0

    exp_date = input("Enter expense date: ")

    num_sub = int(input(f"How many subcategories does '{exp_name}' have? (0 for none): "))

    if num_sub > 0:
        sub_name = input("  Enter subcategory name: ")
        sub_amount = float(input(f"  Enter amount for {sub_name}: $"))
        exp_amount += sub_amount
        expense_tree.insert(sub_name, exp_date, sub_amount)  # first subcategory becomes root

        for _ in range(num_sub - 1):
            sub_name = input("  Enter subcategory name: ")
            sub_amount = float(input(f"  Enter amount for {sub_name}: $"))
            exp_amount += sub_amount
            expense_tree.insert(sub_name, exp_date, sub_amount)
    else:
        exp_amount = float(input(f"Enter amount for {exp_name}: $"))
        expense_tree.insert(exp_name, exp_date, exp_amount)

    total_spent += exp_amount
    expense_trees.append(expense_tree)

# display expense report
print("\nYour Expense Report:")
for tree in expense_trees:
    print(f"\nExpense Category: {tree.name} (Total: ${tree.total_amount:.2f})")
    tree.display(tree.root, total_spent=total_spent)

# print total spent
print(f"\nTotal Spent: ${total_spent:.2f}")
