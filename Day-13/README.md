1. What is Object Detection?

Object Detection is a computer vision task that identifies what objects are present in an image and where they are located by drawing bounding boxes around them.

2. How is it different from Image Classification?
Image Classification: Predicts the object class for the entire image.
Object Detection: Identifies multiple objects and provides their locations using bounding boxes.

4. What is YOLO?
YOLO (You Only Look Once) is a fast and accurate real-time object detection model that detects multiple objects in a single pass through the neural network.

4. Which dataset did you use?

I used the pre-trained YOLOv8 Nano (yolov8n.pt) model, which was trained on the COCO dataset containing 80 object classes.

5. What objects were detected?
Image 1: 5 persons and 1 tennis racket.
Image 2: 1 person and 1 motorcycle.

6. Your observations about the detection results
The model accurately detected most of the major objects.
Confidence scores were high for most detections, indicating reliable predictions.
One object was classified as a tennis racket with low confidence, likely due to a misclassification.
The model performed well overall but may miss or incorrectly classify objects that are small, partially hidden, or not included in the COCO dataset (such as helmets).
