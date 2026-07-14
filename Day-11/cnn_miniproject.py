import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import fashion_mnist

# Loads and preprocesses the dataset.
dataset = fashion_mnist
(x_train, y_train), (x_test, y_test) = dataset.load_data()
x_train = x_train / 255.0
x_test = x_test / 255.0

# Displays sample images.

data = x_train[:10]
labels = y_train[:10]

plt.figure(figsize=(12, 5))

for i in range(10):
    plt.subplot(2, 5, i + 1)     
    plt.imshow(data[i], cmap='gray')
    plt.title(f"Label: {labels[i]}")
    plt.axis('off')

plt.tight_layout()
plt.savefig('sample_images.png')
plt.show()

# Trains a CNN for image classification.
cnn_model = keras.Sequential([
    keras.layers.Reshape((28, 28, 1), input_shape=(28, 28)),
    keras.layers.Conv2D(32, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# Evaluates the model on the test dataset.
cnn_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
history = cnn_model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test)) 

# Predicts the class of sample images.
predictions = cnn_model.predict(x_test)
predicted_labels = predictions.argmax(axis=1)

# Displays both the predicted and actual labels.


print("Actual labels:", y_test[:5])
print("Predicted labels:", predicted_labels[:5])



# Plots the training and validation accuracy curves.
plt.figure(figsize=(10, 5))
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('accuracy_plot.png')
plt.show()

# Display a confusion matrix.
confusion_mtx = tf.math.confusion_matrix(y_test, predicted_labels)
print("Confusion Matrix:\n", confusion_mtx)

# Show 10 correctly classified and 10 incorrectly classified images with their predicted labels.
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

correctly_classified = []
incorrectly_classified = []

for i in range(len(y_test)):
    if predicted_labels[i] == y_test[i]:
        correctly_classified.append(i)
    else:
        incorrectly_classified.append(i)

plt.figure(figsize=(20, 4))
for i in range(10):
    plt.subplot(2, 10, i + 1)
    plt.imshow(x_test[correctly_classified[i]], cmap='gray')
    plt.title(f"Pred: {class_names[predicted_labels[correctly_classified[i]]]} \nTrue: {class_names[y_test[correctly_classified[i]]]}", fontsize=8)
    plt.axis('off')

plt.tight_layout()
plt.savefig('correctly_classified_images.png')
plt.show()

plt.figure(figsize=(20, 4))
for i in range(10):
    plt.subplot(2, 10, i + 11)
    plt.imshow(x_test[incorrectly_classified[i]], cmap='gray')
    plt.title(f"Pred: {class_names[predicted_labels[incorrectly_classified[i]]]} \nTrue: {class_names[y_test[incorrectly_classified[i]]]}", fontsize=8)
    plt.axis('off')

plt.tight_layout()
plt.savefig('incorrectly_classified_images.png')
plt.show()