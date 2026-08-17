from ultralytics import YOLO
import os

FRAMES_FOLDER = "frames"
LABELS_FOLDER = "labels"
CONFIDENCE = 0.35 

CLASS_MAP = {
    "car": 0,
    "motorcycle": 1,
    "bus": 2,
    "truck": 3,
}

os.makedirs(LABELS_FOLDER, exist_ok=True)

model = YOLO("yolov8n.pt")

frame_files = []

for f in os.listdir(FRAMES_FOLDER):
    if f.lower().endswith((".jpg", ".jpeg", ".png")):
        frame_files.append(f)
print(f"Found {len(frame_files)} frames to auto-annotate.")

labeled_count = 0

for frame_name in frame_files:

    frame_path = os.path.join(FRAMES_FOLDER, frame_name)
    label_name = os.path.splitext(frame_name)[0] + ".txt"
    label_path = os.path.join(LABELS_FOLDER, label_name)

    if os.path.exists(label_path):
        continue

    results = model.predict(frame_path, conf=CONFIDENCE, verbose=False)[0]

    lines_to_save = []

    for box in results.boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        if class_name not in CLASS_MAP:
            continue

        our_class_id = CLASS_MAP[class_name]

        x_center, y_center, width, height = box.xywhn[0].tolist()

        lines_to_save.append(f"{our_class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    if lines_to_save:
        with open(label_path, "w") as f:
            f.write("\n".join(lines_to_save) + "\n")
        labeled_count += 1

print(f"Done. Auto-labeled {labeled_count} out of {len(frame_files)} frames.")
print("Open the annotation tool to review, fix mistakes, and add rickshaws manually.")