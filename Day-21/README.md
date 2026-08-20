# Document Text Extraction Tool

An OCR pipeline that preprocesses document images (deskewing, denoising, contrast correction) and extracts text using Tesseract OCR, with bounding boxes, confidence scores, and accuracy evaluation against ground truth.

## Pipeline Overview

```
Raw Image → Preprocessing → OCR (Tesseract) → Annotated Output + Text/JSON
                                ↓
                  Accuracy comparison: Raw vs Preprocessed
```

### 1. Preprocessing
Each image goes through three steps, in this order:

- **Deskew** — Estimates the tilt angle of the text using contour detection then rotates the image to straighten it. Skew estimates beyond 30° are treated as unreliable and skipped, to avoid making a clean image worse.
- **Denoise** — A median blur removes small speckle noise  while mostly preserving text edges.
- **Contrast correction** — Contrast Limited Adaptive Histogram Equalization(CLAHE) is applied instead of simple global contrast stretching, since it adjusts contrast locally which handles uneven lighting.

### 2. OCR Extraction
Tesseract's `image_to_data` function is used instead of plain text extraction, since it returns, for every detected word:
- The recognized text
- Its bounding box (x, y, width, height)
- A confidence score (0–100)

This allows word-level bounding boxes to be drawn on the image color-coded by confidence (green = high, orange = medium, red = low) and saved alongside a structured text output.

### 3. Accuracy Evaluation
Ground truth text is compared against OCR output using two standard metrics:

- **CER (Character Error Rate)** — the proportion of characters that would need to be changed to turn the OCR output into the correct text.
- **WER (Word Error Rate)** — Since a single wrong character breaks a whole word, WER is typically higher than CER.

Lower values are better for both.

## Results

Accuracy was measured across the full labeled dataset, comparing OCR run on raw images versus OCR run on preprocessed images:

| Version | CER | WER |
|---|---|---|
| Raw | 0.537 | 0.711 |
| Preprocessed | 0.634 | 0.842 |

**Preprocessing did not improve OCR accuracy on this dataset — accuracy actually decreased.**

### Reason:

This dataset (CORD — scanned/photographed receipts) is already reasonably clean, upright, and consistently lit. Because of this, the preprocessing pipeline had little genuine distortion to correct and instead introduced small side effects that hurt OCR performance:

- **Deskew** occasionally applied unnecessary micro-rotations on already-straight images, introducing rotation-interpolation blur.
- **Median blur** softened already-crisp printed text, making similar-looking characters (e.g. `rn` vs `m`) harder to distinguish.
- **CLAHE** amplified fine image noise on already well-exposed images adding visual grain that wasn't there before.



### Hardest Images 

Three of the most visually challenging document images were manually selected and reviewed individually, with their raw, preprocessed, and OCR-annotated versions placed side by side for direct comparison.
## Key Takeaway

Preprocessing benefit is conditional on input quality:
- On genuinely degraded images (tilted, blurry, poorly lit phone photos)  preprocessing is expected to improve OCR accuracy.
- On already-clean scanned images — preprocessing can introduce small negative effects rather than helping.

