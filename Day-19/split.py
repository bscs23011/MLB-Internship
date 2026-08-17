import os

for split in ["train", "val", "test"]:
    os.makedirs("dataset/" + split + "/images", exist_ok=True)
    os.makedirs("dataset/" + split + "/labels", exist_ok=True)

counts = {
    "train": 0,
    "val": 0,
    "test": 0
}

frames = os.listdir("annotation_tool/frames")

for frame in frames:

    if not frame.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    name = os.path.splitext(frame)[0]

    # Get video name
    video = name.rsplit("_frame_", 1)[0]

    # Decide where the frame goes
    if video in ["video12", "video14"]:
        split = "test"

    elif video in ["video11"]:
        split = "val"

    else:
        split = "train"

    # Copy image
    with open("annotation_tool/frames/" + frame, "rb") as source:
        with open("dataset/" + split + "/images/" + frame, "wb") as destination:
            destination.write(source.read())

    # Copy label
    label = name + ".txt"

    if os.path.exists("annotation_tool/labels/" + label):

        with open("annotation_tool/labels/" + label, "rb") as source:
            with open("dataset/" + split + "/labels/" + label, "wb") as destination:
                destination.write(source.read())

    counts[split] += 1


print("Split complete.")
print("Train:", counts["train"])
print("Val:", counts["val"])
print("Test:", counts["test"])