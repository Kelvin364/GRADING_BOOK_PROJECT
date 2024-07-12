from gradebook import GradeBook, Student, Course
from tabulate import tabulate

def teacher_menu(gradebook):
    while True:
        print("\nTeacher Menu:")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Register Student for Course")
        print("4. Calculate GPA")
        print("5. Calculate Ranking")
        print("6. Search by Grade")
        print("7. Generate Transcript")
        print("8. Exit to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            email = input("Enter student email: ")
            names = input("Enter student names: ")
            student = Student(email, names)
            gradebook.add_student(student)
        elif choice == '2':
            name = input("Enter course name: ")
            trimester = input("Enter course trimester: ")
            credits = int(input("Enter course credits: "))
            grade = float(input("Enter course grade (0 if not applicable): "))
            course = Course(name, trimester, credits, grade)
            gradebook.add_course(course)
        elif choice == '3':
            student_email = input("Enter student email: ")
            course_name = input("Enter course name: ")
            gradebook.register_student_for_course(student_email, course_name)
        elif choice == '4':
            student_email = input("Enter student email: ")
            gpa = gradebook.calculate_GPA(student_email)
            print(f"GPA of {student_email}: {gpa}")
        elif choice == '5':
            ranking = gradebook.calculate_ranking()
            print("Student Ranking by GPA:")
            table = [[i + 1, student.names, student.GPA] for i, student in enumerate(ranking)]
            headers = ["Rank", "Student Name", "GPA"]
            print(tabulate(table, headers, tablefmt="grid"))
        elif choice == '6':
            grade = float(input("Enter grade to search for: "))
            students = gradebook.search_by_grade(grade)
            print("Students with the specified grade:")
            table = [[student.names, student.email] for student in students]
            headers = ["Student Name", "Email"]
            print(tabulate(table, headers, tablefmt="grid"))
        elif choice == '7':
            student_email = input("Enter student email: ")
            transcript = gradebook.generate_transcript(student_email)
            if transcript:
                print(f"Transcript for {student_email}:")
                table = [[course['name'], course['trimester'], course['credits'], course['grade']] for course in transcript['courses']]
                headers = ["Course Name", "Trimester", "Credits", "Grade"]
                print(tabulate(table, headers, tablefmt="grid"))
                print(f"GPA: {transcript['GPA']}")
            else:
                print("Student not found.")
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")

def student_menu(gradebook):
    email = input("Enter your email: ")
    name = input("Enter your name: ")
    student = next((s for s in gradebook.student_list if s.email == email and s.names == name), None)

    if not student:
        print("Student not found.")
        return

    while True:
        print("\nStudent Menu:")
        print("1. View Courses")
        print("2. Learn Courses")
        print("3. Take Test")
        print("4. View Transcript")
        print("5. Exit to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            if student.courses_registered:
                print("Courses you are enrolled in:")
                table = [[course.name, course.trimester, course.credits, course.grade] for course in student.courses_registered]
                headers = ["Course Name", "Trimester", "Credits", "Grade"]
                print(tabulate(table, headers, tablefmt="grid"))
            else:
                print("You are not enrolled in any courses.")
        elif choice == '2':
            print("click here to learn(https://docs.google.com/presentation/d/1fqoRKIdtH5APhsZwcjrQOMx6iflsHrRKym_LoZr7Cdk/edit?usp=sharing)")
        elif choice == '3':
            if student.courses_registered:
                for course in student.courses_registered:
                    grade = float(input(f"Enter grade for {course.name}: "))
                    course.grade = grade
                student.calculate_GPA()
                gradebook.save_students()
                print(f"Your GPA has been updated: {student.GPA}")
            else:
                print("You are not enrolled in any courses.")
        elif choice == '4':
            transcript = gradebook.generate_transcript(email)
            if transcript:
                print(f"Transcript for {email}:")
                table = [[course['name'], course['trimester'], course['credits'], course['grade']] for course in transcript['courses']]
                headers = ["Course Name", "Trimester", "Credits", "Grade"]
                print(tabulate(table, headers, tablefmt="grid"))
                print(f"GPA: {transcript['GPA']}")
            else:
                print("Student not found.")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    gradebook = GradeBook()

    while True:
        print("\nMain Menu:")
        print("1. Teacher")
        print("2. Student")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            email = input("Enter your email: ")
            if email.endswith('@alueducation.com'):
                teacher_menu(gradebook)
            else:
                print("Invalid email. Access denied.")
        elif choice == '2':
            student_menu(gradebook)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
