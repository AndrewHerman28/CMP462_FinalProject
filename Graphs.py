import matplotlib.pyplot as plt

def display_graph(self):
  plt.plot(self.net_earnings, marker='o', linestyle='-', color='b')
  plt.xlabel("Transactions")
  plt.ylabel("Net Earnings")
  plt.title("Net Earnings Over Time")
  plt.grid()
  plt.show()

display_graph()
