from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.utils import clean_text
from backend.database import save_sentiment_record
from typing import Optional
import pandas as pd
import io
import torch
import mimetypes
import nltk
from nltk.corpus import stopwords

# Transformers/PEFT imports
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from peft import PeftModel

router = APIRouter()

# ==============================
# 🔧 Model Config
# ==============================
MODEL_ID = "Shiva-k22/sentiment-lora-distilbert"
BASE_MODEL = "distilbert-base-uncased"
_tokenizer = None
_model = None
_pipeline = None

# Label mapping (based on your fine-tuning: 0=Negative, 1=Neutral, 2=Positive)
LABEL_MAP = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
}

# ==============================
# 🧠 Load Model Once
# ==============================
def load_model_once():
    global _tokenizer, _model, _pipeline
    if _pipeline is not None:
        return _pipeline

    print("🚀 Loading tokenizer and model...")

    _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    try:
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
        print("✅ Direct model load successful.")
    except Exception as e:
        print("⚙️ Loading as LoRA adapter:", e)
        base_model = AutoModelForSequenceClassification.from_pretrained(BASE_MODEL, num_labels=3)
        _model = PeftModel.from_pretrained(base_model, MODEL_ID)
        print("✅ LoRA model applied successfully.")

    device = 0 if torch.cuda.is_available() else -1
    _pipeline = pipeline("sentiment-analysis", model=_model, tokenizer=_tokenizer, device=device)
    print("✅ Pipeline initialized successfully.")
    return _pipeline


# ==============================
# 🧹 Helper: Clean + Remove Stopwords
# ==============================
def preprocess_text(text: str):
    text = clean_text(text)
    nltk.download("stopwords", quiet=True)
    stop_words = set(stopwords.words("english"))
    tokens = [word for word in text.split() if word.lower() not in stop_words]
    return " ".join(tokens)


# ==============================
# 🎯 Single Text Prediction
# ==============================
@router.post("/predict_single")
def predict_single(email: str = Form(...), text: str = Form(...)):
    print(f"📥 Request: Email={email}, Text preview={text[:60]}")

    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    try:
        pipe = load_model_once()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model load failed: {e}")

    try:
        cleaned = preprocess_text(text)
        res = pipe(cleaned, truncation=True)
        print("🧠 Pipeline output:", res)
        label = res[0]['label']
        score = float(res[0]['score'])
        readable_label = LABEL_MAP.get(label, label)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {e}")

    try:
        save_sentiment_record(email, text, cleaned, readable_label, score)
    except Exception as e:
        print(f"⚠️ DB save failed: {e}")

    return {
        "original": text,
        "cleaned": cleaned,
        "label": readable_label,
        "score": score
    }


# ==============================
# 📂 Batch Prediction
# ==============================
@router.post("/predict_batch")
async def predict_batch(
    email: str = Form(...),
    file: UploadFile = File(...),
    text_column: Optional[str] = Form(None)
):
    try:
        print("📥 Received request for batch prediction")
        print(f"📧 Email: {email}")
        print(f"📄 Filename: {file.filename}")
        contents = await file.read()
        print(f"📦 File size: {len(contents)} bytes")

        # ✅ Robust File Format Handling
        filename = file.filename.lower()
        try:
            if filename.endswith(".csv"):
                df = pd.read_csv(io.BytesIO(contents))
                print("✅ File read as CSV")
            elif filename.endswith((".xls", ".xlsx")):
                df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
                print("✅ File read as Excel")
            else:
                # Try auto-detecting format just in case
                try:
                    df = pd.read_csv(io.BytesIO(contents))
                    print("⚙️ Auto-detected CSV format")
                except Exception:
                    try:
                        df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
                        print("⚙️ Auto-detected Excel format")
                    except Exception:
                        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload CSV or Excel.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not parse file: {str(e)}")

        print(f"📊 Columns found: {list(df.columns)}")

        # Require user to specify text column name
        if not text_column:
            raise HTTPException(
                status_code=400,
                detail=f"Please specify which column contains text data. Available columns: {list(df.columns)}"
            )

        if text_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Invalid column '{text_column}'. Available: {list(df.columns)}")

        # Extract text data
        texts = df[text_column].astype(str).tolist()
        print(f"🧾 Number of texts: {len(texts)}")

        # Load model and predict
        pipe = load_model_once()
        cleaned = [preprocess_text(t) for t in texts]
        res = pipe(cleaned, truncation=True)

        # Extract label and score for each prediction
        labels = [LABEL_MAP.get(r["label"], r["label"]) for r in res]
        scores = [round(float(r["score"]), 4) for r in res]  # rounded for readability

        # ✅ Final DataFrame with required columns
        df_out = pd.DataFrame({
            "original_text": texts,
            "cleaned_text": cleaned,
            "sentiment": labels,
            "confidence_score": scores
        })

        print("✅ Batch prediction completed successfully")

        # Return both summary and preview
        return {
            "message": f"Processed {len(df_out)} rows successfully.",
            "preview": df_out.head(10).to_dict(orient="records")
        }

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
