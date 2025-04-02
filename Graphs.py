import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def expenseReport(arr):
    values = []
    names = []
    dates = []

    for x in arr:
        values.append(x.value)
        names.append(x.name)
        dates.append(x.date)


    total = sum(values)

    # Create a figure and pie chart
    fig = Figure(figsize=(12, 8), dpi=100) #DPI is how sharp itll look but takes more memory

    # Adjust spacing between subplots
    fig.subplots_adjust(wspace=1)  # Increase spacing

    pie_chart = fig.add_subplot(121) #Row #Column #Position
    pie_chart.pie(values, labels=names, autopct='%1.1f%%')
    pie_chart.set_title("Pie Chart")

    # Bar chart with increased spacing
    ax1 = fig.add_subplot(122)
    bars = ax1.bar(names, values, color='blue', width=0.4)  # Decreased width to increase spacing

    # Improve spacing and readability
    ax1.set_title("Bar Chart", pad=15)  # Add padding to title
    ax1.set_xlabel("Categories", labelpad=10)  # Increase label padding
    ax1.set_ylabel("Values", labelpad=10)
    ax1.margins(y=0.2)  # Add margin above bars
    ax1.set_xticks(range(len(names)))  # Ensure correct x-tick positions
    ax1.set_xticklabels(names, rotation=30, ha="right")  # Rotate and align labels

    # Embed the figure in Tkinter window
    global canvas
    if 'canvas' in globals():
        canvas.get_tk_widget().destroy()  # Remove previous graph if exists

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().place(x=0, y=0)
    canvas.draw()

# Build Window
window = tk.Tk()
window.title("Personal Finance Manager")
window.geometry("1600x1000")  # Increased size to fit the graph
window.attributes("-topmost", 1)

expenseReport(tuple_values)
window.mainloop()
