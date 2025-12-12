from fastapi import APIRouter, Form
from backend.database import get_conn

router = APIRouter()

@router.post("/feedback/save")
def save_feedback(
    email: str = Form(...),
    sentence: str = Form(...),
    aspect: str = Form(None),
    model_sentiment: str = Form(...),
    model_score: float = Form(...),
    feedback: str = Form(...)
):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        INSERT INTO user_feedback
        (email, sentence, aspect, model_sentiment, model_score, feedback)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        email,
        sentence,
        aspect,
        model_sentiment,
        model_score,
        feedback
    ))

    conn.commit()
    conn.close()

    return {"message": "Feedback saved successfully"}
