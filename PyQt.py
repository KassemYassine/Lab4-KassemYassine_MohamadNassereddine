from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from Classes import *
import sys
import csv
import re


class Window(QMainWindow):
    """
    A main window class for the School Management System, which provides a
    graphical user interface to manage students, instructors, and courses.
    
    The `Window` class extends `QMainWindow` and sets up the main layout containing
    multiple tabs for different forms and functionalities such as adding or managing
    students, instructors, and courses, as well as viewing records.

    Attributes:
        courses (list): A list of dictionaries containing course details.
        instructors (list): A list of dictionaries containing instructor details.
        students (list): A list of dictionaries containing student details.
    
    Methods:
        SetupUI: Configures the UI components of the main window.
        StudentForm: Returns the form widget for student management.
        InstructorForm: Returns the form widget for instructor management.
        CourseForm: Returns the form widget for course management.
        RecordDisplay: Returns the widget that displays various records.
        CourseDropdownDeployUpdate: Updates course dropdown components.
        save_Data: Saves the current data to a file.
        load_Data: Loads data from a file.
        csvexport: Exports records to a CSV file.
    """

    def __init__(self):
        """
        Constructor method for initializing a new window with predefined settings
        including window title, size, and initial empty lists for courses, instructors,
        and students.
        """
        super().__init__()
        self.courses = []  # Initializes the courses list
        self.instructors = []  # Initializes the instructors list
        self.students = []  # Initializes the students list
        self.SetupUI()

    def SetupUI(self):
        """
        Sets up the user interface for the School Management System main window.
        
        It defines the main layout, adds tab widgets for different management
        sections, and initializes buttons for saving, loading, and exporting data.
        Sets the window title, dimensions, and background color.
        """
        self.setWindowTitle('School Management System')
        self.setGeometry(400, 400, 800, 600)
        self.setStyleSheet("background-color: white;")
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QVBoxLayout()
        mainWidget.setLayout(mainLayout)
        tabWidget = QTabWidget()
        mainLayout.addWidget(tabWidget)
        tabWidget.addTab(self.StudentForm(), 'Student')
        tabWidget.addTab(self.InstructorForm(), 'Instructor')
        tabWidget.addTab(self.CourseForm(), 'Course')
        tabWidget.addTab(self.RecordDisplay(), 'Records')
        self.courses = [{'course_id': 'EECE 490', 'course_name': 'Machine Learning'}]
        self.CourseDropdownDeployUpdate()
        self.save_button = QPushButton("Save Data")
        self.load_button = QPushButton("Load Data")
        exportCSVButton = QPushButton("Export to CSV")
        self.save_button.setStyleSheet("background-color: black; color: white;")
        self.load_button.setStyleSheet("background-color: black; color: white;")
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(exportCSVButton)
        mainLayout.addWidget(self.save_button)
        mainLayout.addWidget(self.load_button)
        mainLayout.addLayout(buttonLayout)
        self.save_button.clicked.connect(self.save_Data)
        self.load_button.clicked.connect(self.load_Data)
        exportCSVButton.clicked.connect(self.csvexport)


    
    def StudentForm(self):
        """
        Creates and returns a QWidget that contains the form for managing student information.
        
        The form includes fields for student name, age, email, ID, and course registration.
        Each field has a corresponding QLineEdit or QComboBox widget for user input.
        An 'Add Student' button is also provided to submit the entered information.

        Returns:
            QWidget: The form widget used for entering student information.
        """
        studentForm = QWidget()
        formLayout = QFormLayout(studentForm)
        addButton = QPushButton('Add Student')
        courseSelector = QComboBox()
        nameEntry = QLineEdit()
        formLayout.addRow('Name:', nameEntry)
        self.student_name = nameEntry
        ageEntry = QLineEdit()
        formLayout.addRow('Age:', ageEntry)
        self.student_age = ageEntry
        emailEntry = QLineEdit()
        formLayout.addRow('Email:', emailEntry)
        self.student_email = emailEntry
        idEntry = QLineEdit()
        formLayout.addRow('ID:', idEntry)
        self.student_id = idEntry
        self.CourseDropdowndeployUpdate()
        formLayout.addRow('Register for Course:', courseSelector)
        self.course_dropdown = courseSelector
        addButton.clicked.connect(self.add_Student)
        formLayout.addWidget(addButton)
        return studentForm

    def CourseForm(self):
        """
        Creates and returns a QWidget that contains the form for managing course information.
        
        The form includes fields for course ID, course name, instructor ID, and a field to
        enter IDs of enrolled students. Each field has a corresponding QLineEdit widget for
        user input. An 'Add Course' button is also provided to submit the entered information.

        Returns:
            QWidget: The form widget used for entering course information.
        """
        courseForm = QWidget()
        formLayout = QFormLayout(courseForm)
        addButton = QPushButton('Add Course')
        courseIdInput = QLineEdit()
        courseNameInput = QLineEdit()
        instructorIdInput = QLineEdit()
        enrolledStudentsInput = QLineEdit()
        formLayout.addRow('Course ID:', courseIdInput)
        self.course_id = courseIdInput
        formLayout.addRow('Course Name:', courseNameInput)
        self.course_name = courseNameInput
        formLayout.addRow('Instructor ID:', instructorIdInput)
        self.course_instructor = instructorIdInput
        formLayout.addRow('Enrolled Students IDs:', enrolledStudentsInput)
        self.course_enrolled_students = enrolledStudentsInput
        addButton.clicked.connect(self.add_Course)
        formLayout.addWidget(addButton)
        return courseForm


    def InstructorForm(self):
        """
        Creates and returns a QWidget that contains the form for managing instructor information.
        
        The form includes fields for instructor name, age, email, ID, and course assignment. Each field
        has a corresponding QLineEdit or QComboBox widget for user input. An 'Add Instructor' button
        is provided to submit the entered information.

        Returns:
            QWidget: The form widget used for entering instructor information.
        """
        instructorForm = QWidget()
        instructorLayout = QFormLayout(instructorForm)
        addInstructorButton = QPushButton('Add Instructor')
        courseSelector = QComboBox()
        self.CourseDropdowndeployUpdate()
        nameInput = QLineEdit()
        ageInput = QLineEdit()
        emailInput = QLineEdit()
        idInput = QLineEdit()
        instructorLayout.addRow('Name:', nameInput)
        self.instructor_name = nameInput
        instructorLayout.addRow('Age:', ageInput)
        self.instructor_age = ageInput
        instructorLayout.addRow('Email:', emailInput)
        self.instructor_email = emailInput
        instructorLayout.addRow('ID:', idInput)
        self.instructor_id = idInput
        instructorLayout.addRow('Assign Course:', courseSelector)
        self.instructor_course_dropdown = courseSelector
        addInstructorButton.clicked.connect(self.add_Instructor)
        instructorLayout.addWidget(addInstructorButton)
        return instructorForm

    def RecordDisplay(self):
        """
        Creates and returns a QWidget that includes a table and search functionality to display
        and manage records of students, instructors, and courses.
        
        The widget incorporates a QTableWidget for displaying records with predefined columns
        for Type, ID, Name, Age, Email, and Assigned Courses. It includes a search area to filter
        records and buttons for editing and deleting records.

        Returns:
            QWidget: The widget used for displaying and managing records.
        """
        displayWidget = QWidget()
        mainLayout = QVBoxLayout(displayWidget)
        recordsTable = QTableWidget()
        recordsTable.setColumnCount(6)
        recordsTable.setHorizontalHeaderLabels(['Type', 'ID', 'Name', 'Age', 'Email', 'Assigned Courses'])
        mainLayout.addWidget(recordsTable)
        searchArea = QHBoxLayout()
        searchBtn = QPushButton('Search')
        searchInput = QLineEdit()
        searchInput.setPlaceholderText('Search by name, ID, or course')
        searchBtn.clicked.connect(self.searchRecords)
        searchArea.addWidget(searchInput)
        searchArea.addWidget(searchBtn)
        mainLayout.addLayout(searchArea)
        actionArea = QHBoxLayout()
        deleteRecordBtn = QPushButton('Delete Record')
        editRecordBtn = QPushButton('Edit Record')
        editRecordBtn.clicked.connect(self.editRecord)
        deleteRecordBtn.clicked.connect(self.deleteRecord)
        actionArea.addWidget(editRecordBtn)
        actionArea.addWidget(deleteRecordBtn)
        mainLayout.addLayout(actionArea)
        self.table_widget = recordsTable
        self.search_field = searchInput
        self.edit_button = editRecordBtn
        self.delete_button = deleteRecordBtn
        self.RecordDisplayupdate()
        return displayWidget


    def CourseDropdowndeployUpdate(self):
        """
        Updates the dropdown lists used in the forms for selecting courses.

        This method refreshes the course options in all dropdown menus by first clearing
        the existing items and then repopulating them based on the current list of courses.
        """
        dropdownsToUpdate = ['course_dropdown', 'instructor_course_dropdown']
        for dropdown in dropdownsToUpdate:
            if hasattr(self, dropdown):
                getattr(self, dropdown).clear()
        for course in self.courses:
            courseDetails = f"{course['course_id']} - {course['course_name']}"
            for dropdown in dropdownsToUpdate:
                if hasattr(self, dropdown):
                    getattr(self, dropdown).addItem(courseDetails, course['course_id'])

    def add_Student(self):
        """
        Adds a new student with the information provided in the student form.

        Gathers the input from the student form, validates the age and email,
        and if valid, creates a new Student object to be added to the list of students.
        Displays a message box upon successful addition.
        """
        name = self.student_name.text()
        age = int(self.student_age.text())
        email = self.student_email.text()
        id = self.student_id.text()
        courseID = self.course_dropdown.currentData()
        validate_age(age)
        validate_email(email)
        newStudent = Student(name, age, email, id)
        self.students.append(newStudent)
        QMessageBox.information(self, 'Student Addition Successful', f'Student {name} has been successfully added and is registered for course ID: {courseID}')
        self.RecordDisplayupdate()

    def add_Course(self):
        """
        Adds a new course with the details provided in the course form.

        Gathers the input from the course form, checks for the existence of the instructor by ID,
        and if found, creates a new Course object to be added to the list of courses.
        Displays a message box upon successful addition.
        """
        courseId = self.course_id.text()
        instructorId = self.course_instructor.text()
        courseName = self.course_name.text()
        studentIds = self.course_enrolled_students.text().split(',')
        instructor = next((inst for inst in self.instructors if inst.instructor_id == instructorId), None)
        if instructor is None:
            QMessageBox.warning(self, 'Error', 'Instructor ID not found!')
            return
        enrolledStudents = []
        for id in studentIds:
            student = next((stu for stu in self.students if stu.student_id == id.strip()), None)
            if student:
                enrolledStudents.append(student)
                student.register_course(courseId)
        newCourse = Course(course_id=courseId, course_name=courseName, instructor=instructor, enrolled_students=enrolledStudents)
        self.courses.append(newCourse)
        QMessageBox.information(self, 'Success', f'New course "{courseName}" has been added successfully.')
        self.RecordDisplayupdate()

    def add_Instructor(self):
        """
        Adds a new instructor with the information provided in the instructor form.

        Gathers the input from the instructor form, validates the age and email,
        and if valid, creates a new Instructor object to be added to the list of instructors.
        Displays a message box upon successful addition and updates course assignments.
        """
        name = self.instructor_name.text()
        age = int(self.instructor_age.text())
        email = self.instructor_email.text()
        id = self.instructor_id.text()
        courseId = self.instructor_course_dropdown.currentData()
        validate_age(age)
        validate_email(email)
        newInstructor = Instructor(name, age, email, id)
        self.instructors.append(newInstructor)
        QMessageBox.information(self, 'Instructor Registration', f'Instructor {name} has been added and assigned to course ID: {courseId}')
        for course in self.courses:
            if course['course_id'] == courseId:
                for instructor in self.instructors:
                    if instructor.instructor_id == id:
                        instructor.assign_course(course)
                        break
                break
        self.RecordDisplayupdate()



    def searchRecords(self):
        """
        Searches for records within the students, instructors, and courses lists based on the query entered in the search field.

        Updates the display table with all records that match the search query, displaying relevant details
        for each type of record (students, instructors, courses). The query can match the name, ID, or,
        in the case of courses, the course name.
        """
        self.table_widget.setColumnCount(6)
        self.table_widget.setRowCount(0)
        self.table_widget.setHorizontalHeaderLabels(['Type', 'ID', 'Name', 'Age', 'Email', 'Assigned Courses'])
        query = self.search_field.text().lower()
        self.table_widget.clear()
        for student in self.students:
            if query in student.name.lower() or query in student.student_id.lower():
                index = self.table_widget.rowCount()
                self.table_widget.insertRow(index)
                self.table_widget.setItem(index, 0, QTableWidgetItem('Student'))
                self.table_widget.setItem(index, 1, QTableWidgetItem(student.student_id))
                self.table_widget.setItem(index, 2, QTableWidgetItem(student.name))
                self.table_widget.setItem(index, 3, QTableWidgetItem(str(student.age)))
                self.table_widget.setItem(index, 4, QTableWidgetItem(student.email))
                self.table_widget.setItem(index, 5, QTableWidgetItem('N/A'))
        for instructor in self.instructors:
            if query in instructor.name.lower() or query in instructor.instructor_id.lower():
                index = self.table_widget.rowCount()
                self.table_widget.insertRow(index)
                self.table_widget.setItem(index, 0, QTableWidgetItem('Instructor'))
                self.table_widget.setItem(index, 1, QTableWidgetItem(instructor.instructor_id))
                self.table_widget.setItem(index, 2, QTableWidgetItem(instructor.name))
                self.table_widget.setItem(index, 3, QTableWidgetItem(str(instructor.age)))
                self.table_widget.setItem(index, 4, QTableWidgetItem(instructor.email))
                assignedCourses = ', '.join(course['course_name'] for course in self.courses if course['course_id'] in instructor.courses)
                self.table_widget.setItem(index, 5, QTableWidgetItem(assignedCourses))
        for course in self.courses:
            if query in course['course_name'].lower() or query in course['course_id'].lower():
                index = self.table_widget.rowCount()
                self.table_widget.insertRow(index)
                self.table_widget.setItem(index, 0, QTableWidgetItem('Course'))
                self.table_widget.setItem(index, 1, QTableWidgetItem(course['course_id']))
                self.table_widget.setItem(index, 2, QTableWidgetItem(course['course_name']))
                self.table_widget.setItem(index, 3, QTableWidgetItem('N/A'))
                self.table_widget.setItem(index, 4, QTableWidgetItem('N/A'))
                self.table_widget.setItem(index, 5, QTableWidgetItem('N/A'))

    def RecordDisplayupdate(self):
        """
        Refreshes the record display table with current data from students, instructors, and courses lists.

        This method clears the current contents of the table and repopulates it with updated data from
        the system's records, reflecting any changes or additions made.
        """
        self.table_widget.setRowCount(0)
        for instructor in self.instructors:
            rowIndex = self.table_widget.rowCount()
            self.table_widget.insertRow(rowIndex)
            self.table_widget.setItem(rowIndex, 0, QTableWidgetItem('Instructor'))
            self.table_widget.setItem(rowIndex, 1, QTableWidgetItem(instructor.instructor_id))
            self.table_widget.setItem(rowIndex, 2, QTableWidgetItem(instructor.name))
            self.table_widget.setItem(rowIndex, 3, QTableWidgetItem(str(instructor.age)))
            self.table_widget.setItem(rowIndex, 4, QTableWidgetItem(instructor.email))
        for student in self.students:
            rowIndex = self.table_widget.rowCount()
            self.table_widget.insertRow(rowIndex)
            self.table_widget.setItem(rowIndex, 0, QTableWidgetItem('Student'))
            self.table_widget.setItem(rowIndex, 1, QTableWidgetItem(student.student_id))
            self.table_widget.setItem(rowIndex, 2, QTableWidgetItem(student.name))
            self.table_widget.setItem(rowIndex, 3, QTableWidgetItem(str(student.age)))
            self.table_widget.setItem(rowIndex, 4, QTableWidgetItem(student.email))
        for course in self.courses:
            rowIndex = self.table_widget.rowCount()
            self.table_widget.insertRow(rowIndex)
            self.table_widget.setItem(rowIndex, 0, QTableWidgetItem('Course'))
            self.table_widget.setItem(rowIndex, 1, QTableWidgetItem(course['course_id']))
            self.table_widget.setItem(rowIndex, 2, QTableWidgetItem(course['course_name']))
            self.table_widget.setItem(rowIndex, 3, QTableWidgetItem('N/A'))
            self.table_widget.setItem(rowIndex, 4, QTableWidgetItem('N/A'))
            instructorInfo = course.get('instructor_id', 'N/A')
            enrolledStudentsInfo = ', '.join(course.get('enrolled_students', []))
            courseDetails = f"Instructor ID: {instructorInfo}\nEnrolled Students: {enrolledStudentsInfo}"
            self.table_widget.setItem(rowIndex, 5, QTableWidgetItem(courseDetails))

    def editRecord(self):
        """
        Allows editing of selected record's details directly from the table view.

        This method provides functionality to edit a selected record's email, age, or name.
        It validates the new input before updating and refreshes the record display upon successful edit.
        """
        currentRow = self.table_widget.currentRow()
        if currentRow == -1:
            QMessageBox.warning(self, 'Edit Record', 'Please select a record to edit.')
            return
        entityType = self.table_widget.item(currentRow, 0).text()
        entityId = self.table_widget.item(currentRow, 1).text()
        if entityType == 'Instructor':
            # Editing an instructor
            instructor = next((inst for inst in self.instructors if inst.instructor_id == entityId), None)
            if instructor:
                newEmail, confirmed = QInputDialog.getText(self, 'Edit Instructor', 'Enter new email:', text=instructor.email)
                isValidEmail = re.match(r"[^@]+@[^@]+\.[^@]+", newEmail) is not None
                if confirmed and isValidEmail:
                    instructor.email = newEmail
                else:
                    QMessageBox.warning(self, 'Edit Instructor', 'Email entry was invalid.')
                    return
                newAge, confirmed = QInputDialog.getText(self, 'Edit Instructor', 'Enter new age:', text=str(instructor.age))
                isValidAge = newAge.isdigit() and int(newAge) > 0
                if confirmed and isValidAge:
                    instructor.age = int(newAge)
                else:
                    QMessageBox.warning(self, 'Edit Instructor', 'Age entry was invalid.')
                    return
                newName, confirmed = QInputDialog.getText(self, 'Edit Instructor', 'Enter new name:', text=instructor.name)
                if confirmed and newName.strip():
                    instructor.name = newName.strip()
                else:
                    QMessageBox.warning(self, 'Edit Instructor', 'Name entry was invalid.')
                    return
        elif entityType == 'Student':
            # Editing a student
            student = next((stu for stu in student if stu.student_id == entityId), None)
            if student:
                newEmail, confirmed = QInputDialog.getText(self, 'Edit Student', 'Enter new email:', text=student.email)
                isValidEmail = re.match(r"[^@]+@[^@]+\.[^@]+", newEmail) is not None
                if confirmed and isValidEmail:
                    student.email = newEmail
                else:
                    QMessageBox.warning(self, 'Edit Student', 'Email entry was invalid.')
                    return
                newAge, confirmed = QInputDialog.getText(self, 'Edit Student', 'Enter new age:', text=str(student.age))
                isValidAge = newAge.isdigit() and int(newAge) > 0
                if confirmed and isValidAge:
                    student.age = int(newAge)
                else:
                    QMessageBox.warning(self, 'Edit Student', 'Age entry was invalid.')
                    return
                newName, confirmed = QInputDialog.getText(self, 'Edit Student', 'Enter new name:', text=student.name)
                if confirmed and newName.strip():
                    student.name = newName.strip()
                else:
                    QMessageBox.warning(self, 'Edit Student', 'Invalid name!')
                    return
        self.RecordDisplayupdate()

    
    def deleteRecord(self):
        """
        Deletes a selected record from the table and updates the corresponding list of entities.

        This function identifies the selected record by its row index in the display table,
        determines the entity type (instructor or student), and removes the entity from its
        respective list. It then updates the display table to reflect the deletion.

        Raises:
            QMessageBox: Shows a warning if no record is selected and an information message on successful deletion.
        """
        rowIndex = self.table_widget.currentRow()
        if rowIndex == -1:
            QMessageBox.warning(self, 'Delete Record', 'Please select a record to delete.')
            return
        entityId = self.table_widget.item(rowIndex, 1).text()
        entityType = self.table_widget.item(rowIndex, 0).text()
        if entityType == 'Instructor':
            self.instructors = [instructor for instructor in self.instructors if instructor.instructor_id != entityId]
        elif entityType == 'Student':
            self.students = [student for student in self.students if student.student_id != entityId]
        self.RecordDisplayupdate()
        QMessageBox.information(self, 'Success', f'Record of {entityType} deleted successfully!')

    def save_Data(self):
        """
        Saves all current data (students, instructors, courses) to a JSON file.

        Attempts to serialize the entire database of entities into JSON format and write it to a file.
        Provides feedback via message boxes about the success of the operation or errors encountered.

        Raises:
            Exception: Captures and displays any exceptions as a critical error message.
        """
        try:
            database = {
                'students': [],
                'instructors': [],
                'courses': []
            }
            for instructor in self.instructors:
                instructor_info = {
                    'instructor_id': instructor.instructor_id,
                    'name': instructor.name,
                    'assigned_courses': [c.course_id for c in instructor.assigned_courses]
                }
                database['instructors'].append(instructor_info)
            for student in self.students:
                student_info = {
                    'student_id': student.student_id,
                    'name': student.name,
                    'age': student.age,
                    'email': student.email,
                    'registered_courses': [c.course_id for c in student.registered_courses]
                }
                database['students'].append(student_info)
            for course in self.courses:
                course_info = {
                    'course_id': course['course_id'],
                    'course_name': course['course_name'],
                    'instructor_id': (course['instructor'].instructor_id if course.get('instructor') else None),
                    'enrolled_students': [s.student_id for s in course.get('enrolled_students', [])]
                }
                database['courses'].append(course_info)
            with open('school_data.json', 'w') as file:
                json.dump(database, file)
            QMessageBox.information(self, 'Success', 'All data has been saved successfully!')
        except Exception as error:
            QMessageBox.critical(self, 'Error', f"Failed to save data due to an error: {str(error)}")

    def csvexport(self):
        """
        Exports the data of all entities (students, instructors, courses) to a CSV file.

        Allows the user to select a file path and saves the data in CSV format. If the operation
        is successful, it confirms completion; if an error occurs, it shows an error message.

        Raises:
            Exception: Displays an error message if there is an issue during file writing.
        """
        exportFilePath, _ = QFileDialog.getSaveFileName(self, "Export Data to CSV", "", "CSV Files (*.csv)")
        if not exportFilePath:
            return
        try:
            with open(exportFilePath, 'w', newline='') as exportFile:
                csvWriter = csv.writer(exportFile)
                csvWriter.writerow(["Entity Type", "Identifier", "Full Name", "Age", "Email Address", "Associated Instructor", "Associated Course", "List of Students"])
                for instructor in self.instructors:
                    csvWriter.writerow([
                        "Instructor",
                        instructor.instructor_id,
                        instructor.name,
                        instructor.age,
                        instructor.email,
                        '',
                        '',
                        ''
                    ])
                for student in self.students:
                    csvWriter.writerow([
                        "Student",
                        student.student_id,
                        student.name,
                        student.age,
                        student.email,
                        '',
                        '',
                        ''
                    ])
                for course in self.courses:
                    student_names = ', '.join(
                        stud.name for stud in getattr(course, 'enrolled_students', [])
                    )
                    csvWriter.writerow([
                        "Course",
                        getattr(course, 'course_id', ''),
                        getattr(course, 'course_name', ''),
                        '',
                        '',
                        getattr(getattr(course, 'instructor', {}), 'name', ''),
                        getattr(course, 'course_name', ''),
                        student_names
                    ])
            QMessageBox.information(self, "Export Complete", "Data has been successfully exported to CSV.")
        except Exception as error:
            QMessageBox.critical(self, "Export Error", f"An error occurred during export: {str(error)}")

    def load_Data(self):
        """
        Loads data for students, instructors, and courses from a JSON file.

        This method prompts the user to select a JSON file to load. It reads the file, clears the current data lists,
        and repopulates them with the loaded data. Each list (students, instructors, courses) is filled based on the
        structured content of the JSON file. This function also re-links instructors and students to their corresponding
        courses as defined in the loaded data.

        Raises:
            QMessageBox: Provides feedback about the status of the loading operation. An information message is displayed
                         if the data loads successfully, or an error message if the file could not be read or parsed.
        """
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Data File", "", "JSON Files (*.json)")
        if filePath:
            try:
                with open(filePath, 'r') as file:
                    content = json.load(file)
                self.students.clear()
                self.instructors.clear()
                self.courses.clear()
                for crs_data in content.get('courses', []):
                    associated_instructor = next((ins for ins in self.instructors if ins.instructor_id == crs_data.get('instructor_id')), None)
                    new_course = Course(
                        course_id=crs_data.get('course_id', ''),
                        course_name=crs_data.get('course_name', ''),
                        instructor=associated_instructor,
                        enrolled_students=crs_data.get('enrolled_students', [])
                    )
                    for stud_id in crs_data.get('enrolled_students_ids', []):
                        linked_student = next((stu for stu in self.students if stu.student_id == stud_id), None)
                        if linked_student:
                            new_course.add_student(linked_student)
                            linked_student.registered_courses.append(new_course)
                    self.courses.append(new_course)
                    if associated_instructor:
                        associated_instructor.assigned_courses.append(new_course)
                for inst_data in content.get('instructors', []):
                    new_instructor = Instructor(
                        instructor_id=inst_data.get('instructor_id', ''),
                        name=inst_data.get('name', ''),
                        age=inst_data.get('age', None),
                        email=inst_data.get('email', '')
                    )
                    self.instructors.append(new_instructor)
                for stud_data in content.get('students', []):
                    new_student = Student(
                        student_id=stud_data.get('student_id', ''),
                        name=stud_data.get('name', ''),
                        age=stud_data.get('age', None),
                        email=stud_data.get('email', '')
                    )
                    self.students.append(new_student)
                self.RecordDisplayupdate()
                QMessageBox.information(self, "Load Complete", "Data successfully loaded from file!")
            except Exception as e:
                QMessageBox.critical(self, "Load Error", f"An error occurred during data loading: {str(e)}")






if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Window()
    mainWindow.show()
    sys.exit(app.exec_())
