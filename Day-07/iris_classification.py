import sklearn
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

# Load and explore the dataset.
data = sklearn.datasets.load_iris()
x = data.data
y = data.target


# Split the data into training and testing sets.
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    

scaler = sklearn.preprocessing.StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# Train a Logistic Regression model.
model = sklearn.linear_model.LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predict flower species.
model_predictions = model.predict(X_test)

# Display model evaluation metrics.
accuracy = sklearn.metrics.accuracy_score(y_test, model_predictions)
precision = sklearn.metrics.precision_score(y_test, model_predictions, average='weighted')
recall = sklearn.metrics.recall_score(y_test, model_predictions, average='weighted')
f1_score = sklearn.metrics.f1_score(y_test, model_predictions, average='weighted')

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-Score:", f1_score)

# Show the Confusion Matrix.
confusion_matrix = sklearn.metrics.confusion_matrix(y_test, model_predictions)
print("Confusion Matrix:\n", confusion_matrix)

# Print sample predictions with actual values.
for i in range(len(model_predictions)):
    print(f"Predicted: {data.target_names[model_predictions[i]]}, Actual: {data.target_names[y_test[i]]}")

# Bonus (Optional):

# Train a Decision Tree model as well.
decision_tree = sklearn.tree.DecisionTreeClassifier()
decision_tree.fit(X_train, y_train)
decision_tree_predictions = decision_tree.predict(X_test)


# Compare its performance with Logistic Regression.
decision_tree_confusion_matrix = sklearn.metrics.confusion_matrix(y_test, decision_tree_predictions)
print("Decision tree confusion matrix:\n", decision_tree_confusion_matrix)

decision_tree_accuracy = sklearn.metrics.accuracy_score(y_test, decision_tree_predictions)
print("Decision tree accuracy:", decision_tree_accuracy)

decision_tree_precision = sklearn.metrics.precision_score(y_test, decision_tree_predictions, average='weighted')
print("Decision tree precision:", decision_tree_precision)

decision_tree_recall = sklearn.metrics.recall_score(y_test, decision_tree_predictions, average='weighted')
print("Decision tree recall:", decision_tree_recall)

decision_tree_f1_score = sklearn.metrics.f1_score(y_test, decision_tree_predictions, average='weighted')
print("Decision tree F1-score:", decision_tree_f1_score)




