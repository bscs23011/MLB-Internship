import os
import cv2
from ultralytics import YOLO
from roboflow import Roboflow

ROBOFLOW_API_KEY = "API_KEY" 
ROBOFLOW_PROJECT = "license-plate-recognition-rxg4e"
ROBOFLOW_VERSION = 11

rf = Roboflow(api_key=ROBOFLOW_API_KEY)
project = rf.workspace().project(ROBOFLOW_PROJECT)
plate_model = project.version(ROBOFLOW_VERSION).model

os.makedirs("plates_output", exist_ok=True)
os.makedirs("plate_crops", exist_ok=True)

yolo_model = YOLO("yolov8n.pt")


def pick_best_plate(predictions, width, height):

    valid_plates = []

    for x1, y1, x2, y2, confidence in predictions:

        plate_width = x2 - x1
        plate_height = y2 - y1

        if plate_width <= 0 or plate_height <= 0:
            continue

        aspect_ratio = plate_width / plate_height
        y_center = ((y1 + y2) / 2) / height

        if aspect_ratio < 1.3 or aspect_ratio > 7.0:
            continue

        if y_center < 0.40:
            continue

        valid_plates.append(
            (x1, y1, x2, y2, confidence)
        )

    if not valid_plates:
        return None

    return max(valid_plates, key=lambda plate: plate[4])


image_files = sorted(
    f for f in os.listdir("dataset/images")
    if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))
)

print(f"Found {len(image_files)} images")

total_vehicles = 0
total_plates = 0
total_rejected = 0

for image_name in image_files:

    image_path = os.path.join("dataset/images", image_name)
    frame = cv2.imread(image_path)

    if frame is None:
        print(f"Skipping {image_name}")
        continue

    image_stem = os.path.splitext(image_name)[0]

    results = yolo_model(frame, verbose=False)[0]

    vehicle_count = 0
    plate_count = 0

    for box in results.boxes:

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        if class_id not in {2, 3, 5, 7}:
            continue

        if confidence < 0.35:
            continue

        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0].tolist()
        )

        vehicle_names = {
            2: "car",
            3: "motorcycle",
            5: "bus",
            7: "truck"
        }

        vehicle_name = vehicle_names[class_id]

        vehicle_count += 1

        vehicle_crop = frame[y1:y2, x1:x2].copy()

        if vehicle_crop.size == 0:
            continue

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 200, 0),
            2
        )

        cv2.putText(
            frame,
            f"{vehicle_name} {confidence:.2f}",
            (x1, max(0, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 200, 0),
            2
        )

        temp_path = os.path.join(
            "plate_crops",
            "temp.jpg"
        )

        cv2.imwrite(temp_path, vehicle_crop)

        prediction = plate_model.predict(
            temp_path,
            confidence=10,
            overlap=30
        )

        prediction_json = prediction.json()
        plate_predictions = prediction_json["predictions"]

        if len(plate_predictions) == 0:
            total_rejected += 1
            continue

        vehicle_height, vehicle_width = vehicle_crop.shape[:2]

        response_width = float(
            prediction_json["image"]["width"]
        )

        response_height = float(
            prediction_json["image"]["height"]
        )

        scale_x = vehicle_width / response_width
        scale_y = vehicle_height / response_height

        candidates = []

        for plate in plate_predictions:

            center_x = plate["x"] * scale_x
            center_y = plate["y"] * scale_y

            plate_width = plate["width"] * scale_x
            plate_height = plate["height"] * scale_y

            px1 = center_x - plate_width / 2
            py1 = center_y - plate_height / 2
            px2 = center_x + plate_width / 2
            py2 = center_y + plate_height / 2

            candidates.append(
                (
                    px1,
                    py1,
                    px2,
                    py2,
                    plate["confidence"]
                )
            )

        best_plate = pick_best_plate(
            candidates,
            vehicle_width,
            vehicle_height
        )

        if best_plate is None:
            total_rejected += 1
            continue

        px1, py1, px2, py2, plate_confidence = best_plate

        plate_width = px2 - px1
        plate_height = py2 - py1

        px1 -= plate_width * 0.08
        px2 += plate_width * 0.08
        py1 -= plate_height * 0.08
        py2 += plate_height * 0.08

        px1 = int(max(0, px1))
        py1 = int(max(0, py1))
        px2 = int(min(vehicle_width, px2))
        py2 = int(min(vehicle_height, py2))

        plate_crop = vehicle_crop[
            py1:py2,
            px1:px2
        ]

        if plate_crop.size == 0:
            continue

        plate_count += 1

        final_x1 = x1 + px1
        final_y1 = y1 + py1
        final_x2 = x1 + px2
        final_y2 = y1 + py2

        cv2.rectangle(
            frame,
            (final_x1, final_y1),
            (final_x2, final_y2),
            (255, 120, 0),
            2
        )

        cv2.putText(
            frame,
            f"plate {plate_confidence:.2f}",
            (final_x1, max(0, final_y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 120, 0),
            2
        )

        crop_name = (
            f"{image_stem}_vehicle"
            f"{vehicle_count}_plate.jpg"
        )

        cv2.imwrite(
            os.path.join("plate_crops", crop_name),
            plate_crop
        )

    total_vehicles += vehicle_count
    total_plates += plate_count

    print(
        f"{image_name}: "
        f"{vehicle_count} vehicle(s), "
        f"{plate_count} plate(s)"
    )

    cv2.imwrite(
        os.path.join("plates_output", image_name),
        frame
    )

if os.path.exists(
    os.path.join("plate_crops", "temp.jpg")
):
    os.remove(
        os.path.join("plate_crops", "temp.jpg")
    )

print("\nDone")
print(f"Total vehicles: {total_vehicles}")
print(f"Total plates: {total_plates}")
print(f"Rejected candidates: {total_rejected}")
print("Annotated images saved in plates_output")
print("Plate crops saved in plate_crops")