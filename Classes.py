import json
import re

class Person:
    """
    Represents a general person characterized by name, age, and email.

    Attributes:
        name (str): The person's name.
        age (int): The person's age.
        _email (str): The person's email address, which is validated upon initialization.

    Methods:
        introduce(): Prints a greeting that includes the person's name and age.
    """
    def __init__(self, name, age, email):
        """
        Initializes a new instance of a Person.

        Validates and sets the age and email attributes. If validation fails,
        these attributes may not be set.

        Args:
            name (str): The name of the person.
            age (int): The age of the person.
            email (str): The email address of the person.
        """
        if validate_age(age):
            self.age = age
        
        if validate_email(email):
            self._email = email

        self.name = name

    def introduce(self):
        """ Prints an introductory sentence about the person. """
        print("Hello, my name is", self.name, "and I am", self.age, "years old.")

class Student(Person):
    """
    Represents a student, which is a specific type of person also characterized by a student ID and registered courses.

    Attributes:
        student_id (str): Unique identifier for the student.
        registered_courses (list): List of courses the student is registered in.

    Methods:
        register_course(course): Registers the student in a specified course if not already registered.
    """
    def __init__(self, name, age, email, student_id):
        """
        Initializes a new instance of a Student.

        Args:
            name (str): The student's name.
            age (int): The student's age.
            email (str): The student's email address.
            student_id (str): The student's unique identifier.
        """
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        """
        Adds a course to the student's list of registered courses if not already added.

        Args:
            course (Course): The course to register.

        Prints a message indicating successful registration or that the course is already registered.
        """
        if course not in self.registered_courses:  
            self.registered_courses.append(course)
            print("Registered", course.course_name, "successfully.")
        else:
            print(course.course_name, "is already registered.")

class Instructor(Person):
    """
    Represents an instructor, a type of person characterized by an instructor ID and assigned courses.

    Attributes:
        instructor_id (str): Unique identifier for the instructor.
        assigned_courses (list): List of courses assigned to the instructor.

    Methods:
        assign_course(course): Assigns a course to the instructor if not already assigned.
    """
    def __init__(self, name, age, email, instructor_id):
        """
        Initializes a new instance of an Instructor.

        Args:
            name (str): The instructor's name.
            age (int): The instructor's age.
            email (str): The instructor's email address.
            instructor_id (str): The instructor's unique identifier.
        """
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """
        Adds a course to the instructor's list of assigned courses if not already added.

        Args:
            course (Course): The course to assign.

        Prints a message indicating successful assignment or that the course is already assigned.
        """
        if course not in self.assigned_courses:  
            self.assigned_courses.append(course)
            print("Course", course.course_name, "has been assigned to instructor", self.name)
        else:
            print("The course", course.course_name, "is already assigned to this instructor.")

class Course:
    """
    Represents a course characterized by a course ID, course name, the instructor, and enrolled students.

    Attributes:
        course_id (str): Unique identifier for the course.
        course_name (str): Name of the course.
        instructor (Instructor): The instructor teaching the course.
        enrolled_students (list): List of students enrolled in the course.

    Methods:
        add_student(student): Enrolls a student in the course if not already enrolled.
    """
    def __init__(self, course_id, course_name, instructor):
        """
        Initializes a new instance of a Course.

        Args:
            course_id (str): The unique identifier for the course.
            course_name (str): The name of the course.
            instructor (Instructor): The instructor associated with the course.
        """
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student):
        """
        Adds a student to the course's list of enrolled students if not already added.

        Args:
            student (Student): The student to enroll.

        Prints a message indicating successful enrollment or that the student is already enrolled.
        """
        if student not in self.enrolled_students:  
            self.enrolled_students.append(student)
            print(student.name, "has been added to", self.course_name)
        else:
            print(student.name, "is already enrolled in", self.course_name)



def save_data_to_file(instructor, courses, students, filename):
    """
    Saves data about an instructor, their courses, and students to a JSON file.

    Args:
        instructor (Instructor): The instructor whose data is to be saved.
        courses (list): A list of Course objects related to the instructor.
        students (list): A list of Student objects enrolled in the courses.
        filename (str): The path to the file where the data will be saved.

    Saves the following details:
    - Instructor details and the courses they are assigned.
    - Course details including enrolled students.
    - Student details and the courses they are registered in.
    """
    data_to_save = [
        {
            "type": "instructor",
            "name": instructor.name,
            "age": instructor.age,
            "email": instructor.email,
            "instructor_id": instructor.instructor_id,
            "assigned_courses": [course.course_id for course in instructor.assigned_courses]
        }
    ]

    data_to_save.extend([
        {
            "type": "course",
            "course_id": course.course_id,
            "course_name": course.course_name,
            "instructor_id": course.instructor.instructor_id,
            "enrolled_students": [student.student_id for student in course.enrolled_students]
        }
        for course in courses
    ])

    data_to_save.extend([
        {
            "type": "student",
            "name": student.name,
            "age": student.age,
            "email": student.email,
            "student_id": student.student_id,
            "registered_courses": [course.course_id for course in student.registered_courses]
        }
        for student in students
    ])

    with open(filename, 'w') as file:
        json.dump(data_to_save, file)


def load_data_from_file(filename):
    """
    Loads data about an instructor, their courses, and students from a JSON file.

    Args:
        filename (str): The path to the file from which data will be loaded.

    Returns:
        tuple: A tuple containing the loaded instructor object, a list of course objects, and a list of student objects.

    Raises:
        ValueError: If there is an issue with the course or student data linkage.
    """
    with open(filename, 'r') as file:
        data = json.load(file)

    instructor = None
    courses = []
    students = []

    for item in data:
        if item['type'] == 'instructor':
            instructor = Instructor(
                item['name'], item['age'], item['email'], item['instructor_id']
            )

        elif item['type'] == 'course':
            if instructor:  
                course = Course(item['course_id'], item['course_name'], instructor)
                courses.append(course)

        elif item['type'] == 'student':
            student = Student(
                item['name'], item['age'], item['email'], item['student_id']
            )
            students.append(student)
            for course_id in item['registered_courses']:
                found_course = next((course for course in courses if course.course_id == course_id), None)
                if found_course:
                    found_course.add_student(student)

    if instructor:
        for course_id in instructor.assigned_courses:
            found_course = next((course for course in courses if course.course_id == course_id), None)
            if found_course:
                instructor.assign_course(found_course)

    return instructor, courses, students

def validate_age(age):
    """
    Validates if the provided age is an integer and non-negative.

    Args:
        age (int): The age to validate.

    Returns:
        bool: True if the age is valid, raises ValueError otherwise.

    Raises:
        ValueError: If age is not an integer or is negative.
    """
    if not isinstance(age, int):
        raise ValueError("Age must be an integer.")
    if age < 0:
        raise ValueError("Age cannot be negative.")
    return True

def validate_email(email):
    """
    Validates if the provided email matches a specific pattern.

    Args:
        email (str): The email to validate.

    Returns:
        bool: True if the email is valid, raises ValueError otherwise.

    Raises:
        ValueError: If the email does not match the expected pattern.
    """
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email):
        raise ValueError("Invalid email format.")
    return True
