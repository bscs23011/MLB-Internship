import sklearn
from sklearn import datasets
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns


# Loads the dataset.
data = datasets.load_breast_cancer()

# Preprocesses the data.
x_train, x_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)
scalar = sklearn.preprocessing.StandardScaler()
x_train = scalar.fit_transform(x_train)
x_test = scalar.transform(x_test)


# Trains a Logistic Regression model.
model = sklearn.linear_model.LogisticRegression(max_iter=1000)
model.fit(x_train, y_train)

# Performs Hyperparameter Tuning using GridSearchCV.
grid_search = sklearn.model_selection.GridSearchCV(
    estimator=sklearn.linear_model.LogisticRegression(max_iter=1000),
    param_grid={
        'C': [0.01, 0.1, 1, 10, 100], #penalty was set to default
        'solver': ['liblinear']
    }, cv=5)
grid_search.fit(x_train, y_train)

# Evaluates the model before and after tuning.
#before tuning:
LR_accuracy = sklearn.metrics.accuracy_score(y_test, model.predict(x_test))
LR_precision = sklearn.metrics.precision_score(y_test, model.predict(x_test))
LR_recall = sklearn.metrics.recall_score(y_test, model.predict(x_test))
LR_f1_score = sklearn.metrics.f1_score(y_test, model.predict(x_test))
LR_confusion_matrix = sklearn.metrics.confusion_matrix(y_test, model.predict(x_test))

# after tuning:
Tuned_accuracy = sklearn.metrics.accuracy_score(y_test, grid_search.predict(x_test))
Tuned_precision = sklearn.metrics.precision_score(y_test, grid_search.predict(x_test))
Tuned_recall = sklearn.metrics.recall_score(y_test, grid_search.predict(x_test))
Tuned_f1_score = sklearn.metrics.f1_score(y_test, grid_search.predict(x_test))
Tuned_confusion_matrix = sklearn.metrics.confusion_matrix(y_test, grid_search.predict(x_test))

# Prints the best parameters selected by GridSearchCV.
print("Best parameters found: ", grid_search.best_params_)
print("Best cross-validation score: ", grid_search.best_score_)

# Displays the final evaluation metrics.
print("\nBaseline Model Performance:")
print("Accuracy:", LR_accuracy)
print("Precision:", LR_precision)
print("Recall:", LR_recall)
print("F1-Score:", LR_f1_score)
print("Confusion Matrix:\n", LR_confusion_matrix)

print("\nTuned Model Performance:")
print("Accuracy:", Tuned_accuracy)
print("Precision:", Tuned_precision)
print("Recall:", Tuned_recall)
print("F1-Score:", Tuned_f1_score)
print("Confusion Matrix:\n", Tuned_confusion_matrix)

# Bonus (Optional):

# Create a confusion matrix heatmap and compare the baseline and tuned model results.

plt.figure()
sns.heatmap(LR_confusion_matrix, annot=True, fmt='d', cmap='Blues')
plt.title("Baseline Model Confusion Matrix")
plt.savefig("baseline_confusion_matrix.png")
plt.show()

plt.figure()
sns.heatmap(Tuned_confusion_matrix, annot=True, fmt='d', cmap='Blues')
plt.title("Tuned Model Confusion Matrix")
plt.savefig("tuned_confusion_matrix.png")
plt.show()