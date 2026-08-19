import os
import time
from ultralytics import YOLO


# model 1 from scratch


print("\n" + "-" * 50)
print("MODEL 1 - FROM SCRATCH")
print("-" * 50)

model1 = YOLO("yolov8n-seg.yaml")

start = time.time()

model1.train(
    data="data.yaml",
    imgsz=320,
    batch=4,
    epochs=50,
    device="cpu",
    workers=2,
    seed=42,
    project="runs",
    name="scratch",
    exist_ok=True,
    patience=0
)

train_time1 = time.time() - start


# Validation
metrics1 = model1.val(
    data="data.yaml",
    imgsz=320,
    batch=4,
    device="cpu",
    split="val"
)

map50_1 = metrics1.seg.map50
map95_1 = metrics1.seg.map


# Inference time
times1 = []

for image in os.listdir("dataset/images/val"):

    start = time.time()

    model1.predict(
        os.path.join("dataset/images/val", image),
        imgsz=320,
        device="cpu",
        verbose=False
    )

    times1.append(time.time() - start)

avg_time1 = sum(times1) / len(times1)


# Test
model1.predict(
    source="dataset/images/test",
    imgsz=320,
    device="cpu",
    save=True,
    project="runs",
    name="scratch_test"
)


# model 2 pretrained



print("\n" + "-" * 50)
print("MODEL 2 - PRETRAINED")
print("-" * 50)

model2 = YOLO("yolov8n-seg.pt")

start = time.time()

model2.train(
    data="data.yaml",
    imgsz=320,
    batch=4,
    epochs=50,
    device="cpu",
    workers=2,
    seed=42,
    project="runs",
    name="pretrained",
    exist_ok=True,
    patience=0
)

train_time2 = time.time() - start


# Validation
metrics2 = model2.val(
    data="data.yaml",
    imgsz=320,
    batch=4,
    device="cpu",
    split="val"
)

map50_2 = metrics2.seg.map50
map95_2 = metrics2.seg.map


# Inference time
times2 = []

for image in os.listdir("dataset/images/val"):

    start = time.time()

    model2.predict(
        os.path.join("dataset/images/val", image),
        imgsz=320,
        device="cpu",
        verbose=False
    )

    times2.append(time.time() - start)

avg_time2 = sum(times2) / len(times2)


# Test
model2.predict(
    source="dataset/images/test",
    imgsz=320,
    device="cpu",
    save=True,
    project="runs",
    name="pretrained_test"
)


#Results comparison

print("\n")
print("-" * 70)
print("FINAL COMPARISON")
print("-" * 70)

print(f"{'Metric':<30} {'Scratch':<20} {'Pretrained':<20}")
print("-" * 70)

print(
    f"{'Training time (min)':<30}"
    f"{train_time1 / 60:<20.2f}"
    f"{train_time2 / 60:<20.2f}"
)

print(
    f"{'Mask mAP50':<30}"
    f"{map50_1:<20.4f}"
    f"{map50_2:<20.4f}"
)

print(
    f"{'Mask mAP50-95':<30}"
    f"{map95_1:<20.4f}"
    f"{map95_2:<20.4f}"
)

print(
    f"{'Inference time (sec/image)':<30}"
    f"{avg_time1:<20.4f}"
    f"{avg_time2:<20.4f}"
)

print("-" * 70)