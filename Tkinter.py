"""

This module initializes the system with lists for storing student, instructor, and course objects.
An initial course 'EECE 435L' is created with a predefined ID and added to the course list.

Global Variables
----------------
students : list of Student
    Stores instances of Student.
instructors : list of Instructor
    Stores instances of Instructor.
courses : list of Course
    Stores instances of Course.
courseXX : str
    The name of the initial course, set to 'EECE 435L'.
idcourse : int
    A counter for course IDs, starting at 1.

Setup Actions
-------------
- An initial course is created without an assigned instructor and added to the courses list.
- The course ID counter is incremented to prepare for the next course addition.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from Classes import *

students = []
instructors = []
courses = []

courseXX = "EECE 435L"
idcourse = 1  

course = Course(course_id=str(idcourse), course_name=courseXX, instructor=None)
courses.append(course)
idcourse += 1

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from Classes import *  

students = []
instructors = []
courses = []

courseXX = "EECE 435L"

idcourse = 1  

course = Course(course_id=str(idcourse), course_name=courseXX, instructor=None)
courses.append(course)
idcourse += 1  

def add_course():
    """
    Adds a new course to the global list of courses if the specified instructor exists.

    :param None: Uses values from user input fields.
    :return: None
    :raises ValueError: If the instructor does not exist in the global list.
    """
    courseid = Input_Course_id.get()  
    coursename = Input_course_name.get()
    instructorname = Input_Course_Instructor.get()

    instructor = next((inst for inst in instructors if inst.name == instructorname), None)

    if instructor:
        course = Course(course_id=courseid, course_name=coursename, instructor=instructor)
        courses.append(course)
        messagebox.showinfo("Success", f"Course {coursename} added successfully!")
        update_list_deploy_courses()
        Clear_course_inputs()  
        treeviewupdate()
    else:
        messagebox.showerror("Error", "Instructor not found. Please add the instructor first.")

def add_student():
    """
    Adds a new student to the global list of students and registers them for a selected course.

    :param None: Uses values from user input fields.
    :return: None
    :raises ValueError: If age or email validation fails.
    """
    name = Input_Student_name.get()
    age = int(Input_Student_age.get())
    email = Input_Student_email.get()
    studentid = Input_Student_id.get()
    selectedcourse = Listofcoursesdeploystudents.get()  

    try:
        validate_age(age)
        validate_email(email)
        student = Student(name, age, email, studentid)
        students.append(student)
        
        course = next((c for c in courses if c.course_name == selectedcourse), None)
        if course:
            course.add_student(student)
            messagebox.showinfo("Success Student", f"{name} added and registered for {selectedcourse}")
        else:
            messagebox.showwarning("Warning", f"{selectedcourse} not available.")
        Clear_Student_inputs()  
        treeviewupdate()
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def add_instructor():
    """
    Adds a new instructor to the global list of instructors and assigns them to a selected course.
    This function retrieves values directly from the user interface, validates the inputs,
    and updates the system's state accordingly.

    :param None: Uses values from user input fields.
    :return: None
    :raises ValueError: If age or email validation fails, indicating invalid inputs.
    """
    name = Input_Instructor_Name.get()
    age = int(Input_Instructor_age.get())
    email = Input_Instructor_email.get()
    instructorid = Input_Instructor_id.get()
    selectedcourse = Listofcoursesdeployinstructor.get()

    try:
        validate_age(age)
        validate_email(email)
        instructor = Instructor(name, age, email, instructorid)
        instructors.append(instructor)

        course = next((c for c in courses if c.course_name == selectedcourse), None)
        if course:
            course.instructor = instructor
            messagebox.showinfo("Success", f"{name} added and assigned to {selectedcourse}!")
        else:
            messagebox.showwarning("Warning", f"{selectedcourse} not available.")

        Clear_Instructor_inputs()
        treeviewupdate()
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def Clear_Student_inputs():
    """
    Clears all input fields in the student section of the user interface.
    This function resets the fields to be ready for new student data entry.

    :return: None
    """
    Input_Student_name.delete(0, tk.END)
    Input_Student_age.delete(0, tk.END)
    Input_Student_email.delete(0, tk.END)
    Input_Student_id.delete(0, tk.END)
    Listofcoursesdeploystudents.set('')



def update_list_deploy_courses():
    """
    Updates the list of course names in the user interface dropdowns for student and instructor sections.

    :return: None
    """
    Listofcoursesdeploystudents['values'] = [course.course_name for course in courses]
    Listofcoursesdeployinstructor['values'] = [course.course_name for course in courses]

def Clear_course_inputs():
    """
    Clears all input fields in the course section of the user interface.
    This function resets the fields to be ready for new course data entry.

    :return: None
    """
    Input_Course_id.delete(0, tk.END)
    Input_course_name.delete(0, tk.END)
    Input_Course_Instructor.delete(0, tk.END)

def Clear_Instructor_inputs():
    """
    Clears all input fields in the instructor section of the user interface.
    This function resets the fields to be ready for new instructor data entry.

    :return: None
    """
    Input_Instructor_Name.delete(0, tk.END)
    Input_Instructor_age.delete(0, tk.END)
    Input_Instructor_email.delete(0, tk.END)
    Input_Instructor_id.delete(0, tk.END)
    Listofcoursesdeployinstructor.set('')

def Clear_Student_inputs():
    """
    Clears all input fields in the student section of the user interface.
    This function resets the fields to be ready for new student data entry.

    :return: None
    """
    Input_Student_name.delete(0, tk.END)
    Input_Student_age.delete(0, tk.END)
    Input_Student_email.delete(0, tk.END)
    Input_Student_id.delete(0, tk.END)
    Listofcoursesdeploystudents.set('')





def search_records():
    """
    Searches for student, instructor, and course records based on input from user interface fields.
    Filters results based on the search criteria provided and updates the UI treeviews with these results.

    :return: None
    """
    nameStudent = search_student_input.get().strip().lower()
    idStudent = search_studentid_input.get().strip().lower()
    nameInstructor = search_instructor_input.get().strip().lower()
    nameCourse = search_course_input.get().strip().lower()

    studentsMatching = [
        student for student in students
        if (nameStudent in student.name.lower() or not nameStudent)
        and (idStudent in student.student_id.lower() or not idStudent)
    ]

    instructorsMatching = [
        instructor for instructor in instructors
        if nameInstructor in instructor.name.lower() or not nameInstructor
    ]

    coursesMatching = [
        course for course in courses
        if nameCourse in course.course_name.lower() or not nameCourse
    ]

    treeviewupdate(studentsMatching, instructorsMatching, coursesMatching)
def treeviewupdate(studentList=None, instructorList=None, courseList=None):
    """
    Updates the UI treeviews for students, instructors, and courses with the provided lists.

    Local Functions:
    - clearTreeView: Clears all items from a given treeview.
        :param treeview: The treeview widget to clear.
        :type treeview: tk.Treeview

    - insertTreeViewData: Inserts data into a treeview based on the specified attributes of the data objects.
        :param treeview: The treeview widget where data will be inserted.
        :type treeview: tk.Treeview
        :param dataList: List of data objects (students, instructors, or courses).
        :type dataList: list
        :param attributes: List of attributes to retrieve from each data object for display.
        :type attributes: list of str

    :param studentList: List of students to display, defaults to all students if None.
    :type studentList: list, optional
    :param instructorList: List of instructors to display, defaults to all instructors if None.
    :type instructorList: list, optional
    :param courseList: List of courses to display, defaults to all courses if None.
    :type courseList: list, optional
    :return: None
    """
    studentList = students if studentList is None else studentList
    instructorList = instructors if instructorList is None else instructorList
    courseList = courses if courseList is None else courseList

    def clearTreeView(treeview):
        """
        Clears all items from the specified treeview.

        :param treeview: The treeview from which to remove all items.
        :type treeview: tk.Treeview
        """
        for item in treeview.get_children():
            treeview.delete(item)

    clearTreeView(studentstreeview)
    clearTreeView(instructorstreeview)
    clearTreeView(coursestreeview)

    def insertTreeViewData(treeview, dataList, attributes):
        """
        Inserts data into a treeview based on specified attributes of data objects.

        :param treeview: The treeview where data will be inserted.
        :type treeview: tk.Treeview
        :param dataList: List of data objects to display.
        :type dataList: list
        :param attributes: Attributes of data objects to be displayed.
        :type attributes: list of str
        """
        for data in dataList:
            values = [getattr(data, attr) for attr in attributes]
            treeview.insert("", tk.END, values=values)

    studentAttributes = ['name', 'age', '_email', 'student_id']
    instructorAttributes = ['name', 'age', '_email', 'instructor_id']
    courseAttributes = ['course_id', 'course_name', 'instructor']

    insertTreeViewData(studentstreeview, studentList, studentAttributes)
    insertTreeViewData(instructorstreeview, instructorList, instructorAttributes)
    insertTreeViewData(coursestreeview, courseList, courseAttributes)

def Student_edit():
    """
    Edits the selected student's data using the form in the user interface. This function allows
    for updating a student's information currently displayed in the treeview.

    :return: None
    :raises: None
    """
    selected_item = studentstreeview.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a student to edit.")
        return

    student_data = studentstreeview.item(selected_item, "values")
    student = next((s for s in students if s.student_id == student_data[3]), None)

    if student:
        Input_Student_name.delete(0, tk.END)
        Input_Student_age.delete(0, tk.END)
        Input_Student_email.delete(0, tk.END)
        Input_Student_id.delete(0, tk.END)

        Input_Student_name.insert(0, student.name)
        Input_Student_age.insert(0, student.age)
        Input_Student_email.insert(0, student.email)
        Input_Student_id.insert(0, student.student_id)
        Listofcoursesdeploystudents.set(next(c.course_name for c in courses if student in c.enrolled_students))

        save_button.config(state=tk.NORMAL)

def Studentdelete():
    """
    Deletes the selected student from the system and updates the UI accordingly.

    :return: None
    :raises: None
    """
    chosenItem = studentstreeview.selection()
    if not chosenItem:
        messagebox.showwarning("Warning", "Please select a student to delete.")
        return

    studentDetails = studentstreeview.item(chosenItem, "values")
    targetStudent = next((stud for stud in students if stud.student_id == studentDetails[3]), None)

    if targetStudent:
        for courseItem in courses:
            if targetStudent in courseItem.enrolled_students:
                courseItem.enrolled_students.remove(targetStudent)
        students.remove(targetStudent)
        studentstreeview.delete(chosenItem)
        Input_Student_name.delete(0, tk.END)
        Input_Student_age.delete(0, tk.END)
        Input_Student_email.delete(0, tk.END)
        Input_Student_id.delete(0, tk.END)
        Listofcoursesdeploystudents.set('')
        messagebox.showinfo("Success", f"Student {targetStudent.name} deleted successfully.")

def savestudent():
    """
    Saves changes to a student's data and updates the associated records in the system.

    :return: None
    :raises: None
    """
    selectedItem = studentstreeview.selection()
    if not selectedItem:
        return

    studentDetails = studentstreeview.item(selectedItem, "values")
    currentStudent = next((item for item in students if item.student_id == studentDetails[3]), None)

    if currentStudent:
        currentStudent.name = Input_Student_name.get()
        currentStudent.age = int(Input_Student_age.get())
        currentStudent._email = Input_Student_email.get()
        currentStudent.student_id = Input_Student_id.get()
        courseChoice = Listofcoursesdeploystudents.get()
        chosenCourse = next((course for course in courses if course.course_name == courseChoice), None)

        if chosenCourse and currentStudent not in chosenCourse.enrolled_students:
            for course in courses:
                if currentStudent in course.enrolled_students:
                    course.enrolled_students.remove(currentStudent)
            chosenCourse.add_student(currentStudent)

        studentstreeview.item(selectedItem, values=(
            currentStudent.name, currentStudent.age, currentStudent._email, currentStudent.student_id
        ))
        Input_Student_name.delete(0, tk.END)
        Input_Student_age.delete(0, tk.END)
        Input_Student_email.delete(0, tk.END)
        Input_Student_id.delete(0, tk.END)
        Listofcoursesdeploystudents.set('')
        save_button.config(state=tk.DISABLED)
        messagebox.showinfo("Success", f"Student {currentStudent.name}'s record updated successfully.")


import json

def save_data():
    """
    Saves current data of students, courses, and instructors to a JSON file.
    Compiles data into structured dictionaries and prompts the user to save it in a file.

    :return: None
    """
    saveData = {"students": [], "courses": [], "instructors": []}
    for student in students:
        studentDetails = {
            "name": student.name,
            "age": student.age,
            "email": student._email,
            "student_id": student.student_id,
            "course": student.registered_courses.course_name if student.registered_courses else None
        }
        saveData["students"].append(studentDetails)
    for course in courses:
        courseData = {
            "course_name": course.course_name,
            "students": [learner.student_id for learner in course.enrolled_students],
            "instructor": course.instructor.instructor_id if course.instructor else None
        }
        saveData["courses"].append(courseData)
    for instructor in instructors:
        instructorData = {
            "name": instructor.name,
            "instructor_id": instructor.instructor_id,
            "courses": [session.course_name for session in instructor.assigned_courses]
        }
        saveData["instructors"].append(instructorData)

    filePath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filePath:
        with open(filePath, 'w') as fileObj:
            json.dump(saveData, fileObj, indent=4)
        messagebox.showinfo("Success", "Data saved successfully")

def load_data():
    """
    Loads data of students, courses, and instructors from a JSON file.
    Reads data from a user-selected file and updates the application state accordingly.

    :return: None
    """
    jsonFilePath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if jsonFilePath:
        with open(jsonFilePath, 'r') as jsonData:
            dataSet = json.load(jsonData)
        students.clear()
        courses.clear()
        instructors.clear()
        studentstreeview.delete(*studentstreeview.get_children())

        for courseEntry in dataSet["courses"]:
            course = Course(course_id=courseEntry.get("course_id", None), course_name=courseEntry.get("course_name", None), instructor=None)
            courses.append(course)
        
        for instructorEntry in dataSet["instructors"]:
            teachingStaff = Instructor(name=instructorEntry["name"], instructor_id=instructorEntry["instructor_id"], courses=[])
            for coursename in instructorEntry["courses"]:
                for classModule in courses:
                    if classModule.course_name == coursename:
                        teachingStaff.courses.append(classModule)
                        classModule.instructor = teachingStaff
            instructors.append(teachingStaff)

        for studentEntry in dataSet["students"]:
            student = Student(name=studentEntry["name"], age=studentEntry["age"], email=studentEntry["email"], student_id=studentEntry["student_id"], registered_courses=[])
            registeredCourseName = studentEntry.get("course", None)
            if registeredCourseName:
                for course in courses:
                    if course.course_name == registeredCourseName:
                        student.registered_courses.append(course)
                        course.enrolled_students.append(student)
                        break
            students.append(student)
            studentstreeview.insert("", "end", values=(student.name, student.age, student.email, student.student_id))

        messagebox.showinfo("Success", "Data loaded successfully!")



"""
This sets up the main interface for a School Management System using Tkinter. It defines the main window
and organizes the interface into a tabbed notebook with separate tabs for managing students, instructors, and courses.

