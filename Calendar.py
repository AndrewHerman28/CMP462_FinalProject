import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

def open_calendar(target_entry):
    def confirm_date():
        selected_date = cal.get_date()
        target_entry.delete(0, tk.END)
        target_entry.insert(0, selected_date)
        top.destroy()

    # Popup window for calendar
    top = tk.Toplevel(root)
    top.title("Select Date")
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=10)

    confirm_btn = ttk.Button(top, text="OK", command=confirm_date)
    confirm_btn.pack(pady=5)

# Main window
root = tk.Tk()
root.title("Date Range Selector")
root.geometry("350x200")
root.resizable(False, False)

# From Date
ttk.Label(root, text="From Date:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
from_entry = ttk.Entry(root, width=20)
from_entry.grid(row=0, column=1, padx=5)
ttk.Button(root, text="📅", width=3, command=lambda: open_calendar(from_entry)).grid(row=0, column=2)

# To Date
ttk.Label(root, text="To Date:", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
to_entry = ttk.Entry(root, width=20)
to_entry.grid(row=1, column=1, padx=5)
ttk.Button(root, text="📅", width=3, command=lambda: open_calendar(to_entry)).grid(row=1, column=2)

# Run the GUI
root.mainloop()
