#Student Grading System

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

student = GradingSystem(name,class_name,mark,subjects)
student_grade = student.calculate_grade()
student_average = student.calculate_average()
print(f"Student name : {student.name}")
print(f"class name : {student.class_name}")
for i in range(subjects_num):
    print(f"Subject : {{student.subjects[i]}}, Marks : {student.marks[i]}")
print(f"Student grade : {student_grade}")
print(f"Student average : {student_average}")
    

 
    
