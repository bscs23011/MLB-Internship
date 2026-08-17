import cv2
import os


# Take any traffic video dataset from internet.
# convert it to frames
# annotate all the classes in it (person, car, bike, truck etc)
# preprocess annotated data
# train YOLOv8-n for object detection
# test on new unseen traffic video
# Important note : Don't take already annotated dataset. Need raw

FRAME_INTERVAL = 30  # keep 1 out of every N frames -> higher = fewer saved frames

os.makedirs("dataset/frames", exist_ok=True)

video_extensions = (".mp4", ".mov")

for video_name in os.listdir("dataset/raw-videos"):

    if not video_name.lower().endswith(video_extensions):
        continue

    video_path = os.path.join("dataset/raw-videos", video_name)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Could not open {video_name}")
        continue

    video_stem = os.path.splitext(video_name)[0]

    frame_count = 0
    saved_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % FRAME_INTERVAL == 0:  # frame interval

            # prefix with video name so frames from different videos
            # never collide when they all land in the same folder
            filename = f"{video_stem}_frame_{saved_count:05}.jpg"

            cv2.imwrite(
                os.path.join("dataset/frames", filename),
                frame
            )

            saved_count += 1

        frame_count += 1

    cap.release()

    print(f"{video_name}: {saved_count} frames extracted.")