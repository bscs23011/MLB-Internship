import os
from PIL import Image, ImageEnhance
import imagehash

dataset_dir = "dataset"
source_image = "1.jpg"

source_path = os.path.join(dataset_dir, source_image)

image = Image.open(source_path).convert("RGB")

base_name = os.path.splitext(source_image)[0]


resized = image.resize(
    (image.width // 2, image.height // 2)
)

resized_path = os.path.join(
    dataset_dir,
    base_name + "_resized.jpg"
)

resized.save(resized_path)

print("Created:", resized_path)



width, height = image.size

left = int(width * 0.15)
top = int(height * 0.15)
right = int(width * 0.85)
bottom = int(height * 0.85)

cropped = image.crop(
    (left, top, right, bottom)
)

cropped_path = os.path.join(
    dataset_dir,
    base_name + "_cropped.jpg"
)

cropped.save(cropped_path)

print("Created:", cropped_path)



brightness = ImageEnhance.Brightness(image)

brightened = brightness.enhance(1.4)

brightened_path = os.path.join(
    dataset_dir,
    base_name + "_bright.jpg"
)

brightened.save(brightened_path)

print("Created:", brightened_path)



original_hash = imagehash.phash(image)  

variants = [
    resized_path,
    cropped_path,
    brightened_path
]

for variant in variants:

    variant_hash = imagehash.phash(Image.open(variant).convert("RGB"))

    distance = original_hash - variant_hash

    if distance <= 10:
        result = "Near duplicate detected"
    else:
        result = "Not detected"

    print(
        os.path.basename(variant),
        "= Hamming distance:",
        distance,
        "=",
        result
    )