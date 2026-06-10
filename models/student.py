from models.person import Person

class Student(Person):
    def __init__(self, student_id, name, email, phone_number):
        super().__init__(name, email, phone_number)
        self.student_id = student_id

    def __str__(self):
        return (f"Student ID: {self.student_id}\n"
                f"Name: {self.name}\n"
                f"Email: {self.email}\n"
                f"Phone: {self.phone_number}")
