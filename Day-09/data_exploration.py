import sklearn.datasets as datasets
import pandas as pd

# Load the Iris dataset.
data = datasets.load_iris()

# Explore the dataset using Pandas.
df = pd.DataFrame(data.data, columns=data.feature_names)

print(df.describe())
print(df.head())
print(df.info())