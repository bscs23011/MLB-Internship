import os
import cv2

os.makedirs("plate_crops_preprocessed", exist_ok=True)

image_files = sorted(
    f for f in os.listdir("plate_crops")
    if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))
)

print(f"Found {len(image_files)} plate crops")

for image_name in image_files:

    image_path = os.path.join("plate_crops", image_name)
    plate_img = cv2.imread(image_path)

    if plate_img is None:
        print(f"Skipping {image_name}")
        continue

    h, w = plate_img.shape[:2]

    if w == 0 or h == 0:
        print(f"Skipping {image_name}")
        continue

    scale = max(1.0, 320 / w)

    resized = cv2.resize(
        plate_img,
        (int(w * scale), int(h * scale)),
        interpolation=cv2.INTER_CUBIC
    )

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(
        clipLimit=2.5,
        tileGridSize=(8, 8)
    )

    contrast = clahe.apply(gray)

    denoised = cv2.fastNlMeansDenoising(
        contrast,
        h=10
    )

    output_path = os.path.join(
        "plate_crops_preprocessed",
        image_name
    )

    cv2.imwrite(output_path, denoised)

    print(f"Processed {image_name}")

print("Done")