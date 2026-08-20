import cv2
import numpy as np
import os

print("Pre-processing images...")

max_skew_angle = 30.0
denoise_kernel = 3
clahe_clip = 2.0
clahe_grid = (8, 8)

input_dir = "dataset/image"
output_dir = "pre-processed-images"

valid_exts = (".jpg", ".jpeg", ".png")

for fname in sorted(os.listdir(input_dir)):
    if not fname.lower().endswith(valid_exts):
        continue

    input_path = os.path.join(input_dir, fname)
    img = cv2.imread(input_path)

    if img is None:
        print(f"Skipped {fname} — could not read image")
        continue

    base_name = os.path.splitext(fname)[0]
    output_path = os.path.join(output_dir, base_name + "_processed.png")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    coords = cv2.findNonZero(thresh)

    angle = 0.0
    if coords is not None:
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

    # Deskew
    if abs(angle) > max_skew_angle:
        print(f"{fname}: skew estimate {angle:.1f}° looks unreliable, skipping rotation")
        deskewed = img
    else:
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        deskewed = cv2.warpAffine(
            img, M, (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
        print(f"{fname}: rotated by {angle:.1f}°")

    deskewed_gray = cv2.cvtColor(deskewed, cv2.COLOR_BGR2GRAY)

    # Denoise
    denoised = cv2.medianBlur(deskewed_gray, denoise_kernel)

    # Contrast
    clahe = cv2.createCLAHE(clipLimit=clahe_clip, tileGridSize=clahe_grid)
    contrasted = clahe.apply(denoised)

    success = cv2.imwrite(output_path, contrasted)
    if success:
        print(f"Saved  {output_path}")
    else:
        print(f"Failed to save {output_path}")