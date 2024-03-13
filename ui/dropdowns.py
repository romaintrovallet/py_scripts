import tkinter as tk
from tkinter import ttk

def update_second_dropdown(event):
    selected_option = first_dropdown.get()
    if selected_option == "A":
        second_dropdown.grid(row=1, column=1)
        third_dropdown.grid_forget()
    elif selected_option == "B":
        second_dropdown.grid_forget()
        third_dropdown.grid_forget()
    elif selected_option == "C":
        second_dropdown.grid_forget()
        third_dropdown.grid(row=1, column=1)

root = tk.Tk()
root.title("Dropdown Menus")

# First Dropdown
first_label = tk.Label(root, text="Select an option:")
first_label.grid(row=0, column=0)
first_options = ["A", "B", "C"]
first_dropdown = ttk.Combobox(root, values=first_options)
first_dropdown.grid(row=0, column=1)
first_dropdown.bind("<<ComboboxSelected>>", update_second_dropdown)

# Second Dropdown
second_label = tk.Label(root, text="Select another option:")
second_options = ["L", "M"]
second_dropdown = ttk.Combobox(root, values=second_options)

# Third Dropdown
third_label = tk.Label(root, text="Select a third option:")
third_options = ["X", "Y", "Z"]
third_dropdown = ttk.Combobox(root, values=third_options)

root.mainloop()
