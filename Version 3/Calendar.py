import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

def open_calendar(button, date):
    def confirm_date():
        selected_date = cal.get_date()
        date.set(selected_date)
        button.config(text = selected_date)
        top.destroy()

    # Popup window for calendar
    top = tk.Tk()
    top.attributes("-topmost", True)
    top.title("Select Date")
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=10)

    confirm_btn = ttk.Button(top, text="OK", command=confirm_date)
    confirm_btn.pack(pady=5)
