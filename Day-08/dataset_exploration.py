import pandas as pd
import sklearn.datasets as datasets

# Load the dataset.
data = datasets.load_breast_cancer()

# Convert it into a Pandas DataFrame.
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target


# Explore the data using:

# head()
print("first 5 rows of the dataframe:")
print(df.head())

# info()
print("dataframe info:")
print(df.info())

# describe()
print("dataframe description:")
print(df.describe())

# Check the distribution of the target classes.
target = df['target'].value_counts()
print("Distribution of target classes:")
print(target)