from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import sentiment
from backend.routes import auth, profile, upload  # 👈 add these
from backend.database import init_db
from backend.routes import active_learning
from backend.routes import admin
from backend.routes import logs
from backend.routes import feedback

app = FastAPI(title="Sentiment Service")

# initialize DB
init_db()

# CORS for Streamlit local dev:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(sentiment.router, prefix="/sentiment", tags=["sentiment"])
app.include_router(profile.router, prefix="", tags=["profile"])   # 👈 added
app.include_router(upload.router, prefix="", tags=["upload"])     # 👈 optional if using file upload
app.include_router(active_learning.router, prefix="", tags=["active_learning"])
app.include_router(admin.router, prefix="", tags=["admin"])

app.include_router(logs.router, prefix="", tags=["logs"])
app.include_router(feedback.router, prefix="", tags=["feedback"])


@app.get("/")
def root():
    return {"message": "Backend running"}
