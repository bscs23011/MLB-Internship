import os
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array

model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    pooling="avg"
)

dataset_dir = "dataset"

filenames = []

for file in os.listdir(dataset_dir):
    if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp")):
        filenames.append(file)

filenames.sort()


embeddings = {}

for filename in filenames:

    image_path = os.path.join(dataset_dir, filename)

    image = load_img(image_path, target_size=(224, 224))

    # Convert image to NumPy array
    image = img_to_array(image)

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    # Apply MobileNetV2 preprocessing
    image = preprocess_input(image)

    # Extract feature embedding
    embedding = model.predict(image, verbose=0)[0]

    # Save embedding using filename as the key
    embeddings[filename] = embedding

    print(filename, "=", embedding.shape)

# Save all embeddings
np.savez("embeddings.npz", **embeddings)
