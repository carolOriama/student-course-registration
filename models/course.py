class Course:
    def __init__(self, course_id, name, trainer, capacity):
        self.course_id = course_id
        self.name = name
        self.trainer = trainer
        self.capacity = int(capacity)

    def __str__(self):
        return (f"Course ID: {self.course_id}\n"
                f"Course Name: {self.name}\n"
                f"Trainer: {self.trainer}\n"
                f"Capacity: {self.capacity} students")
