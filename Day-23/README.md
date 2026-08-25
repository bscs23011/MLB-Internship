# Similar & Duplicate Image Finder

A small pipeline that finds visually similar images and detects duplicate/near-duplicate images in a folder of 20-30 photos.

## How it works (pipeline)

```
dataset/ (20-30 images)
      │
      ├──► extract_embeddings.py
      │        MobileNetV2 (pretrained CNN) converts each image
      │        into a 1280-number "embedding" vector that captures
      │        its visual content/meaning.
      │        → saved to embeddings.npz
      │
      ├──► challenge.py (mandatory challenge)
      │        Takes one image and creates 3 modified copies:
      │        resized, cropped, brightness-changed.
      │        Re-run extract_embeddings.py afterward so these
      │        3 new files also get embeddings.
      │
      └──► report_final.py <query_image>
               1. Cosine similarity: compares the query image's
                  embedding to every other embedding → top 5 most
                  similar images.
               2. Perceptual hashing (pHash): compares a structural
                  fingerprint of every image pair → flags near-identical
                  duplicates (Hamming distance ≤ 10).
               → results_grid.png (query + top 5, visual)
               → report.json (similarity scores + duplicate pairs)
```

## Two methods two jobs

| Method | Detects | Good at | Weak at |
|---|---|---|---|
| **CNN embeddings + cosine similarity** | "Looks like" (same subject/scene) | Similar but not identical images, resizing, brightness, cropping | Exact pixel-level matching |
| **Perceptual hashing (pHash)** | "Is the same photo" (duplicate/edited copy) | Resize, brightness/contrast changes, recompression | Cropping (changes the frame layout) |

Using both catches more cases than either one alone.

## Findings (from the mandatory challenge)

Original: `1.jpg` → created `1_resized.jpg`, `1_cropped.jpg`, `1_bright.jpg`

**Cosine similarity results (top 5 for `1.jpg`):**

| Image | Similarity |
|---|---|
| 1_resized.jpg | 0.987 |
| 1_bright.jpg | 0.976 |
| 1_cropped.jpg | 0.803 |
| (unrelated photo) | 0.695 |
| (unrelated photo) | 0.643 |

All 3 modified versions correctly ranked as the most similar images — clearly above unrelated photos, even the cropped one.

**Perceptual hash duplicate pairs found:**

| Pair | Hamming distance | Flagged? |
|---|---|---|
| 1.jpg ↔ 1_resized.jpg | 0 |  Yes |
| 1.jpg ↔ 1_bright.jpg | 6 |  Yes |
| 1_bright.jpg ↔ 1_resized.jpg | 6 |  Yes |
| 1.jpg ↔ 1_cropped.jpg | 26 |  No |

## Main Points

- **Resize and brightness changes**: caught by *both* methods.
- **Cropping**: caught by CNN embeddings (still ranked top-5, 0.80 similarity) but **missed** by pHash (distance 26, way above the threshold of 10).

This is expected, not a bug: pHash reads the overall spatial layout of an image, and cropping changes that layout. CNN embeddings pool information across the whole image, so they tolerate missing content better. This is exactly why the pipeline uses both methods together instead of relying on just one.

## Files

- `embeddings.npz` — CNN embeddings for every image
- `results_grid.png` — visual grid of query + top 5 matches
- `report.json` — similarity scores + duplicate pairs in structured form


```
