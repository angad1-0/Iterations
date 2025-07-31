#First iteration: Student grade calculator

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

# Get student name and marks as input
student_name = input("Enter the student's name: ")
marks = float(input("Enter the student's marks (0-100): "))

# Validate marks input
if marks < 0 or marks > 100:
    print("Invalid marks entered. Please enter a number between 0 and 100.")
else:
    grade = calculate_grade(marks)
    print(f"{student_name}'s grade is: {grade}")