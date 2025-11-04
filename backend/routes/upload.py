from fastapi import APIRouter, UploadFile, Form, HTTPException
import os

router = APIRouter()

UPLOAD_ROOT = "user_data"

@router.post("/upload_data")
async def upload_data(email: str = Form(...), file: UploadFile = None):
    """
    Upload a dataset file (CSV/XLSX/etc.) for a specific user.
    Stores files under user_data/<email>/filename
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Create user-specific directory
    user_dir = os.path.join(UPLOAD_ROOT, email.replace("@", "_at_"))  # sanitize folder name
    os.makedirs(user_dir, exist_ok=True)

    file_path = os.path.join(user_dir, file.filename)

    # Save the file
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File saving failed: {str(e)}")

    return {"message": f"✅ File '{file.filename}' uploaded successfully!", "path": file_path}

