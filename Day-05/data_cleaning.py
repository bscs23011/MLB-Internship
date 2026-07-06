import pandas as pd

data = pd.read_csv('student-dataset.csv')


# Check for missing values.
print(data.isnull())
print(f"total missing vals: {data.isnull().sum()}")

# Remove duplicate records (if any).

data = data.drop_duplicates()

# Rename one or more columns.

data = data.rename(columns = {"id": "ID"})
data = data.rename(columns = {"latitude": "lat"})
data = data.rename(columns = {"longitude": "lon"})

# Create a new column named Average_Score by calculating the average marks across all subjects.

data["Average_Score"] = (data["math.grade"] + data["english.grade"] + data["language.grade"] + data["sciences.grade"]) / 4

# Create another column named Performance using the following criteria:

#changed the performance criteria accoridng to the data
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

print(data.head())