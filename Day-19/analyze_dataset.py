import os


with open("annotation_tool/classes.txt", "r") as file:
    classes = [line.strip() for line in file if line.strip()]


videos = {}


frames = os.listdir("annotation_tool/frames")

for frame in frames:

    if not frame.lower().endswith((".jpg", ".jpeg", ".png")):
        continue


    name = os.path.splitext(frame)[0]
    video = name.rsplit("_frame_", 1)[0]

    if video not in videos:
        videos[video] = {
            "frames": 0,
            "labeled": 0,
            "classes": [0] * len(classes)
        }

    videos[video]["frames"] += 1

    label_file = os.path.join(
        "annotation_tool/labels",
        os.path.splitext(frame)[0] + ".txt"
    )

    if os.path.exists(label_file):

        with open(label_file, "r") as file:
            labels = file.readlines()

        if len(labels) > 0:
            videos[video]["labeled"] += 1

        # Count objects
        for label in labels:

            parts = label.split()

            if len(parts) > 0:
                class_id = int(parts[0])

                if class_id < len(classes):
                    videos[video]["classes"][class_id] += 1


print("\nDATASET ANALYSIS")
print("=" * 70)

for video in videos:

    print("\nVideo:", video)
    print("Frames:", videos[video]["frames"])
    print("Labeled frames:", videos[video]["labeled"])

    print("Objects:")

    for i in range(len(classes)):
        print("  ", classes[i], ":", videos[video]["classes"][i])

    print("\n" + "-" * 70)

