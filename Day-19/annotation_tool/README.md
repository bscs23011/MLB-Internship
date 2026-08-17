# Vehicle Annotation Tool

A minimal, self-contained bounding-box annotation tool for building a YOLO-format
dataset from your traffic videos. Two pieces: a frame extractor, and a browser-based
annotation UI backed by a local FastAPI server.

## Setup

```bash
pip install -r requirements.txt
```

## Step 1 — Extract frames from your videos

Put all your videos in one folder, then run:

```bash
python extract_frames.py --input_dir /path/to/your/videos --output_dir frames --fps 2
```

This samples 2 frames per second from every video in that folder and saves them into
`frames/`, named `{video_name}_{index}.jpg`. The video name is kept in the filename
on purpose — it's what lets you split train/val/test by whole video later, instead of
by time-slices, which avoids near-duplicate frames leaking across splits.

Adjust `--fps` based on your total footage. At ~7 minutes total footage, 2 fps gives
you roughly 800-900 frames — a reasonable, annotatable-solo target.

## Step 2 — Edit your class list

Open `classes.txt` and edit it — one class name per line. The order matters: line 1
is class 0, line 2 is class 1, etc. This order becomes your YOLO class IDs, so don't
reorder it after you've started annotating (or you'll need to relabel).

Default classes provided: `car`, `motorcycle`, `bus`, `truck`, `rickshaw`.

## Step 3 — Run the annotation tool

```bash
python app.py
```

Then open **http://localhost:8000** in your browser.

### How to annotate
- Click and drag on the image to draw a box around a vehicle
- Press number keys **1-9** to switch the active class before drawing (or use the dropdown)
- **A** / Left Arrow → previous frame (auto-saves current frame first)
- **D** / Right Arrow → next frame (auto-saves current frame first)
- **S** → manually save the current frame
- **Backspace** → delete the most recently drawn box
- Click "delete" next to any box in the sidebar list to remove it specifically
- The counter at the top tracks how many frames have at least one saved box

Labels are saved as standard YOLO `.txt` files in `labels/`, one per frame, same
basename as the image (e.g. `frames/vid1_00003.jpg` → `labels/vid1_00003.txt`).
A frame with no vehicles simply gets no label file — that's valid YOLO behavior for
a negative (background) example, and you don't need to force an empty box.

## Step 4 — Build your train/val/test split

Once annotation is done, split by video (not by time-slice) to avoid leakage. A
quick example, assuming you want to hold out full videos rather than shuffle frames:

```python
import shutil, random
from pathlib import Path

frames_dir = Path("frames")
labels_dir = Path("labels")

# group frame filenames by their source video (the part before the last underscore)
videos = {}
for f in frames_dir.glob("*.jpg"):
    video_name = f.stem.rsplit("_", 1)[0]
    videos.setdefault(video_name, []).append(f)

video_names = list(videos.keys())
random.seed(42)
random.shuffle(video_names)

# adjust split counts to match your actual number of videos
test_videos = video_names[:1]
val_videos = video_names[1:2]
train_videos = video_names[2:]

def copy_split(video_list, split_name):
    out_img = Path(f"dataset/{split_name}/images"); out_img.mkdir(parents=True, exist_ok=True)
    out_lbl = Path(f"dataset/{split_name}/labels"); out_lbl.mkdir(parents=True, exist_ok=True)
    for v in video_list:
        for f in videos[v]:
            shutil.copy(f, out_img / f.name)
            lbl = labels_dir / f"{f.stem}.txt"
            if lbl.exists():
                shutil.copy(lbl, out_lbl / lbl.name)

copy_split(train_videos, "train")
copy_split(val_videos, "val")
copy_split(test_videos, "test")
print("train videos:", train_videos)
print("val videos:", val_videos)
print("test videos:", test_videos)
```

This produces a standard `dataset/{train,val,test}/{images,labels}` layout, which
you can point a `data.yaml` at for YOLOv8 training:

```yaml
train: dataset/train/images
val: dataset/val/images
test: dataset/test/images
nc: 5
names: [car, motorcycle, bus, truck, rickshaw]
```

## Notes

- Re-running `extract_frames.py` on the same output folder will overwrite frames with
  matching names but won't delete unrelated ones — safe to re-run per-video if you add footage later.
- If you resize the browser window mid-session, the canvas resizes on the next frame
  navigation; boxes are stored normalized (0-1) so they stay correct regardless of display size.
- This is a local tool only — nothing leaves your machine, no accounts, no cloud dependency.
