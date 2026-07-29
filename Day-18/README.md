# Video Processing with OpenCV

## How OpenCV Reads Videos

OpenCV reads videos using the `cv2.VideoCapture()` function. A video is treated as a sequence of individual image frames. The `read()` method retrieves one frame at a time and returns:

* `ret`: A boolean value indicating whether a frame was successfully read.
* `frame`: The current frame of the video.

The program processes these frames continuously until the end of the video is reached.

## What FPS Means

FPS (Frames Per Second) represents the number of frames displayed every second during video playback. A higher FPS results in smoother motion, while a lower FPS produces less smooth playback. The program retrieves the video's FPS using `cv2.CAP_PROP_FPS` to ensure the processed video is saved with the same playback speed as the original.

## Processing Techniques Applied

* **Frame Resizing:** Resized each frame to 640 × 480 pixels for consistent processing and display.
* **Grayscale Conversion:** Converted color frames to grayscale to simplify image processing.
* **Gaussian Blur:** Reduced image noise and smoothed the frames before edge detection.
* **Canny Edge Detection:** Detected object boundaries and highlighted significant edges in each frame.
* **Video Writing:** Saved the processed frames into a new video using OpenCV's `VideoWriter`.

## Challenges Faced

* Resetting the video position after displaying the original video so it could be processed again from the beginning.
* Ensuring all frames were resized consistently before processing and saving.
* Releasing video resources properly to avoid file access and display issues.
* Processing multiple videos efficiently without duplicating code by creating a reusable processing function.

## Recording:
[video link](https://drive.google.com/file/d/1ZpcWBfTNw8G7ElHQngFeybTdi7-RjBj_/edit)
