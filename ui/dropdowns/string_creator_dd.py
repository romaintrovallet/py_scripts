import tkinter as tk
from tkinter import ttk

# Can only be "pack" or "grid"
LOOK = "pack"

first_options = ["This", "It"]
second_options = ["is", "was", "will be"]
third_options = ["a test", "a failure", "a succes"]

sentence = [None] * 3

def print_first_selected(event):
    select = first_dropdown.get()
    sentence [0] = select
    print(f"First dropdown value = {select}")

def print_second_selected(event):
    select = second_dropdown.get()
    sentence [1] = select
    print(f"Second dropdown value = {select}")

def print_third_selected(event):
    select = third_dropdown.get()
    sentence [2] = select
    print(f"Third dropdown value = {select}")

def print_sentence():
    sentence_str = ' '.join(sentence)
    result_label.configure(text=sentence_str)
    print(sentence_str)

root = tk.Tk()
root.title("Dropdown Menus")

# First Dropdown
first_label = tk.Label(root, text="Select a first option:")
first_dropdown = ttk.Combobox(root, values=first_options)
first_dropdown.bind("<<ComboboxSelected>>", print_first_selected)
if LOOK == "grid":
    first_label.grid(row=0, column=0)
    first_dropdown.grid(row=0, column=1)
elif LOOK == "pack":
    first_label.pack()
    first_dropdown.pack()

# Second Dropdown
second_label = tk.Label(root, text="Select a second option:")
second_dropdown = ttk.Combobox(root, values=second_options)
second_dropdown.bind("<<ComboboxSelected>>", print_second_selected)
if LOOK == "grid":
    second_label.grid(row=1, column=0)
    second_dropdown.grid(row=1, column=1)
elif LOOK == "pack":
    second_label.pack()
    second_dropdown.pack()

# Third Dropdown
third_label = tk.Label(root, text="Select a third option:")
third_dropdown = ttk.Combobox(root, values=third_options)
third_dropdown.bind("<<ComboboxSelected>>", print_third_selected)
if LOOK == "grid":
    third_label.grid(row=2, column=0)
    third_dropdown.grid(row=2, column=1)
elif LOOK == "pack":
    third_label.pack()
    third_dropdown.pack()

sentence_button = tk.Button(root, text="Print sentence", command=print_sentence)
sentence_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()