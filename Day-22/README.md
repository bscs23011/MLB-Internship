# ANPR Pipeline (Automatic Number Plate Recognition)

This project finds vehicle in a photo, finds the number plate on each vehicle, cleans up the
plate image, and then reads the text on it. Here's how it works, step by step.

## The 3 steps

**1. `plate_detection.py` — find the vehicle, then find the plate on it**

- Uses YOLOv8n (a ready-made, pre-trained model) to find vehicles
  (car / motorcycle / bus / truck) in each photo from `dataset/images`.
- For every vehicle it finds, it crops just that vehicle out of the photo and sends the
  crop to a plate-detector model hosted on Roboflow (`license-plate-recognition-rxg4e`,
  version 11).
- Not every box Roboflow suggests is trusted blindly — a plate is always a wide
  rectangle sitting on the lower half of the vehicle, so any suggested box that's the
  wrong shape or sits too high up (grille, badge, windshield area) is thrown away.
- The plate is cropped out with a little extra margin around it (so OCR later doesn't
  lose a character at the edge), saved into `plate_crops/`, and the full photo with
  boxes drawn on it is saved into `plates_output/`.

**2. `preprocess.py` — clean up the plate crop before reading it**

- Scales the crop up if it's small.
- Converts it to grayscale.
- Boosts contrast (CLAHE) so faint characters stand out more.
- Removes noise/graininess.
- Saves the cleaned-up version into `plate_crops_preprocessed/`.

**3. `ocr_plates.py` — read the text on the plate**

- Runs Tesseract OCR on every cleaned-up crop, word by word.
- Each word gets marked "Readable" or "Unreadable" depending on how confident
  Tesseract is.
- Saves one JSON file per plate crop into `ocr_jsn_output/` (the text found, its
  position, and its confidence score).
- Also saves a copy of the plate crop with colored boxes drawn on it (green =
  readable, red = unreadable) into `annotated-ocr-images/`, so you can see visually
  what was and wasn't read.

**The `challenging_images/` folder** holds the 3 hand-picked hard test cases
(angled / blurry / low-resolution plates) used to check where the pipeline
struggles — see the last section below.

## Why some cars don't get detected at all

YOLOv8n is the smallest, fastest version of YOLOv8 — it trades away some accuracy for
speed, so it occasionally misses a real, clearly visible car. A few reasons this
happens with this dataset in particular:

- Some source photos are extreme close-ups of just the bumper/plate area — there's no
  visible car shape (roof, windows, wheels) left in the frame, so a detector trained
  to recognize whole-car silhouettes has nothing to latch onto.
- YOLOv8n was trained on general COCO photos, not this specific dataset, so odd
  angles, reflections, or unusual crops it never saw much of during training reduce
  its confidence — and the script only keeps a detection if it's at least 35%
  confident.
- A bigger model (YOLOv8s/m/l) would catch more of these, at the cost of running
  slower.

## Why some detected cars don't get a plate crop

Once a vehicle is found, the plate detector doesn't always succeed inside it either.
Two different things can happen:

- **Roboflow finds nothing at all.** Its model, like any detector, has limits a
  plate that's tiny heavily
  angled, or partly hidden behind another vehicle or object is much harder for it to
  spot confidently.
- **Roboflow suggests a box, but it gets rejected.** This is on purpose. Earlier the
  model kept confidently pointing at the badge above the real plate instead of
  the plate itself, so a sanity check was added: reject anything that isn't a
  wide-rectangle shape, or that sits in the top 40% of the vehicle. 
  This fixed the wrong-crop problem, but it's a trade-off — a real
  plate mounted in an unusual spot can also get
  rejected by the same rule.

## Why some plates are read with low confidence

- **The crops are just small to begin with.** Many raw plate crops are very
  low-resolution — meaning very few real pixels of the plate were captured in the
  first place. `preprocess.py` scales them up, but scaling up a blurry, low-detail
  image just makes a bigger blurry image; it can't invent detail that was never
  captured.
- **Motion blur, out-of-focus shots, and camera angle.** A plate photographed at a
  sideways angle has its characters squeezed and slanted, which throws off Tesseract,
  since it expects flat, horizontal text.
- **Glare and uneven lighting.** Plates are shiny/reflective, so bright spots wash out
  characters to solid white and shadows crush others to black — contrast enhancement
  (`preprocess.py`) helps but can't recover detail that's genuinely gone.
- **Tesseract itself is a classic OCR engine**, built mainly for clean scanned
  documents — not for photographed, tilted, noisy real-world text the way modern
  scene-text readers are. That's the main reason confidence stays mediocre even on
  crops that look "okay" to the eye.
- **Confidence can also be misleadingly high on very short fragments.** A junk 1-2
  character reading can sometimes score a high confidence just by coincidentally
  looking letter-shaped — the shorter the fragment, the less trustworthy its
  confidence score is in general.

