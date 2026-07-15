import tensorflow as tf
from tensorflow import keras
import tensorflow_datasets as tfds

# Practice 1

# Load a pre-trained MobileNetV2 model.
model = keras.applications.MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Explore its architecture.
model.summary()

# Freeze the base model layers.
for layer in model.layers:
    layer.trainable = False

# Add your own classification head.
classifier = keras.Sequential([
    keras.layers.GlobalAveragePooling2D(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(2, activation='softmax')
])

# Practice 2

# Load the Cats vs Dogs dataset using TensorFlow Datasets (TFDS).


train_ds = tf.keras.utils.image_dataset_from_directory(
    "PetImages",
    image_size=(224, 224),
    batch_size=32
)

# Preprocess and resize the images.
def preprocess_image(image, label):
    image = tf.image.resize(image, (224, 224))
    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
    return image, label

# Split the dataset into training and validation sets.
dataset = train_ds.map(preprocess_image)
train_dataset = dataset.take(1000)
validation_dataset = dataset.skip(1000).take(200)
