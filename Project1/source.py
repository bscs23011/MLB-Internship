# pip install -r requirements.txt
import cv2
from ultralytics import YOLO 

# Load trained model
model = YOLO("best.pt")


for i in range(1,32):

    image = cv2.imread(f"sample-images/{i}.png")
    if image is None:
        print("Error: Could not load image.")
        continue

    # Run detection
    results = model(image)

    # Get class names
    names = model.names

    occupied = 0
    free = 0

    for box in results[0].boxes:

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cls = int(box.cls[0])

        conf = float(box.conf[0])

        label = names[cls]

        if label.lower() == "car":
            color = (0, 0, 255)      # Red
            occupied += 1
        else:
            color = (0, 255, 0)      # Green
            free += 1

        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

        cv2.putText(
            image,
            f"{label} {conf:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    # Display statistics
    total = occupied + free

    cv2.putText(
        image,
        f"Occupied: {occupied}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    cv2.putText(
        image,
        f"Free: {free}",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.putText(
        image,
        f"Total: {total}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )


    cv2.imwrite(f"output/parking_result{i}.jpg", image)
