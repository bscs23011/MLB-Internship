What you learned about model evaluation.

Model evaluation is used to measure how well a machine learning model performs on unseen data.
I learned the importance of comparing training and testing performance to detect underfitting and overfitting.
I learned how cross-validation provides a more reliable estimate of model performance by evaluating the model on multiple data splits.
I also learned how to use evaluation metrics such as Accuracy, Precision, Recall, F1-Score, and the Confusion Matrix to assess classification models.

What hyperparameter tuning is and why it matters.

Hyperparameter tuning is the process of finding the best values for a model's hyperparameters before training.
Instead of relying on default settings, tuning helps improve the model's performance and generalization.
I learned how GridSearchCV tests different combinations of hyperparameters using cross-validation and selects the combination that produces the best average performance.
Proper hyperparameter tuning can increase accuracy, reduce classification errors, and help prevent overfitting.

The best parameters found by GridSearchCV.
Best parameters found:  {'C': 0.1, 'solver': 'liblinear'}
Best cross-validation score:  0.9780219780219781

Comparison between the baseline and tuned models.
Baseline Model Performance:
Accuracy: 0.9736842105263158
Precision: 0.9722222222222222
Recall: 0.9859154929577465
F1-Score: 0.9790209790209791
 [ 1 70]]

Tuned Model Performance:
Accuracy: 0.9912280701754386
Precision: 0.9861111111111112
Recall: 1.0
F1-Score: 0.993006993006993
Confusion Matrix:
 [[42  1]
 [ 0 71]]
 
Key observations from the results.
Hyperparameter tuning improved the model's performance across all evaluation metrics.
The tuned model achieved 99.12% accuracy, compared to 97.37% for the baseline model.
Recall increased to 100%, meaning no positive samples were missed.
The confusion matrix showed fewer misclassifications after tuning indicating better generalization.
Overall, GridSearchCV successfully identified better hyperparameters, resulting in a more accurate and reliable Logistic Regression model.
