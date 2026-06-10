# Student Course Registration System

A terminal-based Python application designed to help a training school manage students, courses, and student registrations. 

## Features Implemented

1. **Student Management**: Add a new student, view all students, and search for students by name or ID. Prevents duplicate Student IDs.
2. **Course Management**: Add a new course and view all courses. Prevents duplicate Course IDs.
3. **Registration Management**: Register students to courses, preventing double registration and enforcing course capacity limits.
4. **File Handling**: Automatic data loading at startup and data saving upon exit. Supports manual saving/loading. Uses pipe-separated (`|`) text files.

## Classes and Object-Oriented Principles

- **`Person`** (`models/person.py`): The base class storing core identity fields (`name`, `email`, `phone_number`).
- **`Student`** (`models/student.py`): Inherits from `Person`, adding `student_id` and custom string representations (`__str__`).
- **`Course`** (`models/course.py`): Models a course with `course_id`, `name`, `trainer`, and `capacity`.
- **`SchoolSystem`** (`services/school_system.py`): Manages the list of students, courses, and registration pairs. Encapsulates business logic, data persistence, and data validations.

## Validation & Error Handling

- Ensures all inputs are non-empty.
- Emails must contain `@`.
- Course capacity must be a positive integer.
- Intercepts duplicate entries (IDs).
- Prevents course capacity overflow.
- Handles invalid inputs, EOFError, and keyboard interrupts gracefully without crashing.

## How to Run

1. Make sure you are in the project's root directory:
   ```bash
   cd student-course-registration
   ```
2. Execute the application using Python 3:
   ```bash
   python3 main.py
   ```

## Folder Structure

```
student-course-registration/
│
├── main.py
├── models/
│   ├── person.py
│   ├── student.py
│   └── course.py
│
├── services/
│   └── school_system.py
│
├── data/
│   ├── students.txt
│   ├── courses.txt
│   └── registrations.txt
│
└── README.md
```
