import os
import pandas as pd
from datasets import Dataset
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          TrainingArguments, Trainer, DataCollatorWithPadding)

# 1) Konfigurasi
MODEL_NAME = os.environ.get("MODEL_NAME", "indobenchmark/indobert-base-p1")  # bisa ganti ke "bert-base-multilingual-cased"
MAX_LEN = int(os.environ.get("MAX_LEN", 256))
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "outputs_classifier")
TRAIN_PATH = os.environ.get("TRAIN_PATH", "data/train.csv")
VALID_PATH = os.environ.get("VALID_PATH", "data/valid.csv")

# 2) Load data
train_df = pd.read_csv(TRAIN_PATH)
valid_df = pd.read_csv(VALID_PATH)

# Bersihkan nan
train_df = train_df.dropna(subset=["text", "label"]).reset_index(drop=True)
valid_df = valid_df.dropna(subset=["text", "label"]).reset_index(drop=True)

# 3) Label encoding
le = LabelEncoder()
train_df["label_id"] = le.fit_transform(train_df["label"])
valid_df["label_id"] = le.transform(valid_df["label"])  # pastikan label valid ada di train
id2label = {i: l for i, l in enumerate(le.classes_)}
label2id = {l: i for i, l in id2label.items()}

train_ds = Dataset.from_pandas(train_df[["text", "label_id"]])
valid_ds = Dataset.from_pandas(valid_df[["text", "label_id"]])

# 4) Tokenizer & encode
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def preprocess(batch):
    return tokenizer(batch["text"], truncation=True, max_length=MAX_LEN)

train_ds = train_ds.map(preprocess, batched=True)
valid_ds = valid_ds.map(preprocess, batched=True)

# 5) Model
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(le.classes_),
    id2label=id2label,
    label2id=label2id,
)

# 6) Metrics
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = logits.argmax(axis=-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1_macro": f1_score(labels, preds, average="macro"),
    }

# 7) Trainer args
args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="steps",
    logging_steps=50,
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    num_train_epochs=3,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="f1_macro",
    greater_is_better=True,
    fp16=True,
)

collator = DataCollatorWithPadding(tokenizer)

# 8) Train
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_ds,
    eval_dataset=valid_ds,
    tokenizer=tokenizer,
    data_collator=collator,
    compute_metrics=compute_metrics,
)

trainer.train()

# 9) Simpan label encoder & model
os.makedirs(OUTPUT_DIR, exist_ok=True)
le_path = os.path.join(OUTPUT_DIR, "labels.txt")
with open(le_path, "w", encoding="utf-8") as f:
    for c in le.classes_:
        f.write(c + "\n")

trainer.save_model(OUTPUT_DIR)
print("Training selesai. Model di:", OUTPUT_DIR)