import streamlit as st
import requests
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Document Verifier",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Neon Theme ---
css = """
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
body { background-color: #000000; color: #ffffff; font-family: 'Roboto Mono', monospace; }
.stApp { background-color: #000000; }
h1, h2, h3, h4, h5, h6 { color: #ffffff; text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff; }
.stButton>button { color: #000000; background: #00ffff; border: 2px solid #00ffff; border-radius: 10px; padding: 15px 30px; font-size: 1.2rem; font-weight: 700; box-shadow: 0 0 15px #00ffff, 0 0 25px #00ffff; transition: all 0.3s ease; }
.stButton>button:hover { box-shadow: 0 0 25px #00ffff, 0 0 45px #00ffff; transform: scale(1.05); }
.stFileUploader { border: 3px dashed #00ff00; border-radius: 15px; padding: 2rem; text-align: center; background: rgba(0, 255, 0, 0.05); }
.stFileUploader label { font-size: 1.5rem; color: #00ff00; text-shadow: 0 0 5px #00ff00; }
.metric-card { border-radius: 15px; padding: 20px; text-align: center; background: #1a1a1a; box-shadow: 0 0 10px rgba(255, 255, 255, 0.1); }
.metric-card-total { border: 2px solid #00ff00; box-shadow: 0 0 15px #00ff00; }
.metric-card-verified { border: 2px solid #00ffff; box-shadow: 0 0 15px #00ffff; }
.metric-card-suspicious { border: 2px solid #ff00ff; box-shadow: 0 0 15px #ff00ff; }
.metric-card-time { border: 2px solid #ffff00; box-shadow: 0 0 15px #ffff00; }
.metric-card .value { font-size: 2.5rem; font-weight: 700; }
.metric-card .label { font-size: 1rem; margin-top: 10px; }
"""
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'total_docs' not in st.session_state: st.session_state.total_docs = 0
if 'verified_docs' not in st.session_state: st.session_state.verified_docs = 0
if 'suspicious_docs' not in st.session_state: st.session_state.suspicious_docs = 0
if 'time_saved' not in st.session_state: st.session_state.time_saved = 0.0
if 'last_result' not in st.session_state: st.session_state.last_result = None

# --- UI Layout ---
st.markdown("<h1 style='text-align: center;'>AI Document Verifier</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffff;'>Black + Neon Dashboard</p>", unsafe_allow_html=True)

main_container = st.container()
with main_container:
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown("---")
        uploaded_file = st.file_uploader("Drag & Drop Certificate or click to upload", type=["jpg", "jpeg", "png"])
        st.markdown("---")
        verify_button_pressed = st.button("Verify Document", use_container_width=True)

# --- Handle Verify Button ---
if verify_button_pressed and uploaded_file is not None:
    with st.spinner('Analyzing document... Backend is at work!'):
        start_time = time.time()
        try:
            # Send file to backend API
            files = {"file": uploaded_file.getvalue()}
            res = requests.post("http://127.0.0.1:8000/verify", files=files)
            data = res.json()

            # Store result
            st.session_state.last_result = {
                "status": data["status"],
                "reasons": " | ".join(data["reasons"]),
                "hash": data["hash"],
                "filename": uploaded_file.name
            }

            # Update stats
            st.session_state.total_docs += 1
            if data["status"] == 'Verified':
                st.session_state.verified_docs += 1
            else:
                st.session_state.suspicious_docs += 1

        except Exception as e:
            st.session_state.last_result = {
                "status": "Error",
                "reasons": str(e),
                "filename": uploaded_file.name
            }

        end_time = time.time()
        time_saved_this_doc = 120.0 - (end_time - start_time)  # Simulate 2 mins saved
        st.session_state.time_saved += max(0, time_saved_this_doc) / 60.0

elif verify_button_pressed and uploaded_file is None:
    st.warning("Please upload a document before verifying.")

# --- Display Verification Result ---
if st.session_state.last_result:
    res = st.session_state.last_result
    st.subheader("Verification Result")
    status = res.get('status', 'Unknown')
    if status == 'Verified': st.success(f"**Status: {status}**")
    elif status == 'Error': st.error(f"**Status: {status}**")
    else: st.warning(f"**Status: {status}**")
    st.write(f"**File:** `{res.get('filename', 'N/A')}`")
    st.write(f"**Reasons:** {res.get('reasons', 'No details provided.')}")
    st.code(f"Document Hash (SHA256): {res.get('hash', 'N/A')}", language=None)

st.markdown("---")
st.subheader("Automation Metrics")

# --- Metric Cards ---
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f'<div class="metric-card metric-card-total"><div class="value">{st.session_state.total_docs}</div><div class="label">Total Docs</div></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric-card metric-card-verified"><div class="value">{st.session_state.verified_docs}</div><div class="label">Verified</div></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="metric-card metric-card-suspicious"><div class="value">{st.session_state.suspicious_docs}</div><div class="label">Suspicious</div></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="metric-card metric-card-time"><div class="value">{st.session_state.time_saved:.1f} min</div><div class="label">Time Saved</div></div>', unsafe_allow_html=True)
