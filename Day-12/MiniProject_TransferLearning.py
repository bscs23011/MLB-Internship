import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt



# Loads and preprocesses the dataset.
train_dataset = tf.keras.utils.image_dataset_from_directory(
    "PetImages",
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(224, 224),
    batch_size=32
)

validation_dataset = tf.keras.utils.image_dataset_from_directory(
    "PetImages",
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(224, 224),
    batch_size=32
)

def preprocess_image(image, label):
    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
    return image, label

train_dataset = train_dataset.map(preprocess_image)
validation_dataset = validation_dataset.map(preprocess_image)

train_dataset = train_dataset.apply(tf.data.experimental.ignore_errors())
validation_dataset = validation_dataset.apply(tf.data.experimental.ignore_errors())


# Uses MobileNetV2 as the pre-trained backbone.

base_model = keras.applications.MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freezes the base model.
base_model.trainable = False

# Adds custom classification layers.

model = keras.Sequential([
    base_model,
    keras.layers.GlobalAveragePooling2D(),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dense(2, activation="softmax")
])


# Trains the model.

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(
    train_dataset,
    epochs=5,
    validation_data=validation_dataset
)

# Evaluates it on the validation dataset.

loss, accuracy = model.evaluate(validation_dataset)

print(f"Validation Loss: {loss:.4f}")
print(f"Validation Accuracy: {accuracy:.4f}")

# Displays sample predictions.

class_names = ["Cat", "Dog"]

images, labels = next(iter(validation_dataset))
predictions = model.predict(images)

plt.figure(figsize=(12, 5))

for i in range(10):
    plt.subplot(2, 5, i + 1)

    # Convert image back to displayable range
    plt.imshow((images[i].numpy() + 1) / 2)

    predicted = class_names[predictions[i].argmax()]
    actual = class_names[labels[i].numpy()]

    plt.title(f"P: {predicted}\nA: {actual}")
    plt.axis("off")

plt.tight_layout()
plt.savefig("sample_predictions.png")
plt.show()


# Plots the training and validation accuracy and loss curves.

plt.figure(figsize=(10, 5))

plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")

plt.title("Training and Validation Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

plt.savefig("accuracy_plot.png")
plt.show()


plt.figure(figsize=(10, 5))

plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")

plt.title("Training and Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

plt.savefig("loss_plot.png")
plt.show()