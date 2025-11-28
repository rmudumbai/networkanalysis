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
    
    /* Toolbar */
    .toolbar-container {
        background-color: var(--bg-card);
        border-bottom: 1px solid var(--border);
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
    }
    
    .toolbar-btn {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: none;
        border: none;
        cursor: pointer;
        color: var(--text-sub);
        padding: 0.5rem;
        border-radius: 4px;
        transition: all 0.2s;
    }
    
    .toolbar-btn:hover {
        background-color: #ebecf0;
        color: var(--primary);
    }
    
    .toolbar-icon {
        font-size: 1.5rem;
        margin-bottom: 0.25rem;
    }
    
    .toolbar-label {
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    /* Action Area */
    .action-area {
        background-color: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        animation: slideDown 0.3s ease-out;
    }
    
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
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
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--bg-card);
        border-right: 1px solid var(--border);
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
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 4, 2])
    
    with col1:
        if st.button("📂 Upload", use_container_width=True, type="primary" if st.session_state.active_tab == 'upload' else "secondary"):
            st.session_state.active_tab = 'upload'
            st.rerun()
            
    with col2:
        if st.button("☁️ GCS", use_container_width=True, type="primary" if st.session_state.active_tab == 'gcs' else "secondary"):
            st.session_state.active_tab = 'gcs'
            st.rerun()
            
    with col3:
        if st.button("📊 Sample", use_container_width=True, type="primary" if st.session_state.active_tab == 'sample' else "secondary"):
            st.session_state.active_tab = 'sample'
            st.session_state['use_sample'] = True # Trigger load immediately
            st.rerun()

    with col4:
        # Admin Settings
        if st.session_state.user_email and st.session_state.is_admin:
            if st.button("⚙️ Settings", use_container_width=True):
                go_to_settings()
                st.rerun()
    
    with col6:
        # Auth Status
        if st.session_state.user_email:
            st.caption(f"Signed in as: {st.session_state.user_email}")
            if st.button("Sign Out", key="logout_btn"):
                logout()
                st.rerun()
        else:
            if st.button("Sign in with Google", key="login_btn"):
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

