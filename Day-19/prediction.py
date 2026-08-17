from ultralytics import YOLO


model = YOLO("best.pt")

results = model.predict(
    source="vid3.mp4",
    conf=0.4,
    save=True,
    project="predictions",
    name="output"
)

print("Done. Output video saved in predictions/output/")

