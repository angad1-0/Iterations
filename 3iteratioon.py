#------- Bring in tools from tkinter to make windows and buttons-----#
import tkinter as tk
# -----Bring in extra tools for pop-up messages and tables-----
from tkinter import messagebox, ttk
# -----Bring in json for saving data to a file-----
import json

# ------These are blueprints for organizing information about students and courses------

#  - - - - - - - -Blueprint for a basic person, who just has a name - - - - - - -
class Person:
    def __init__(self, name):
        # Store the person's name in this object
        self.name = name

#  - -  - - - - -Blueprint for a student, who is a person plus more info - - - - - - - -
class Student(Person):
    def __init__(self, name, student_id):
        # First, set up the name using the Person blueprint
        super().__init__(name)
        # Store the unique ID number for this student
        self.student_id = student_id
        # Create an empty list to hold all the courses this student is taking
        self.courses = []  # list of Course objects

    # Function to add a new course to this student's list
    def add_course(self, course):
        # Put the course at the end of the list
        self.courses.append(course)

# Blueprint for a course, which has a name and a grade
class Course:
    def __init__(self, course_name, grade):
        # Store the name of the course, like "Math"
        self.course_name = course_name
        # Store the grade earned in this course, like "A" or "Merit"
        self.grade = grade

# -----Blueprint for the gradebook, which keeps track of all students-----
class Gradebook:
    def __init__(self):
        # Start with an empty list to hold all the students
        self.students = []  # list of Student objects

    #------ Function to add a new student to the gradebook-----
    def add_student(self, student):
        # Look through existing students to see if this ID is already used
        for s in self.students:
            if s.student_id == student.student_id:
                return False  # student already exists, so don't add
        # If not found, add the student to the list
        self.students.append(student)
        return True

    # Function to find a student by their ID
    def get_student(self, student_id):
        # Go through each student in the list
        for s in self.students:
            if s.student_id == student_id:
                return s  # Found the student, return it
        return None  # Didn't find the student

    # Function to add a course to a specific student
    def add_course_to_student(self, student_id, course):
        # Find the student first
        student = self.get_student(student_id)
        if student:
            # If student exists, add the course to them
            student.add_course(course)
            return True  # Success
        return False  # Student not found

# - - - - -The part that makes the windows and buttons you see on screen - - - - -

