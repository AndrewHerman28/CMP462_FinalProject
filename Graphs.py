import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

def make_pie_chart(fig, values, names, pos, chart_name):
    pie_chart = fig.add_subplot(pos)
    wedges, texts, autotexts = pie_chart.pie(values, labels=names, autopct='%1.1f%%',
                                             startangle=90, shadow=True,
                                             colors=plt.cm.Paired.colors)  # Use color palette for better distinction
    pie_chart.set_title(chart_name)

    for text in texts:
        text.set_fontsize(12)  # Adjust label font size for readability
    for autotext in autotexts:
        autotext.set_fontsize(12)  # Adjust percentage font size
        autotext.set_color('white')  # Make percentage text white for contrast

    ax = plt.gca()
    ax.set_axis_off()


def make_bar_graph(fig, values, names, pos, chart_name):
    bar_graph = fig.add_subplot(pos)
    bars = bar_graph.bar(names, values, color=plt.cm.Set3.colors, width=0.5)  # Use a nice color palette

    bar_graph.set_title(chart_name, pad=10)
    bar_graph.set_xlabel("Categories", labelpad=10)
    bar_graph.set_ylabel("Amount ($)", labelpad=10)

    bar_graph.margins(y=0.2)
    bar_graph.set_xticks(range(len(names)))
    bar_graph.set_xticklabels(names, rotation=45, ha="right", fontsize=10)  # Rotating labels for clarity

    # Add gridlines to improve readability
    bar_graph.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Adjust subplot spacing
    fig.subplots_adjust(bottom=0.2)


def make_line_graph(fig, values, dates, pos, chart_name):
    sorted_dates = sorted(dates)

    line_chart = fig.add_subplot(pos)
    line_chart.plot(sorted_dates, values, marker='o', linestyle='-', color='dodgerblue', markersize=8, linewidth=2)

    line_chart.set_title(chart_name, pad=10)
    line_chart.set_xlabel("Date")
    line_chart.set_ylabel("Amount Spent")

    line_chart.set_xticks(sorted_dates[::2])  # Show fewer x-ticks for better readability
    line_chart.set_xticklabels(sorted_dates[::2], rotation=45, ha="right", fontsize=10)

    # Add gridlines to make trends clearer
    line_chart.grid(True, axis='both', linestyle='--', alpha=0.6)
