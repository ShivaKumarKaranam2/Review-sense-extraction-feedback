import streamlit as st
import requests
import pandas as pd

BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Sentiment Portal", layout="centered")
st.title("🧠 Sentiment Analysis Portal")

if "email" not in st.session_state:
    st.session_state["email"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# --- Authentication ---
if not st.session_state["email"]:
    st.subheader("Welcome to Sentiment Portal")
    menu = ["Sign Up", "Sign In"]
    choice = st.selectbox("Menu", menu)

    if choice == "Sign Up":
        st.subheader("Create an Account")
        email = st.text_input("Email")
        pwd = st.text_input("Password", type="password")
        full = st.text_input("Full Name (optional)")
        age = st.number_input("Age (optional)", min_value=0, value=0)
        bio = st.text_area("Bio (optional)")

        if st.button("Create Account"):
            payload = {
                "email": email,
                "password": pwd,
                "full_name": full,
                "age": age if age > 0 else None,
                "bio": bio
            }
            r = requests.post(f"{BASE}/signup", json=payload)
            if r.status_code == 200:
                st.success("✅ Account created — please Sign In")
            else:
                try:
                    st.error(r.json().get("detail", "Error creating account"))
                except Exception:
                    st.error("⚠️ Unexpected error during signup")

    elif choice == "Sign In":
        st.subheader("🔐 Sign In")
        email = st.text_input("Email")
        pwd = st.text_input("Password", type="password")

        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("Sign In"):
                if not email or not pwd:
                    st.warning("Please enter both email and password.")
                else:
                    try:
                        r = requests.post(f"{BASE}/login", json={"email": email, "password": pwd})
                        if r.status_code == 200:
                            st.session_state["email"] = email
                            st.success("✅ Logged in successfully!")
                            st.rerun()
                        else:
                            st.error(r.json().get("detail", "Login failed"))
                    except Exception as e:
                        st.error(f"⚠️ Unexpected error during login: {e}")

        with col2:
            if st.button("Forgot Password?"):
                st.session_state["reset_mode"] = True
                st.rerun()

# --- Authenticated Section ---
else:
    menu = ["Profile", "Single Sentiment", "Batch Prediction", "Logout"]
    choice = st.sidebar.radio("Menu", menu)

    # --- Profile ---
    if choice == "Profile":
        st.subheader("👤 My Profile")
        email = st.session_state["email"]
        st.info(f"Logged in as: **{email}**")

        try:
            r = requests.get(f"{BASE}/profile", params={"email": email})
            if r.ok:
                user = r.json()
                full_name = st.text_input("Full Name", value=user.get("full_name", ""))
                age = st.number_input("Age", min_value=0, value=user.get("age", 0))
                bio = st.text_area("Bio", value=user.get("bio", ""))
            else:
                st.warning("Could not load profile info.")
                full_name, age, bio = "", 0, ""
        except Exception:
            full_name, age, bio = "", 0, ""

        if st.button("Update Profile"):
            payload = {"email": email, "full_name": full_name, "age": age, "bio": bio}
            r = requests.put(f"{BASE}/update_profile", json=payload)
            if r.ok:
                st.success("✅ Profile updated successfully")
            else:
                st.error(r.text)

    # --- Logout ---
    elif choice == "Logout":
        st.session_state["email"] = None
        st.session_state["chat_history"] = []
        st.success("👋 Logged out successfully!")
        st.rerun()

    # --- Single Sentiment ---
    elif choice == "Single Sentiment":
        st.subheader("🔍 Single Text Sentiment")
        text = st.text_area("Enter your text here")

        if st.button("Predict Sentiment"):
            if not text.strip():
                st.warning("Please enter some text.")
            else:
                data = {"email": st.session_state["email"], "text": text}
                r = requests.post(f"{BASE}/sentiment/predict_single", data=data)

                if r.ok:
                    out = r.json()
                    st.write("**🧹 Cleaned text:**", out["cleaned"])
                    st.write("**🏷️ Label:**", out["label"])
                    st.write("**📊 Score:**", round(out["score"], 3))
                else:
                    st.error(r.text)

    # --- Batch Prediction ---
    elif choice == "Batch Prediction":
        st.subheader("📂 Batch Sentiment Prediction")
        uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

        if uploaded_file is not None:
            try:
                # Read and preview uploaded file
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
                st.success("✅ File uploaded successfully!")
                st.dataframe(df.head(), use_container_width=True)

                # Ask user to select text column
                text_column = st.selectbox(
                    "Select the column containing the text for sentiment analysis:",
                    options=df.columns.tolist()
                )

                if st.button("Run Batch Prediction"):
                    if not text_column:
                        st.warning("Please select a valid text column.")
                    else:
                        with st.spinner("Running batch predictions..."):
                            files = {"file": uploaded_file.getvalue()}
                            data = {
                                "email": st.session_state["email"],
                                "text_column": text_column
                            }

                            try:
                                r = requests.post(f"{BASE}/sentiment/predict_batch", files=files, data=data)
                                if r.ok:
                                    result = r.json()
                                    st.success(result.get("message", "✅ Batch prediction completed!"))

                                    # ✅ Extract preview safely
                                    if "preview" in result and isinstance(result["preview"], list):
                                        df_result = pd.DataFrame(result["preview"])

                                        # ✅ Display clean table view without scrollbars
                                        st.markdown("### 🧾 Predicted Results")
                                        st.dataframe(df_result, use_container_width=True, hide_index=True)

                                    else:
                                        st.warning("No preview data returned from the server.")
                                else:
                                    st.error(r.text)

                            except Exception as e:
                                st.error(f"Error during batch prediction: {e}")

            except Exception as e:
                st.error(f"Error reading file: {e}")

    