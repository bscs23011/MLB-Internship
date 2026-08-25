# Similar & Duplicate Image Finder

A small pipeline that finds visually similar images and detects duplicate/near-duplicate images in a folder of 20-30 photos.

## Pipeline

1. `extract_embeddings.py` - Loads a pretrained MobileNetV2 CNN and converts every image in `dataset/` into a 1280-number embedding vector that represents its visual content. Saved to `embeddings.npz`.
2. `challenge.py` - Takes one image and creates 3 modified copies: resized, cropped, and brightness-changed. After running this, re-run `extract_embeddings.py` so the new files get embeddings too.
3. `report_final.py <query_image>` - Does two things:
   - Cosine similarity: compares the query image's embedding to every other image's embedding, finds the top 5 most similar.
   - Perceptual hashing (pHash): compares a structural fingerprint of every image pair, flags near-identical duplicates (Hamming distance under 10).
   - Saves `results_grid.png` (query + top 5 images) and `report.json` (similarity scores + duplicate pairs).

## Two methods, two jobs

CNN embeddings + cosine similarity find images that "look like" each other in content, even if they aren't the same photo. Good at handling resizing, brightness changes, and cropping. Not meant for exact pixel matching.

Perceptual hashing finds images that are the same photo, possibly edited. Good at catching resizing, brightness/contrast changes, and recompression. Weak at catching crops, since cropping changes the overall layout of the image.

Using both together catches more cases than either one alone.

## Findings from the mandatory challenge

Original image: `1.jpg`. Created variants: `1_resized.jpg`, `1_cropped.jpg`, `1_bright.jpg`.

Cosine similarity results for `1.jpg`:

- 1_resized.jpg: 0.987
- 1_bright.jpg: 0.976
- 1_cropped.jpg: 0.803
- next closest unrelated photo: 0.695

All 3 modified versions were correctly ranked as the most similar images, clearly above unrelated photos, even the cropped one.

Perceptual hash duplicate pairs found:

- 1.jpg and 1_resized.jpg: distance 0, flagged as duplicate
- 1.jpg and 1_bright.jpg: distance 6, flagged as duplicate
- 1_bright.jpg and 1_resized.jpg: distance 6, flagged as duplicate
- 1.jpg and 1_cropped.jpg: distance 26, NOT flagged

## Key takeaway

Resize and brightness changes were caught by both methods. Cropping was caught by CNN embeddings (still ranked top 5, 0.80 similarity) but missed by perceptual hashing (distance 26, well above the threshold of 10).

This is expected, not a bug. Perceptual hashing reads the overall spatial layout of an image, and cropping changes that layout. CNN embeddings summarize information across the whole image, so they tolerate missing content better. This is why the pipeline uses both methods together instead of relying on just one.

## Files produced

- `embeddings.npz` - CNN embeddings for every image
- `results_grid.png` - visual grid of query image + top 5 matches
- `report.json` - similarity scores and duplicate pairs

