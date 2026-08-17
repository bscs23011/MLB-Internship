import cv2
from ultralytics import YOLO

confidence = 0.4

class_names = ["car", "motorcycle", "bus", "truck", "rickshaw", "pedestrian"]

tail_length = 30  #
tail_color = (255, 255, 255)

class_color = [
    (0, 200, 255),   
    (0, 255, 0),     
    (255, 0, 0),     
    (255, 165, 0),   
    (255, 0, 255),   
    (0, 0, 255),    
]

model = YOLO("best.pt")

cap = cv2.VideoCapture("vid2.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.release()

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter("tracked_output.mp4", fourcc, fps, (width, height))

track_history = {}       
seen_ids_by_class = {}   

for class_id in range(len(class_names)):
    seen_ids_by_class[class_id] = set()

results_stream = model.track(
    source="vid2.mp4",
    conf=confidence,
    tracker="bytetrack.yaml",
    persist=True,
    stream=True,
    verbose=False,
)

frame_count = 0

for result in results_stream:

    frame = result.orig_img.copy()
    frame_count += 1

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
            color = class_color[class_id]

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # update trail history
            if track_id not in track_history:
                track_history[track_id] = []

            track_history[track_id].append((center_x, center_y))

            # keep only the last TAIL_LENGTH points
            if len(track_history[track_id]) > tail_length:
                track_history[track_id] = track_history[track_id][-tail_length:]

            # count this track id once, the first time we see it
            seen_ids_by_class[class_id].add(track_id)

            # draw box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)

            label = f"{class_name} ID:{track_id} {conf:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1) - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # draw trail (tail/path)
            points = track_history[track_id]
            for j in range(1, len(points)):
                cv2.line(frame, points[j - 1], points[j], tail_color, 2)

    # overlay running counts, top-left corner
    y_offset = 30
    for class_id in range(len(class_names)):
        class_name = class_names[class_id]
        count = len(seen_ids_by_class[class_id])
        text = f"{class_name}: {count}"
        cv2.putText(frame, text, (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, class_color[class_id], 2)
        y_offset += 25

    writer.write(frame)

writer.release()

print("Done. Output saved to", "tracked_output.mp4")
print("\nFinal counts:")
for class_id in range(len(class_names)):
    class_name = class_names[class_id]
    print(f"  {class_name}: {len(seen_ids_by_class[class_id])}")