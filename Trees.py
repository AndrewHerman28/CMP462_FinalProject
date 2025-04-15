class Node:
    def __init__(self, group, name, date, amount=0):
        self.group = group
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

    def insert(self, group, name, date, amount):
        # inserts a node into the tree
        new_node = Node(group, name, date, amount)
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

    def search(self, node, amount):

        if node is None:
            return None
        if node.amount == amount:
            return node.group, node.amount, node.date
        elif amount < node.amount:
            self.search(node.left, amount)
            return node.left.group, node.left.amount, node.left.date
        elif amount > node.amount:
            self.search(node.right, amount)
            return node.right.group, node.right.amount, node.right.date
        else:
            return None, None, None

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

    def display(self, node, level=0, total_spent=1):
        # displays expenses in tree format
        if node is not None:
            self.display(node.left, level + 1, total_spent)
            print(f"[{node.group}]" + f" {node.name}: ${node.amount:.2f} ({node.date})")
            self.display(node.right, level + 1, total_spent)
