import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import sklearn.preprocessing as preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


data = pd.read_csv('student_performance.csv')

encoder = preprocessing.LabelEncoder()
data["Program"] = encoder.fit_transform(data["Program"])
data["Average_Score"] = data[["Mathematics", "Python", "Statistics", "Machine_Learning"]].mean(axis=1)

X = data[["Attendance"]]
y = data["Average_Score"]

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=50)
scaler = preprocessing.StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)


#Machine Learning

# Make predictions on the test dataset.

model = LinearRegression()
model.fit(x_train_scaled, y_train)
y_pred = model.predict(x_test_scaled)


# Compare Actual vs Predicted values.

plt.scatter(y_test, y_pred)
plt.xlabel("Actual values")
plt.ylabel("Predicted values")
plt.title("Actual vs predicted values based on Attendance")
plt.show()
plt.savefig("actual_vs_predicted-practice.png")

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