Features:
- Configuration of the main window with specific dimensions and background color.
- Creation of a style for Tkinter widgets that is applied globally.
- Setup of a Notebook widget with three tabs: Students, Instructors, and Courses.
- Each tab contains a form to add new entries and a tree view to display existing entries.
- Implementation of buttons for various functionalities like adding new entries, editing, and deleting.

The interface allows for easy management of school data, facilitating the addition, modification, and viewing of student,
instructor, and course information in a structured and user-friendly manner.
"""
root = tk.Tk()
root.title("School Management System")
root.geometry("600x400")
root.configure(bg="purple")

style = ttk.Style()
style.configure("TButton", background="#D3D3D3", foreground="black", font=("Times New Roman", 12))
style.map("TButton", background=[("active", "#D3D3D3")])

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

students_frame = ttk.Frame(notebook)
instructors_frame = ttk.Frame(notebook)
courses_frame = ttk.Frame(notebook)

notebook.add(students_frame, text="Students")
notebook.add(instructors_frame, text="Instructors")
notebook.add(courses_frame, text="Courses")

student_frame = ttk.LabelFrame(students_frame, text="Add Student")
student_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(student_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
Input_Student_name = ttk.Entry(student_frame)
Input_Student_name.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(student_frame, text="Age:").grid(row=1, column=0, padx=5, pady=5)
Input_Student_age = ttk.Entry(student_frame)
Input_Student_age.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(student_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
Input_Student_email = ttk.Entry(student_frame)
Input_Student_email.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(student_frame, text="Student ID:").grid(row=3, column=0, padx=5, pady=5)
Input_Student_id = ttk.Entry(student_frame)
Input_Student_id.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(student_frame, text="Select Course:").grid(row=4, column=0, padx=5, pady=5)
Listofcoursesdeploystudents = ttk.Combobox(student_frame, values=[course.course_name for course in courses])
Listofcoursesdeploystudents.grid(row=4, column=1, padx=5, pady=5)

ttk.Button(student_frame, text="Add Student", command=add_student).grid(row=5, columnspan=2, pady=5)

instructor_frame = ttk.LabelFrame(instructors_frame, text="Add Instructor")
instructor_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(instructor_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
Input_Instructor_Name = ttk.Entry(instructor_frame)
Input_Instructor_Name.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(instructor_frame, text="Age:").grid(row=1, column=0, padx=5, pady=5)
Input_Instructor_age = ttk.Entry(instructor_frame)
Input_Instructor_age.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(instructor_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
Input_Instructor_email = ttk.Entry(instructor_frame)
Input_Instructor_email.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(instructor_frame, text="Instructor ID:").grid(row=3, column=0, padx=5, pady=5)
Input_Instructor_id = ttk.Entry(instructor_frame)
Input_Instructor_id.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(instructor_frame, text="Assign to Course:").grid(row=4, column=0, padx=5, pady=5)
Listofcoursesdeployinstructor = ttk.Combobox(instructor_frame, values=[course.course_name for course in courses])
Listofcoursesdeployinstructor.grid(row=4, column=1, padx=5, pady=5)

ttk.Button(instructor_frame, text="Add Instructor", command=add_instructor).grid(row=5, columnspan=2, pady=5)

course_frame = ttk.LabelFrame(courses_frame, text="Add Course")
course_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(course_frame, text="Course ID:").grid(row=0, column=0, padx=5, pady=5)
Input_Course_id = ttk.Entry(course_frame)
Input_Course_id.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(course_frame, text="Course Name:").grid(row=1, column=0, padx=5, pady=5)
Input_course_name = ttk.Entry(course_frame)
Input_course_name.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(course_frame, text="Instructor Name:").grid(row=2, column=0, padx=5, pady=5)
Input_Course_Instructor = ttk.Entry(course_frame)
Input_Course_Instructor.grid(row=2, column=1, padx=5, pady=5)

ttk.Button(course_frame, text="Add Course", command=add_course).grid(row=3, columnspan=2, pady=5)

treeviewframe = ttk.Frame(root)
treeviewframe.pack(fill="both", expand=True, padx=10, pady=10)

studentstreeview = ttk.Treeview(treeviewframe, columns=("Name", "Age", "Email", "Student ID"), show='headings')
studentstreeview.heading("Name", text="Name")
studentstreeview.heading("Age", text="Age")
studentstreeview.heading("Email", text="Email")
studentstreeview.heading("Student ID", text="Student ID")
studentstreeview.column("Name", width=50)
studentstreeview.column("Age", width=50)
studentstreeview.column("Email", width=50)
studentstreeview.column("Student ID", width=50)
studentstreeview.pack(side="left", fill="both", expand=True)

instructorstreeview = ttk.Treeview(treeviewframe, columns=("Name", "Age", "Email", "Instructor ID"), show='headings')
instructorstreeview.heading("Name", text="Name")
instructorstreeview.heading("Age", text="Age")
instructorstreeview.heading("Email", text="Email")
instructorstreeview.heading("Instructor ID", text="Instructor ID")
instructorstreeview.column("Name", width=50)
instructorstreeview.column("Age", width=50)
instructorstreeview.column("Email", width=50)
instructorstreeview.column("Instructor ID", width=50)
instructorstreeview.pack(side="left", fill="both", expand=True)

coursestreeview = ttk.Treeview(treeviewframe, columns=("Course ID", "Course Name", "Instructor"), show='headings')
coursestreeview.heading("Course ID", text="Course ID")
coursestreeview.heading("Course Name", text="Course Name")
coursestreeview.heading("Instructor", text="Instructor")
coursestreeview.column("Course ID", width=50)
coursestreeview.column("Course Name", width=50)
coursestreeview.column("Instructor", width=50)
coursestreeview.pack(side="left", fill="both", expand=True)

refresh_button = ttk.Button(root, text="Refresh Data", command=treeviewupdate)
refresh_button.pack(pady=10)

search_frame = ttk.LabelFrame(root, text="Search Records")
search_frame.pack(fill="x", padx=10, pady=2)

ttk.Label(search_frame, text="Student Name:").grid(row=0, column=0, padx=5, pady=2)
search_student_input = ttk.Entry(search_frame)
search_student_input.grid(row=0, column=1, padx=5, pady=2)

ttk.Label(search_frame, text="Student ID:").grid(row=0, column=2, padx=5, pady=2)
search_studentid_input = ttk.Entry(search_frame)
search_studentid_input.grid(row=0, column=3, padx=5, pady=2)

ttk.Label(search_frame, text="Instructor Name:").grid(row=1, column=0, padx=5, pady=2)
search_instructor_input = ttk.Entry(search_frame)
search_instructor_input.grid(row=1, column=1, padx=5, pady=2)

ttk.Label(search_frame, text="Course Name:").grid(row=1, column=2, padx=5, pady=2)
search_course_input = ttk.Entry(search_frame)
search_course_input.grid(row=1, column=3, padx=5, pady=2)

search_button = ttk.Button(search_frame, text="Search", command=search_records)
search_button.grid(row=0, column=5, padx=10, pady=5)

edit_button = ttk.Button(students_frame, text="Edit Student", command=Student_edit)
edit_button.pack(side=tk.LEFT, padx=5, pady=5)

delete_button = ttk.Button(students_frame, text="Delete Student", command=Studentdelete)
delete_button.pack(side=tk.LEFT, padx=5, pady=5)

save_button = ttk.Button(students_frame, text="Save Changes", command=savestudent, state=tk.DISABLED)
save_button.pack(side=tk.LEFT, padx=5, pady=5)

savex_button = ttk.Button(students_frame, text="Save Data", command=save_data)
savex_button.pack()

load_button = ttk.Button(students_frame, text="Load Data", command=load_data)
load_button.pack()

edit_button.configure(style="TButton")
delete_button.configure(style="TButton")
save_button.configure(style="TButton")
savex_button.configure(style="TButton")
load_button.configure(style="TButton")

root.mainloop()


