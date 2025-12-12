from backend.database import get_conn
from fastapi import APIRouter
import os

router = APIRouter()

# -----------------------------
# Already Existing 👇
# -----------------------------
@router.get("/admin/users")
def admin_get_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT email, full_name, age, bio FROM users")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

@router.get("/admin/predictions")
def admin_get_predictions():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM aspect_sentiment_records ORDER BY created_at DESC
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

@router.get("/admin/corrections")
def admin_get_corrections():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM active_learning ORDER BY created_at DESC
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

@router.delete("/admin/delete_user") 
def delete_user(email: str): 
    conn = get_conn() 
    cur = conn.cursor() 
    cur.execute("DELETE FROM users WHERE email = ?", (email,)) 
    conn.commit() 
    conn.close() 
    return {"message": "User deleted"}

@router.get("/admin/global_stats")
def admin_global_stats():
    conn = get_conn()
    cur = conn.cursor()

    # total users
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    # total predictions made
    cur.execute("SELECT COUNT(*) FROM aspect_sentiment_records")
    total_predictions = cur.fetchone()[0]

    # total active learning corrections
    cur.execute("SELECT COUNT(*) FROM active_learning")
    total_corrections = cur.fetchone()[0]

    # Fetch full dataset
    cur.execute("""
        SELECT email, sentence, aspect, aspect_sentiment AS sentiment, 
               aspect_score AS score, overall_sentiment, overall_score
        FROM aspect_sentiment_records
    """)
    rows = [dict(r) for r in cur.fetchall()]

    conn.close()

    return {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "total_corrections": total_corrections,
        "records": rows
    }


# -----------------------------
# 2️⃣ ALL ACTIVE LEARNING CORRECTIONS
# -----------------------------
@router.get("/admin/all_corrections")
def admin_all_corrections():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT email, sentence, aspect, original_sentiment,
               original_score, corrected_sentiment, created_at
        FROM active_learning
        ORDER BY created_at DESC
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return rows


# -----------------------------

UPLOAD_ROOT = "user_data"

@router.get("/admin/list_datasets")
def admin_list_datasets():
    if not os.path.exists(UPLOAD_ROOT):
        return []

    results = []
    for user_folder in os.listdir(UPLOAD_ROOT):
        folder_path = os.path.join(UPLOAD_ROOT, user_folder)

        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                results.append({
                    "user": user_folder.replace("_at_", "@"),
                    "file_name": file,
                    "path": os.path.join(folder_path, file),
                })

    return results


# -----------------------------
# 4️⃣ SIMPLE LOG VIEWER
# -----------------------------
@router.get("/admin/logs")
def admin_logs():
    LOG_FILE = "server.log"

    if not os.path.exists(LOG_FILE):
        return {"content": "No logs found"}

    with open(LOG_FILE, "r") as f:
        content = f.read()

    return {"content": content}