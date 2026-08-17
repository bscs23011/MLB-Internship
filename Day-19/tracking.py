import cv2
from ultralytics import YOLO

model_path = "best.pt"
video_path = "vid3.mp4"
output_path = "tracked_output.mp4"
confidence = 0.4

class_names = ["car", "motorcycle", "bus", "truck", "rickshaw", "pedestrian"]

line_color = (0, 255, 255)

class_colors = [
    (0, 200, 255),   
    (0, 255, 0),     
    (255, 0, 0),     
    (255, 165, 0),   
    (255, 0, 255),   
    (0, 0, 255),     
]

model = YOLO(model_path)

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.release()

line_y = int(height * 0.15)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

track_prev_y = {}      
crossed_ids = set()    

class_counts = {}
for class_id in range(len(class_names)):
    class_counts[class_id] = 0

results_stream = model.track(
    source=video_path,
    conf=confidence,
    tracker="bytetrack.yaml",
    persist=True,
    stream=True,
    verbose=False,
)

for result in results_stream:

    frame = result.orig_img.copy()

    cv2.line(frame, (0, line_y), (width, line_y), line_color, 2)

    boxes = result.boxes

    if boxes is not None and boxes.id is not None:

        xyxy = boxes.xyxy.cpu().numpy()
        track_ids = boxes.id.cpu().numpy().astype(int)
        class_ids = boxes.cls.cpu().numpy().astype(int)
        confs = boxes.conf.cpu().numpy()

        for i in range(len(track_ids)):
            x1, y1, x2, y2 = xyxy[i]
            track_id = track_ids[i]
            class_id = class_ids[i]
            conf = confs[i]

            class_name = class_names[class_id]
            color = class_colors[class_id]

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            if track_id in track_prev_y:
                prev_y = track_prev_y[track_id]
                crossed_downward = prev_y < line_y <= center_y
                crossed_upward = prev_y > line_y >= center_y

                if (crossed_downward or crossed_upward) and track_id not in crossed_ids:
                    crossed_ids.add(track_id)
                    class_counts[class_id] += 1

            track_prev_y[track_id] = center_y

            box_color = color
            if track_id in crossed_ids:
                box_color = (0, 255, 0)  

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), box_color, 2)

            label = f"{class_name} ID:{track_id} {conf:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1) - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)

    panel_height = 30 + (25 * len(class_names))
    x_text = 10

    cv2.putText(frame, "Vehicle Count", (x_text, height - panel_height),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    y_offset = height - panel_height + 30
    for class_id in range(len(class_names)):
        class_name = class_names[class_id]
        count = class_counts[class_id]
        text = f"{class_name}: {count}"
        cv2.putText(frame, text, (x_text, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, class_colors[class_id], 2)
        y_offset += 25

    writer.write(frame)

writer.release()

print("Done. Output saved to", output_path)
print("\nFinal counts (vehicles that crossed the line):")
for class_id in range(len(class_names)):
    print(f"  {class_names[class_id]}: {class_counts[class_id]}")