import os

images = sorted(
    f for f in os.listdir("yolo_seg_dataset/images")
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
)

train = images[:48]
val = images[48:54]
test = images[54:60]

splits = {
    "train": train,
    "val": val,
    "test": test
}

for split in splits:
    os.makedirs("dataset" + "/images/" + split, exist_ok=True)
    os.makedirs("dataset" + "/labels/" + split, exist_ok=True)

for split, images_list in splits.items():

    for image in images_list:

        label = os.path.splitext(image)[0] + ".txt"
        with open("yolo_seg_dataset/images" + "/" + image, "rb") as f:
            data = f.read()

        with open("dataset" + "/images/" + split + "/" + image, "wb") as f:
            f.write(data)

        with open("yolo_seg_dataset/labels" + "/" + label, "r") as f:
            data = f.read()

        with open("dataset" + "/labels/" + split + "/" + label, "w") as f:
            f.write(data)

print("Total:", len(images))
print("Train:", len(train))
print("Val:", len(val))
print("Test:", len(test))