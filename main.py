import sys
from services.school_system import SchoolSystem

def display_menu():
    print("\n===== Student Course Registration System =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Add Course")
    print("5. View Courses")
    print("6. Register Student to Course")
    print("7. View Students in a Course")
    print("8. View Courses for a Student")
    print("9. Save Data")
    print("10. Load Data")
    print("0. Exit")
    print("==============================================")

def main():
    system = SchoolSystem()
    print("Loading saved data...")
    system.load_data()
    print("Data loaded successfully.")

    while True:
        try:
            display_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                print("\n--- Add Student ---")
                student_id = input("Enter Student ID: ")
                name = input("Enter Name: ")
                email = input("Enter Email: ")
                phone = input("Enter Phone: ")
                
                try:
                    student = system.add_student(student_id, name, email, phone)
                    print(f"\nStudent {student.name} successfully added.")
                except ValueError as e:
                    print(f"\nError: {e}")

            elif choice == "2":
                print("\n--- View All Students ---")
                students = system.view_students()
                if not students:
                    print("No students registered in the system.")
                else:
                    for s in students:
                        print("----------------------------------------")
                        print(s)
                    print("----------------------------------------")

            elif choice == "3":
                print("\n--- Search Student ---")
                search_term = input("Enter Student ID or Name to search: ")
                results = system.search_student(search_term)
                if not results:
                    print("No student found matching the search criteria.")
                else:
                    print(f"\nFound {len(results)} student(s):")
                    for s in results:
                        print("----------------------------------------")
                        print(s)
                    print("----------------------------------------")

            elif choice == "4":
                print("\n--- Add Course ---")
                course_id = input("Enter Course ID: ")
                name = input("Enter Course Name: ")
                trainer = input("Enter Trainer Name: ")
                capacity = input("Enter Capacity: ")

                try:
                    course = system.add_course(course_id, name, trainer, capacity)
                    print(f"\nCourse '{course.name}' successfully added.")
                except ValueError as e:
                    print(f"\nError: {e}")

            elif choice == "5":
                print("\n--- View All Courses ---")
                courses = system.view_courses()
                if not courses:
                    print("No courses available in the system.")
                else:
                    for c in courses:
                        print("----------------------------------------")
                        print(c)
                        # Display number of available slots as a helper
                        registered = len(system.view_students_in_course(c.course_id))
                        print(f"Available Slots: {c.capacity - registered} / {c.capacity}")
                    print("----------------------------------------")

            elif choice == "6":
                print("\n--- Register Student to Course ---")
                student_id = input("Enter Student ID: ")
                course_id = input("Enter Course ID: ")

                try:
                    msg = system.register_student(student_id, course_id)
                    print(f"\nSuccess: {msg}")
                except ValueError as e:
                    print(f"\nError: {e}")

            elif choice == "7":
                print("\n--- View Students in a Course ---")
                course_id = input("Enter Course ID: ")

                try:
                    students = system.view_students_in_course(course_id)
                    course = system.find_course_by_id(course_id)
                    print(f"\nStudents registered in {course.name} ({course_id}):")
                    if not students:
                        print("No students are currently registered in this course.")
                    else:
                        for idx, s in enumerate(students, 1):
                            print(f"{idx}. {s.name} (ID: {s.student_id})")
                except ValueError as e:
                    print(f"\nError: {e}")

            elif choice == "8":
                print("\n--- View Courses for a Student ---")
                student_id = input("Enter Student ID: ")

                try:
                    courses = system.view_courses_for_student(student_id)
                    student = system.find_student_by_id(student_id)
                    print(f"\nCourses registered by {student.name} (ID: {student_id}):")
                    if not courses:
                        print("This student has not registered for any courses.")
                    else:
                        for idx, c in enumerate(courses, 1):
                            print(f"{idx}. {c.name} (ID: {c.course_id})")
                except ValueError as e:
                    print(f"\nError: {e}")

            elif choice == "9":
                print("\nSaving data...")
                system.save_data()
                print("Data saved successfully.")

            elif choice == "10":
                print("\nLoading data...")
                system.load_data()
                print("Data loaded successfully.")


            elif choice == "0":
                print("\nSaving data before exiting...")
                system.save_data()
                print("Goodbye!")
                sys.exit(0)

            else:
                print("\nInvalid option. Please choose a number between 0 and 10.")

        except KeyboardInterrupt:
            print("\n\nDetected interrupt. Saving data before exiting...")
            system.save_data()
            print("Goodbye!")
            sys.exit(0)
        except EOFError:
            print("\n\nDetected EOF. Saving data before exiting...")
            system.save_data()
            print("Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
