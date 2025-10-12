import tkinter as tk
from tkinter import messagebox, ttk

# Classes for the student management system

# This class is for a person. It has a name.
class Person:
    def __init__(self, name):
        # Save the name of the person.
        self.name = name

# This class is for a student. A student is a person with extra details.
class Student(Person):
    def __init__(self, name, student_id):
        # Use the Person class to set the name.
        super().__init__(name)
        # Save the student ID.
        self.student_id = student_id
        # Make a list to keep the courses this student takes.
        self.courses = []  # list of Course objects

    # This function adds a course to the student's list.
    def add_course(self, course):
        self.courses.append(course)

class Course:
    def __init__(self, course_name, grade):
        self.course_name = course_name
        self.grade = grade

class Gradebook:
    def __init__(self):
        self.students = []  # list of Student objects

    def add_student(self, student):
        # Check if student already exists by student_id
        for s in self.students:
            if s.student_id == student.student_id:
                return False  # student already exists
        self.students.append(student)
        return True

    def get_student(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                return s
        return None

    def add_course_to_student(self, student_id, course):
        student = self.get_student(student_id)
        if student:
            student.add_course(course)
            return True
        return False

# GUI Application

# This class creates the main application window and handles user interaction.
class StudentManagementApp:
    def __init__(self, root):
        # Save the main window object.
        self.root = root
        # Set the title of the main window.
        self.root.title("Student Management System")
        # Set the size of the main window to 400x200 pixels.
        self.root.geometry("400x200")
        self.root.configure(bg='#FFFF00')  # Set background color to bright yellow

        # Try to load an image, but handle the case if it doesn't exist
        try:
            self.image = tk.PhotoImage(file="path_to_image.png")  # Use the correct path to your image file
            self.image_label = tk.Label(root, image=self.image)  # Create label with image
            self.image_label.pack(pady=10)  # Pack the image with some padding
        except tk.TclError:
            # If image doesn't exist, skip it
            pass

        # Create a Gradebook object to keep track of students.
        self.gradebook = Gradebook()

        # Create a label widget that asks the user if they want to add a student.
        self.label = tk.Label(root, text="Do you want to add a student?", bg='#FFFF00', fg='black')
        # Add the label to the window with some vertical padding.
        self.label.pack(pady=20)

        # Create a button labeled "Yes" that opens the student form when clicked.
        self.btn_yes = tk.Button(root, text="Yes", width=10, command=self.open_student_form, bg='#FFD700')
        # Place the "Yes" button on the left side with horizontal padding.
        self.btn_yes.pack(side=tk.LEFT, padx=50)

        # Create a button labeled "No" that quits the program when clicked.
        self.btn_no = tk.Button(root, text="No", width=10, command=self.quit_program, bg='#FFD700')
        # Place the "No" button on the right side with horizontal padding.
        self.btn_no.pack(side=tk.RIGHT, padx=50)

    # This method opens a new window to add student details.
    def open_student_form(self):
        # Create a new window on top of the main window.
        self.form = tk.Toplevel(self.root)
        # Set the title of this new window.
        self.form.title("Add Student")
        self.form.configure(bg='red')  # Set background color to red
        # Set the size of this window.
        self.form.geometry("400x350")

        # Create a label for "Student Name" and place it in the grid.
        tk.Label(self.form, text="Student Name:", bg='red', fg='white').grid(row=0, column=0, padx=10, pady=10, sticky="e")
        # Create an entry box for the user to type the student's name.
        self.entry_name = tk.Entry(self.form)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)

        # Create a label for "Student ID" and place it in the grid.
        tk.Label(self.form, text="Student ID:", bg='red', fg='white').grid(row=1, column=0, padx=10, pady=10, sticky="e")
        # Create an entry box for the user to type the student ID.
        self.entry_id = tk.Entry(self.form)
        self.entry_id.grid(row=1, column=1, padx=10, pady=10)

        # Create a label for "Course Name" and place it in the grid.
        tk.Label(self.form, text="Course Name:", bg='red', fg='white').grid(row=2, column=0, padx=10, pady=10, sticky="e")
        # Create an entry box for the user to type the course name.
        self.entry_course = tk.Entry(self.form)
        self.entry_course.grid(row=2, column=1, padx=10, pady=10)

        # Create a label for "Marks" and place it in the grid.
        tk.Label(self.form, text="Marks:", bg='red', fg='white').grid(row=3, column=0, padx=10, pady=10, sticky="e")
        # Create an entry box for the user to type the marks.
        self.entry_marks = tk.Entry(self.form)
        self.entry_marks.grid(row=3, column=1, padx=10, pady=10)

        # Create a button labeled "Submit" that calls submit_student when clicked.
        tk.Button(self.form, text="Submit", command=self.submit_student, bg='#FF6B6B').grid(row=4, column=0, columnspan=2, pady=20)

        # Create a button labeled "Show All Students" that calls show_all_students when clicked.
        tk.Button(self.form, text="Show All Students", command=self.show_all_students, bg='#FF6B6B').grid(row=5, column=0, columnspan=2, pady=10)

    # This method calculates the grade based on the marks given.
    def calculate_grade(self, marks):
        try:
            # Try to convert the marks to an integer number.
            marks = int(marks)
        except ValueError:
            # If conversion fails, return "NA" meaning not available.
            return "NA"
        # If marks are 90 or above, grade is Excellence.
        if marks >= 90:
            return "Excellence"
        # If marks are 80 or above, grade is Merit.
        elif marks >= 80:
            return "Merit"
        # If marks are 50 or above, grade is Achieved.
        elif marks >= 50:
            return "Achieved"
        # Otherwise, grade is NA.
        else:
            return "NA"

    def submit_student(self):
        # Get input values from text fields and remove any leading/trailing spaces
        name = self.entry_name.get().strip()
        student_id = self.entry_id.get().strip()
        course_name = self.entry_course.get().strip()
        marks = self.entry_marks.get().strip()

        # Check if any fields are empty; if so, show error message and stop
        if not (name and student_id and course_name and marks):
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        # Validate that marks is a numerical value
        try:
            int(marks)
        except ValueError:
            messagebox.showerror("Input Error", "Marks must be a numerical value.")
            return

        # Convert marks to a letter grade (A, B, C, etc.)
        grade = self.calculate_grade(marks)

        # Try to find the student in the gradebook using their ID
        student = self.gradebook.get_student(student_id)
        if not student:
            # If student not found, create a new Student object and add to gradebook
            student = Student(name, student_id)
            self.gradebook.add_student(student)

        # Create a Course object and add it to the student's list of courses
        course = Course(course_name, grade)
        student.add_course(course)

        # Clear the input fields so the form is empty again
        self.entry_name.delete(0, tk.END)
        self.entry_id.delete(0, tk.END)
        self.entry_course.delete(0, tk.END)
        self.entry_marks.delete(0, tk.END)

        # Open the window that shows the student's info
        self.open_student_info_window(student)

    def open_student_info_window(self, student):
        # Create a new popup window (Toplevel is a separate window on top of the main one)
        self.info_window = tk.Toplevel(self.form)
        self.info_window.title(f"Student Info - {student.name}")
        self.info_window.configure(bg='green')  # Set background color to green
        self.info_window.geometry("500x400")

        # Display the student's name and ID using Label widgets
        tk.Label(self.info_window, text=f"Name: {student.name}", bg='green', fg='white').grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Label(self.info_window, text=f"Student ID: {student.student_id}", bg='green', fg='white').grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Treeview is a widget that shows data in table format (like a list of courses and grades)
        tree = ttk.Treeview(self.info_window)
        tree["columns"] = ("Course", "Grade")  # Define columns (no index column)
        tree.heading("Course", text="Course")  # Set the header for the Course column
        tree.column("Course", width=250)       # Set the width for the Course column
        tree.heading("Grade", text="Grade")    # Set the header for the Grade column
        tree.column("Grade", width=150)        # Set the width for the Grade column

        # Loop through the student’s courses and add them as rows in the tree
        for course in student.courses:
            tree.insert("", "end", values=(course.course_name, course.grade))  # Insert row into table

        # Place the Treeview in the window layout using grid
        tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Section for adding/updating a course for the student
        tk.Label(self.info_window, text="Add/Update Course:", bg='green', fg='white').grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Input field for new course name
        tk.Label(self.info_window, text="Course Name:", bg='green', fg='white').grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.new_course_entry = tk.Entry(self.info_window)
        self.new_course_entry.grid(row=4, column=1, padx=10, pady=5)

        # Input field for new marks
        tk.Label(self.info_window, text="Marks:", bg='green', fg='white').grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.new_marks_entry = tk.Entry(self.info_window)
        self.new_marks_entry.grid(row=5, column=1, padx=10, pady=5)

        # Button that updates the student’s record (lambda is used to send student and treeview as arguments)
        tk.Button(self.info_window, text="Update Record", command=lambda: self.update_student_record(student, tree)).grid(row=6, column=0, columnspan=2, pady=15)

        # Exit button beneath the Update Record button
        tk.Button(self.info_window, text="Exit", command=self.info_window.destroy).grid(row=7, column=0, columnspan=2, pady=10)

        # Allow row 2 and column 1 to expand if the window is resized
        self.info_window.grid_rowconfigure(2, weight=1)
        self.info_window.grid_columnconfigure(1, weight=1)

        # Show a message once the student info window is opened
        messagebox.showinfo("Info", "You are now opening the student info window.")

    def update_student_record(self, student, tree):
        # Get input values from the new course fields
        course_name = self.new_course_entry.get().strip()
        marks = self.new_marks_entry.get().strip()

        # Show error if either input is empty
        if not (course_name and marks):
            messagebox.showerror("Input Error", "Please fill in both course name and marks.")
            return

        # Validate that marks is a numerical value
        try:
            int(marks)
        except ValueError:
            messagebox.showerror("Input Error", "Marks must be a numerical value.")
            return

        # Convert the marks to a grade
        grade = self.calculate_grade(marks)

        # Check if the course already exists; if so, update its grade
        for course in student.courses:
            if course.course_name == course_name:
                course.grade = grade
                break
        else:
            # If course doesn't exist, create and add a new one
            new_course = Course(course_name, grade)
            student.add_course(new_course)

        # Clear the Treeview and refresh it with updated course data
        for item in tree.get_children():
            tree.delete(item)
        for idx, course in enumerate(student.courses, start=1):
            tree.insert("", "end", text=str(idx), values=(course.course_name, course.grade))

        # Clear the new course entry fields
        self.new_course_entry.delete(0, tk.END)
        self.new_marks_entry.delete(0, tk.END)

    # the messagebox thanks the user for using the program and helps the user exit the code
    def show_all_students(self):
        """Display a window showing all students in the gradebook."""
        if not self.gradebook.students:
            messagebox.showinfo("No Students", "There are no students in the system yet.")
            return
            
        all_students_window = tk.Toplevel(self.form)
        all_students_window.title("All Students")
        all_students_window.geometry("600x400")
        
        # Create a treeview to display all students and their courses
        tree = ttk.Treeview(all_students_window)
        tree["columns"] = ("Student ID", "Name", "Course", "Grade")
        tree.heading("#0", text="Index")
        tree.column("#0", width=50)
        tree.heading("Student ID", text="Student ID")
        tree.column("Student ID", width=100)
        tree.heading("Name", text="Name")
        tree.column("Name", width=150)
        tree.heading("Course", text="Course")
        tree.column("Course", width=150)
        tree.heading("Grade", text="Grade")
        tree.column("Grade", width=100)
        
        # Populate the treeview with all students and their courses
        index = 1
        for student in self.gradebook.students:
            if student.courses:
                for course in student.courses:
                    tree.insert("", "end", text=str(index), 
                              values=(student.student_id, student.name, course.course_name, course.grade))
                    index += 1
            else:
                tree.insert("", "end", text=str(index), 
                          values=(student.student_id, student.name, "No courses", ""))
                index += 1
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add a close button
        tk.Button(all_students_window, text="Close", command=all_students_window.destroy).pack(pady=10)

    def quit_program(self):
        messagebox.showinfo("Exit", "Thanks for using the Student Management System")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()  # Creates the main application window
    app = StudentManagementApp(root)  # Initializes the Student Management App
    root.mainloop()  # Runs the Tkinter event loop so the window stays open
    

