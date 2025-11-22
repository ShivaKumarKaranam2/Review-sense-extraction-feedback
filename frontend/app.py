# import streamlit as st
# import pandas as pd
# import requests
# import plotly.express as px
# from io import BytesIO

# # ----------------------------------------------
# # CONFIG
# # ----------------------------------------------
# BASE = "http://127.0.0.1:8000"

# st.set_page_config(
#     page_title="Infosys ReviewSense",
#     layout="wide"
# )

# ACCENT = "#00A8FF"  # Neon blue

# # ----------------------------------------------
# # GLOBAL CSS (Glassmorphic UI)
# # ----------------------------------------------
# st.markdown(
#     f"""
#     <style>

#         /* Background */
#         body {{
#             background: linear-gradient(135deg, #0A0A0A, #1A1A1A);
#             color: white;
#             font-family: 'Segoe UI';
#         }}

#         .block-container {{
#             padding-top: 2rem;
#         }}

#         .glass-card {{
#             background: rgba(255,255,255,0.06);
#             padding: 25px;
#             border-radius: 15px;
#             border: 1px solid rgba(255,255,255,0.12);
#             backdrop-filter: blur(12px);
#             margin-bottom: 25px;
#         }}

#         .neon-title {{
#             font-size: 36px;
#             font-weight: 900;
#             color: {ACCENT};
#             margin-bottom: 15px;
#             text-shadow: 0 0 12px {ACCENT};
#         }}

#         /* Buttons */
#         .stButton>button {{
#             background-color: {ACCENT} !important;
#             color: white !important;
#             padding: 8px 18px;
#             border-radius: 6px;
#             border: none;
#             font-weight: 600;
#         }}

#         .stButton>button:hover {{
#             background-color: #0077cc !important;
#             transform: scale(1.03);
#         }}

#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # -------------------------------------------------
# # SESSION STATE
# # -------------------------------------------------
# if "email" not in st.session_state:
#     st.session_state.email = None
# if "reset_mode" not in st.session_state:
#     st.session_state.reset_mode = False


# # -------------------------------------------------
# # AUTH PAGES
# # -------------------------------------------------
# def signup_page():
#     st.markdown("<div class='neon-title'>Create Your Account</div>", unsafe_allow_html=True)

#     with st.form("signup_form"):
#         email = st.text_input("Email", key="su_email")
#         pwd = st.text_input("Password", type="password", key="su_pwd")
#         fullname = st.text_input("Full Name", key="su_full")
#         age = st.number_input("Age", min_value=0, key="su_age")
#         bio = st.text_area("Bio", key="su_bio")

#         if st.form_submit_button("Sign Up"):
#             payload = {
#                 "email": email,
#                 "password": pwd,
#                 "full_name": fullname,
#                 "age": age if age > 0 else None,
#                 "bio": bio
#             }
#             r = requests.post(f"{BASE}/signup", json=payload)
#             if r.status_code == 200:
#                 st.success("🎉 Account created! Please sign in.")
#             else:
#                 st.error(r.json().get("detail", "Signup failed"))


# def login_page():
#     st.markdown("<div class='neon-title'>Welcome Back</div>", unsafe_allow_html=True)

#     with st.form("login_form"):
#         email = st.text_input("Email", key="li_email")
#         pwd = st.text_input("Password", type="password", key="li_pwd")

#         col1, col2 = st.columns(2)

#         if col1.form_submit_button("Sign In"):
#             r = requests.post(f"{BASE}/login", json={"email": email, "password": pwd})
#             if r.status_code == 200:
#                 st.session_state.email = email
#                 st.rerun()
#             else:
#                 st.error(r.json().get("detail", "Login failed"))

#         if col2.form_submit_button("Forgot Password?"):
#             st.session_state.reset_mode = True
#             st.rerun()


# def forgot_password_page():
#     st.markdown("<div class='neon-title'>Forgot Password</div>", unsafe_allow_html=True)

#     with st.form("fp_form"):
#         email = st.text_input("Registered email", key="fp_mail")

