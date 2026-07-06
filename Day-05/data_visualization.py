import pandas as pd
import matplotlib.pyplot as plt


data=pd.read_csv('student-dataset.csv')

data["Average_Score"] = (data["math.grade"] + data["english.grade"] + data["language.grade"] + data["sciences.grade"]) / 4
def performance(average):
    if average >= 4:
        return "Excellent"
    elif average >= 3:
        return "Good"
    elif average > 2:
        return "Average"
    else:
        return "Need improvement"

data["performance"] = data["Average_Score"].apply(performance)

# Bar chart showing the average marks of each student.
students = data['name']
average_marks = data["Average_Score"]
plt.bar(students, average_marks)
plt.xlabel('Student Name')
plt.ylabel('Average Marks')
plt.title('Average Marks of each student')
plt.show()

# Histogram showing the distribution of Average Scores.
plt.hist(average_marks)
plt.xlabel('Average Marks')
plt.ylabel('Frequency')
plt.title('Distribution of average scores')
plt.show()

# Scatter plot comparing Python and Machine Learning marks.
#my dataset have math and english scores assuming them as Python and ML marks

data = data.rename(columns={"math.grade": "Python Marks", "english.grade": "ML Marks"})
plt.scatter(data["Python Marks"], data["ML Marks"])
plt.xlabel('Python marks')
plt.ylabel('ML marks')
plt.title('Scatter plot of python vs ML marks')
plt.show()


# Pie chart showing the distribution of students by Performance category.
students = data['name']
performance = data['performance'].value_counts()

plt.pie(performance, labels = performance.index)
plt.title('Distribution of students by performance category')
plt.show()

# Box plot to visualize the spread of marks in all subjects.
plt.boxplot([data["Python Marks"], data["ML Marks"], data["language.grade"], data["sciences.grade"]] , 
            tick_labels=["Python Marks", "ML Marks", "Language Marks", "Science Marks"])
plt.title('Box plot of marks in all subjects')
plt.show()