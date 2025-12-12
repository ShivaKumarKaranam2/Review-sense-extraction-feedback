from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.utils import clean_text
from backend.database import save_sentiment_record, save_aspect_sentiment_record
from typing import Optional
import pandas as pd
import io
import torch
import nltk
from nltk.corpus import stopwords
import spacy
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from peft import PeftModel
from backend.database import save_log

router = APIRouter()

# ==============================
# 🔧 Model Config
# ==============================
MODEL_ID = "Shiva-k22/sentiment-lora-distilbert"
BASE_MODEL = "distilbert-base-uncased"
_tokenizer = None
_model = None
_pipeline = None

LABEL_MAP = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
}

# Load spaCy for aspect extraction
nlp = spacy.load("en_core_web_sm")

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
# 🧩 Aspect Extraction
# ==============================
def extract_aspects(text: str):
    """Extract candidate aspects using noun phrases and named entities."""
    doc = nlp(text)
    aspects = set()
    for chunk in doc.noun_chunks:
        aspects.add(chunk.text.strip())
    for ent in doc.ents:
        aspects.add(ent.text.strip())
    return list(aspects)


# ==============================
# 🎯 Aspect + Overall Sentiment (for a single text)
# ==============================
def analyze_aspects_with_overall(original_text: str):
    pipe = load_model_once()

    # Clean text for inference
    cleaned = preprocess_text(original_text)
    aspects = extract_aspects(original_text)
    results = []

    

    # ✅ Overall sentiment (use cleaned text, not undefined "text")
    overall_res = pipe(cleaned)[0]
    overall_label = LABEL_MAP.get(overall_res["label"], overall_res["label"])
    overall_score = round(float(overall_res["score"]), 3)

    # ✅ Aspect-level sentiment (use original text in prompt)
    for aspect in aspects:
        prompt = f"Aspect: {aspect}. Sentence: {original_text}"
        res = pipe(prompt)[0]
        label = LABEL_MAP.get(res["label"], res["label"])
        score = round(float(res["score"]), 3)
        results.append({
            "aspect": aspect,
            "aspect_sentiment": label,
            "aspect_score": score
        })

    return {
        "sentence": original_text,
        "cleaned_sentence": cleaned,
        "overall_sentiment": overall_label,
        "overall_score": overall_score,
        "aspects": results
    }



# ==============================
# 🎯 Single Text Prediction
# ==============================
@router.post("/predict_single")
def predict_single(email: str = Form(...), text: str = Form(...)):
    print(f"📥 Request: Email={email}, Text preview={text[:60]}")

    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    try:
        cleaned = preprocess_text(text)
        
        result = analyze_aspects_with_overall(cleaned)

        # Save both overall & aspect sentiments
        save_sentiment_record(
            email,
            text,
            cleaned,
            result["overall_sentiment"],
            result["overall_score"]
        )
        save_aspect_sentiment_record(
            email=email,
            sentence=result["sentence"],
            aspects=result["aspects"],
            overall_sentiment=result["overall_sentiment"],
            overall_score=result["overall_score"]
        )
        save_log(
            email=email,
            route="/predict_single",
            action="SINGLE_PREDICTION",
            message=f"Prediction: {result['overall_sentiment']} ({round(result['overall_score'],3)})",
            payload=text
        )

        return result
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Inference failed: {e}")


# # ==============================
# # 📂 Batch Prediction (with Aspect Support)
# # ==============================
# @router.post("/predict_batch")
# async def predict_batch(
#     email: str = Form(...),
#     file: UploadFile = File(...),
#     text_column: Optional[str] = Form(None)
# ):
#     try:
#         print("📥 Received request for batch prediction")
#         contents = await file.read()
#         filename = file.filename.lower()

#         # Load file
#         if filename.endswith(".csv"):
#             df = pd.read_csv(io.BytesIO(contents))
#         elif filename.endswith((".xls", ".xlsx")):
#             df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
#         else:
#             raise HTTPException(status_code=400, detail="Unsupported file format. Please upload CSV or Excel.")

#         if not text_column or text_column not in df.columns:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Please specify which column contains text data. Available columns: {list(df.columns)}"
#             )

