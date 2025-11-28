import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Network Log Analyzer", layout="wide", page_icon="🛡️")

# Custom CSS for Clean Professional Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500&display=swap');
    
    :root {
        --primary: #0052cc; /* Professional Blue */
        --bg-main: #f4f5f7;
        --bg-card: #ffffff;
        --text-main: #172b4d;
        --text-sub: #5e6c84;
        --border: #dfe1e6;
    }

    /* Global Reset */
    .stApp {
        background-color: var(--bg-main);
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
    }
    
    /* Main Layout */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Headers */
    h1 {
        font-weight: 600;
        color: var(--text-main);
        font-size: 2rem;
        margin-bottom: 0.5rem;
        letter-spacing: -0.01em;
    }
    
    h3 {
        font-weight: 600;
        color: var(--text-main);
        font-size: 1.1rem;
        margin-bottom: 0.75rem;
    }
    
    /* Cards */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 4px; /* Sharper corners for pro look */
        padding: 1.25rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: var(--text-main);
    }
    
    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-sub);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Log Viewer - Clean Terminal */
    .log-container {
        background-color: #091e42; /* Dark Navy */
        border-radius: 4px;
        border: 1px solid #091e42;
        margin-top: 1.5rem;
        font-family: 'Roboto Mono', monospace;
        overflow: hidden;
    }
    
    .log-header {
        background-color: #172b4d;
        padding: 8px 16px;
        border-bottom: 1px solid #253858;
        color: #b3bac5;
        font-size: 0.75rem;
        font-weight: 500;
        display: flex;
        align-items: center;
    }
    
    .log-content {
        max-height: 600px;
        overflow-y: auto;
        padding: 0.5rem 0;
    }
    
    .log-line {
        padding: 4px 16px;
        font-size: 0.8rem;
        line-height: 1.5;
        color: #ebecf0;
        border-left: 3px solid transparent;
    }
    
    .log-line:hover {
        background-color: rgba(255,255,255,0.05);
    }
    
    .log-error {
        background-color: rgba(222, 53, 11, 0.15);
        border-left-color: #de350b;
        color: #ffbdad;
    }
    
    .log-warning {
        background-color: rgba(255, 153, 31, 0.15);
        border-left-color: #ff991f;
        color: #fffae6;
    }
    
    /* Right Panel */
    [data-testid="column"]:nth-of-type(2) {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 1.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    /* Buttons */
    .stButton > button {
        background-color: var(--primary);
        color: white;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 3px;
        border: none;
        transition: background 0.1s;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #0047b3;
        box-shadow: none;
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        background-color: #fafbfc;
        border: 2px solid #dfe1e6;
        border-radius: 3px;
        color: var(--text-main);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        background-color: #fff;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: #fafbfc;
        border: 2px dashed #dfe1e6;
        border-radius: 4px;
        padding: 1.5rem;
    }
    
    /* Hide default sidebar */
    [data-testid="stSidebar"] { display: none; }
    
</style>
""", unsafe_allow_html=True)

import os
import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Initialize Session State
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'llm_provider': 'Gemini',
        'api_key': '',
        'gcp_project_id': ''
    }

# Admin Configuration
ADMIN_EMAILS = ["admin@example.com", "mohanr@google.com", "rmudumbai@gmail.com", "mohanraman1000@gmail.com"] # Add your email here for testing

# Navigation Functions
def go_to_settings():
    st.session_state.current_page = 'settings'

def go_to_home():
    st.session_state.current_page = 'home'

def login_with_google():
    # Check for client_secret.json
    if not os.path.exists("client_secret.json"):
        st.error("client_secret.json not found. Please upload it below.")
        return

    try:
        # Validate credential type
        import json
        with open("client_secret.json", "r") as f:
            secret_data = json.load(f)
        
        if 'web' in secret_data:
            st.error("⚠️ Configuration Error")
            st.warning("""
            You uploaded a **Web Application** credential.
            
            Please go to Google Cloud Console and create a **Desktop App** credential instead.
            1. Go to APIs & Services > Credentials
            2. Create Credentials > OAuth client ID
            3. Application type: **Desktop app**
            4. Download the JSON and upload it here.
            """)
            return
            
        if 'installed' not in secret_data:
            st.error("Invalid client_secret.json format. Unknown client type.")
            return

        # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'])

        # Launch the flow in the browser
        # Note: This works for localhost. For production, you'd need a different flow.
        # Allow HTTP for local testing
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        creds = flow.run_local_server(port=0)
        
        # Get user info
        from googleapiclient.discovery import build
        service = build('oauth2', 'v2', credentials=creds)
        user_info = service.userinfo().get().execute()
        email = user_info['email']
        
        st.session_state.user_email = email
        if email in ADMIN_EMAILS:
            st.session_state.is_admin = True
            st.success(f"Logged in as Admin: {email}")
        else:
            st.session_state.is_admin = False
            st.warning(f"Logged in as User: {email} (No Admin Access)")
            
    except Exception as e:
        st.error(f"Login failed: {str(e)}")

def logout():
    st.session_state.user_email = None
    st.session_state.is_admin = False
    st.session_state.current_page = 'home'

# --- Settings Page ---
def render_settings_page():
    st.markdown("### ⚙️ Admin Settings")
    st.markdown("---")
    
    if not st.session_state.is_admin:
        st.error("Access Denied. You must be an admin to view this page.")
        if st.button("Back to Home"):
            go_to_home()
            st.rerun()
        return

    with st.form("settings_form"):
        st.subheader("LLM Configuration")
        llm_provider = st.selectbox(
            "LLM Provider", 
            ["Gemini", "Vertex AI", "OpenAI"], 
            index=["Gemini", "Vertex AI", "OpenAI"].index(st.session_state.settings.get('llm_provider', 'Gemini'))
        )
        
        api_key = st.text_input(
            "API Key", 
            value=st.session_state.settings.get('api_key', ''), 
            type="password",
            help="Enter the API Key for the selected provider"
        )
        
        st.subheader("Google Cloud Configuration")
        gcp_project = st.text_input(
            "GCP Project ID", 
            value=st.session_state.settings.get('gcp_project_id', ''),
            help="Required for Vertex AI and GCS integration"
        )
        
        if st.form_submit_button("Save Settings"):
            st.session_state.settings['llm_provider'] = llm_provider
            st.session_state.settings['api_key'] = api_key
            st.session_state.settings['gcp_project_id'] = gcp_project
            st.success("Settings Saved Successfully!")

    if st.button("Back to Home"):
        go_to_home()
        st.rerun()

# --- Home Page ---
def render_home_page():
    # Main Layout: Left (Content) and Right (Controls & Chat)
    left_col, right_col = st.columns([3, 1])

    with left_col:
        st.title("Network Log Analyzer")
        st.markdown("Enterprise-grade log analysis and anomaly detection.")

    # --- Right Column: Control Panel ---
    with right_col:
        # Admin Settings Button (Top Right)
        if st.session_state.user_email and st.session_state.is_admin:
            if st.button("⚙️ Admin Settings", use_container_width=True):
                go_to_settings()
                st.rerun()
        
        st.markdown("### Control Panel")
        
        # Auth Section
        if st.session_state.user_email:
            st.success(f"👤 {st.session_state.user_email}")
            if st.button("Sign Out", use_container_width=True):
                logout()
                st.rerun()
        else:
            # Check for client_secret.json
            if not os.path.exists("client_secret.json"):
                st.warning("OAuth Config Missing")
                uploaded_secret = st.file_uploader("Upload client_secret.json", type=["json"], key="secret_uploader")
                if uploaded_secret:
                    with open("client_secret.json", "wb") as f:
                        f.write(uploaded_secret.getbuffer())
                    st.success("Config uploaded! Reloading...")
                    st.rerun()
            else:
                if st.button("Sign in with Google", use_container_width=True):
                    login_with_google()
                    st.rerun()
                
                if st.button("Reset OAuth Config", help="Click to upload a new client_secret.json"):
                    if os.path.exists("client_secret.json"):
                        os.remove("client_secret.json")
                        st.rerun()
        
        st.markdown("---")
        
        # File Upload Section
        uploaded_file = st.file_uploader("Upload Log File", type=["log", "txt"])
        
        with st.expander("Advanced Options"):
            if st.button("Load Sample Data", use_container_width=True):
                st.session_state['use_sample'] = True
            
            st.markdown("---")
            st.markdown("**Import from GCS**")
            gcs_bucket = st.text_input("Bucket Name", placeholder="my-log-bucket")
            gcs_blob = st.text_input("File Path", placeholder="logs/syslog.log")
            if st.button("Load from GCS", use_container_width=True):
                if gcs_bucket and gcs_blob:
                     st.session_state['use_gcs'] = True
                     st.session_state['gcs_bucket'] = gcs_bucket
                     st.session_state['gcs_blob'] = gcs_blob
                else:
                    st.error("Please provide both Bucket Name and File Path.")

    # --- Logic to handle file source ---
    files = None
    json_data = None
    api_url = "http://localhost:8000/analyze"

    if uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file, "text/plain")}
    elif st.session_state.get('use_sample'):
        try:
            f = open("sample_syslog.log", "rb")
            files = {"file": ("sample_syslog.log", f, "text/plain")}
        except FileNotFoundError:
            st.error("Sample file not found.")
    elif st.session_state.get('use_gcs'):
        api_url = "http://localhost:8000/analyze-gcs"
        json_data = {
            "bucket_name": st.session_state['gcs_bucket'],
            "blob_name": st.session_state['gcs_blob']
        }

    # --- Processing & Display ---
    if files or json_data:
        with st.spinner("Processing logs..."):
            try:
                # Reset file pointer if it's a reused file object
                if files and 'f' in locals() and not f.closed:
                    f.seek(0)
                
                if files:
                    response = requests.post(api_url, files=files)
                else:
                    response = requests.post(api_url, json=json_data)
                
                if files and 'f' in locals() and not f.closed:
                    f.close()
                    
                if response.status_code == 200:
                    logs = response.json()
                    st.session_state.analyzed_logs = logs
                    
                    # --- Left Column: Analysis Results ---
                    with left_col:
                        # Metrics
                        total_logs = len(logs)
                        errors = sum(1 for l in logs if l['type'] == 'error')
                        warnings = sum(1 for l in logs if l['type'] == 'warning')
                        
                        m_col1, m_col2, m_col3 = st.columns(3)
                        with m_col1:
                            st.markdown(f"""<div class="metric-card"><div class="metric-value">{total_logs}</div><div class="metric-label">Total Lines</div></div>""", unsafe_allow_html=True)
                        with m_col2:
                            st.markdown(f"""<div class="metric-card"><div class="metric-value" style="color: #c53030;">{errors}</div><div class="metric-label">Errors</div></div>""", unsafe_allow_html=True)
                        with m_col3:
                            st.markdown(f"""<div class="metric-card"><div class="metric-value" style="color: #2b6cb0;">{warnings}</div><div class="metric-label">Warnings</div></div>""", unsafe_allow_html=True)
                        
                        st.markdown("### Analysis Results")
                        
                        # Filter controls
                        filter_type = st.multiselect("Filter by Type", ["error", "warning", "normal"], default=["error", "warning", "normal"])
                        
                        # Log Display
                        st.markdown("""
                        <div class="log-container">
                            <div class="log-header">
                                <span>analysis_output.log</span>
                            </div>
                            <div class="log-content">
                        """, unsafe_allow_html=True)
                        
                        # Limit display for performance
                        display_limit = 1000
                        count = 0
                        
                        for log in logs:
                            if log['type'] in filter_type:
                                if count < display_limit:
                                    line_content = log["content"]
                                    line_type = log["type"]
                                    
                                    css_class = "log-normal"
                                    if line_type == "error":
                                        css_class = "log-error"
                                    elif line_type == "warning":
                                        css_class = "log-warning"
                                        
                                    st.markdown(f'<div class="log-line {css_class}">{line_content}</div>', unsafe_allow_html=True)
                                    count += 1
                                else:
                                    st.markdown(f'<div class="log-line log-normal">... and {len(logs) - display_limit} more lines hidden for performance ...</div>', unsafe_allow_html=True)
                                    break
                                    
                        st.markdown('</div></div>', unsafe_allow_html=True)
                    
                    # --- Right Column: Chatbot (Stacked below controls) ---
                    with right_col:
                        st.markdown("---")
                        st.markdown("### 🤖 Log Assistant")
                        
                        # Use global settings for API Key
                        gemini_api_key = st.session_state.settings.get('api_key')
                        
                        if not gemini_api_key:
                            st.info("Enter your Gemini API Key in Settings to enable the chatbot.")
                        else:
                            # Display chat messages
                            chat_container = st.container(height=400)
                            with chat_container:
                                for message in st.session_state.messages:
                                    with st.chat_message(message["role"]):
                                        st.markdown(message["content"])
                            
                            # Chat input
                            if prompt := st.chat_input("Ask about the logs..."):
                                # Add user message
                                st.session_state.messages.append({"role": "user", "content": prompt})
                                
                                # Prepare context from logs
                                log_context = "\n".join([f"{l['type'].upper()}: {l['content']}" for l in logs[:100]])  # Limit to first 100 lines
                                
                                # Call Gemini
                                try:
                                    import google.generativeai as genai
                                    genai.configure(api_key=gemini_api_key)
                                    model = genai.GenerativeModel('gemini-pro')
                                    
                                    full_prompt = f"""You are a network log analysis assistant. Here are the analyzed logs:

{log_context}

User question: {prompt}

Please provide a concise and helpful answer based on the log data."""
                                    
                                    response = model.generate_content(full_prompt)
                                    assistant_message = response.text
                                    
                                    # Add assistant message
                                    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                                    
                                    # Rerun to display new messages
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Chatbot error: {str(e)}")
                
                else:
                    st.error(f"Analysis failed with status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        with left_col:
            st.info("Please upload a log file or load sample data from the Control Panel to begin analysis.")

# Main App Logic
if st.session_state.current_page == 'settings':
    render_settings_page()
else:
    render_home_page()

