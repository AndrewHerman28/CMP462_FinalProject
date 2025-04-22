import tkinter as tk
from datetime import datetime


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
        date = datetime.strptime(date, "%m/%d/%Y")
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

    def newSearch(self, node, group, name, f_date, t_date, amount, nodes):
        if node is None:
            return nodes

        self.newSearch(node.left, group, name, f_date, t_date, amount, nodes)

        group_match = (group is None) or (group == node.group)  # If expense group matches or null
        name_match = (name is None) or (name == node.name)  # If name matches or null
        amount_match = (amount is None) or (amount == node.amount)  # If value matches or null
        from_date_match = (f_date is None) or (datetime.strptime(f_date, "%m/%d/%Y") <= node.date)  # If node date is greater than from date
        to_date_match = (t_date is None) or (datetime.strptime(t_date, "%m/%d/%Y") >= node.date)  # If node date is less than to date

        # If all matches are met add nodes to list
        if group_match and name_match and from_date_match and to_date_match and amount_match:
            nodes.append([node.group, node.name, node.amount, node.date])

        self.newSearch(node.right, group, name, f_date, t_date, amount, nodes)

        return nodes
