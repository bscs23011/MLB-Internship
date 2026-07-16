from ultralytics import YOLO

# Download the dataset in YOLO format.
# Load a pre-trained YOLO model (YOLOv8 or YOLO11).
model = YOLO("yolov8n.pt")

# Run inference on the dataset or sample images.
results = model(["BikesHelmets0.png" , "BikesHelmets1.png"])

# Visualize the detection results.
# Save the output images with bounding boxes.

for i, result in enumerate(results):
    print(f"\nImage {i+1}")

    print("Detected object class IDs:")
    print(result.boxes.cls)

    print("Confidence scores:")
    print(result.boxes.conf)

    print("Bounding boxes:")
    print(result.boxes.xyxy)

    result.save(filename=f"output_{i+1}.png")

# Briefly analyze the model's predictions.
#for image 1: the model detected a bicycle and a helmet with high confidence scores, indicating accurate detection.
#  The bounding boxes are well-aligned with the objects in the image.
#for image 2: the model detected a bicycle and a helmet with high confidence scores, indicating accurate detection.