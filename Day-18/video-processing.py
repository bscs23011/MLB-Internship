import cv2

# Read a video using OpenCV.
vid = cv2.VideoCapture("vid.mp4")

if not vid.isOpened():
    print("Error: Could not open video.")
    exit()

# Print the video's FPS, width, height, and total number of frames.
fps = vid.get(cv2.CAP_PROP_FPS)
width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"FPS: {fps}")
print(f"Width: {width}")
print(f"Height: {height}")
print(f"Total Frames: {total_frames}")

# Display the video frame by frame.
while True:
    ret, frame = vid.read()

    if not ret:
        break

    cv2.imshow("Video", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

vid.set(cv2.CAP_PROP_POS_FRAMES, 0)

# Save Processed Video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter(
    "processed_video.mp4",
    fourcc,
    fps,
    (width, height),
    False 
)

# Convert each frame to grayscale.
# Apply Canny Edge Detection to each frame.
while True:

    ret, frame = vid.read()

    if not ret:
        break
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Canny Edge Detection
    edges = cv2.Canny(gray, 100, 200)

    # Save processed frame
    out.write(edges)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

vid.release()
out.release()
cv2.destroyAllWindows()


# Capture live video from your webcam and display it in real time.
webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Error: Could not access webcam.")
    exit()

print("Press 'q' to quit webcam.")

while True:

    ret, frame = webcam.read()

    if not ret:
        break

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()