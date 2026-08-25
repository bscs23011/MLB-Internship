import os
import json
import csv
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import imagehash



query_name = "1.jpg"
dataset_dir = "dataset"
data = np.load("embeddings.npz")


names = data.files

matrix = np.stack([data[name] for name in names])

query_embedding = data[query_name].reshape(1, -1)

similarities = cosine_similarity(query_embedding, matrix)[0]

results = []

for i in range(len(names)):

    if names[i] != query_name:
        results.append((names[i], similarities[i]))

results.sort(key=lambda x: x[1], reverse=True)


results = results[:5]


filenames = []

for file in os.listdir(dataset_dir):

    if file.lower().endswith(
        (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    ):
        filenames.append(file)

filenames.sort()

# Calculate pHash
hashes = {}

for filename in filenames:

    image_path = os.path.join(dataset_dir, filename)

    hashes[filename] = imagehash.phash(Image.open(image_path).convert("RGB"))


# Compare every pair of images
duplicate_pairs = []

for i in range(len(filenames)):

    for j in range(i + 1, len(filenames)):

        name1 = filenames[i]
        name2 = filenames[j]

        distance = hashes[name1] - hashes[name2]

        # Duplicate threshold
        if distance <= 10:

            duplicate_pairs.append(
                (name1, name2, distance)
            )



images_to_show = [query_name]

for name, score in results:
    images_to_show.append(name)

fig, axes = plt.subplots(
    1,
    len(images_to_show),
    figsize=(3 * len(images_to_show), 3.5)
)

if len(images_to_show) == 1:
    axes = [axes]


query_path = os.path.join(dataset_dir, query_name)

query_image = Image.open(query_path)

axes[0].imshow(query_image)
axes[0].set_title(
    "QUERY\n" + query_name,
    fontsize=9
)
axes[0].axis("off")


for i, (name, score) in enumerate(results, start=1):

    image_path = os.path.join(dataset_dir, name)

    image = Image.open(image_path)

    axes[i].imshow(image)

    axes[i].set_title(
        f"#{i}: {name}\nsim={score:.3f}",
        fontsize=8
    )

    axes[i].axis("off")


plt.tight_layout()

plt.savefig(
    "results_grid.png",
    dpi=150
)

plt.close()

print("Saved results grid to results_grid.png")



report = {
    "query_image": query_name,

    "top_5_similar": [],

    "duplicate_pairs": []
}


# Add similarity results
for name, score in results:

    report["top_5_similar"].append(
        {
            "filename": name,
            "cosine_similarity": round(
                float(score),
                4
            )
        }
    )


# Add duplicate results
for name1, name2, distance in duplicate_pairs:

    report["duplicate_pairs"].append(
        {
            "image1": name1,
            "image2": name2,
            "hamming_distance": int(distance)
        }
    )


with open("report.json", "w") as file:

    json.dump(
        report,
        file,
        indent=2
    )

print("Saved JSON report to report.json")