import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Network Log Analyzer", layout="wide", page_icon="🛡️")

# Custom CSS for Material Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    :root {
        /* Material Design Color Palette */
        --md-primary: #1976d2;
        --md-primary-dark: #1565c0;
        --md-primary-light: #42a5f5;
        --md-secondary: #424242;
        --md-error: #d32f2f;
        --md-warning: #f57c00;
        --md-success: #388e3c;
        --md-info: #0288d1;
        
        /* Surfaces */
        --md-surface: #ffffff;
        --md-background: #fafafa;
        --md-surface-variant: #f5f5f5;
        
        /* Text */
        --md-text-primary: rgba(0, 0, 0, 0.87);
        --md-text-secondary: rgba(0, 0, 0, 0.60);
        --md-text-disabled: rgba(0, 0, 0, 0.38);
        
        /* Elevation Shadows (Material Design) */
        --md-elevation-1: 0px 2px 1px -1px rgba(0,0,0,0.2), 0px 1px 1px 0px rgba(0,0,0,0.14), 0px 1px 3px 0px rgba(0,0,0,0.12);
        --md-elevation-2: 0px 3px 1px -2px rgba(0,0,0,0.2), 0px 2px 2px 0px rgba(0,0,0,0.14), 0px 1px 5px 0px rgba(0,0,0,0.12);
        --md-elevation-3: 0px 3px 3px -2px rgba(0,0,0,0.2), 0px 3px 4px 0px rgba(0,0,0,0.14), 0px 1px 8px 0px rgba(0,0,0,0.12);
        --md-elevation-4: 0px 2px 4px -1px rgba(0,0,0,0.2), 0px 4px 5px 0px rgba(0,0,0,0.14), 0px 1px 10px 0px rgba(0,0,0,0.12);
        --md-elevation-8: 0px 5px 5px -3px rgba(0,0,0,0.2), 0px 8px 10px 1px rgba(0,0,0,0.14), 0px 3px 14px 2px rgba(0,0,0,0.12);
        
        /* 4px Spacing Scale */
        --spacing-1: 4px;
        --spacing-2: 8px;
        --spacing-3: 12px;
        --spacing-4: 16px;
        --spacing-5: 20px;
        --spacing-6: 24px;
        --spacing-7: 28px;
        --spacing-8: 32px;
        --spacing-10: 40px;
        --spacing-12: 48px;
    }

    /* Global Reset */
    .stApp {
        background-color: var(--md-background);
        font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--md-text-primary);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Main Layout */
    .main .block-container {
        padding-top: var(--spacing-4);
        padding-bottom: var(--spacing-8);
        max-width: 1440px;
    }
    
    /* Typography - Material Design */
    h1 {
        font-family: 'Roboto', sans-serif;
        font-weight: 300;
        font-size: 2.125rem;
        line-height: 1.235;
        letter-spacing: -0.00833em;
        color: var(--md-text-primary);
        margin-bottom: var(--spacing-4);
    }
    
    h2 {
        font-family: 'Roboto', sans-serif;
        font-weight: 400;
        font-size: 1.5rem;
        line-height: 1.334;
        letter-spacing: 0em;
        color: var(--md-text-primary);
        margin-bottom: var(--spacing-4);
    }
    
    h3 {
        font-family: 'Roboto', sans-serif;
        font-weight: 500;
        font-size: 1.25rem;
        line-height: 1.6;
        letter-spacing: 0.0075em;
        color: var(--md-text-primary);
        margin-bottom: var(--spacing-3);
    }
    
    p, .stMarkdown {
        font-family: 'Roboto', sans-serif;
        font-weight: 400;
        font-size: 1rem;
        line-height: 1.5;
        letter-spacing: 0.00938em;
        color: var(--md-text-secondary);
    }
    
    /* Material Design Cards */
    .metric-card {
        background: var(--md-surface);
        border-radius: 4px;
        padding: var(--spacing-4);
        box-shadow: var(--md-elevation-2);
        transition: box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        box-shadow: var(--md-elevation-4);
    }
    
    .metric-value {
        font-family: 'Roboto', sans-serif;
        font-size: 2.125rem;
        font-weight: 400;
        line-height: 1.235;
        color: var(--md-text-primary);
        margin-bottom: var(--spacing-2);
    }
    
    .metric-label {
        font-family: 'Roboto', sans-serif;
        font-size: 0.875rem;
        font-weight: 500;
        line-height: 1.57;
        letter-spacing: 0.00714em;
        color: var(--md-text-secondary);
        text-transform: uppercase;
    }
    
    /* Log Viewer - Material Design */
    .log-container {
        background-color: #263238;
        border-radius: 4px;
        margin-top: var(--spacing-6);
        font-family: 'Roboto Mono', monospace;
        overflow: hidden;
        box-shadow: var(--md-elevation-3);
    }
    
    .log-header {
        background-color: #37474f;
        padding: var(--spacing-3) var(--spacing-4);
        border-bottom: 1px solid #455a64;
        color: rgba(255, 255, 255, 0.87);
        font-size: 0.875rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .log-content {
        max-height: 600px;
        overflow-y: auto;
        padding: var(--spacing-2) 0;
        background-color: #263238;
    }
    
    .log-content::-webkit-scrollbar {
        width: 8px;
    }
    
    .log-content::-webkit-scrollbar-track {
        background: #37474f;
    }
    
    .log-content::-webkit-scrollbar-thumb {
        background: #546e7a;
        border-radius: 4px;
    }
    
    .log-content::-webkit-scrollbar-thumb:hover {
        background: #607d8b;
    }
    
    .log-line {
        padding: var(--spacing-1) var(--spacing-4);
        font-size: 0.875rem;
        line-height: 1.5;
        color: rgba(255, 255, 255, 0.87);
        border-left: 3px solid transparent;
        transition: background-color 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .log-line:hover {
        background-color: rgba(255, 255, 255, 0.08);
    }
    
    .log-error {
        background-color: rgba(211, 47, 47, 0.12);
        border-left-color: var(--md-error);
        color: #ef5350;
    }
    
    .log-warning {
        background-color: rgba(245, 124, 0, 0.12);
        border-left-color: var(--md-warning);
        color: #ffa726;
    }
    
    /* Material Design Buttons */
    .stButton > button {
        background-color: var(--md-primary);
        color: white;
        font-family: 'Roboto', sans-serif;
        font-weight: 500;
        font-size: 0.875rem;
        line-height: 1.75;
        letter-spacing: 0.02857em;
        text-transform: uppercase;
        padding: var(--spacing-2) var(--spacing-4);
        border-radius: 4px;
        border: none;
        box-shadow: var(--md-elevation-2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: var(--md-primary-dark);
        box-shadow: var(--md-elevation-4);
    }
    
    .stButton > button:active {
        box-shadow: var(--md-elevation-8);
    }
    
    /* Secondary Buttons */
    .stButton > button[kind="secondary"] {
        background-color: transparent;
        color: var(--md-primary);
        border: 1px solid rgba(25, 118, 210, 0.5);
        box-shadow: none;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background-color: rgba(25, 118, 210, 0.04);
        border-color: var(--md-primary);
    }
    
    /* Material Design Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        background-color: transparent;
        border: none;
        border-bottom: 1px solid rgba(0, 0, 0, 0.42);
        border-radius: 4px 4px 0 0;
        background-color: rgba(0, 0, 0, 0.04);
        color: var(--md-text-primary);
        padding: var(--spacing-2) var(--spacing-3);
        font-family: 'Roboto', sans-serif;
        font-size: 1rem;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stTextInput > div > div > input:hover {
        background-color: rgba(0, 0, 0, 0.08);
        border-bottom-color: rgba(0, 0, 0, 0.87);
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        background-color: rgba(0, 0, 0, 0.09);
        border-bottom: 2px solid var(--md-primary);
        outline: none;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: var(--md-surface-variant);
        border: 2px dashed rgba(0, 0, 0, 0.38);
        border-radius: 4px;
        padding: var(--spacing-6);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--md-primary);
        background-color: rgba(25, 118, 210, 0.04);
    }
    
    /* Sidebar - Material Design */
    [data-testid="stSidebar"] {
        background: var(--md-surface);
        border-right: 1px solid rgba(0, 0, 0, 0.12);
        box-shadow: var(--md-elevation-1);
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        border-radius: 4px;
    }
    
    /* Alert Boxes */
    .stAlert {
        border-radius: 4px;
        border-left-width: 4px;
        padding: var(--spacing-4);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-family: 'Roboto', sans-serif;
        font-weight: 500;
        color: var(--md-text-primary);
        padding: var(--spacing-3) var(--spacing-4);
    }
    
    /* Material Design Divider */
    hr {
        border: none;
        border-top: 1px solid rgba(0, 0, 0, 0.12);
        margin: var(--spacing-4) 0;
    }
    
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
        
        # --- WEB APPLICATION FLOW (For Streamlit Cloud) ---
        if 'web' in secret_data:
            st.info("☁️ Cloud/Web Authentication Detected")
            
            # Get the redirect URI (App URL)
            # Try to get from secrets, or ask user
            redirect_uri = st.text_input(
                "Enter your App URL", 
                placeholder="https://your-app.streamlit.app",
                help="Copy the URL from your browser address bar. Ensure this URI is added to 'Authorized redirect URIs' in Google Cloud Console."
            )
            
            if redirect_uri:
                # Remove trailing slash if present
                if redirect_uri.endswith('/'):
                    redirect_uri = redirect_uri[:-1]
                    
                flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                    'client_secret.json',
                    scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
                    redirect_uri=redirect_uri
                )
                
                # Check for auth code in query params
                if 'code' in st.query_params:
                    code = st.query_params['code']
                    try:
                        flow.fetch_token(code=code)
                        creds = flow.credentials
                        
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
                            
                        # Clear query params to prevent re-use
                        st.query_params.clear()
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Authentication failed: {str(e)}")
                        st.query_params.clear()
                else:
                    # Generate Login Link
                    auth_url, _ = flow.authorization_url(prompt='consent')
                    st.link_button("Login with Google", auth_url, type="primary", use_container_width=True)
                    st.caption("Click above to sign in. You will be redirected back.")
            else:
                st.warning("Please enter your App URL to proceed.")
            return

        # --- DESKTOP APP FLOW (For Localhost) ---
        if 'installed' in secret_data:
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
        else:
             st.error("Invalid client_secret.json format. Unknown client type.")

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
    # Initialize UI state for toggles
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 'upload'  # Default to upload

    # --- Top Toolbar ---
    # Centered banner image with icons on the right
    col_left_spacer, col_banner, col_right_spacer, col1, col2, col3, col4, col5 = st.columns([1, 6, 1, 0.5, 0.5, 0.5, 0.5, 0.5])
    
    with col_banner:
        st.markdown("""
            <h1 style="
                font-family: 'Playfair Display', 'Georgia', serif;
                font-size: 2.5rem;
                font-weight: 700;
                background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-align: center;
                margin: 0;
                padding: 0.5rem 0;
                letter-spacing: 0.02em;
            ">Network Analyzeee</h1>
        """, unsafe_allow_html=True)
    
    with col1:
        if st.button("⬆", help="Upload File", use_container_width=True, type="primary" if st.session_state.active_tab == 'upload' else "secondary", key="btn_upload"):
            st.session_state.active_tab = 'upload'
            st.rerun()
            
    with col2:
        if st.button("☁", help="Import from GCS", use_container_width=True, type="primary" if st.session_state.active_tab == 'gcs' else "secondary", key="btn_gcs"):
            st.session_state.active_tab = 'gcs'
            st.rerun()
            
    with col3:
        if st.button("📊", help="Load Sample Data", use_container_width=True, type="primary" if st.session_state.active_tab == 'sample' else "secondary", key="btn_sample"):
            st.session_state.active_tab = 'sample'
            st.session_state['use_sample'] = True # Trigger load immediately
            st.rerun()

    with col4:
        # Admin Settings
        if st.session_state.user_email and st.session_state.is_admin:
            if st.button("⚙", help="Admin Settings", use_container_width=True, key="btn_settings"):
                go_to_settings()
                st.rerun()
        else:
            # Empty placeholder to maintain layout
            st.write("")
    
    with col5:
        # Auth Status - Use icon for both states
        if st.session_state.user_email:
            if st.button("⎋", help=f"Sign Out ({st.session_state.user_email})", key="logout_btn", use_container_width=True):
                logout()
                st.rerun()
        else:
            if st.button("👤", help="Sign In with Google", key="login_btn", type="primary", use_container_width=True):
                st.session_state.active_tab = 'auth'
                st.rerun()

    st.markdown("---")

    # --- Action Area (Dynamic Content) ---
    uploaded_file = None
    
    if st.session_state.active_tab == 'upload':
        st.markdown("### 📂 Upload Log File")
        uploaded_file = st.file_uploader("Select a .log or .txt file", type=["log", "txt"])
        
    elif st.session_state.active_tab == 'gcs':
        st.markdown("### ☁️ Import from Google Cloud Storage")
        c1, c2, c3 = st.columns([3, 3, 1])
        with c1:
            gcs_bucket = st.text_input("Bucket Name", placeholder="my-log-bucket")
        with c2:
            gcs_blob = st.text_input("File Path", placeholder="logs/syslog.log")
        with c3:
            st.write("") # Spacer
            st.write("")
            if st.button("Load", use_container_width=True):
                if gcs_bucket and gcs_blob:
                     st.session_state['use_gcs'] = True
                     st.session_state['gcs_bucket'] = gcs_bucket
                     st.session_state['gcs_blob'] = gcs_blob
                else:
                    st.error("Missing fields")
                    
    elif st.session_state.active_tab == 'auth':
        st.markdown("### 🔐 Authentication")
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
            if st.button("Login with Google", key="auth_login_btn"):
                login_with_google()
                st.rerun()
            
            if st.button("Reset OAuth Config", help="Click to upload a new client_secret.json"):
                if os.path.exists("client_secret.json"):
                    os.remove("client_secret.json")
                    st.rerun()

    # --- Main Content: Log Analysis ---
    st.title("Network Log Analyzer")
    st.markdown("Enterprise-grade log analysis and anomaly detection.")

    # Logic to handle file source
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
                
                else:
                    st.error(f"Analysis failed with status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Please select an action from the top menu to begin.")

    # --- Sidebar: Chatbot ---
    with st.sidebar:
        st.markdown("### 🤖 Log Assistant")
        
        # Use global settings for API Key
        gemini_api_key = st.session_state.settings.get('api_key')
        
        if not gemini_api_key:
            st.info("Enter your Gemini API Key in Settings to enable the chatbot.")
        else:
            # Display chat messages
            chat_container = st.container(height=500)
            with chat_container:
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
            
            # Chat input
            if prompt := st.chat_input("Ask about the logs..."):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Prepare context from logs
                log_context = ""
                if st.session_state.analyzed_logs:
                     log_context = "\n".join([f"{l['type'].upper()}: {l['content']}" for l in st.session_state.analyzed_logs[:100]])
                
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

# Main App Logic
if st.session_state.current_page == 'settings':
    render_settings_page()
else:
    render_home_page()

