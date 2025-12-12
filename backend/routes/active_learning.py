from fastapi import APIRouter, HTTPException, Form
from backend.database import get_conn
from backend.database import get_aspect_predictions
from backend.database import save_log

router = APIRouter()

@router.post("/active_learning/save")
def save_correction(
    email: str = Form(...),
    sentence: str = Form(...),
    aspect: str = Form(...),
    original_sentiment: str = Form(...),
    original_score: float = Form(...),
    corrected_sentiment: str = Form(...)
):
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO active_learning
            (email, sentence, aspect, original_sentiment, original_score, corrected_sentiment)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            email, sentence, aspect, original_sentiment,
            original_score, corrected_sentiment
        ))

        conn.commit()
        conn.close()
        


        return {"message": "Correction saved successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/active_learning/get")
def get_active_learning_data(email: str):
    return get_aspect_predictions(email)


