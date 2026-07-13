import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import fashion_mnist

# Load the Fashion MNIST dataset.
dataset = fashion_mnist
(x_train, y_train), (x_test, y_test) = dataset.load_data()

# Explore the dataset (shape, labels, sample images).
print("Training data shape:", x_train.shape)
print("Training labels shape:", y_train.shape)
print("Test data shape:", x_test.shape)
print("Test labels shape:", y_test.shape)
print("Sample training labels:", y_train[:10])
print("Sample test labels:", y_test[:10])

# Normalize the pixel values.
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Build a simple Artificial Neural Network (ANN).
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# Train the model.
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

# Evaluate the model on the test dataset.
test_loss, test_accuracy = model.evaluate(x_test, y_test)

# Display the training and validation accuracy.
print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)

# Make predictions on a few test images.
predictions = model.predict(x_test[:5])
predicted_labels = predictions.argmax(axis=1)

#Display the predicted and actual labels.
print("Actual labels:", y_test[:5])

print("Predictions:", predicted_labels)

# Plot the training and validation accuracy curves.
plt.figure(figsize=(10, 5))
plt.plot(model.history.history['accuracy'], label='Training Accuracy')
plt.plot(model.history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('accuracy_plot.png')
plt.show()

#Display a few sample predictions with their corresponding images.
class_names = [
    "T-shirt/Top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle Boot"
]


plt.figure(figsize=(12,5))

for i in range(5):
    plt.subplot(1,5,i+1)
    plt.imshow(x_test[i], cmap='gray')

    predicted_class = class_names[predicted_labels[i]]
    actual_class = class_names[y_test[i]]

    plt.title(f"Pred: {predicted_class}\nTrue: {actual_class}", fontsize=8)
    plt.axis('off')

plt.tight_layout()
plt.savefig('sample_predictions.png')
plt.show()