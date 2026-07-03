import pandas as pd

# Load the dataset.
data = pd.read_csv('student-dataset.csv')

# Display the first and last five rows.
print("first five rows:")
print(data.head(5))
print("\nlast five rows:")
print(data.tail(5))

# Display dataset information.
print("\ndataset info:")
print(data.info())

# Find missing values.
print("\nmissing values:")
print(data.isnull())

# Filter data based on a condition.
print("\nfiltered data (age > 25):")
filtered_data = data[data['age'] > 25]
print(filtered_data)

# Calculate summary statistics.
print("\nsummary statistics:")
print(data.describe())