import cv2
import pytesseract
from pytesseract import Output
import os
import json

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

input_dir = "plate_crops_preprocessed"
output_json_dir = "ocr_jsn_output"
output_annotated_dir = "annotated-ocr-images"

MIN_CONFIDENCE = 50

os.makedirs(output_json_dir, exist_ok=True)
os.makedirs(output_annotated_dir, exist_ok=True)

for fname in sorted(os.listdir(input_dir)):

    if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    img_path = os.path.join(input_dir, fname)
    img = cv2.imread(img_path)

    if img is None:
        print(f"Skipped {fname}")
        continue

    print(f"Running OCR on {fname}...")

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    data = pytesseract.image_to_data(
        rgb_img,
        output_type=Output.DICT
    )

    annotated = img.copy()
    ocr_data = []
    readable_count = 0

    for i in range(len(data["text"])):

        text = data["text"][i].strip()
        confidence = int(data["conf"][i])

        if confidence == -1 or text == "":
            continue

        x = data["left"][i]
        y = data["top"][i]
        w = data["width"][i]
        h = data["height"][i]

        if confidence < MIN_CONFIDENCE:
            status = "Unreadable"
            display_text = "Unreadable"
            color = (0, 0, 255)
        else:
            status = "Readable"
            display_text = text
            readable_count += 1
            color = (0, 255, 0)

        ocr_data.append({
            "text": text,
            "display_text": display_text,
            "status": status,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "confidence": confidence
        })

        cv2.rectangle(
            annotated,
            (x, y),
            (x + w, y + h),
            color,
            2
        )

        cv2.putText(
            annotated,
            f"{display_text} ({confidence})",
            (x, max(y - 5, 15)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            1
        )

    base_name = os.path.splitext(fname)[0]

    json_path = os.path.join(
        output_json_dir,
        base_name + ".json"
    )

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            ocr_data,
            f,
            indent=4,
            ensure_ascii=False
        )

    annotated_path = os.path.join(
        output_annotated_dir,
        base_name + "_annotated.png"
    )

    cv2.imwrite(
        annotated_path,
        annotated
    )

    print(f"Saved {json_path}")
    print(f"Saved {annotated_path}")
    print(f"Readable text: {readable_count}")

print("Done")