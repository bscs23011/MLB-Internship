import sklearn
import sklearn.datasets as datasets
from sklearn.model_selection import train_test_split

data = datasets.load_breast_cancer()


# Use GridSearchCV to find the best parameters for the Logistic Regression model.
grid_search = sklearn.model_selection.GridSearchCV(
    estimator=sklearn.linear_model.LogisticRegression(max_iter=1000),
    param_grid={
        'C': [0.01, 0.1, 1, 10, 100], #penalty was set to default
        'solver': ['liblinear']
    }, cv=5)

x_train, x_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

scalar = sklearn.preprocessing.StandardScaler()
x_train = scalar.fit_transform(x_train)
x_test = scalar.transform(x_test)

grid_search.fit(x_train, y_train)

print("Best parameters found: ", grid_search.best_params_)
print("Best cross-validation score: ", grid_search.best_score_)

# Compare:

# Baseline Model Performance

# Accuracy: 0.9736842105263158
# Precision: 0.9722222222222222
# Recall: 0.9859154929577465
# F1-Score: 0.9790209790209791
# Confusion Matrix:
#  [[41  2]
#  [ 1 70]]

# Tuned Model Performance
accuracy = sklearn.metrics.accuracy_score(y_test, grid_search.predict(x_test))
print("Accuracy:", accuracy)

precision = sklearn.metrics.precision_score(y_test, grid_search.predict(x_test))
print("Precision:", precision)

recall = sklearn.metrics.recall_score(y_test, grid_search.predict(x_test))
print("Recall:", recall)

f1_score = sklearn.metrics.f1_score(y_test, grid_search.predict(x_test))
print("F1-Score:", f1_score)

confusion_matrix = sklearn.metrics.confusion_matrix(y_test, grid_search.predict(x_test))
print("Confusion Matrix:\n", confusion_matrix)