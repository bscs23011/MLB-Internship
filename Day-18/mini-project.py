import cv2

def process_video(input_video, output_video):

    # Read video
    vid = cv2.VideoCapture(input_video)

    if not vid.isOpened():
        print(f"Could not open {input_video}")
        return

    # Video properties
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"\nProcessing: {input_video}")
    print(f"FPS: {fps}")
    print(f"Width: {width}")
    print(f"Height: {height}")

    # Display original video
    while True:

        ret, frame = vid.read()

        if not ret:
            break

        resized = cv2.resize(frame, (640, 480))

        cv2.imshow("Original Video", resized)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Reset video to beginning
    vid.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(
        output_video,
        fourcc,
        fps,
        (640, 480),
        False
    )

    # Process video
    while True:

        ret, frame = vid.read()

        if not ret:
            break

        # Resize
        frame = cv2.resize(frame, (640, 480))

        # Grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Gaussian Blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Canny Edge Detection
        edges = cv2.Canny(blur, 100, 200)

        # Display processed video
        cv2.imshow("Processed Video", edges)

        # Save processed frame
        out.write(edges)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    vid.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"{output_video} saved successfully.")


# Process 3 Videos

videos = [
    ("input/vid1.mp4", "output/processed_vid1.mp4"),
    ("input/vid2.mp4", "output/processed_vid2.mp4"),
    ("input/vid3.mp4", "output/processed_vid3.mp4")
]

for input_video, output_video in videos:
    process_video(input_video, output_video)
