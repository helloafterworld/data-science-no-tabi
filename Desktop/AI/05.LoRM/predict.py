import sys, os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_DIR = sys.argv[1] if len(sys.argv) > 1 else "outputs_classifier"
text = sys.argv[2] if len(sys.argv) > 2 else "Pengiriman cepat dan ramah"

# Load label mapping
labels = [l.strip() for l in open(os.path.join(MODEL_DIR, "labels.txt"), encoding="utf-8").readlines()]
id2label = {i: l for i, l in enumerate(labels)}

# Load model & tok
tok = AutoTokenizer.from_pretrained(MODEL_DIR)
mdl = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)

inputs = tok(text, return_tensors="pt", truncation=True)
with torch.no_grad():
    out = mdl(**inputs)
probs = out.logits.softmax(dim=-1).squeeze().tolist()

pred_id = int(out.logits.argmax(dim=-1))
print({"text": text, "pred_label": id2label[pred_id], "probs": dict(zip(labels, [round(p,4) for p in probs]))})