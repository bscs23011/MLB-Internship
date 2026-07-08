import sklearn
from sklearn.model_selection import train_test_split



#wine dataset
data = sklearn.datasets.load_breast_cancer()

# Train a simple classification model.

x = data.data
y = data.target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = sklearn.linear_model.LogisticRegression(max_iter=100)
model.fit(x_train, y_train)
model_predictions = model.predict(x_test)

# Evaluate it using Accuracy, Precision, Recall, and F1-Score.
accuracy = sklearn.metrics.accuracy_score(y_test, model_predictions)
precision = sklearn.metrics.precision_score(y_test, model_predictions)
recall = sklearn.metrics.recall_score(y_test, model_predictions)
f1_score = sklearn.metrics.f1_score(y_test, model_predictions)
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-Score:", f1_score)

# Generate a Confusion Matrix.

confusion_matrix = sklearn.metrics.confusion_matrix(y_test, model_predictions)
print("Confusion Matrix:\n", confusion_matrix)

# Understand what each metric tells you about the model.
