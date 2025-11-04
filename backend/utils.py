import re
import secrets
from passlib.hash import argon2
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# ===============================
# 1️⃣ SECURITY UTILITIES
# ===============================

def hash_password(password: str) -> str:
    """Hash password using Argon2 (secure and supports long passwords)."""
    return argon2.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password using Argon2."""
    return argon2.verify(plain_password, hashed_password)

def generate_token(length: int = 48) -> str:
    """Generate a secure random token for session/auth."""
    return secrets.token_urlsafe(length)

# ===============================
# 2️⃣ TEXT CLEANING UTILITIES
# ===============================

# Ensure NLTK data is available
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

STOPWORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()

def clean_text(text: str) -> str:
    """
    Clean text for sentiment or NLP tasks:
    - Lowercase
    - Remove URLs, mentions, punctuation, and numbers
    - Remove stopwords
    - Lemmatize remaining words
    """
    if not isinstance(text, str):
        return ""

    # Lowercase and strip
    text = text.strip().lower()

    # Remove URLs and mentions
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+", "", text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Remove punctuation and numbers
    text = re.sub(r"[^a-z\s]", " ", text)

    # Tokenize
    tokens = text.split()

    # Remove stopwords and lemmatize
    tokens = [LEMMATIZER.lemmatize(word) for word in tokens if word not in STOPWORDS]

    # Join back to cleaned string
    cleaned = " ".join(tokens)

    return cleaned.strip()

