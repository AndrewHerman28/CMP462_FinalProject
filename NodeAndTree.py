class Node:
    def __init__(self, value, name, date):
        self.value = value
        self.name = name
        self.date = date
        self.left = None
        self.right = None


class Tree:
    def __init__(self, name):
        self.root = None
        self.name = name

    def insert(self, value, name, date):
        self.root = self._insert_rec(self.root, value, name, date)

    def _insert_rec(self, root, value, name, date):
        if root is None:
            return Node(value, name, date)

        if value < root.value:
            root.left = self._insert_rec(root.left, value, name, date)
        else:
            root.right = self._insert_rec(root.right, value, name, date)

        return root


    def convert_to_list(self, current, items = None):
        if items is None:
            items = []

        if current:
            self.convert_to_list(current.left, items)
            items.append(current)
            self.convert_to_list(current.right, items)

        return items






