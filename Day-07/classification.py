import sklearn
from sklearn.model_selection import train_test_split


# Load the dataset. (from Scikit-learn built-in datasets)

data = sklearn.datasets.load_wine()


# Explore the features and target classes.
x = data.data
y = data.target
print("Features shape:", x.shape)
print("Target shape:", y.shape)

#number of classes
print("Number of classes:", len(data.target_names))
print("Target names:", data.target_names)

# Standardize the features.

# Split the data into training and testing sets.
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

scaler = sklearn.preprocessing.StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train a Logistic Regression model.

model = sklearn.linear_model.LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Make predictions.
model_predictions = model.predict(X_test)

# Evaluate the model using the metrics above.
confusion_matrix = sklearn.metrics.confusion_matrix(y_test, model_predictions)
print("Confusion matrix:\n", confusion_matrix)

accuracy = sklearn.metrics.accuracy_score(y_test, model_predictions)
print("Accuracy:", accuracy)

precision = sklearn.metrics.precision_score(y_test, model_predictions, average='weighted')
print("Precision:", precision)

recall = sklearn.metrics.recall_score(y_test, model_predictions, average='weighted')
print("Recall:", recall)

f1_score = sklearn.metrics.f1_score(y_test, model_predictions, average='weighted')
print("F1-score:", f1_score)
