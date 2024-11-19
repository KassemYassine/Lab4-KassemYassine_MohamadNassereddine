import json
import re

class Person:
    """
    Represents a generic person.

    :param name: The name of the person.
    :type name: str
    :param age: The age of the person, must be a valid integer.
    :type age: int
    :param email: The email of the person, must be a valid email format.
    :type email: str
    :raises ValueError: Raises an exception if the age or email is invalid.
    """
    def __init__(self, name, age, email):
        if validate_age(age):
            self.age = age
        if validate_email(email):
            self._email = email
        self.name = name

    def introduce(self):
        """
        Prints a greeting message from the person.

        :return: None
        """
        print("Hello, my name is", self.name, "and I am", self.age, "years old.")

class Student(Person):
    """
    Represents a student, a specialized type of Person.

    :param name: The name of the student.
    :type name: str
    :param age: The age of the student.
    :type age: int
    :param email: The email of the student.
    :type email: str
    :param student_id: The unique identifier for the student.
    :type student_id: str
    """
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        """
        Registers the student in a course if not already registered.

        :param course: The course to register the student in.
        :type course: Course
        :return: None
        """
        if course not in self.registered_courses:
            self.registered_courses.append(course)
            print("Registered", course.course_name, "successfully.")
        else:
            print(course.course_name, "is already registered.")

class Instructor(Person):
    """
    Represents an instructor, a specialized type of Person.

    :param name: The name of the instructor.
    :type name: str
    :param age: The age of the instructor.
    :type age: int
    :param email: The email of the instructor.
    :type email: str
    :param instructor_id: The unique identifier for the instructor.
    :type instructor_id: str
    """
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """
        Assigns a course to the instructor if not already assigned.

        :param course: The course to assign.
        :type course: Course
        :return: None
        """
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            print("Course", course.course_name, "has been assigned to instructor", self.name)
        else:
            print("The course", course.course_name, "is already assigned to this instructor.")

class Course:
    """
    Represents a course with assigned students and instructor.

    :param course_id: The unique identifier for the course.
    :type course_id: str
    :param course_name: The name of the course.
    :type course_name: str
    :param instructor: The instructor responsible for the course.
    :type instructor: Instructor
    """
    def __init__(self, course_id, course_name, instructor):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student):
        """
        Adds a student to the course if not already enrolled.

        :param student: The student to enroll in the course.
        :type student: Student
        :return: None
        """
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
            print(student.name, "has been added to", self.course_name)
        else:
            print(student.name, "is already enrolled in", self.course_name)

def validate_age(age):
    """
    Validates that the provided age is a non-negative integer.

    :param age: The age to validate.
    :type age: int
    :raises ValueError: If age is not an integer or if it is negative.
    :return: True if the age is a valid non-negative integer.
    :rtype: bool
    """
    if not isinstance(age, int):
        raise ValueError("Age must be an integer.")
    if age < 0:
        raise ValueError("Age cannot be negative.")
    return True

def validate_email(email):
    """
    Validates that the provided email address conforms to a standard email format.

    :param email: The email address to validate.
    :type email: str
    :raises ValueError: If the email does not match the standard email format.
    :return: True if the email format is valid.
    :rtype: bool
    """
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email):
        raise ValueError("Invalid email format.")
    return True

def save_data_to_file(instructor, courses, students, filename):
    """
    Saves data related to an instructor, their courses, and students to a JSON file.

    :param instructor: The instructor whose data is to be saved.
    :type instructor: Instructor
    :param courses: List of courses taught by the instructor.
    :type courses: list of Course
    :param students: List of students enrolled in the courses.
    :type students: list of Student
    :param filename: The filename where the data will be saved.
    :type filename: str
    :return: None
    """
    data_to_save = [{
        "type": "instructor",
        "name": instructor.name,
        "age": instructor.age,
        "email": instructor.email,
        "instructor_id": instructor.instructor_id,
        "assigned_courses": [course.course_id for course in instructor.assigned_courses]
    }]

    data_to_save.extend([{
        "type": "course",
        "course_id": course.course_id,
        "course_name": course.course_name,
        "instructor_id": course.instructor.instructor_id,
        "enrolled_students": [student.student_id for student in course.enrolled_students]
    } for course in courses])

    data_to_save.extend([{
        "type": "student",
        "name": student.name,
        "age": student.age,
        "email": student.email,
        "student_id": student.student_id,
        "registered_courses": [course.course_id for course in student.registered_courses]
    } for student in students])

    with open(filename, 'w') as file:
        json.dump(data_to_save, file)

def load_data_from_file(filename):
    """
    Loads data related to an instructor, their courses, and students from a JSON file.

    :param filename: The filename from which the data will be loaded.
    :type filename: str
    :return: A tuple containing the loaded instructor, list of courses, and list of students.
    :rtype: tuple (Instructor, list of Course, list of Student)
    """
    with open(filename, 'r') as file:
        data = json.load(file)

    instructor = None
    courses = []
    students = []

    for item in data:
        if item['type'] == 'instructor':
            instructor = Instructor(item['name'], item['age'], item['email'], item['instructor_id'])

        elif item['type'] == 'course':
            if instructor:
                course = Course(item['course_id'], item['course_name'], instructor)
                courses.append(course)

        elif item['type'] == 'student':
            student = Student(item['name'], item['age'], item['email'], item['student_id'])
            students.append(student)
            for course_id in item['registered_courses']:
                found_course = next((course for course in courses if course.course_id == course_id), None)
                if found_course:
                    found_course.add_student(student)

    if instructor:
        for course in instructor.assigned_courses:
            found_course = next((course for course in courses if course.course_id == course_id), None)
            if found_course:
                instructor.assign_course(found_course)

    return instructor, courses, students
