#First iteration: Student grade calculator with GUI

import tkinter as tk
from tkinter import messagebox

# Function to calculate grade
def calculate_grade(marks):
    if marks <= 50:
        return "NA"
    elif 51 <= marks <= 75:
        return "A"
    elif 76 <= marks <= 89:
        return "M"
    elif 90 <= marks <= 100:
        return "E"

def on_calculate():
    student_name = entry_name.get()
    marks_str = entry_marks.get()
    try:
        marks = float(marks_str)
        if marks < 0 or marks > 100:
            messagebox.showerror("Invalid Input", "Please enter marks between 0 and 100.")
            return
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for marks.")
        return

    grade = calculate_grade(marks)
    label_result.config(text=f"{student_name}'s grade is: {grade}")

# Create main window
root = tk.Tk()
root.title("Student Grade Calculator")

# Student name label and entry
label_name = tk.Label(root, text="Enter the student's name:")
label_name.pack()
entry_name = tk.Entry(root)
entry_name.pack()

# Marks label and entry
label_marks = tk.Label(root, text="Enter the student's marks (0-100):")
label_marks.pack()
entry_marks = tk.Entry(root)
entry_marks.pack()

# Calculate button
button_calculate = tk.Button(root, text="Calculate Grade", command=on_calculate)
button_calculate.pack()

# Result label
label_result = tk.Label(root, text="")
label_result.pack()
