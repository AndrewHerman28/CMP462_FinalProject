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

    def get_min(self, node):
        while node.left is not None:
            node = node.left
        return node

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
            return node.group, node.name, node.amount, node.date
        elif amount < node.amount:
            return self.search(node.left, amount)
        elif amount > node.amount:
            return self.search(node.right, amount)
        else:
            return None, None, None

    # New Remove Function
    def remove(self, root, name, amount):
        def replacement(nodeRoot):
            # when item has 2 children
            nodeRoot = nodeRoot.right
            while nodeRoot is not None and nodeRoot.left is not None:
                nodeRoot = nodeRoot.left
            return nodeRoot

        if root is None:  # base
            return root

        if root.amount > amount:  # 1 child
            root.left = self.remove(root.left, name, amount)
        elif root.amount < amount:  # 1 child
            root.right = self.remove(root.right, name, amount)

        else:  # 2 children
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left

            newRoot = replacement(root)
            root.name = newRoot.name
            root.right = self.remove(root.right, newRoot.name, amount)

        return root

    def display(self, node):
        # displays expenses in tree format
        if node is not None:
            self.display(node.left)
            print(f"[{node.group}]" + f" {node.name}: ${node.amount:.2f} ({node.date})")
            self.display(node.right)

    def traverse(self, node):
        if node:
            self.traverse(node.left)
            print(node.group, node.name, node.amount, node.date)
            self.traverse(node.right)

    def newSearch(self, node, group, name, from_date, to_date, amount, nodes):
        if node is None:
            return None

        f_date = HelperFunctions.convert_to_date(from_date)
        t_date = HelperFunctions.convert_to_date(to_date)

        if node:
            node_date = HelperFunctions.convert_to_date(node.date)
            self.newSearch(node.left, group, name, from_date, to_date, amount, nodes)
            if (group == node.group or group is None
                    and name == node.name or name is None
                    and f_date <= node_date <= t_date
                    and amount == node.amount or amount is None):
                nodes.append([node.group, node.name, node.amount, node.date])
            self.newSearch(node.right, group, name, from_date, to_date, amount, nodes)

        return nodes