#         if st.form_submit_button("Send Reset Token"):
#             r = requests.post(f"{BASE}/forgot-password", json={"email": email})
#             st.success("Reset token created! Check backend logs.")


# def reset_password_page():
#     st.markdown("<div class='neon-title'>Reset Password</div>", unsafe_allow_html=True)

#     with st.form("reset_form"):
#         email = st.text_input("Email", key="rp_email")
#         token = st.text_input("Reset Token", key="rp_token")
#         newpass = st.text_input("New Password", type="password", key="rp_new")

#         if st.form_submit_button("Update Password"):
#             r = requests.post(
#                 f"{BASE}/reset-password",
#                 json={"email": email, "token": token, "new_password": newpass},
#             )
#             if r.status_code == 200:
#                 st.success("Password updated! Please login.")
#                 st.session_state.reset_mode = False
#             else:
#                 st.error("Reset failed")


# # -------------------------------------------------
# # PROFILE + DASHBOARD
# # -------------------------------------------------
# def profile_page():
#     st.markdown("<div class='neon-title'>My Profile</div>", unsafe_allow_html=True)

#     email = st.session_state.email

#     # Fetch profile
#     prof = requests.get(f"{BASE}/profile", params={"email": email})
#     if not prof.ok:
#         st.error("Failed to load profile")
#         return

#     user = prof.json()

#     # -------- Profile Form --------
#     with st.form("profile_form"):
#         full = st.text_input("Full Name", value=user.get("full_name", ""), key="pf_full")
#         age = st.number_input("Age", min_value=0, value=user.get("age", 0), key="pf_age")
#         bio = st.text_area("Bio", value=user.get("bio", ""), key="pf_bio")

#         if st.form_submit_button("Update Profile"):
#             payload = {"email": email, "full_name": full, "age": age, "bio": bio}
#             r = requests.put(f"{BASE}/update_profile", json=payload)
#             if r.ok:
#                 st.success("Profile updated.")
#             else:
#                 st.error("Failed to update.")

#     # -------- User Stats --------
#     st.write("___")
#     st.markdown("<div class='neon-title'>Your Sentiment Dashboard</div>", unsafe_allow_html=True)

#     stats = requests.get(f"{BASE}/user_stats", params={"email": email})

#     if not stats.ok:
#         st.error("Failed to load sentiment stats.")
#         return

#     data = stats.json()

#     if data["total_records"] == 0:
#         st.info("No analysis records found yet.")
#         return

#     df = pd.DataFrame(data["records"])
#     st.dataframe(df, use_container_width=True)

#     # Sentiment summary
#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Total Reviews", data["total_records"])
#     col2.metric("Positive", sum(df["Overall Sentiment"] == "Positive"))
#     col3.metric("Neutral", sum(df["Overall Sentiment"] == "Neutral"))
#     col4.metric("Negative", sum(df["Overall Sentiment"] == "Negative"))

#     # Charts
#     pie = px.pie(df, names="Aspect Sentiment", title="Aspect Sentiment Distribution")
#     st.plotly_chart(pie, use_container_width=True)

#     bar = px.bar(df, x="Aspect", y="Aspect Score", color="Aspect Sentiment")
#     st.plotly_chart(bar, use_container_width=True)

#     # Download CSV
#     csv = df.to_csv(index=False).encode("utf-8")
#     st.download_button("Download CSV", csv, "sentiment_records.csv", "text/csv")


# # -------------------------------------------------
# # SINGLE REVIEW ANALYSIS
# # -------------------------------------------------
# def single_sentiment_page():
#     st.markdown("<div class='neon-title'>Single Review Analysis</div>", unsafe_allow_html=True)

#     with st.form("single_form"):
#         text = st.text_area("Enter review text", key="single_txt")

#         if st.form_submit_button("Analyze"):
#             if not text.strip():
#                 st.warning("Enter review text")
#                 return

#             payload = {"email": st.session_state.email, "text": text}
#             r = requests.post(f"{BASE}/sentiment/predict_single", data=payload)

#             if not r.ok:
#                 st.error("Prediction failed")
#                 return

#             result = r.json()
#             st.success("Analysis complete!")

