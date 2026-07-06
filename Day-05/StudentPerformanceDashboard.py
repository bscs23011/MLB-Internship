import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv('student-dataset.csv')

# How many students are in the dataset?
number = len(data)
print(f"total number of students: {number}")

# What is the average score for each subject?
avg_math = data["math.grade"].mean()
avg_english = data["english.grade"].mean()
avg_language = data["language.grade"].mean()
avg_science = data["sciences.grade"].mean()

print(f'Average score for math: {avg_math}')
print(f'Average score for english: {avg_english}')
print(f'Average score for language: {avg_language}')
print(f'Average score for science: {avg_science}')

# Who are the Top 5 performing students?

data["Average_Score"] = (data["math.grade"] + data["english.grade"] + data["language.grade"] + data["sciences.grade"]) / 4
data = data.sort_values(by="Average_Score", ascending=False)
top_5_students = data.head(5)
print(top_5_students[["name", "Average_Score"]])

# Which students need improvement?
imp = data[data["Average_Score"] < 3]
print(imp[["name", "Average_Score"]])


#Which subject has the highest class average?
highest = max(avg_math, avg_english, avg_language, avg_science)
if highest == avg_math:
    subject = "math"
elif highest == avg_english:
    subject = "english"
elif highest == avg_language:
    subject = "language"
else:
    subject = "sciences"

print(f'subject with the highest class average is: {highest} : {subject}' )


# Visualize your findings using appropriate charts.

plt.bar(['Math', 'English', 'Language', 'Science'], [avg_math, avg_english, avg_language, avg_science])
plt.title('Average scores by subject')
plt.xlabel('Subjects')
plt.ylabel('Average scores')    
plt.show()
plt.savefig('average-scores-subject.png')

plt.plot(top_5_students['name'], top_5_students['Average_Score'] , marker= 'x')
plt.title('Top 5 performing Students')
plt.xlabel('Student names')
plt.ylabel('Average scores')
plt.show()
plt.savefig('top-5-students.png')


plt.bar(imp['name'], imp['Average_Score'])
plt.title('Students who need improvement')  
plt.xlabel('Student names')
plt.ylabel('Average scores')
plt.show()
plt.savefig('students-need-improvement.png')



data.to_csv('cleaned-student-performance.csv', index=False)