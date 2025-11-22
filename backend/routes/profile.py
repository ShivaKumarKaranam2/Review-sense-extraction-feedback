from fastapi import APIRouter, HTTPException
from ..database import get_conn
from ..models import ProfileUpdate
from backend.database import get_user_stats
router = APIRouter()

@router.get("/profile")
def get_profile(email: str):
    """
    Fetch user profile details by email.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT email, full_name, age, bio FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()
    
    if not user:
        return {"detail": "User not found"}
    
    return {
        "email": user["email"],
        "full_name": user["full_name"],
        "age": user["age"],
        "bio": user["bio"]
    }


@router.put("/update_profile")
def update_profile(payload: ProfileUpdate):
    """
    Update user profile details using JSON body (not query parameters)
    """
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM users WHERE email = ?", (payload.email,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    cur.execute(
        "UPDATE users SET full_name = ?, age = ?, bio = ? WHERE email = ?",
        (payload.full_name, payload.age, payload.bio, payload.email),
    )
    conn.commit()
    conn.close()

    return {"message": "Profile updated successfully ✅"}


@router.get("/user_stats")
def user_stats(email: str):
    try:
        data = get_user_stats(email)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch statistics: {e}")


