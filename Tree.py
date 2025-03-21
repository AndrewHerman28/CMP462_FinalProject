class AccountingTree:
    def __init__(self):
        self.root = TreeNode(0)  # Root is neutral (0)
        self.net_earnings = [0]  # Tracks cumulative earnings

    def insert(self, value):
        self._insert_node(self.root, value)
        self.net_earnings.append(self.net_earnings[-1] + value)  # Update net earnings

    def _insert_node(self, node, value):
        if value < 0:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_node(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_node(node.right, value)

    def display_graph(self):
        plt.plot(self.net_earnings, marker='o', linestyle='-', color='b')
        plt.xlabel("Transactions")
        plt.ylabel("Net Earnings")
        plt.title("Net Earnings Over Time")
        plt.grid()
        plt.show()
