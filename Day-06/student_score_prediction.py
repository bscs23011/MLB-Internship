
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import sklearn.preprocessing as preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


# Loads the dataset.
data = pd.read_csv("student_performance.csv")

# Preprocesses the data.
encoder = preprocessing.LabelEncoder()
data["Program"] = encoder.fit_transform(data["Program"])
data["Average_Score"] = data[["Mathematics", "Python", "Statistics", "Machine_Learning"]].mean(axis=1)


# Trains a Linear Regression model.
X = data[["Age", "Attendance", "Program"]]
y = data["Average_Score"]

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=50)

scaler = preprocessing.StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

model = LinearRegression()
model.fit(x_train_scaled, y_train)

# Predicts student average scores.
y_pred = model.predict(x_test_scaled)

# Displays the model evaluation metrics.
print("Mean absolute error:", mean_absolute_error(y_test, y_pred))
print("Mean squared error:", mean_squared_error(y_test, y_pred))
print("R-squared Score:", r2_score(y_test, y_pred))

# Prints a comparison table of Actual vs Predicted scores
comparison = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
print(comparison)


plt.scatter(y_test, y_pred)
plt.xlabel("Actual values")
plt.ylabel("Predicted values")
plt.title("Actual vs predicted values based on Attendance, Program and Age")
plt.show()
plt.savefig("actual_vs_predicted_mini-project.png")