# Blueprint for the main app that shows windows and responds to clicks
class StudentManagementApp:
    def __init__(self, root):
        # Keep a reference to the main window
        self.root = root
        # Give the window a title that shows in the top bar
        self.root.title("Student Management System")
        # Make the window 400 pixels wide and 400 pixels tall
        self.root.geometry("400x400")
        # Paint the background bright yellow
        self.root.configure(bg='#FFFF00')  # Set background color to bright yellow

        self.role = None

        # Make a new gradebook to store all student info
        self.gradebook = Gradebook()

        # List to save all user inputs
        self.saved_inputs = []
        # Load saved inputs from file if exists
        self.load_saved_inputs()

        self.select_role()

    def select_role(self):
        # Create role selection window
        role_window = tk.Toplevel(self.root)
        role_window.title("Select Role")
        role_window.geometry("300x200")
        role_window.configure(bg='purple')

        tk.Label(role_window, text="Select your role:", bg='purple', fg='white').pack(pady=20)

        tk.Button(role_window, text="Student", command=lambda: self.set_role('student', role_window)).pack(pady=10)
        tk.Button(role_window, text="Teacher", command=lambda: self.set_role('teacher', role_window)).pack(pady=10)

    def set_role(self, role, window):
        self.role = role
        window.destroy()
        self.setup_main_ui()

    def setup_main_ui(self):
        #adding my images now
        try:
            # Load the image from a file (I put the right file path here)
            self.image = tk.PhotoImage(file="~/Documents/91909/gradetrack.png").subsample(4, 4)  # Use the correct path to my image file, resized to quarter size
            # Make a label to hold the image
            self.image_label = tk.Label(self.root, image=self.image)  # Create label with image
            # Put the image in the window with some space around it
            self.image_label.pack(pady=5)  # Pack the image with some padding
        except tk.TclError:
            # If the image file is missing, don't show anything
            pass

        # Make buttons for the main menu so users can choose what to do
        # Button to add a new student
        self.btn_add = tk.Button(self.root, text="Add Student", width=15, command=self.open_student_form, bg='#FFD700')
        self.btn_add.pack(pady=10)

        # Button to search for a student by ID
        self.btn_search = tk.Button(self.root, text="Search Student", width=15, command=self.search_student, bg='#FFD700')
        self.btn_search.pack(pady=10)

        # Button to show a list of all students
        self.btn_show_all = tk.Button(self.root, text="Show All Students", width=15, command=self.show_all_students, bg='#FFD700')
        self.btn_show_all.pack(pady=10)

        # Button to close the program
        self.btn_quit = tk.Button(self.root, text="Quit", width=15, command=self.quit_program, bg='#FFD700')
        self.btn_quit.pack(pady=10)

        if self.role == 'student':
            self.btn_search.config(state='disabled')
            self.btn_show_all.config(state='disabled')

    #   - - - - - Function to open a window where you can search for a student - - - - - -
    def search_student(self):
        # Make a new small window on top of the main one
        search_window = tk.Toplevel(self.root)
        # Title for this search window
        search_window.title("Search Student")
        # Size it to 300 wide by 150 tall
        search_window.geometry("300x150")
        # Make the background yellow like the main window
        search_window.configure(bg='#FFFF00')

        # Put a label asking for the student ID
        tk.Label(search_window, text="Enter Student ID:", bg='#FFFF00', fg='black').pack(pady=10)
        # Make a text box for typing the ID
        entry_id = tk.Entry(search_window)
        entry_id.pack(pady=5)

        # Inner function that runs when the search button is clicked
        def on_search():
            # Get the ID from the text box and remove extra spaces
            sid = entry_id.get().strip()
            # Look up the student in the gradebook
            student = self.gradebook.get_student(sid)
            if student:
                # If found, show the student's info window
                self.open_student_info_window(student)
                # Close the search window
                search_window.destroy()
            else:
                # If not found, show an error message
                messagebox.showerror("Not Found", "Student not found.")

        #  - - - - - -Make a button that says "Search" and runs the on_search function - - - - -
        tk.Button(search_window, text="Search", command=on_search, bg='#FFD700').pack(pady=10)

    #  - - - - -Function to open a window where you can add a new student or course - - - - - -
    def open_student_form(self):
        # Make a new window that pops up over the main one
        self.form = tk.Toplevel(self.root)
        # Name this window "Add Student"
        self.form.title("Add Student")
        # Color the background red
        self.form.configure(bg='red')  # Set background color to red
        # Make it 400 pixels wide and 350 pixels tall
        self.form.geometry("400x350")

        # Put a label saying "Student Name:" on the left
        tk.Label(self.form, text="Student Name:", bg='red', fg='white').grid(row=0, column=0, padx=10, pady=10, sticky="e")
        # Make a text box next to it for typing the name
        self.entry_name = tk.Entry(self.form)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)

        # Label for "Student ID:" on the left
        tk.Label(self.form, text="Student ID:", bg='red', fg='white').grid(row=1, column=0, padx=10, pady=10, sticky="e")
        # Text box for the ID
        self.entry_id = tk.Entry(self.form)
        self.entry_id.grid(row=1, column=1, padx=10, pady=10)

        # Label for "Course Name:" on the left
        tk.Label(self.form, text="Course Name:", bg='red', fg='white').grid(row=2, column=0, padx=10, pady=10, sticky="e")
        # Text box for the course name
        self.entry_course = tk.Entry(self.form)
        self.entry_course.grid(row=2, column=1, padx=10, pady=10)

        # Label for "Marks:" on the left
        tk.Label(self.form, text="Marks:", bg='red', fg='white').grid(row=3, column=0, padx=10, pady=10, sticky="e")
        # Text box for the marks (numbers)
        self.entry_marks = tk.Entry(self.form)
        self.entry_marks.grid(row=3, column=1, padx=10, pady=10)

        # Big button at the bottom that says "Submit" to save the info
        tk.Button(self.form, text="Submit", command=self.submit_student, bg='#FF6B6B').grid(row=4, column=0, columnspan=2, pady=20)

        # Another button to show all students
        tk.Button(self.form, text="Show All Students", command=self.show_all_students, bg='#FF6B6B').grid(row=5, column=0, columnspan=2, pady=10)

    # - - - - -  Function to turn marks (numbers) into a grade letter - - - - - - - -
    def calculate_grade(self, marks):
        try:
            # Try to change the marks from text to a number
            marks = int(marks)
        except ValueError:
            # If it's not a number, say "NA" for not available
            return "NA"
        # If the number is 90 or higher, give "Excellence"
        if marks >= 90:
            return "Excellence"
        # If 80 or higher, give "Merit"
        elif marks >= 80:
            return "Merit"
        # If 50 or higher, give "Achieved"
        elif marks >= 50:
            return "Achieved"
        # If lower than 50, give "NA"
        else:
            return "NA"

    # Function that runs when you click Submit to save the student info
    def submit_student(self):
        # Grab the text from each box and remove any extra spaces at the start or end
        name = self.entry_name.get().strip()
        student_id = self.entry_id.get().strip()
        course_name = self.entry_course.get().strip()
        marks = self.entry_marks.get().strip()

        # Make sure none of the boxes are empty; if any are, show an error and stop
        if not (name and student_id and course_name and marks):
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        # Save the inputs to the list and file
        input_data = {
            "name": name,
            "student_id": student_id,
            "course_name": course_name,
            "marks": marks
        }
        self.saved_inputs.append(input_data)
        self.save_saved_inputs()

        # Turn the marks number into a grade like "Merit"
        grade = self.calculate_grade(marks)

        # Look for the student in the gradebook by ID
        student = self.gradebook.get_student(student_id)
        if not student:
            # If this is a new student, make a Student object and add to gradebook
            student = Student(name, student_id)
            self.gradebook.add_student(student)

        # Make a Course object with the name and grade
        course = Course(course_name, grade)
        # Add this course to the student's list
        student.add_course(course)

        # Empty all the text boxes so you can enter new info
        self.entry_name.delete(0, tk.END)
        self.entry_id.delete(0, tk.END)
        self.entry_course.delete(0, tk.END)
        self.entry_marks.delete(0, tk.END)

        # Show a window with the student's details
        self.open_student_info_window(student)

    # Function to show a window with details about one student
    def open_student_info_window(self, student):
        # Make a new window that pops up to show student info
        self.info_window = tk.Toplevel(self.root)
        # Title it with the student's name
        self.info_window.title(f"Student Info - {student.name}")
        # Paint the background green
        self.info_window.configure(bg='green')  # Set background color to green
        # Size it to 500 wide by 400 tall
        self.info_window.geometry("500x400")

        # Show the student's name with a label
        tk.Label(self.info_window, text=f"Name: {student.name}", bg='green', fg='white').grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # Show the student's ID below it
        tk.Label(self.info_window, text=f"Student ID: {student.student_id}", bg='green', fg='white').grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Make a table (treeview) to list the courses and grades
        tree = ttk.Treeview(self.info_window)
        # Set up columns: one for Course name, one for Grade
        tree["columns"] = ("Course", "Grade")  # Define columns (no index column)
        # Label the Course column
        tree.heading("Course", text="Course")  # Set the header for the Course column
        # Make Course column 250 pixels wide
        tree.column("Course", width=250)       # Set the width for the Course column
        # Label the Grade column
        tree.heading("Grade", text="Grade")    # Set the header for the Grade column
        # Make Grade column 150 pixels wide
        tree.column("Grade", width=150)        # Set the width for the Grade column

        # For each course the student has, add a row to the table
        for course in student.courses:
            # Put the course name and grade in the row
            tree.insert("", "end", values=(course.course_name, course.grade))  # Insert row into table

        # Put the table in the window, making it take up space
        tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Below the table, add a section to add or change a course
        tk.Label(self.info_window, text="Add/Update Course:", bg='green', fg='white').grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Label and text box for entering a new course name
        tk.Label(self.info_window, text="Course Name:", bg='green', fg='white').grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.new_course_entry = tk.Entry(self.info_window)
        self.new_course_entry.grid(row=4, column=1, padx=10, pady=5)

        # Label and text box for entering marks for that course
        tk.Label(self.info_window, text="Marks:", bg='green', fg='white').grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.new_marks_entry = tk.Entry(self.info_window)
        self.new_marks_entry.grid(row=5, column=1, padx=10, pady=5)

        # Button to update the student's courses with the new info
        tk.Button(self.info_window, text="Update Record", command=lambda: self.update_student_record(student, tree)).grid(row=6, column=0, columnspan=2, pady=15)

        # Button to close this window
        tk.Button(self.info_window, text="Exit", command=self.info_window.destroy).grid(row=7, column=0, columnspan=2, pady=10)

        # Make sure the table can grow if the window gets bigger
        self.info_window.grid_rowconfigure(2, weight=1)
        self.info_window.grid_columnconfigure(1, weight=1)

        # Pop up a message saying the window is open
        messagebox.showinfo("Info", "You are now opening the student info window.")

    # Function to update a student's course when you click Update Record
    def update_student_record(self, student, tree):
        # Get the course name and marks from the text boxes
        course_name = self.new_course_entry.get().strip()
        marks = self.new_marks_entry.get().strip()

        # If either box is empty, show error and stop
        if not (course_name and marks):
            messagebox.showerror("Input Error", "Please fill in both course name and marks.")
            return

        # Turn marks into a grade
        grade = self.calculate_grade(marks)

        # Look through the student's courses to see if this course is already there
        for course in student.courses:
            if course.course_name == course_name:
                # If yes, just update the grade
                course.grade = grade
                break
        else:
            # If not, make a new course and add it
            new_course = Course(course_name, grade)
            student.add_course(new_course)

        # Remove all rows from the table
        for item in tree.get_children():
            tree.delete(item)
        # Add back all courses, now updated
        for idx, course in enumerate(student.courses, start=1):
            tree.insert("", "end", text=str(idx), values=(course.course_name, course.grade))

        # Clear the text boxes for next time
        self.new_course_entry.delete(0, tk.END)
        self.new_marks_entry.delete(0, tk.END)

    # Function to show a list of all students and their courses
    def show_all_students(self):
        # If there are no students, tell the user and stop
        if not self.gradebook.students:
            messagebox.showinfo("No Students", "There are no students in the system yet.")
            return

        # Make a new window for the list
        all_students_window = tk.Toplevel(self.root)
        all_students_window.title("All Students")
        all_students_window.geometry("600x400")

        # Make a table to show student ID, name, course, grade
        tree = ttk.Treeview(all_students_window)
        tree["columns"] = ("Student ID", "Name", "Course", "Grade")
        # Label the index column
        tree.heading("#0", text="Index")
        tree.column("#0", width=50)
        # Label Student ID column
        tree.heading("Student ID", text="Student ID")
        tree.column("Student ID", width=100)
        # Label Name column
        tree.heading("Name", text="Name")
        tree.column("Name", width=150)
        # Label Course column
        tree.heading("Course", text="Course")
        tree.column("Course", width=150)
        # Label Grade column
        tree.heading("Grade", text="Grade")
        tree.column("Grade", width=100)

        # Go through each student and add their info to the table
        index = 1
        for student in self.gradebook.students:
            if student.courses:
                # If they have courses, list each one
                for course in student.courses:
                    tree.insert("", "end", text=str(index),
                              values=(student.student_id, student.name, course.course_name, course.grade))
                    index += 1
            else:
                # If no courses, say "No courses"
                tree.insert("", "end", text=str(index),
                          values=(student.student_id, student.name, "No courses", ""))
                index += 1

        # Put the table in the window and make it fill the space
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add a button to close the window
        tk.Button(all_students_window, text="Close", command=all_students_window.destroy).pack(pady=10)

    # Function to quit the program when you click Quit
    def quit_program(self):
        # Show a thank you message
        messagebox.showinfo("Exit", "Thanks for using the Student Management System")
        # Close the main window and end the program
        self.root.destroy()

    # Function to save saved inputs to a JSON file
    def save_saved_inputs(self):
        try:
            with open('saved_inputs.json', 'w') as f:
                json.dump(self.saved_inputs, f, indent=4)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save inputs: {str(e)}")

    # Function to load saved inputs from a JSON file
    def load_saved_inputs(self):
        try:
            with open('saved_inputs.json', 'r') as f:
                self.saved_inputs = json.load(f)
        except FileNotFoundError:
            self.saved_inputs = []
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load inputs: {str(e)}")
            self.saved_inputs = []

# This part runs when you start the program
if __name__ == "__main__":
    # Make the main window for the app
    root = tk.Tk()  # Creates the main application window
    # Set up the app with the main window
    app = StudentManagementApp(root)  # Initializes the Student Management App
    # Start the app and wait for user actions
    root.mainloop()  # Runs the Tkinter event loop so the window stays open

