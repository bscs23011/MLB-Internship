import os
import json
import torch
import cv2

from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
    CLIPProcessor,
    CLIPModel
)



image_folder = "dataset"
output_json_path = "results.json"


print("Loading BLIP")

blip_processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

blip_model.to("cpu")
blip_model.eval()



print("Loading CLIP")

clip_processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

clip_model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
)

clip_model.to("cpu")
clip_model.eval()



image_filenames = sorted(
    f for f in os.listdir(image_folder)
    if f.lower().endswith(
        (".jpg", ".jpeg", ".png", ".webp", ".bmp")
    )
)

if len(image_filenames) == 0:
    raise SystemExit(
        f"No images found in '{image_folder}'. "
        "Add some images and run again."
    )


print(f"\nFound {len(image_filenames)} images.")
print("Creating captions and embeddings...\n")




gallery = []


with torch.no_grad():

    for filename in image_filenames:

        image_path = os.path.join(
            image_folder,
            filename
        )

        image = cv2.imread(image_path)

        if image is None:
            print(f"Could not read: {filename}")
            continue

        
        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )


        blip_inputs = blip_processor(
            images=image,
            return_tensors="pt"
        )

        caption_ids = blip_model.generate(
            **blip_inputs,
            max_new_tokens=30
        )

        caption = blip_processor.decode(
            caption_ids[0],
            skip_special_tokens=True
        )


        clip_inputs = clip_processor(
            images=image,
            return_tensors="pt"
        )

        image_embedding = clip_model.get_image_features(**clip_inputs)

        image_embedding = image_embedding.pooler_output 

        image_embedding = (
            image_embedding /
            image_embedding.norm(
                p=2,
                dim=-1,
                keepdim=True
            )
        )

        gallery.append(
            {
                "filename": filename,
                "caption": caption,
                "embedding": image_embedding[0]
            }
        )


        print(f"{filename}")
        print(f"Caption: {caption}")
        print()



print("----------------------------------------")
print("Type a search query.")
print("Press Enter without text to stop.")
print("----------------------------------------\n")


all_query_results = []


while True:

    query_text = input("Search query: ").strip()

    if query_text == "":
        break


    with torch.no_grad():

        text_inputs = clip_processor(
            text=[query_text],
            return_tensors="pt",
            padding=True
        )

        text_embedding = clip_model.get_text_features(**text_inputs)
        text_embedding = text_embedding.pooler_output             
        text_embedding = (
            text_embedding /
            text_embedding.norm(
                p=2,
                dim=-1,
                keepdim=True
            )
        )

        text_embedding = text_embedding[0]


    scored_images = []


    for entry in gallery:

        similarity = torch.dot(
            entry["embedding"],
            text_embedding
        )

        similarity = float(similarity)

        scored_images.append(
            (
                similarity,
                entry["filename"],
                entry["caption"]
            )
        )


    scored_images.sort(
        key=lambda item: item[0],
        reverse=True
    )


    top_5 = scored_images[:5]



    print()
    print(f'Top 5 matches for "{query_text}":')


    query_result = {
        "query": query_text,
        "results": []
    }


    for rank, (
        similarity,
        filename,
        caption
    ) in enumerate(top_5, start=1):

        print(
            f"{rank}. {filename}"
        )

        print(
            f"   Similarity: {similarity:.4f}"
        )

        print(
            f"   Caption: {caption}"
        )

        print()


        query_result["results"].append(
            {
                "rank": rank,
                "filename": filename,
                "similarity_score": round(
                    similarity,
                    4
                ),
                "caption": caption
            }
        )


    all_query_results.append(
        query_result
    )




report = {
    "images": [
        {
            "filename": entry["filename"],
            "caption": entry["caption"]
        }
        for entry in gallery
    ],

    "queries": all_query_results
}


with open(
    output_json_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        report,
        file,
        indent=2,
        ensure_ascii=False
    )


print(f"Saved results to: {output_json_path}")