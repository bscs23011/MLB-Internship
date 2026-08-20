import cv2
import pytesseract
from pytesseract import Output
import os

input_dir = "dataset/image"
output_txt_dir = "raw-images-output"
output_annotated_dir = "annotated-raw-images"

exts = (".jpg", ".jpeg", ".png")

for fname in sorted(os.listdir(input_dir)):
    if not fname.lower().endswith(exts):
        continue

    img_path = os.path.join(input_dir, fname)
    img = cv2.imread(img_path)

    if img is None:
        print(f"Skipped {fname} — could not read image")
        continue

    print(f"Running OCR on {fname}...")

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    data = pytesseract.image_to_data(rgb_img, output_type=Output.DICT)

  
    annotated = img.copy()
    if len(annotated.shape) == 2: 
        annotated = cv2.cvtColor(annotated, cv2.COLOR_GRAY2BGR)

    lines_out = []
    n_boxes = len(data['text'])

    for i in range(n_boxes):
        word = data['text'][i].strip()
        conf = int(data['conf'][i])

        if conf == -1 or word == "":
            continue

        x = data['left'][i]
        y = data['top'][i]
        w = data['width'][i]
        h = data['height'][i]

        lines_out.append(f"{word}\t(x={x}, y={y}, w={w}, h={h})\tconf={conf}")

        if conf > 80:
            color = (0, 255, 0)
        elif conf > 50:
            color = (0, 165, 255)
        else:
            color = (0, 0, 255)

        cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 2)
        cv2.putText(
            annotated, f"{conf}", (x, max(y - 5, 10)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1
        )

    base_name = os.path.splitext(fname)[0]

    txt_path = os.path.join(output_txt_dir, base_name + ".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines_out))

    # Save annotated image
    annotated_path = os.path.join(output_annotated_dir, base_name + "_annotated.png")
    cv2.imwrite(annotated_path, annotated)

    print(f"  Saved  {txt_path}")
    print(f"  Saved  {annotated_path}")
