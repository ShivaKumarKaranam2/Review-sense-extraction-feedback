import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
ACCENT = "#00A8FF"


# ----------------------------------------------
# CONFIG
# ----------------------------------------------
BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Infosys ReviewSense",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------
# MODERN UI DESIGN - 2025 AESTHETIC
# ----------------------------------------------
st.markdown("""
<style>
/* ----------------------------
   GLOBAL STYLING 
---------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 50%, #16213e 100%);
}

/* ----------------------------
   RESPONSIVE SIDEBAR (NO FIXED WIDTH)
---------------------------- */
section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.03) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 1.5rem !important;
    transition: all 0.3s ease-in-out !important;
}

/* Sidebar content inside */
section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
    padding: 0.5rem !important;
}

/* ----------------------------
   TITLES
---------------------------- */
.modern-title {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: rgba(255,255,255,0.6);
    margin-bottom: 1.5rem;
}

/* ----------------------------
   GLASS CARD
---------------------------- */
.glass-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 1.8rem;
    backdrop-filter: blur(20px);
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}

.glass-card:hover {
    border-color: rgba(99, 102, 241, 0.3);
    box-shadow: 0 12px 30px rgba(0,0,0,0.3);
}

/* ----------------------------
   INPUT FIELDS
---------------------------- */
.stTextInput > div > div > input,
textarea, 
.stNumberInput > div > div > input {
    background: rgba(255, 255, 255, 0.06) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 12px !important;
    padding: 0.8rem !important;
    color: white !important;
}

/* ----------------------------
   BUTTONS
---------------------------- */
.stButton > button, .stForm button[type="submit"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important;
    padding: 0.8rem 2rem !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: 600 !important;
    transition: 0.25s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(99,102,241,0.4);
}

/* ----------------------------
   FILE UPLOADER
---------------------------- */
.stFileUploader {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 2px dashed rgba(255, 255, 255, 0.2) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
}

/* ----------------------------
   DATAFRAME
---------------------------- */
.stDataFrame {
    border-radius: 15px !important;
    overflow: hidden !important;
}

/* ----------------------------
   MESSAGES
---------------------------- */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 12px !important;
    backdrop-filter: blur(10px) !important;
}

/* ----------------------------
   REMOVE STREAMLIT FOOTER/BRANDING
---------------------------- */
#MainMenu, footer { visibility: hidden; }
            
/* SIDEBAR GLASS BACKGROUND */
section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

/* SIDEBAR TITLES */
section[data-testid="stSidebar"] h2 {
    color: rgba(255, 255, 255, 0.9) !important;
    font-weight: 700 !important;
}

/* RADIO BUTTON CONTAINER */
.stRadio > div {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

/* EACH MENU BUTTON LOOKS LIKE A GLASS CARD */
.stRadio > div > label {
    background: rgba(255, 255, 255, 0.07) !important;
    backdrop-filter: blur(18px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(18px) saturate(180%) !important;
    border-radius: 16px !important;
    padding: 1rem 1.2rem !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    color: rgba(255, 255, 255, 0.85) !important;
    font-weight: 600 !important;
    transition: 0.25s ease;
}

/* HOVER EFFECT */
.stRadio > div > label:hover {
    background: rgba(255, 255, 255, 0.12) !important;
    transform: translateX(6px);
    border-color: rgba(99, 102, 241, 0.4) !important;
}

/* SELECTED MENU ITEM */
.stRadio > div > label[data-checked="true"] {
    background: rgba(99, 102, 241, 0.25) !important;
    border: 1px solid rgba(99, 102, 241, 0.6) !important;
    color: white !important;
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
    transform: translateX(8px);
}
/* Prevent long sidebar labels from wrapping */
.stRadio > div > label {
    white-space: nowrap !important;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Increase space so labels fit in single line */
section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
    min-width: 230px !important;
}


</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------
if "email" not in st.session_state:
    st.session_state.email = None
if "reset_mode" not in st.session_state:
    st.session_state.reset_mode = False
if "single_prediction" not in st.session_state:
    st.session_state.single_prediction = None
if "batch_results" not in st.session_state:
    st.session_state.batch_results = None


# -------------------------------------------------
# AUTH SYSTEM
# -------------------------------------------------
def signup_page():
    st.markdown("<div class='modern-title'>Create Account</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Join ReviewSense to start analyzing sentiments</div>", unsafe_allow_html=True)

    with st.form("signup_form"):


        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Email Address", key="su_email", placeholder="you@example.com")
            fullname = st.text_input("Full Name", key="su_full", placeholder="John Doe")
        with col2:
            pwd = st.text_input("Password", type="password", key="su_pwd", placeholder="••••••••")
            age = st.number_input("Age", min_value=0, key="su_age", value=25)
        
        bio = st.text_area("Bio", key="su_bio", placeholder="Tell us about yourself...", height=100)

        submitted = st.form_submit_button("Create Account")

        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            r = requests.post(
                f"{BASE}/signup",
                json={
                    "email": email,
                    "password": pwd,
                    "full_name": fullname,
                    "age": age,
                    "bio": bio
                }
            )
            if r.status_code == 200:
                st.success("🎉 Account created successfully! Please sign in.")
            else:
                st.error(r.json().get("detail", "Signup failed"))


def login_page():
    st.markdown("<div class='modern-title'>Welcome Back</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Sign in to continue to ReviewSense</div>", unsafe_allow_html=True)

    with st.form("login_form"):


        email = st.text_input("Email Address", key="li_email", placeholder="you@example.com")
        pwd = st.text_input("Password", type="password", key="li_pwd", placeholder="••••••••")

        col1, col2, col3 = st.columns([2, 2, 1])
        login_btn = col1.form_submit_button("Sign In")
        forgot_btn = col2.form_submit_button("Forgot Password?")

        st.markdown("</div>", unsafe_allow_html=True)

        if login_btn:
            r = requests.post(f"{BASE}/login", json={"email": email, "password": pwd})
            if r.status_code == 200:
                st.session_state.email = email
                st.rerun()
            else:
                st.error(r.json().get("detail", "Login failed"))

        if forgot_btn:
            st.session_state.reset_mode = True
            st.rerun()


def forgot_password_page():
    st.markdown("<div class='modern-title'>Reset Password</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Enter your email to receive a reset token</div>", unsafe_allow_html=True)

    with st.form("fp_form"):


        email = st.text_input("Registered Email", key="fp_email", placeholder="you@example.com")
        submitted = st.form_submit_button("Send Reset Token")

        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            r = requests.post(f"{BASE}/forgot-password", json={"email": email})
            st.success("✅ Reset token generated! Check backend logs.")


def reset_password_page():
    st.markdown("<div class='modern-title'>Set New Password</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Enter the token and your new password</div>", unsafe_allow_html=True)

    with st.form("rp_form"):


        email = st.text_input("Email Address", key="rp_email", placeholder="you@example.com")
        token = st.text_input("Reset Token", key="rp_token", placeholder="Enter token from email")
        newpwd = st.text_input("New Password", type="password", key="rp_pass", placeholder="••••••••")

        submitted = st.form_submit_button("Update Password")

        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            r = requests.post(
                f"{BASE}/reset-password",
                json={"email": email, "token": token, "new_password": newpwd},
            )
            if r.status_code == 200:
                st.success("✅ Password updated successfully! Please login.")
                st.session_state.reset_mode = False
            else:
                st.error("❌ Reset failed. Please check your details.")


# -------------------------------------------------
# PROFILE & DASHBOARD
# -------------------------------------------------
def profile_page():
    st.markdown("<div class='modern-title'>Profile</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Manage your account and view analytics</div>", unsafe_allow_html=True)

    email = st.session_state.email
    res = requests.get(f"{BASE}/profile", params={"email": email})

    if not res.ok:
        st.error("❌ Profile not found")
        return

    user = res.json()

    # Profile card
    with st.form("profile_form"):
        
        st.markdown("### Account Information")

        col1, col2 = st.columns(2)
        with col1:
            fullname = st.text_input("Full Name", value=user.get("full_name", ""), placeholder="John Doe")
            age = st.number_input("Age", min_value=0, value=user.get("age", 0))
        with col2:
            st.markdown(f"**Email:** {email}")
            st.markdown("")  # Spacing
        
        bio = st.text_area("Bio", value=user.get("bio", ""), placeholder="Tell us about yourself...", height=100)

        submitted = st.form_submit_button("Save Changes")

        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            r = requests.put(
                f"{BASE}/update_profile",
                json={"email": email, "full_name": fullname, "age": age, "bio": bio}
            )
            if r.ok:
                st.success("✅ Profile updated successfully!")
            else:
                st.error("❌ Update failed")

    # Stats Section
    st.markdown("<div class='modern-title' style='font-size: 2rem; margin-top: 3rem;'>Analytics Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Your sentiment analysis overview</div>", unsafe_allow_html=True)
    
    stats = requests.get(f"{BASE}/user_stats", params={"email": email})

    if not stats.ok:
        st.error("❌ Failed to load analytics")
        return

    data = stats.json()

    if data["total_records"] == 0:
        st.info("📊 No sentiment analysis performed yet. Start analyzing reviews!")
        return

    df = pd.DataFrame(data["records"])

    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Reviews", data["total_records"])
    col2.metric("Positive", sum(df["Overall Sentiment"] == "Positive"), delta="Good")
    col3.metric("Neutral", sum(df["Overall Sentiment"] == "Neutral"))
    col4.metric("Negative", sum(df["Overall Sentiment"] == "Negative"), delta="Watch")

    st.markdown("---")

    # Data Table
    with st.container():
            st.markdown("### Recent Analysis")
            st.dataframe(df, use_container_width=True, height=300)
            st.markdown("</div>", unsafe_allow_html=True)

    # Charts
    col1, col2 = st.columns(2)
    
    with col1:

        fig_pie = px.pie(
            df, 
            names="Aspect Sentiment", 
            title="Aspect Sentiment Distribution",
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:

        fig_bar = px.bar(
            df, 
            x="Aspect", 
            y="Aspect Score", 
            color="Aspect Sentiment",
            title="Aspect Score Breakdown"
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV Report", csv, "sentiment_records.csv", "text/csv")


# -------------------------------------------------
# SINGLE SENTIMENT
# -------------------------------------------------
def single_sentiment_page():
    st.markdown("<div class='modern-title'>Single Review Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Analyze sentiment for a single review text</div>", unsafe_allow_html=True)

    with st.form("single_form"):


        text = st.text_area("Review Text", placeholder="Enter the review you want to analyze...", height=150)

        submitted = st.form_submit_button("🔍 Analyze Sentiment")

        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            if not text.strip():
                st.warning("⚠️ Please enter some text to analyze")
            else:
                with st.spinner("Analyzing sentiment..."):
                    r = requests.post(
                        f"{BASE}/sentiment/predict_single",
                        data={"email": st.session_state.email, "text": text}
                    )

                if not r.ok:
                    st.error("❌ Prediction failed")
                else:
                    st.session_state.single_prediction = r.json()
                    st.success("✅ Analysis Complete!")

    # Display results if available in session state
    if st.session_state.single_prediction:
        result = st.session_state.single_prediction

        # Overall Sentiment Card

        st.markdown("### Overall Sentiment")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            sentiment_emoji = {
                "Positive": "😊",
                "Neutral": "😐",
                "Negative": "😞"
            }
            st.markdown(f"<h1 style='text-align: center; font-size: 4rem;'>{sentiment_emoji.get(result['overall_sentiment'], '📊')}</h1>", unsafe_allow_html=True)
        
        with col2:
            st.metric("Sentiment", result["overall_sentiment"])
            st.metric("Confidence Score", f"{result['overall_score']:.2f}")
        
        st.markdown("</div>", unsafe_allow_html=True)

        # Aspects Table
        # Aspects Table
        if result.get("aspects"):

            st.markdown("### Aspect Analysis")
            df = pd.DataFrame(result["aspects"])
            st.dataframe(df, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ===========================
            #   ⭐ ADD BAR CHART HERE ⭐
            # ===========================

            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### Aspect Score Bar Chart")

            fig_bar = px.bar(
                df,
                x="aspect",
                y="aspect_score",
                color="aspect_sentiment",
                title="Aspect-wise Sentiment Scores",
                text="aspect_score"
            )

            fig_bar.update_traces(textposition="outside")

            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )

            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ===========================
            #   EXISTING VISUALIZATIONS
            # ===========================

            col1, col2 = st.columns(2)
            
            with col1:
                fig_pie = px.pie(
                    df, 
                    names="aspect_sentiment", 
                    title="Aspect Sentiment Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_layout(
                    width=1400,          # Increase width
                    height=600,          # Increase height
                    margin=dict(l=40, r=40, t=80, b=80),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    title=dict(font=dict(size=26))

                )
                st.plotly_chart(fig_pie, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=result['overall_score'],
                    title={'text': "Overall Sentiment Score"},
                    gauge={
                        'axis': {'range': [None, 1]},
                        'bar': {'color': "rgba(99, 102, 241, 0.8)"},
                        'steps': [
                            {'range': [0, 0.33], 'color': "rgba(239, 68, 68, 0.3)"},
                            {'range': [0.33, 0.66], 'color': "rgba(251, 191, 36, 0.3)"},
                            {'range': [0.66, 1], 'color': "rgba(16, 185, 129, 0.3)"}
                        ]
                    }
                ))
                fig_gauge.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_gauge, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # ===========================
        #   👍 👎 USER FEEDBACK
        # ===========================

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### ✅ Was this prediction correct? Help improve the model")

        fb_col1, fb_col2 = st.columns(2)

        with fb_col1:
            if st.button("👍 Thumbs Up"):
                feedback_payload = {
                    "email": st.session_state.email,
                    "sentence": result["sentence"],
                    "aspect": "OVERALL",
                    "model_sentiment": result["overall_sentiment"],
                    "model_score": result["overall_score"],
                    "feedback": "LIKE"
                }

                res = requests.post(f"{BASE}/feedback/save", data=feedback_payload)

                if res.ok:
                    st.success("✅ Thanks! Your feedback was saved successfully.")
                else:
                    st.error("❌ Failed to save feedback")

        with fb_col2:
            if st.button("👎 Thumbs Down"):
                feedback_payload = {
                    "email": st.session_state.email,
                    "sentence": result["sentence"],
                    "aspect": "OVERALL",
                    "model_sentiment": result["overall_sentiment"],
                    "model_score": result["overall_score"],
                    "feedback": "DISLIKE"
                }

                res = requests.post(f"{BASE}/feedback/save", data=feedback_payload)

                if res.ok:
                    st.warning("⚠️ Thanks! This will help the model learn.")
                else:
                    st.error("❌ Failed to save feedback")

        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# BATCH SENTIMENT
# -------------------------------------------------
def batch_sentiment_page():
    st.markdown("<div class='modern-title'>Batch Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Analyze multiple reviews at once from CSV or Excel</div>", unsafe_allow_html=True)

    file = st.file_uploader("📁 Upload File", type=["csv", "xlsx"], help="Upload a CSV or Excel file containing reviews")
    st.markdown("</div>", unsafe_allow_html=True)

    if file:
        try:
            df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
            
    
            st.markdown("### Preview")
            st.dataframe(df.head(10), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            column = st.selectbox("📋 Select Text Column", df.columns)

            if st.button("🚀 Run Batch Analysis"):
                with st.spinner("Processing batch analysis... This may take a moment."):
                    files = {"file": (file.name, file.getvalue(), file.type)}
                    data = {"email": st.session_state.email, "text_column": column}

                    r = requests.post(f"{BASE}/sentiment/predict_batch", files=files, data=data)

                if not r.ok:
                    st.error("❌ Batch processing failed")
                else:
                    out = r.json()
                    st.session_state.batch_results = pd.DataFrame(out["results"])
                    st.success("✅ Batch Completed!")

        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

    # Display batch results if available in session state
    if st.session_state.batch_results is not None:
        df_out = st.session_state.batch_results

        st.markdown("### Results")
        st.dataframe(df_out, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Charts section
        col1, col2 = st.columns(2)

        with col1:
    
            fig_pie = px.pie(
                df_out,
                names="Aspect Sentiment",
                title="Aspect Sentiment Distribution"
            )
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
    
            fig_bar = px.bar(
                df_out,
                x="Aspect",
                y="Aspect Score",
                color="Aspect Sentiment",
                title="Aspect Score Breakdown"
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Download CSV
        csv = df_out.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Batch Output CSV",
            csv,
            "batch_results.csv",
            "text/csv"
        )

def active_learning_page():
    st.markdown("<div class='modern-title'>Active Learning</div>", unsafe_allow_html=True)    
    st.info("Improve the model by correcting wrong sentiment predictions.")

    # Fetch predictions
    r = requests.get(f"{BASE}/active_learning/get", params={"email": st.session_state.email})
    if not r.ok:
        st.error("Failed to fetch predictions")
        return

    data = r.json()
    if len(data) == 0:
        st.info("No predictions found. Do some Single or Batch analysis first!")
        return

    df = pd.DataFrame(data)

    

    # Show filtered table
    st.subheader("📊 Model Predictions")
    st.dataframe(df, use_container_width=True)

    st.write("---")
    st.subheader("🔧 Correct Predictions")
    # --------------------------------------------
    # 🔍 SEARCH BAR — filter by sentence or aspect
    # --------------------------------------------
    st.write("### 🔎 Search your predictions")
    search = st.text_input(
        "Search by sentence or aspect",
        placeholder="Type: battery, camera, delivery, speed..."
    )

    if search.strip():
        df = df[
            df["sentence"].str.contains(search, case=False, na=False) |
            df["aspect"].str.contains(search, case=False, na=False)
        ]

        st.success(f"Found {len(df)} matching results")

        if len(df) == 0:
            return
    # -------------------------------------------------
    # Sentiment Correction Loop (same as before)
    # -------------------------------------------------
    for idx, row in df.iterrows():
        st.markdown(f"### ➤ Sentence: `{row['sentence']}`")
        st.markdown(f"**Aspect:** {row['aspect']}")
        st.markdown(f"**Original Sentiment:** {row['overall_sentiment']} ({row['overall_score']*100:.1f}%)")

        corrected = st.selectbox(
            f"Correct sentiment for: {row['aspect']}",
            ["Positive", "Neutral", "Negative"],
            index=["Positive", "Neutral", "Negative"].index(row["overall_sentiment"]),
            key=f"correct_{idx}"
        )

        if st.button(f"Save Correction #{idx}", key=f"save_correct_{idx}"):
            payload = {
                "email": st.session_state.email,
                "sentence": row['sentence'],
                "aspect": row['aspect'],
                "original_sentiment": row['aspect_sentiment'],
                "original_score": row['aspect_score'],
                "corrected_sentiment": corrected
            }

            res = requests.post(f"{BASE}/active_learning/save", data=payload)

            if res.ok:
                st.success(f"Correction saved for aspect: {row['aspect']}")
            else:
                st.error("Failed to save correction")



def admin_dashboard_page():
    st.markdown("<div class='neon-title'>🛠️ Admin Control Panel</div>", unsafe_allow_html=True)
    st.caption("This dashboard is visible only to platform administrators.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["👥 User Management", "📊 Global Sentiment Analytics", 
         "🎯 Active Learning Corrections", "📁 Dataset Explorer", "📝 System Logs"]
    )

    # -----------------------------------
    # 👥 USER MANAGEMENT
    # -----------------------------------
    with tab1:
        st.subheader("Registered Users")

        users = requests.get(f"{BASE}/admin/users")
        if users.ok:
            df_users = pd.DataFrame(users.json())
            search_user = st.text_input("Search users by email/name")

            if search_user:
                df_users = df_users[
                    df_users["email"].str.contains(search_user, case=False) |
                    df_users["full_name"].str.contains(search_user, case=False)
                ]

            st.dataframe(df_users, use_container_width=True)

            # Delete user
            del_email = st.text_input("Enter email to delete user")
            if st.button("Delete User"):
                res = requests.delete(f"{BASE}/admin/delete_user?email={del_email}")
                if res.ok:
                    st.success(f"User {del_email} removed.")
                else:
                    st.error("Failed to delete user")
        else:
            st.error("Failed to load users")

    # -----------------------------------
    # 📊 GLOBAL SENTIMENT ANALYTICS
    # -----------------------------------
    with tab2:
        st.subheader("Platform-wide Sentiment Metrics")

        stats = requests.get(f"{BASE}/admin/global_stats")
        if stats.ok:
            data = stats.json()

            c1, c2, c3 = st.columns(3)
            c1.metric("Total Users", data.get("total_users", 0))
            c2.metric("Total Predictions", data.get("total_predictions", 0))
            c3.metric("Total Corrections", data.get("total_corrections", 0))

            df_all = pd.DataFrame(data["records"])

            pie = px.pie(df_all, names="sentiment", title="Overall Sentiment Split")
            st.plotly_chart(pie, use_container_width=True)

            if "aspect" in df_all:
                bar = px.bar(df_all, x="aspect", title="Most Common Aspects")
                st.plotly_chart(bar, use_container_width=True)

            csv = df_all.to_csv().encode("utf-8")
            st.download_button("Download Full Dataset", csv, "platform_data.csv")

        else:
            st.error("Unable to fetch analytics")

    # -----------------------------------
    # 🎯 ACTIVE LEARNING PANEL
    # -----------------------------------
    with tab3:
        st.subheader("Active Learning – User Corrections")

        cli = requests.get(f"{BASE}/admin/all_corrections")
        if cli.ok:
            df_corr = pd.DataFrame(cli.json())
            st.dataframe(df_corr, use_container_width=True)

            csv = df_corr.to_csv(index=False).encode("utf-8")
            st.download_button("Download Corrections", csv, "active_learning_corrections.csv")
        else:
            st.error("Failed to fetch corrections")

    # -----------------------------------
    # 📁 DATASET EXPLORER
    # -----------------------------------
    with tab4:
        st.subheader("Uploaded Datasets")

        files = requests.get(f"{BASE}/admin/list_datasets")
        if files.ok:
            df_files = pd.DataFrame(files.json())
            st.dataframe(df_files, use_container_width=True)
        else:
            st.error("Could not load dataset info")

    # -----------------------------------
    # 📝 LOGS
    # -----------------------------------
    with tab5:
        st.subheader("System Logs")

        # Filters
        colA, colB = st.columns(2)
        limit = colA.number_input("Max Records", min_value=20, max_value=1000, value=200)
        search_logs = colB.text_input("Search logs...", placeholder="email, route, action, timestamp...")

        # Fetch logs from backend
        logs = requests.get(f"{BASE}/logs/all", params={"limit": limit})

        if logs.ok:
            logs_data = logs.json()

            if len(logs_data) == 0:
                st.info("No log records found in database.")
                return

            df_logs = pd.DataFrame(logs_data)

            # Apply search filter
            if search_logs.strip():
                df_logs = df_logs[
                    df_logs.apply(
                        lambda row: row.astype(str).str.contains(search_logs, case=False, na=False),
                        axis=1
                    )
                ]

                st.success(f"🔍 Found {len(df_logs)} matching log records")

                if len(df_logs) == 0:
                    return

            # Display the logs table
            st.dataframe(df_logs, use_container_width=True)

            # Download logs
            csv = df_logs.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇ Download Logs CSV",
                csv,
                "system_logs.csv",
                "text/csv"
            )

            st.write("---")
            st.subheader("📌 Recent Log Activity Timeline")

            # Timeline (latest 40 logs only)
            df_time = df_logs.head(40) if len(df_logs) > 40 else df_logs

            for _, row in df_time.iterrows():
                st.markdown(
                    f"""
                    <div style='padding:10px;margin-bottom:6px;border-left:3px solid {ACCENT};background:#1a1a1a;border-radius:6px'>
                        <b>{row['timestamp']}</b><br>
                        👤 <b>User:</b> {row.get('email','-')}<br>
                        🛠 <b>Route:</b> {row.get('route','-')}<br>
                        🎯 <b>Action:</b> {row.get('action','-')}<br>
                        ✍ <b>Message:</b> {row.get('message','-')}<br>
                        🧩 <b>Payload:</b> <code>{row.get('payload','')}</code>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:
            st.error("❌ Failed to load logs from backend")


# -------------------------------------------------
# ROUTING
# -------------------------------------------------

# ---------------- SIDEBAR NAV ----------------
if st.session_state.email is None:

    if st.session_state.reset_mode:
        reset_password_page()

    screen = st.sidebar.radio("Menu", ["Sign In", "Sign Up", "Forgot Password"])

    if screen == "Sign In":
        login_page()
    elif screen == "Sign Up":
        signup_page()
    else:
        forgot_password_page()

else:
    # LOGGED IN
    if st.session_state.email == "admin@springboard.com":
        screen = st.sidebar.radio("Menu", [
            "Profile",
            "Single Review Analysis",
            "Batch Analysis",
            "Active Learning",
            "Admin Dashboard",
            "Logout"
        ])
    else:
        screen = st.sidebar.radio("Menu", [
            "Profile",
            "Single Review Analysis",
            "Batch Analysis",
            "Active Learning",
            "Logout"
        ])

    if screen == "Profile":
        profile_page()
    elif screen == "Single Review Analysis":
        single_sentiment_page()
    elif screen == "Batch Analysis":
        batch_sentiment_page()
    elif screen == "Active Learning":
        active_learning_page()
    elif screen == "Admin Dashboard":
        admin_dashboard_page()
    elif screen == "Logout":
        st.session_state.email = None
        st.rerun()
