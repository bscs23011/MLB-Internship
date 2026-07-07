What you learned about data preprocessing.
Data preprocessing prepares data for machine learning and to train the model.
I learned how to encode variables using Label Encoding.
I separated the dataset into features (X) and target (y).
I applied Standardization using StandardScaler so that the features had similar scales.
I also learned to avoid data leakage by fitting the scaler only on the training data and then using it to transform the test data.

Why train-test splitting is important.
Train-test splitting ensures that the model is evaluated on unseen data rather than 
the data it was trained on. This provides a better estimate and prediciton

Which evaluation metrics you used.
Mean Absolute Error (MAE): Measures the average absolute difference between the actual and predicted values.
Mean Squared Error (MSE): Measures the average squared difference between actual and predicted values. 
R² Score : Measures how well the model explains the variation in the target variable. 

Your model's performance and observations.
The Linear Regression model was trained susing the selected features (Age, Attendance, and Program) to predict Average_Score. 
The model's performance was evaluated using MAE, MSE, and R² Score. Lower MAE and MSE values indicate more accurate predictions, 
while a higher R² Score indicates that the model explains a larger portion of the variation in the target variable.