#             # Convert to table
#             df = pd.DataFrame(result["aspects"])
#             st.dataframe(df, use_container_width=True)

#             # Overall Sentiment Bar
#             bar = px.bar(
#                 x=["Positive", "Neutral", "Negative"],
#                 y=[
#                     result["overall_score"] if result["overall_sentiment"] == "Positive" else 0,
#                     result["overall_score"] if result["overall_sentiment"] == "Neutral" else 0,
#                     result["overall_score"] if result["overall_sentiment"] == "Negative" else 0,
#                 ],
#                 title="Overall Sentiment Strength"
#             )
#             st.plotly_chart(bar, use_container_width=True)

#             # Aspect Pie
#             pie = px.pie(df, names="aspect_sentiment", title="Aspect Sentiment Split")
#             st.plotly_chart(pie, use_container_width=True)


# # -------------------------------------------------
# # BATCH ANALYSIS
# # -------------------------------------------------

# def batch_sentiment_page():
#     st.markdown("<div class='neon-title'>Batch Review Analysis</div>", unsafe_allow_html=True)

#     file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

#     if file:
#         df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
#         st.dataframe(df.head(), use_container_width=True)

#         column = st.selectbox("Select Review Text Column", df.columns)

#         if st.button("Run Batch Analysis"):
#             files = {
#                 "file": (file.name, file.getvalue(), file.type)
#             }

#             data = {
#                 "email": st.session_state.email,
#                 "text_column": column
#             }

#             # MUST use correct route
#             r = requests.post(f"{BASE}/sentiment/predict_batch", files=files, data=data)

#             if not r.ok:
#                 st.error(f"Batch failed: {r.text}")
#                 return

#             out = r.json()
#             df_out = pd.DataFrame(out["results"])
#             st.success("Batch Completed Successfully!")
#             st.dataframe(df_out, use_container_width=True)

#             # Charts
#             pie = px.pie(df_out, names="Aspect Sentiment", title="Aspect Sentiment Distribution")
#             st.plotly_chart(pie, use_container_width=True)

#             bar = px.bar(df_out, x="Aspect", y="Aspect Score", color="Aspect Sentiment")
#             st.plotly_chart(bar, use_container_width=True)

#             # Download
#             csv = df_out.to_csv(index=False).encode("utf-8")
#             st.download_button("Download CSV", csv, "batch_results.csv", "text/csv")


# # -------------------------------------------------
# # ROUTING
# # -------------------------------------------------
# if st.session_state.email is None:

#     if st.session_state.reset_mode:
#         reset_password_page()

#     else:
#         screen = st.sidebar.radio("Menu", ["Sign In", "Sign Up", "Forgot Password"])

#         if screen == "Sign In":
#             login_page()
#         elif screen == "Sign Up":
#             signup_page()
#         else:
#             forgot_password_page()

# else:
#     screen = st.sidebar.radio("Menu", ["Profile", "Single Review Analysis", "Batch Analysis", "Logout"])

#     if screen == "Profile":
#         profile_page()
#     elif screen == "Single Review Analysis":
#         single_sentiment_page()
#     elif screen == "Batch Analysis":
#         batch_sentiment_page()
#     elif screen == "Logout":
#         st.session_state.email = None
#         st.rerun()

import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

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


# -------------------------------------------------
# ROUTING
# -------------------------------------------------
if st.session_state.email is None:

    if st.session_state.reset_mode:
        reset_password_page()
    else:
        screen = st.sidebar.radio("Menu", ["Sign In", "Sign Up", "Forgot Password"])

        if screen == "Sign In":
            login_page()
        elif screen == "Sign Up":
            signup_page()
        else:
            forgot_password_page()

else:
    screen = st.sidebar.radio("Menu", [
        "Profile",
        "Single Review Analysis",
        "Batch Analysis",
        "Logout"
    ])

    if screen == "Profile":
        profile_page()
    elif screen == "Single Review Analysis":
        single_sentiment_page()
    elif screen == "Batch Analysis":
        batch_sentiment_page()
    elif screen == "Logout":
        st.session_state.email = None
        st.rerun()
