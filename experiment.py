class Node:
    def __init__(self, name, amount=0):
        self.name = name
        self.amount = amount
        self.left = None
        self.right = None


class Tree:
    def __init__(self, name, date):
        self.root = None
        self.name = name
        self.date = date
        self.total_amount = 0

    def insert(self, name, amount):
        new_node = Node(name, amount)
        self.total_amount += amount

        if self.root is None:
            self.root = new_node
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
        if node is not None:
            self.display(node.left, level + 1, total_spent)
            percent_of_total = (node.amount / total_spent) * 100 if total_spent > 0 else 0
            print("  " * level + f"{node.name}: ${node.amount:.2f} ({percent_of_total:.2f}% of total)")
            self.display(node.right, level + 1, total_spent)

    def search(self, node, name):
        if node is None:
            return None
        if node.name == name:
            return node
        elif name < node.name:
            return self.search(node.left, name)
        else:
            return self.search(node.right, name)

    def remove(self, name):
        def delete_node(root, name):
            if root is None:
                return root, None
            if name < root.name:
                root.left, deleted = delete_node(root.left, name)
            elif name > root.name:
                root.right, deleted = delete_node(root.right, name)
            else:
                self.total_amount -= root.amount
                if root.left is None:
                    return root.right, root
                elif root.right is None:
                    return root.left, root
                min_larger_node = self.get_min(root.right)
                root.name, root.amount = min_larger_node.name, min_larger_node.amount
                root.right, _ = delete_node(root.right, min_larger_node.name)
                deleted = root
            return root, deleted

        self.root, deleted_node = delete_node(self.root, name)
        return deleted_node is not None

    def get_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def list_subcategories(self, node, collected=None):
        if collected is None:
            collected = []
        if node:
            self.list_subcategories(node.left, collected)
            collected.append((node.name, node.amount))
            self.list_subcategories(node.right, collected)
        return collected


# --- Main Logic ---
expense_trees = []
total_spent = 0

# Entry loop
while True:
    has_expense = input("Do you have an expense to add? (yes/no): ").lower()
    if has_expense != 'yes':
        break

    exp_name = input("Enter expense category name: ")
    exp_date = input("Enter date (YYYY-MM-DD): ")
    tree = Tree(exp_name, exp_date)
    exp_amount = 0

    num_sub = int(input(f"How many subcategories does '{exp_name}' have? (0 for none): "))
    if num_sub > 0:
        for _ in range(num_sub):
            sub_name = input("  Enter subcategory name: ")
            sub_amount = float(input(f"  Enter amount for {sub_name}: $"))
            exp_amount += sub_amount
            tree.insert(sub_name, sub_amount)
    else:
        sub_amount = float(input(f"Enter amount for {exp_name}: $"))
        exp_amount += sub_amount
        tree.insert(exp_name, sub_amount)

    total_spent += exp_amount
    expense_trees.append(tree)


# Search or Remove interaction
while True:
    action = input("\nWould you like to search or remove an expense? (search/remove/none): ").lower()
    if action == "none":
        break

    # List categories
    print("\nAvailable Categories:")
    for i, tree in enumerate(expense_trees):
        print(f"{i + 1}. {tree.name} (Date: {tree.date})")

    try:
        selected_index = int(input("Select a category by number: ")) - 1
        if selected_index < 0 or selected_index >= len(expense_trees):
            print("Invalid selection.")
            continue
        tree = expense_trees[selected_index]
    except ValueError:
        print("Please enter a valid number.")
        continue

    # List subcategories
    subcategories = tree.list_subcategories(tree.root)
    if not subcategories:
        print("No subcategories found in this category.")
        continue

    print(f"\nSubcategories in '{tree.name}' (Date: {tree.date}):")
    for i, (sub_name, amt) in enumerate(subcategories):
        print(f"{i + 1}. {sub_name}: ${amt:.2f}")

    try:
        sub_index = int(input("Select a subcategory by number: ")) - 1
        if sub_index < 0 or sub_index >= len(subcategories):
            print("Invalid subcategory selection.")
            continue
        sub_name = subcategories[sub_index][0]
    except ValueError:
        print("Please enter a valid number.")
        continue

    # Perform action
    if action == "search":
        result = tree.search(tree.root, sub_name)
        if result:
            print(f"Found '{sub_name}' in '{tree.name}' on {tree.date}: ${result.amount:.2f}")
        else:
            print(" Subcategory not found.")

    elif action == "remove":
        node = tree.search(tree.root, sub_name)
        if node:
            tree.remove(sub_name)
            total_spent -= node.amount
            print(f"'{sub_name}' removed from '{tree.name}' on {tree.date}.")
        else:
            print(" Subcategory not found.")


# Final display
print("\nYour Expense Report:")
for tree in expense_trees:
    print(f"\nCategory: {tree.name} (Date: {tree.date}) - Total: ${tree.total_amount:.2f}")
    tree.display(tree.root, total_spent=total_spent)

print(f"\nTotal Spent: ${total_spent:.2f}")
