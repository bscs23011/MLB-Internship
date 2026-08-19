# Instance Segmentation: From Scratch vs. Pretrained (YOLOv8n-seg)

This project compares two ways of training an AI model to detect and outline
("segment") an object in images — one model learns from zero, the other
starts with knowledge borrowed from a huge existing dataset (COCO).

---

## 1. What This Project Does

1. **Collected 60 images** of a single object.
2. **Manually drew polygon outlines** (masks) around the object in every
   image using a custom browser-based annotation tool.
3. **Split the data** into:
   - 48 images to train on
   - 6 images to check progress during training (validation)
   - 6 images the models never saw at all, to test them fairly at the end
4. **Trained two YOLOv8n-seg models** using the exact same settings (image
   size, batch size, epochs, CPU-only) so the comparison is fair:
   - **Model 1 — From Scratch:** starts with random, untrained weights.
   - **Model 2 — Pretrained:** starts with weights already trained on
     COCO (a huge dataset of 118,000+ everyday images).
5. **Compared both models** on training time, accuracy, and speed.

---

## 2. Files in This Project

| File | What it does |
|---|---|
| `polygon_annotator.html` | Open in a browser to manually draw polygon masks around objects and export labels in YOLO format. |
| `split_dataset.py` | Splits your labeled images into train / val / test folders. |
| `train_compare.py` | Trains both models (scratch and pretrained) and prints a comparison table. |

---

## 3. How the Code Works (Simple Version)

### `split_dataset.py`
- Looks at your `images/` and `labels/` folders.
- Cuts the list into three chunks: first 48 → train, next 6 → val, last 6 →
- Copies everything into a clean `dataset/` folder that YOLO understands.

### `train_compare.py`
- Trains **Model 1** using `yolov8n-seg.yaml` — this loads only the model's
  architecture , with all knowledge starting at
  random.
- Trains **Model 2** using `yolov8n-seg.pt` — this loads the same
  architecture, but with weights already trained on COCO.
- Both models train with identical settings (image size 320px, batch size
  4, 50 epochs, CPU only) so nothing except the starting weights differs.
- After training, it tests both models on the validation images and reports
  accuracy and speed. It also runs both models on the 6 never-before-seen
  test images and saves the predicted outlines as images you can look at.

---

## 4. Understanding the Metrics (Plain English)

### IoU — "How well do the shapes overlap?"
Imagine the correct outline you drew and the model's predicted outline as
two overlapping shapes. IoU just measures how much they overlap:
- Perfect match → 100%
- No overlap at all → 0%
- Somewhat close → somewhere in between

### Mask mAP50 — "Did it find the object, even roughly?"
This counts a prediction as correct if it overlaps the real object by at
least **50%**. It's a fairly relaxed test even a rough slightly different
outline still passes.

### Mask mAP50-95 — "Did it outline the object precisely?"
This is a much stricter test. Instead of checking overlap at just 50%, it
checks at many levels — 50%, 55%, 60%... up to 95% — and averages the
score. A model can only score well here if its outlines are tightly and
accurately shaped not just roughly in the right place."

---

## 5. Results

| Metric | Model 1 (Scratch) | Model 2 (Pretrained) |
|---|---|---|
| Training time (min) | 22.77 | 20.44 |
| Mask mAP50 | 0.0869 | 0.5927 |
| Mask mAP50-95 | 0.0244 | 0.2662 |
| Inference time (sec/image) | 0.1868 | 0.1339 |

---

## 6. What These Results Mean

### The pretrained model wins by a lot on accuracy
- **Mask mAP50:** the pretrained model was right roughly **6.8 times more
  often** than the scratch model.
- **Mask mAP50-95:** the gap grows even bigger about **11 times more
  accurate** on the strict test.

**Why?** The scratch model has to learn everything from nothing 
what edges look like, what shapes look like, what "an object" even is 
using only 48 training images. That's nowhere near enough data to learn
all of that from zero. The pretrained model already knows all of this from
being trained on 118,000+ COCO images beforehand. It only needs to learn
"apply what I already know to this specific new object," which is a much
easier task with just 48 images.

**Why did the gap grow bigger on the strict test (mAP50-95)?**
It's not just that the scratch model missed objects more often — when it
did find something, its outline was sloppy and imprecise. The pretrained
model's outlines were both more frequently correct AND much more
tightly/accurately shaped.

### Training time was about the same
22.77 vs. 20.44 minutes — a small difference, most likely just normal
variation (background CPU load, system noise) rather than a real
difference. Both models did the same amount of computation per training
step (same architecture, same image size, same batch size, same epochs),
so training speed itself isn't meaningfully affected by which weights you
start from.

### The pretrained model was also faster at inference
0.134 sec/image vs. 0.187 sec/image — about 28% faster. Both models have
the exact same architecture and size, so this difference likely comes from
the pretrained model producing cleaner, more confident predictions, which
means less post-processing work needs to happen afterward.

## The output for the fine-tuned model is given in the "fine-tuned" folder but the model which was trained from scratch wasn't able to detect a single pothole. 
