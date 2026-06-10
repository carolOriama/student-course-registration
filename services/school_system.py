import os
from models.student import Student
from models.course import Course

class SchoolSystem:
    def __init__(self):
        self.students = []
        self.courses = []
        self.registrations = []  # List of tuples: (student_id, course_id)

        # File paths relative to the project directory structure
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.students_file = os.path.join(self.base_dir, 'data', 'students.txt')
        self.courses_file = os.path.join(self.base_dir, 'data', 'courses.txt')
        self.registrations_file = os.path.join(self.base_dir, 'data', 'registrations.txt')

    # Helper search methods
    def find_student_by_id(self, student_id):
        for s in self.students:
            if s.student_id.strip().upper() == student_id.strip().upper():
                return s
        return None

    def find_course_by_id(self, course_id):
        for c in self.courses:
            if c.course_id.strip().upper() == course_id.strip().upper():
                return c
        return None

    # Student Management
    def add_student(self, student_id, name, email, phone):
        if not student_id or not student_id.strip():
            raise ValueError("Student ID cannot be empty.")
        if not name or not name.strip():
            raise ValueError("Student name cannot be empty.")
        if "@" not in email:
            raise ValueError("Email must contain '@'.")
        if not phone or not phone.strip():
            raise ValueError("Phone number cannot be empty.")
        
        if self.find_student_by_id(student_id):
            raise ValueError(f"Student with ID {student_id} already exists.")

        student = Student(student_id.strip(), name.strip(), email.strip(), phone.strip())
        self.students.append(student)
        return student

    def view_students(self):
        return self.students

    def search_student(self, search_term):
        if not search_term or not search_term.strip():
            return []
        term = search_term.strip().upper()
        results = []
        for s in self.students:
            if term in s.student_id.upper() or term in s.name.upper():
                results.append(s)
        return results


    # Course Management
    def add_course(self, course_id, name, trainer, capacity):
        if not course_id or not course_id.strip():
            raise ValueError("Course ID cannot be empty.")
        if not name or not name.strip():
            raise ValueError("Course name cannot be empty.")
        if not trainer or not trainer.strip():
            raise ValueError("Trainer name cannot be empty.")
        
        try:
            capacity_val = int(capacity)
        except (ValueError, TypeError):
            raise ValueError("Course capacity must be a number.")

        if capacity_val <= 0:
            raise ValueError("Course capacity must be greater than 0.")

        if self.find_course_by_id(course_id):
            raise ValueError(f"Course with ID {course_id} already exists.")

        course = Course(course_id.strip(), name.strip(), trainer.strip(), capacity_val)
        self.courses.append(course)
        return course

    def view_courses(self):
        return self.courses


    # Registration Management
    def register_student(self, student_id, course_id):
        student = self.find_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} does not exist.")
        
        course = self.find_course_by_id(course_id)
        if not course:
            raise ValueError(f"Course with ID {course_id} does not exist.")

        # Check for duplicate registration
        for reg_s_id, reg_c_id in self.registrations:
            if reg_s_id.upper() == student_id.strip().upper() and reg_c_id.upper() == course_id.strip().upper():
                raise ValueError(f"{student.name} is already registered for this course.")

        # Check capacity
        students_registered = self.view_students_in_course(course_id)
        if len(students_registered) >= course.capacity:
            raise ValueError("Registration failed. This course is already full.")

        self.registrations.append((student.student_id, course.course_id))
        return f"Student {student.name} successfully registered for {course.name}."

    def view_students_in_course(self, course_id):
        course = self.find_course_by_id(course_id)
        if not course:
            raise ValueError(f"Course with ID {course_id} does not exist.")
        
        registered_students = []
        for reg_s_id, reg_c_id in self.registrations:
            if reg_c_id.upper() == course_id.strip().upper():
                student = self.find_student_by_id(reg_s_id)
                if student:
                    registered_students.append(student)
        return registered_students

    def view_courses_for_student(self, student_id):
        student = self.find_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} does not exist.")
        
        registered_courses = []
        for reg_s_id, reg_c_id in self.registrations:
            if reg_s_id.upper() == student_id.strip().upper():
                course = self.find_course_by_id(reg_c_id)
                if course:
                    registered_courses.append(course)
        return registered_courses

    # File Handling
    def load_data(self):
        # 1. Load Students
        self.students = []
        if os.path.exists(self.students_file):
            try:
                with open(self.students_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split('|')
                        if len(parts) == 4:
                            student_id, name, email, phone = parts
                            # Add to list directly to bypass checks if duplicate ID exists in raw file (or clean it)
                            if not self.find_student_by_id(student_id):
                                student = Student(student_id.strip(), name.strip(), email.strip(), phone.strip())
                                self.students.append(student)
            except Exception as e:
                print(f"Error loading students: {e}")

        # 2. Load Courses
        self.courses = []
        if os.path.exists(self.courses_file):
            try:
                with open(self.courses_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split('|')
                        if len(parts) == 4:
                            course_id, name, trainer, capacity = parts
                            if not self.find_course_by_id(course_id):
                                try:
                                    capacity_val = int(capacity)
                                except ValueError:
                                    capacity_val = 50  # Default fallback
                                course = Course(course_id.strip(), name.strip(), trainer.strip(), capacity_val)
                                self.courses.append(course)
            except Exception as e:
                print(f"Error loading courses: {e}")

        # 3. Load Registrations
        self.registrations = []
        if os.path.exists(self.registrations_file):
            try:
                with open(self.registrations_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split('|')
                        if len(parts) >= 2:
                            part1, part2 = parts[0].strip(), parts[1].strip()
                            
                            # Determine order of elements (student_id|course_id vs course_id|student_id)
                            # Or if it is a legacy entry like SWE3040|Digital Electronics (which we skip)
                            student = self.find_student_by_id(part1)
                            course = self.find_course_by_id(part2)
                            if student and course:
                                # Safe register: no duplicate check or capacity check during reload from file
                                pair = (student.student_id, course.course_id)
                                if pair not in self.registrations:
                                    self.registrations.append(pair)
                            else:
                                # Try reverse order
                                course = self.find_course_by_id(part1)
                                student = self.find_student_by_id(part2)
                                if student and course:
                                    pair = (student.student_id, course.course_id)
                                    if pair not in self.registrations:
                                        self.registrations.append(pair)
            except Exception as e:
                print(f"Error loading registrations: {e}")

    def save_data(self):
        os.makedirs(os.path.dirname(self.students_file), exist_ok=True)
        
        # 1. Save Students
        try:
            with open(self.students_file, 'w', encoding='utf-8') as f:
                for s in self.students:
                    f.write(f"{s.student_id}|{s.name}|{s.email}|{s.phone_number}\n")
        except Exception as e:
            print(f"Error saving students: {e}")

        # 2. Save Courses
        try:
            with open(self.courses_file, 'w', encoding='utf-8') as f:
                for c in self.courses:
                    f.write(f"{c.course_id}|{c.name}|{c.trainer}|{c.capacity}\n")
        except Exception as e:
            print(f"Error saving courses: {e}")

        # 3. Save Registrations
        try:
            with open(self.registrations_file, 'w', encoding='utf-8') as f:
                for reg_s_id, reg_c_id in self.registrations:
                    f.write(f"{reg_s_id}|{reg_c_id}\n")
        except Exception as e:
            print(f"Error saving registrations: {e}")
