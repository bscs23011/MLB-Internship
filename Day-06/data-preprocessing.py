import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import sklearn.preprocessing as preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


# Load the dataset.

data = pd.read_csv('student_performance.csv')

# Encode any categorical columns if required.

encoder = preprocessing.LabelEncoder()
print(data.head())
data["Program"] = encoder.fit_transform(data["Program"])
print(data.head())

# Create a new column named Average_Score (if not already created).
data["Average_Score"] = data[["Mathematics", "Python", "Statistics", "Machine_Learning"]].mean(axis=1)
print(data.head())

# Select appropriate feature columns (X) and target column (y).
X = data[["Age"]]
y = data["Average_Score"]

# Split the dataset into Training (80%) and Testing (20%).

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=50)
print("Training:", x_train.shape)
print("Testing :", x_test.shape)


# Apply feature scaling where appropriate
scaler = preprocessing.StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

print(x_train_scaled.mean(axis=0))
print(x_train_scaled.std(axis=0))
print(x_test_scaled.mean(axis=0))
print(x_test_scaled.std(axis=0))



#Machine Learning

# Make predictions on the test dataset.

model = LinearRegression()
model.fit(x_train_scaled, y_train)
y_pred = model.predict(x_test_scaled)


# Compare Actual vs Predicted values.

plt.scatter(y_test, y_pred)
plt.xlabel("Actual values")
plt.ylabel("Predicted values")
plt.title("Actual vs predicted values")
plt.show()
plt.savefig("actual_vs_predicted.png")

# Calculate:

  
# Mean Absolute Error (MAE)

mae = mean_absolute_error(y_test, y_pred)
print("Mean absolute error :", mae)

# Mean Squared Error (MSE)

mse = mean_squared_error(y_test, y_pred)
print("Mean squared error  :", mse)

# R² Score

r2 = r2_score(y_test, y_pred)
print("R² Score :", r2)


