# Smart Parking Lot Occupancy Analyzer

## Project Overview

This project is a Computer Vision application that automatically detects occupied and vacant parking spaces from parking lot images. It uses a custom-trained YOLOv8 model for object detection and OpenCV for visualization, counting, and displaying parking occupancy statistics.

## Dataset Used

* **Dataset:** [dataset](https://universe.roboflow.com/abdullah-hvgvv/parking-lot-j4ojc/browse?queryText=&pageSize=50&startingIndex=0&browseQuery=true)
* **Classes:** `car` (occupied) and `free` (vacant)
* **Format:** YOLOv8
* **Purpose:** Training and evaluating the parking occupancy detection model.

## Project Workflow

1. Load the trained YOLOv8 model.
2. Read parking lot images.
3. Detect occupied (`car`) and vacant (`free`) parking spaces.
4. Draw color-coded bounding boxes and confidence scores using OpenCV.
5. Count occupied and free spaces.
6. Display parking occupancy statistics on the image.
7. Save the processed output images.

## Technologies Used

* Python
* YOLOv8 (Ultralytics)
* OpenCV
* NumPy
* Roboflow Dataset
* Google Colab (for training)

## Results

* Successfully detected occupied and vacant parking spaces.
* Achieved the following validation metrics:

  * **Precision:** 95.6%
  * **Recall:** 93.5%
  * **mAP@0.50:** 96.9%
  * **mAP@0.50:0.95:** 81.0%
* Generated annotated output images with parking occupancy statistics.

## Challenges Faced

* Selecting a lightweight dataset suitable for quick training.
* Understanding the dataset's class labels and annotations.
* Managing occasional false detections in complex parking scenes.
* Ensuring correct image paths and output generation during inference.

## Future Improvements

* Support real-time video and webcam-based parking detection.
* Improve detection performance under low-light and adverse weather conditions.
* Add parking slot tracking across video frames.
* Develop a web or mobile dashboard for live parking availability.
* Deploy the model for real-time smart parking management.

##recordings:
(part-1)[https://drive.google.com/file/d/1ouWNJJtl9GYR08zPO5XAH4D82imdmAYP/edit]
(parrt-2)[https://drive.google.com/file/d/1ouWNJJtl9GYR08zPO5XAH4D82imdmAYP/edit]

