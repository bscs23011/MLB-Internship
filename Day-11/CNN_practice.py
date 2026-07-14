import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import fashion_mnist



# Practice 1

# Load the Fashion MNIST dataset.
dataset = fashion_mnist
(x_train, y_train), (x_test, y_test) = dataset.load_data()

# Visualize at least 10 sample images with their labels.
data = x_train[:10]
labels = y_train[:10]

plt.figure(figsize=(12, 5))

for i in range(10):
    plt.subplot(2, 5, i + 1)     
    plt.imshow(data[i], cmap='gray')
    plt.title(f"Label: {labels[i]}")
    plt.axis('off')

plt.tight_layout()
plt.show()

# Normalize the dataset.
x_train = x_train / 255.0
x_test = x_test / 255.0


# Practice 2

# Build a simple CNN model that includes:
# Convolution Layer
# Max Pooling Layer
# Flatten Layer
# Dense Layers
# Output Layer


cnn_model = keras.Sequential([
    keras.layers.Reshape((28, 28, 1), input_shape=(28, 28)),
    keras.layers.Conv2D(32, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])


# Train the model and observe the training progress.
cnn_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
history = cnn_model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

# Practice 3

# Evaluate the trained model using:

# Training Accuracy
training_accuracy = history.history['accuracy'][-1]

# Test Accuracy
test_loss, test_accuracy = cnn_model.evaluate(x_test, y_test)
print(f"Test accuracy: {test_accuracy}")

# Loss
print(f"Test loss: {test_loss}")

# Predictions on sample images
predictions = cnn_model.predict(x_test[:5])
predicted_labels = predictions.argmax(axis=1)

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
plt.show()
