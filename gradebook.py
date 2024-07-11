import csv

class Student:
    def __init__(self, email, names):
        self.email = email
        self.names = names
        self.courses_registered = []
        self.GPA = 0.0

    def calculate_GPA(self):
        total_credits = sum(course.credits for course in self.courses_registered)
        if total_credits == 0:
            return 0
        total_points = sum(course.grade * course.credits for course in self.courses_registered)
        self.GPA = total_points / total_credits
        return self.GPA

    def register_for_course(self, course):
        self.courses_registered.append(course)

    def to_csv_row(self):
        return [self.email, self.names, ','.join(course.name for course in self.courses_registered), self.GPA]

    @staticmethod
    def from_csv_row(row, courses):
        email, names, courses_registered_str, GPA = row
        student = Student(email, names)
        student.GPA = float(GPA)
        course_names = courses_registered_str.split(',')
        student.courses_registered = [course for course in courses if course.name in course_names]
        return student


class Course:
    def __init__(self, name, trimester, credits, grade=0):
        self.name = name
        self.trimester = trimester
        self.credits = credits
        self.grade = grade

    def to_csv_row(self):
        return [self.name, self.trimester, self.credits, self.grade]

    @staticmethod
    def from_csv_row(row):
        name, trimester, credits, grade = row
        return Course(name, trimester, int(credits), float(grade))


class GradeBook:
    def __init__(self, students_file='students.csv', courses_file='courses.csv'):
        self.students_file = students_file
        self.courses_file = courses_file
        self.student_list = self.load_students()
        self.course_list = self.load_courses()

    def add_student(self, student):
        self.student_list.append(student)
        self.save_students()

    def add_course(self, course):
        self.course_list.append(course)
        self.save_courses()

    def register_student_for_course(self, student_email, course_name):
        student = next((s for s in self.student_list if s.email == student_email), None)
        course = next((c for c in self.course_list if c.name == course_name), None)
        if student and course:
            student.register_for_course(course)
            self.save_students()

    def calculate_GPA(self, student_email):
        student = next((s for s in self.student_list if s.email == student_email), None)
        if student:
            gpa = student.calculate_GPA()
            self.save_students()
            return gpa
        return None

    def calculate_ranking(self):
        return sorted(self.student_list, key=lambda s: s.GPA, reverse=True)

    def search_by_grade(self, grade):
        return [student for student in self.student_list if any(course.grade == grade for course in student.courses_registered)]

    def generate_transcript(self, student_email):
        student = next((s for s in self.student_list if s.email == student_email), None)
        if student:
            return {
                'email': student.email,
                'names': student.names,
                'GPA': student.GPA,
                'courses': [{'name': course.name, 'trimester': course.trimester, 'credits': course.credits, 'grade': course.grade} for course in student.courses_registered]
            }
        return None

    def load_students(self):
        students = []
        courses = self.load_courses()
        try:
            with open(self.students_file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                for row in reader:
                    students.append(Student.from_csv_row(row, courses))
        except FileNotFoundError:
            pass
        return students

    def save_students(self):
        with open(self.students_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['email', 'names', 'courses_registered', 'GPA'])
            for student in self.student_list:
                writer.writerow(student.to_csv_row())

    def load_courses(self):
        courses = []
        try:
            with open(self.courses_file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                for row in reader:
                    courses.append(Course.from_csv_row(row))
        except FileNotFoundError:
            pass
        return courses

    def save_courses(self):
        with open(self.courses_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['name', 'trimester', 'credits', 'grade'])
            for course in self.course_list:
                writer.writerow(course.to_csv_row())
