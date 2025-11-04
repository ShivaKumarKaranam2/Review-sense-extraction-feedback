from fastapi import APIRouter, HTTPException
from backend.models import SignupModel, LoginModel, ResetRequestModel, ResetConfirmModel
from backend.database import init_db, user_exists, add_user, get_user_password, set_reset_token, get_reset_token, update_password
from backend.utils import hash_password, verify_password, generate_token
from backend.utils import hash_password as make_hashes

router = APIRouter()
init_db()

@router.post("/signup")
def signup(payload: SignupModel):
    print("🔍 Signup payload:", payload.dict())
    try:
        if user_exists(payload.email):
            print("⚠️ User already exists")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        print("✅ Hashing password")
        hashed = hash_password(payload.password)
        
        print("✅ Adding user to DB")
        add_user(payload.email, hashed, payload.full_name, payload.age, payload.bio)
        
        print("✅ Signup completed successfully")
        return {"message": "Account created"}

    except Exception as e:
        print("❌ Signup error:", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
def login(payload: LoginModel):
    if not user_exists(payload.email):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    stored = get_user_password(payload.email)
    if not stored or not verify_password(payload.password, stored):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # for now, return simple success response (or you can add JWT here)
    return {"message": "Login successful"}

@router.post("/forgot-password")
def forgot_password(payload: ResetRequestModel):
    if not user_exists(payload.email):
        # don't reveal user existence — but user requested exact behavior: we can return same message
        # For dev, we return success or store token only if user exists
        return {"message": "If the email is registered, a reset token was generated. (Check logs)"}
    token = generate_token(24)
    set_reset_token(payload.email, token)
    # In production: send email with token + link. For now return token in response for testing.
    return {"message": "Reset token created (in production you would email this).", "token": token}

@router.post("/reset-password")
def reset_password(payload: ResetConfirmModel):
    if not user_exists(payload.email):
        raise HTTPException(status_code=400, detail="Invalid token or email")
    stored_token = get_reset_token(payload.email)
    if not stored_token or stored_token != payload.token:
        raise HTTPException(status_code=400, detail="Invalid token")
    new_hashed = hash_password(payload.new_password)
    update_password(payload.email, new_hashed)
    return {"message": "Password updated"}
