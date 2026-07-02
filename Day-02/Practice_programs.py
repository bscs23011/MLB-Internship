import json

# FILE HANDLING

with open("data.txt", "w") as file:
    file.write("I'm Hassan \n")
    file.write("I'm an ML/AI internee at ML-Bench \n")

with open("data.txt", "r") as file: #reads all lines at once
    data = file.read()
print(data)

with open("data.txt", "r") as file:
    line = file.readline()
    print(f"Using readline(): {line}") #reads one line at a time

with open("data.txt", "r") as file:
    line = file.readlines()
    print(f"Using readlines(): {line}") #returns lines as a list

with open("data.txt", "a") as file:
    file.write("I am learning basic python programming \n")

with open("data.txt", "r") as file:
    data = file.read()
print(data)

count = 0
with open("data.txt", "r") as file:
    for line in file:
        count += 1
print(f"Number of lines in the file: {count}")

#JSON

student = [
    {
        "name": "Hassan",
        "age": 21,
        "grade": "A",
        "subjects": ["Math", "Science", "English"]
    },
    {
        "name": "Ali",
        "age": 20,
        "grade": "B",
        "subjects": ["Math", "History", "English"]
    }
]

with open("students.json", "w") as file:
    json.dump(student, file, indent=4)

with open("students.json", "r") as file:
    data = json.load(file)
print("\nData:")
print(data)

for student in data:
    if student["name"] == "Hassan":
        student["grade"] = "A+"
        

with open("students.json", "w") as file:
    json.dump(data, file, indent=4)

with open("students.json", "r") as file:
    data = json.load(file)
print("\nData after modification:")
print(data)

another_student = {
    "name": "Muhammad",
    "age": 22,  
    "grade": "A",
    "subjects": ["Math", "Science", "English"]
}

data.append(another_student)

with open("students.json", "w") as file:
    json.dump(data, file, indent=4)

with open("students.json", "r") as file:
    data = json.load(file)
print("\nData after adding another student:")
print(data)


#dump saves the record to the file and dumps returns the record as a string.