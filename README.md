# 💬 Infosys_ReviewSense  
**AI-Powered Review Analysis and Chat-based Feedback Management System**

---

## 📘 About the Project

**Infosys_ReviewSense** is an AI-driven feedback analysis platform built using **Streamlit** and **FastAPI**, designed to extract meaningful insights from customer reviews.  
It combines **secure user authentication**, **profile management**, and **sentiment analysis** through an intuitive and interactive interface.

### 👤 Users can:
- 🔐 Sign up, log in, and manage their profiles securely (Argon2 password hashing)  
- 💬 Interact through a chat interface for real-time sentiment insights  
- 📂 Upload CSV/Excel files for batch sentiment prediction  
- 🧠 Analyze feedback using a fine-tuned **LoRA DistilBERT** model trained for 3 sentiment labels:  
  - `Positive`, `Neutral`, and `Negative`  

All user and prediction data are stored securely in a **SQLite database**, ensuring persistence and integrity.

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| Frontend | Streamlit (Python) |
| Backend | FastAPI |
| Database | SQLite |
| Model | LoRA fine-tuned DistilBERT |
| Authentication | Argon2 Password Hashing |
| Deployment | Local / Docker-ready setup |

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/Infosys_ReviewSense.git
cd Infosys_ReviewSense


### 2️⃣ Create a Virtual Environment
python -m venv infosys
source infosys/bin/activate   # On macOS/Linux
infosys\Scripts\activate      # On Windows

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Run the Backend (FastAPI)
uvicorn backend.main:app --reload


The backend will start at: http://127.0.0.1:8000

### 5️⃣ Run the Frontend (Streamlit)
streamlit run frontend/app.py


The app will open in your browser at: http://localhost:8501

### 🧩 Project Structure
Infosys_ReviewSense/
│
├── backend/
│   ├── main.py                 # FastAPI main entry
│   ├── database.py             # SQLite connection & CRUD functions
│   ├── utils.py                # Hashing, token, and text cleaning utilities
│   ├── routes/
│   │   ├── auth.py             # Signup & Login
│   │   ├── profile.py          # Profile management
│   │   └── sentiment.py        # Sentiment prediction endpoints
│
├── frontend/
│   └── app.py                  # Streamlit frontend
│
├── requirements.txt
└── README.md

### 🧠 Model Information

The project uses the fine-tuned model:
👉 Shiva-k22/sentiment-lora-distilbert

Trained to classify sentiments as:

LABEL_0 → Negative

LABEL_1 → Neutral

LABEL_2 → Positive

### 🏁 Conclusion

Infosys_ReviewSense provides a secure and intelligent foundation for analyzing customer feedback with modern AI techniques.
It unifies authentication, chat-based interaction, and sentiment analysis — paving the way for advanced feedback intelligence and analytics in future versions.

### 👨‍💻 Developed by

Shiva Kumar Karanam

