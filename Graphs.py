import matplotlib.pyplot as plt

# Get input values from the user
values = input("Enter numbers separated by spaces: ")
values = list(map(float, values.split()))  # Convert input to a list of floats

# Generate x values (indices of the input values)
x_values = list(range(1, len(values) + 1))

# Plot the values (The main function)
plt.plot(x_values, values, marker='o', linestyle='-', color='b', label='Input Values')

# Add labels and title
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Line Chart of Input Values')
plt.legend()
plt.grid()

# Show the graph
plt.show()
