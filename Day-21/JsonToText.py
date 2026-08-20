import json
import os

annotations_dir = "dataset/json"
ground_truth_dir = "ground_truth"

for fname in sorted(os.listdir(annotations_dir)):
    if not fname.endswith(".json"):
        continue

    json_path = os.path.join(annotations_dir, fname)
    with open(json_path, "r", encoding="utf-8") as f:
        annotation = json.load(f)

    words_in_order = []
    for line in annotation["valid_line"]:
        for word in line["words"]:
            text = word["text"].strip()
            if text:
                words_in_order.append(text)

    plain_text = " ".join(words_in_order)

    base_name = os.path.splitext(fname)[0]
    txt_path = os.path.join(ground_truth_dir, base_name + ".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(plain_text)

    print(f"Saved ground truth -> {txt_path}")

print("Done.")