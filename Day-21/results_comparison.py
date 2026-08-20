import cv2
import pytesseract
from pytesseract import Output
from jiwer import cer, wer
import os
import csv


raw_dir = "dataset/image"
preprocessed_dir = "pre-processed-images"
ground_truth_dir = "ground_truth"
per_image_csv_path = "overall_accuracy_report.csv"

raw_files = sorted(os.listdir(raw_dir))
preprocessed_files = sorted(os.listdir(preprocessed_dir))
gt_files = sorted(os.listdir(ground_truth_dir))

n = min(len(raw_files), len(preprocessed_files), len(gt_files))
print(f"Matching {n} files by sorted order (raw={len(raw_files)}, "
      f"preprocessed={len(preprocessed_files)}, ground_truth={len(gt_files)})")

per_image_results = []
all_gt_texts = []
all_raw_texts = []
all_pre_texts = []

for idx in range(n):
    raw_path = os.path.join(raw_dir, raw_files[idx])
    preprocessed_path = os.path.join(preprocessed_dir, preprocessed_files[idx])
    gt_path = os.path.join(ground_truth_dir, gt_files[idx])

    raw_img = cv2.imread(raw_path)
    preprocessed_img = cv2.imread(preprocessed_path)

    if raw_img is None or preprocessed_img is None:
        print(f"Skipping index {idx} — could not read raw or preprocessed image")
        continue

    with open(gt_path, "r", encoding="utf-8") as f:
        ground_truth_text = f.read().strip()

    if not ground_truth_text:
        print(f"Skipping index {idx} — empty ground truth")
        continue
    #RAW OCR    
    raw_rgb = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
    raw_data = pytesseract.image_to_data(raw_rgb, output_type=Output.DICT)
    raw_words = [
        raw_data['text'][i].strip()
        for i in range(len(raw_data['text']))
        if int(raw_data['conf'][i]) != -1 and raw_data['text'][i].strip() != ""
    ]
    raw_text = " ".join(raw_words)

    #OCR preprocessed
    if len(preprocessed_img.shape) == 2:
        preprocessed_rgb = cv2.cvtColor(preprocessed_img, cv2.COLOR_GRAY2RGB)
    else:
        preprocessed_rgb = cv2.cvtColor(preprocessed_img, cv2.COLOR_BGR2RGB)

    pre_data = pytesseract.image_to_data(preprocessed_rgb, output_type=Output.DICT)
    pre_words = [
        pre_data['text'][i].strip()
        for i in range(len(pre_data['text']))
        if int(pre_data['conf'][i]) != -1 and pre_data['text'][i].strip() != ""
    ]
    pre_text = " ".join(pre_words)

    #Per-image CER/WER
    raw_cer = cer(ground_truth_text, raw_text) if raw_text else 1.0
    raw_wer = wer(ground_truth_text, raw_text) if raw_text else 1.0
    pre_cer = cer(ground_truth_text, pre_text) if pre_text else 1.0
    pre_wer = wer(ground_truth_text, pre_text) if pre_text else 1.0

    per_image_results.append({
        "index": idx,
        "raw_file": raw_files[idx],
        "preprocessed_file": preprocessed_files[idx],
        "gt_file": gt_files[idx],
        "raw_CER": round(raw_cer, 3),
        "raw_WER": round(raw_wer, 3),
        "preprocessed_CER": round(pre_cer, 3),
        "preprocessed_WER": round(pre_wer, 3),
    })

    all_gt_texts.append(ground_truth_text)
    all_raw_texts.append(raw_text)
    all_pre_texts.append(pre_text)

    print(f"[{idx}] raw CER={raw_cer:.3f} WER={raw_wer:.3f} | "
          f"preprocessed CER={pre_cer:.3f} WER={pre_wer:.3f}")


# Overall CER/WER
combined_gt = " ".join(all_gt_texts)
combined_raw = " ".join(all_raw_texts)
combined_pre = " ".join(all_pre_texts)

overall_raw_cer = cer(combined_gt, combined_raw)
overall_raw_wer = wer(combined_gt, combined_raw)
overall_pre_cer = cer(combined_gt, combined_pre)
overall_pre_wer = wer(combined_gt, combined_pre)

print("\nOVERALL OCR ACCURACY")
print(f"RAW          -> CER: {overall_raw_cer:.3f} | WER: {overall_raw_wer:.3f}")
print(f"PREPROCESSED -> CER: {overall_pre_cer:.3f} | WER: {overall_pre_wer:.3f}")