#         texts = df[text_column].astype(str).tolist()
#         print(f"🧾 Processing {len(texts)} sentences...")

#         all_results = []
#         for text in texts:
#             cleaned = preprocess_text(text)
#             result = analyze_aspects_with_overall(text)

#             # Save each result
#             save_sentiment_record(email, text, cleaned, result["overall_sentiment"], result["overall_score"])
#             save_aspect_sentiment_record(
#                 email=email,
#                 sentence=result["sentence"],
#                 aspects=result["aspects"],
#                 overall_sentiment=result["overall_sentiment"],
#                 overall_score=result["overall_score"]
#             )
#             all_results.append(result)

#         # Flatten for preview
#         rows = []
#         for r in all_results:
#             for a in r["aspects"]:
#                 rows.append({
#                     "Sentence": r["sentence"],
#                     "Aspect": a["aspect"],
#                     "Aspect Sentiment": a["aspect_sentiment"],
#                     "Aspect Score": a["aspect_score"],
#                     "Overall Sentiment": r["overall_sentiment"],
#                     "Overall Score": r["overall_score"]
#                 })

#         df_out = pd.DataFrame(rows)
#         print("✅ Batch Aspect Analysis Complete")

#         return {
#                 "message": f"Processed {len(all_results)} reviews successfully.",
#                 "results": df_out.to_dict(orient="records")
#                 }


#     except HTTPException:
#         raise
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"Internal error: {e}")

# ==============================
# 📂 Batch Prediction (with Aspect Support)
# ==============================
@router.post("/predict_batch")
async def predict_batch(
    email: str = Form(...),
    file: UploadFile = File(...),
    text_column: Optional[str] = Form(None)
):
    try:
        print("📥 Received request for batch prediction")

        contents = await file.read()
        filename = file.filename.lower()

        # 🔥 SAVE FILE FIRST
        from backend.database import get_conn
        import os

        user_dir = os.path.join("user_data", email.replace("@", "_at_"))
        os.makedirs(user_dir, exist_ok=True)

        saved_path = os.path.join(user_dir, file.filename)
        with open(saved_path, "wb") as f:
            f.write(contents)

        # 🔥 Store DB record
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO uploaded_datasets (email, filename, file_path)
            VALUES (?, ?, ?)
        """, (email, file.filename, saved_path))
        conn.commit()

        # -------------------------
        # Load file into dataframe
        # -------------------------
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
        else:
            raise HTTPException(status_code=400,
                detail="Unsupported file format. Please upload CSV or Excel."
            )

        if not text_column or text_column not in df.columns:
            raise HTTPException(
                status_code=400,
                detail=f"Please specify which column contains text data. Available columns: {list(df.columns)}"
            )

        texts = df[text_column].astype(str).tolist()
        print(f"🧾 Processing {len(texts)} sentences...")

        all_results = []
        for text in texts:
            cleaned = preprocess_text(text)
            result = analyze_aspects_with_overall(cleaned)

            save_sentiment_record(email, text, cleaned,
                                  result["overall_sentiment"],
                                  result["overall_score"])

            save_aspect_sentiment_record(
                email=email,
                sentence=result["sentence"],
                aspects=result["aspects"],
                overall_sentiment=result["overall_sentiment"],
                overall_score=result["overall_score"]
            )
            all_results.append(result)

        # Flatten for preview
        rows = []
        for r in all_results:
            for a in r["aspects"]:
                rows.append({
                    "Sentence": r["sentence"],
                    "Aspect": a["aspect"],
                    "Aspect Sentiment": a["aspect_sentiment"],
                    "Aspect Score": a["aspect_score"],
                    "Overall Sentiment": r["overall_sentiment"],
                    "Overall Score": r["overall_score"]
                })

        df_out = pd.DataFrame(rows)
        print("✅ Batch Aspect Analysis Complete")
        save_log(
            email,
            "/predict_batch",
            "BATCH_PREDICTION",
            f"{len(all_results)} reviews processed"
        )


        return {
            "message": f"Processed {len(all_results)} reviews successfully.",
            "results": df_out.to_dict(orient="records")
        }

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
