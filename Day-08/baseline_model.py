import sklearn
from sklearn import datasets
from sklearn.model_selection import train_test_split

data = datasets.load_breast_cancer()

# Split the dataset into training and testing sets.
x_train, x_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

scalar = sklearn.preprocessing.StandardScaler()
x_train = scalar.fit_transform(x_train)
x_test = scalar.transform(x_test)

# Train a Logistic Regression model.
model = sklearn.linear_model.LogisticRegression(max_iter=1000)
model.fit(x_train, y_train)

# Evaluate the model using:
  
# Accuracy
accuracy = sklearn.metrics.accuracy_score(y_test, model.predict(x_test))
print("Accuracy:", accuracy)

# Precision
precision = sklearn.metrics.precision_score(y_test, model.predict(x_test))
print("Precision:", precision)

# Recall
recall = sklearn.metrics.recall_score(y_test, model.predict(x_test))
print("Recall:", recall)

# F1-Score
f1_score = sklearn.metrics.f1_score(y_test, model.predict(x_test))
print("F1-Score:", f1_score)

# Confusion Matrix
confusion_matrix = sklearn.metrics.confusion_matrix(y_test, model.predict(x_test))
print("Confusion Matrix:\n", confusion_matrix)
