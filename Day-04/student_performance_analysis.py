import pandas as pd

# Load the dataset using Pandas.
student_data = pd.read_csv('student-dataset.csv')

# Display basic information about the dataset.
print("Dataset Information:")
print(student_data.info())

# Calculate average marks for each subject.
average_marks = student_data[['math.grade', 'english.grade', 'sciences.grade', 'language.grade']].mean()
print("\naverage marks:")
print(average_marks)

# Identify the top 5 performing students.
student_data["Average"] = student_data[
    ['math.grade','english.grade','sciences.grade','language.grade']].mean(axis=1)
top = student_data.sort_values(by="Average", ascending=False).head(5)

print("\nTop 5 Performers:")
print(top)

# Find students scoring below the average.
avg = student_data["Average"].mean()
below_average = student_data[student_data["Average"] < avg].dropna()
print("\nStudents scoring below the average:")
print(below_average)

# Display the total number of students.
print(f"total number of students: {len(student_data)}")

# Save the cleaned or analyzed dataset as a new CSV file.
student_data.to_csv('cleaned-dataset.csv', index=False)
