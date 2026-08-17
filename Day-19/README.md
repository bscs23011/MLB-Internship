# Traffic Vehicle Detection — Final Year Project

A CPU/GPU-friendly pipeline for detecting and counting vehicles (car, motorcycle,
bus, truck, rickshaw) and pedestrians in traffic video, using a YOLOv8n model
trained **from scratch** (no pretrained weights) on self-collected, self-annotated
footage.

## What this project does, end to end

```
Raw traffic videos
      │
      ▼
Extract frames  (frames.py)
      │
      ▼
Annotate frames 
      │
      ▼
Analyze dataset (analyze_dataset.py) 
      │
      ▼
Split train / val / test (split.py)
      │
      ▼
Train YOLOv8n from scratch (Google Colab)
      │
      ▼
Evaluate on held-out test set (get mAP / precision / recall)
      │
      ▼
Track + count vehicles on new video (tracking.py)


## Folder structure

```
project/
├── raw-videos/              your original traffic videos go here
├── frames/                  extracted frames (output of extract_frames.py)
├── labels/                  YOLO .txt annotation files, one per frame
├── classes.txt              your class list, one per line, in class-ID order
├── frames.py
├── analyze_dataset.py
├── split.py
├── tracking.py
├── dataset/                 created by final_split.py (train/val/test folders)
├── best.pt                  your trained model weights (downloaded from Colab)
└── annotation_tool/
    ├── app.py                the annotation web app (backend)
    ├── static/                the annotation web app (frontend)
    ├── auto_annotate.py       optional: pre-fills boxes using a pretrained model
    └── requirements.txt
```

---

## Step 1 — Collect and extract frames

Put your raw videos in one folder, then run:

```bash
python frames.py
```

This samples frames from every video at a fixed interval (edit `FRAME_INTERVAL`
in the script — a higher number means fewer frames saved) and writes them into
`frames/`, named `{video_name}_frame_{index}.jpg`. Keeping the video name in the
filename matters — later steps rely on it to know which video each frame came from.

---

## Step 2 — Annotate the frames

### Setup

```bash
cd annotation_tool
pip install -r requirements.txt
```

Open `classes.txt` and edit your class list — one name per line. **The line order
becomes the class ID your model learns** (line 1 = class 0, line 2 = class 1,
etc.), so lock this in before you start annotating.


```bash
python auto_annotate.py
```

This runs a pretrained YOLO model over your frames and auto-draws boxes for any
class it already recognizes (car, motorcycle, bus, truck). It will **not** detect
classes that don't exist in its training data (e.g. rickshaw) — those still need
to be drawn by hand. This step only speeds up labeling; it has no effect on your
own model being trained from scratch.

### Run the annotation tool

```bash
python app.py
```

Open **http://localhost:8000** in your browser.

### How to use it

| Action | How |
|---|---|
| Draw a new box | Click and drag on an empty part of the image |
| Select an existing box | Click on it — you'll see square handles appear at its corners |
| Move a selected box | Click and drag from inside it |
| Resize a selected box | Drag one of its corner handles |
| Change the active class | Click the dropdown, or press number keys **1–9** |
| Delete the selected box | Press **Backspace** or **Delete** |
| Delete a specific box without selecting it | Click "delete" next to it in the sidebar list |
| Deselect | Press **Escape** |
| Go to the previous frame | Press **A** or **←** (auto-saves the current frame first) |
| Go to the next frame | Press **D** or **→** (auto-saves the current frame first) |
| Manually save | Press **S** |

Everything you draw or edit is saved as a standard YOLO `.txt` file in `labels/`,
matching each frame's filename. A frame with no vehicles in it simply gets no
label file — that's normal and expected, not an error.

The counter at the top of the page shows how many frames have at least one saved
box, so you can track your progress at a glance.

---

## Step 3 — Check your dataset before splitting

```bash
python analyze_dataset.py
```

Prints a table of how many frames and how many instances of each class every
video contributes. **Do this before splitting** — if one video holds almost all
of a rare class (this happened in this project with rickshaw and pedestrian),
you need to know that before deciding which videos become your test set, or
you risk removing a class from training entirely.

---

## Step 4 — Split into train / val / test

Edit `split.py` to set which videos go into `TEST_VIDEOS` and `VAL_VIDEOS`
(everything else automatically goes to train), then run:

```bash
python split.py
```

This produces `dataset/train`, `dataset/val`, and `dataset/test`, each with
`images/` and `labels/` subfolders — ready for YOLO training.

**Rule of thumb for picking test videos:** always hold out whole videos, never
random individual frames — frames next to each other in time look nearly
identical, so mixing them across splits leaks information and makes your
evaluation numbers look better than they really are.

---

## Step 5 — Train YOLOv8n from scratch (Google Colab)

Upload your `dataset/` folder to Google Drive, then in Colab:

```python
from ultralytics import YOLO

model = YOLO("yolov8n.yaml") 

model.train(
    data="/content/drive/MyDrive/dataset/data.yaml",
    epochs=200,
    imgsz=640,
    batch=16,
    patience=50,
    project="/content/drive/MyDrive/runs",
    name="vehicle_detector_scratch"
)
```

Training saves checkpoints straight to your Drive as it goes, so a disconnected
Colab session doesn't lose your progress. Once done, download
`runs/vehicle_detector_scratch/weights/best.pt` — that's your trained model.

---

## Step 6 — Evaluate on your test set

```python
from ultralytics import YOLO

model = YOLO("best.pt")
metrics = model.val(data="dataset/data.yaml", split="test", conf=0.4)

print("mAP50:", metrics.box.map50)
print("mAP50-95:", metrics.box.map)
print("Precision:", metrics.box.mp)
print("Recall:", metrics.box.mr)
```

This gives real numbers (not just a visual check) by comparing your model's
predictions against the ground-truth boxes in your test set.

---

## Step 7 — Track and count vehicles on new footage

```bash
python tracking.py
```

Runs your trained model with an object tracker (ByteTrack) over a video,
drawing a bounding box, class label. Each object is counted once it passes through the tracking line, the box turns
from yellow to green once it is detected — giving you results like
"8 cars, 2 motorcycles, 5 rickshaws passed."

Edit `model_path` and `video_path` at the top of the script before running.

---

## LINK FOR OUTPUT VIDEOS
[object detection](https://drive.google.com/drive/folders/1m6eS438NmAIlPbST5IBIv9rshE7uasdi?usp=sharing)
[object tracking](https://drive.google.com/file/d/1CFqM--aLM-XrA395e9fJPd1GJlUahxO5/view?usp=sharing)
