#Student Grading System

import json
import os   

class GradingSystem:

    def __init__(self, name, class_name, marks, subjects):
        self.name = name
        self.class_name = class_name
        self.marks = marks
        self.subjects = subjects

    def calculate_grade(self):
        total_marks = sum(self.marks)
        average_marks = total_marks / len(self.marks)

        if average_marks >= 90:
            return 'A'
        elif average_marks >= 80:
            return 'B'
        elif average_marks >= 70:
            return 'C'
        elif average_marks >= 60:
            return 'D'
        else:
            return 'F'
        
    def calculate_average(self):
        total_marks = sum(self.marks)
        average_marks = total_marks / len(self.marks)
        return average_marks
    

a = True

if not os.path.exists("student_data.json"):
    with open("student_data.json", "w") as file:
        json.dump([], file)
else:
    with open("student_data.json", "r") as file:
        data = json.load(file)



while a:

    while True:
        student_id = input("Enter student ID: ")

        duplicate = False

        for student in data:
            if student["id"] == student_id:
                duplicate = True
                print("ID already exists.")
                break

        if not duplicate:
            break

    name = input("enter student name : ")
    while True:
        try:
            class_name = int(input("Enter class name (1-12): "))

            if 1 <= class_name <= 12:
                break

            print("Class must be between 1 and 12.")

        except ValueError:
            print("Please enter a valid integer.")


    while True:
        try:
            subjects_num = int(input("Enter number of subjects (1-5): "))

            if 1 <= subjects_num <= 5:
                break

            print("Number of subjects must be between 1 and 5.")

        except ValueError:
            print("Please enter a valid integer.")



    initally_subjects = ["Math", "Science", "English", "History", "Geography"]
    subjects = []
    mark = []
    for i in range(subjects_num):
        subject = input("enter subject name (Math, Science, English, History, Geography): ")
        while subject not in initally_subjects:
            subject = input("Invalid subject name. chose from Math, Science, English, History, Geography: ")
        
        while True:
            try:
                marks = int(input(f"Enter marks for {subject} (0-100): "))

                if 0 <= marks <= 100:
                    break

                print("Marks must be between 0 and 100.")

            except ValueError:
                print("Please enter a valid integer.")

        subjects.append(subject)
        mark.append(marks)
    student = GradingSystem(name,class_name,mark,subjects)
    student_grade = student.calculate_grade()
    student_average = student.calculate_average()

    student_data = {
        "id" : student_id,
        "name": student.name,
        "class_name": student.class_name,
        "subjects": student.subjects,
        "marks": student.marks,
        "grade": student_grade,
        "average": student_average
    }
    data.append(student_data)
    with open("student_data.json", "w") as file:
        json.dump(data, file, indent=4)

    choice = input("Do you want to add another student? (y/n): ")
    if choice.lower() == 'y':
        a = True
    elif choice.lower() == 'n':
        a = False
    else:
        while choice.lower() not in ['y', 'n']:
            choice = input("Invalid choice. Please enter 'y' or 'n': ")

with open("student_data.json", "r") as file:
    data = json.load(file)

for student in data:
    print("id: ",student["id"])
    print(f"Name: {student['name']}")
    print(f"Class: {student['class_name']}")
    print(f"Subjects: {student['subjects']}")
    print(f"Marks: {student['marks']}")
    print(f"Grade: {student['grade']}")
    print(f"Average: {student['average']}")
    print("------------------------")


print("type u to update student data, d to delete student data , s to search student data, q to quit")
choice = input("Enter your choice: ")
while choice != 'q':
    if choice == 'u':
        student_id = input("Enter student id to update: ")


        for student in data:
            if student["id"] == student_id:
                name = input("enter student name : ")
                class_name = input("enter class name: ")
                subjects_num = int(input("enter number of subjects: "))
                subjects = []
                mark = []
                for i in range(subjects_num):
                    subject = input("enter subject name: ")
                    marks = int(input(f"enter marks for {subject} : "))
                    subjects.append(subject)
                    mark.append(marks)
                student["name"] = name
                student["class_name"] = class_name
                student["subjects"] = subjects
                student["marks"] = mark
                temp = GradingSystem(name,class_name,mark,subjects)
                student["grade"] = temp.calculate_grade()
                student["average"] = temp.calculate_average()

        with open("student_data.json", "w") as file:
            json.dump(data, file, indent=4)
    elif choice == 'd':
        student_id = input("Enter student id to delete: ")
        for student in data:
            if student["id"] == student_id:
                data.remove(student)
                print("Student data deleted successfully.")
                break
        with open("student_data.json", "w") as file:
            json.dump(data, file, indent=4)

    elif choice == 's':
        student_id = input("Enter student id to search: ")
        found = False
        for student in data:
            if student["id"] == student_id:
                print("id: ",student["id"])
                print(f"Name: {student['name']}")
                print(f"Class: {student['class_name']}")
                print(f"Subjects: {student['subjects']}")
                print(f"Marks: {student['marks']}")
                print(f"Grade: {student['grade']}")
                print(f"Average: {student['average']}")
                found = True
                break
        if not found:
            print("Student not found.")
    else:
        print("Invalid choice. Please try again.")
        
    choice = input("Enter your choice:(u/d/s/q) ")


    




    

 
    
