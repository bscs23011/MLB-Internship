import os
from ultralytics import YOLO

FRAMES_FOLDER = "dataset/test/images"
LABELS_FOLDER = "dataset/test/labels"
MODEL_PATH = "best.pt"
TEMP_FOLDER = "temp_eval"

VIDEOS = ["video12", "video14"]  # change to your actual new video names

CLASS_NAMES = "[car, motorcycle, bus, truck, rickshaw, pedestrian]"


def copy_file(src, dst):
    with open(src, "rb") as f_in:
        data = f_in.read()
    with open(dst, "wb") as f_out:
        f_out.write(data)


model = YOLO(MODEL_PATH)

for video in VIDEOS:

    img_dir = os.path.join(TEMP_FOLDER, video, "images")
    lbl_dir = os.path.join(TEMP_FOLDER, video, "labels")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(lbl_dir, exist_ok=True)

    matched_frames = 0

    for frame in os.listdir(FRAMES_FOLDER):

        if not frame.startswith(video + "_frame_"):
            continue
        if not frame.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        name = os.path.splitext(frame)[0]
        label_file = name + ".txt"

        src_img = os.path.join(FRAMES_FOLDER, frame)
        src_lbl = os.path.join(LABELS_FOLDER, label_file)

        if not os.path.exists(src_lbl):
            print("WARNING: no label found for", frame, "- skipping")
            continue

        copy_file(src_img, os.path.join(img_dir, frame))
        copy_file(src_lbl, os.path.join(lbl_dir, label_file))
        matched_frames += 1

    print("\n" + video + ": " + str(matched_frames) + " annotated frames found")

    if matched_frames == 0:
        print("Skipping " + video + " - no annotated frames to evaluate.")
        continue

    yaml_path = os.path.join(TEMP_FOLDER, video, "data.yaml")
    yaml_lines = [
        "path: " + os.path.abspath(os.path.join(TEMP_FOLDER, video)),
        "train: images",
        "val: images",
        "",
        "nc: 6",
        "names: " + CLASS_NAMES,
    ]
    with open(yaml_path, "w") as f:
        f.write("\n".join(yaml_lines))

    print("Evaluating on " + video + "...")
    metrics = model.val(data=yaml_path, split="val", conf=0.4)

    print("\n--- Results for " + video + " ---")
    print("mAP50:", metrics.box.map50)
    print("mAP50-95:", metrics.box.map)
    print("Precision:", metrics.box.mp)
    print("Recall:", metrics.box.mr)