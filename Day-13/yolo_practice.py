
# Install the Ultralytics YOLO package and explore its basic usage.
from ultralytics import YOLO

# Load a pre-trained YOLO model.
model = YOLO("yolov8n.pt")

# Perform object detection on:
  
# An image
results = model("image1.PNG")

# Multiple images
results = model(["image1.PNG", "image2.PNG"], save=True)

# Save the prediction results.

# Practice 2

# Test the model on your own images.
# Observe:
  
# Detected objects
objects = results[0].boxes.cls
print("Detected objects:", objects)

# Confidence scores
confidence_scores = results[0].boxes.conf 
print("Confidence scores:", confidence_scores)

# Bounding boxes
bounding_boxes = results[0].boxes.xyxy  
print("Bounding boxes:", bounding_boxes)