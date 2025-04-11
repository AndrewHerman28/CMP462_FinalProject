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
    has_expense = input("Do you have an expense to add? (yes/no): ").strip().lower()
    if has_expense not in ['yes', 'no']:
        print("Invalid input. Please enter 'yes' or 'no'.")
        continue
    if has_expense == 'no':
        break

    exp_name = input("Enter expense category name: ").strip()
    exp_date = input("Enter date (YYYY-MM-DD): ").strip()
    if not exp_date:
        print("Invalid date. Try again.")
        continue

    tree = Tree(exp_name, exp_date)
    exp_amount = 0

    try:
        num_sub = int(input(f"How many subcategories does '{exp_name}' have? (0 for none): "))
        if num_sub < 0:
            print("Subcategory count can't be negative.")
            continue
    except ValueError:
        print("Invalid number.")
        continue

    if num_sub > 0:
        for _ in range(num_sub):
            sub_name = input("  Enter subcategory name: ").strip()
            try:
                sub_amount = float(input(f"  Enter amount for {sub_name}: $"))
                if sub_amount < 0:
                    print("  Amount can't be negative.")
                    continue
                exp_amount += sub_amount
                tree.insert(sub_name, sub_amount)
            except ValueError:
                print("  Invalid amount. Skipping this subcategory.")
    else:
        try:
            sub_amount = float(input(f"Enter amount for {exp_name}: $"))
            if sub_amount < 0:
                print("Amount can't be negative.")
                continue
            exp_amount += sub_amount
            tree.insert(exp_name, sub_amount)
        except ValueError:
            print("Invalid amount.")
            continue

    total_spent += exp_amount
    expense_trees.append(tree)


# Search or Remove interaction
while True:
    action = input("\nWould you like to search or remove an expense? (search/remove/none): ").lower()
    if action not in ['search', 'remove', 'none']:
        print("Invalid action. Please choose 'search', 'remove', or 'none'.")
        continue
    if action == "none":
        break

    if action == "search":
        print("\n--- Choose Filters for Search ---")
        use_name = input("Filter by name? (yes/no): ").strip().lower() == 'yes'
        use_amount = input("Filter by amount? (yes/no): ").strip().lower() == 'yes'
        use_date = input("Filter by date? (yes/no): ").strip().lower() == 'yes'

        if not (use_name or use_amount or use_date):
            print("You must select at least one filter.")
            continue

        search_name = None
        search_amount = None
        search_date = None

        if use_name:
            search_name = input("Enter subcategory name: ").strip()
        if use_amount:
            try:
                search_amount = float(input("Enter amount: $"))
            except ValueError:
                print("Invalid amount.")
                continue
        if use_date:
            search_date = input("Enter date (YYYY-MM-DD): ").strip()
            if not search_date:
                print("Invalid date.")
                continue

        results = []
        for tree in expense_trees:
            def matches_criteria(node):
                if use_name and node.name != search_name:
                    return False
                if use_amount and node.amount != search_amount:
                    return False
                if use_date and tree.date != search_date:
                    return False
                return True

            def traverse(node):
                if node is None:
                    return
                traverse(node.left)
                if matches_criteria(node):
                    results.append({
                        "category": tree.name,
                        "subcategory": node.name,
                        "amount": node.amount,
                        "date": tree.date
                    })
                traverse(node.right)

            traverse(tree.root)

        if results:
            print("\nSearch Results:")
            for r in results:
                print(f"Category: {r['category']} | Subcategory: {r['subcategory']} | Amount: ${r['amount']:.2f} | Date: {r['date']}")
        else:
            print("No matches found.")

    elif action == "remove":
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

        node = tree.list_subcategories(tree.root)
        match = next((item for item in node if item[0] == sub_name), None)

        if match:
            tree.remove(sub_name)
            total_spent -= match[1]
            print(f"'{sub_name}' removed from '{tree.name}' on {tree.date}.")
        else:
            print(" Subcategory not found.")


# Final display
print("\nYour Expense Report:")
for tree in expense_trees:
    print(f"\nCategory: {tree.name} (Date: {tree.date}) - Total: ${tree.total_amount:.2f}")
    tree.display(tree.root, total_spent=total_spent)

print(f"\nTotal Spent: ${total_spent:.2f}")
