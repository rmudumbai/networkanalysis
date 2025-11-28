import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Network Log Analyzer", layout="wide", page_icon="🛡️")

# Custom CSS for Enterprise Professional Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    
    :root {
        --primary: #1e3a8a; /* Deep Professional Blue */
        --primary-hover: #1e40af;
        --accent: #3b82f6;
        --success: #059669;
        --warning: #d97706;
        --error: #dc2626;
        --bg-main: #f8fafc;
        --bg-card: #ffffff;
        --bg-elevated: #fafbfc;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-tertiary: #94a3b8;
        --border-light: #e2e8f0;
        --border-medium: #cbd5e1;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    /* Global Reset */
    .stApp {
        background: linear-gradient(to bottom, #f8fafc 0%, #f1f5f9 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Main Layout */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    
    /* Typography Hierarchy */
    h1 {
        font-weight: 700;
        color: var(--text-primary);
        font-size: 2.25rem;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
        line-height: 1.2;
    }
    
    h2 {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 1.5rem;
        margin-bottom: 1rem;
        letter-spacing: -0.015em;
    }
    
    h3 {
        font-weight: 600;
        color: var(--text-secondary);
        font-size: 1.125rem;
        margin-bottom: 0.75rem;
        letter-spacing: -0.01em;
    }
    
    p, .stMarkdown {
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Top Bar */
    .top-bar {
        background: linear-gradient(135deg, var(--primary) 0%, #1e40af 100%);
        padding: 0.75rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: var(--shadow-md);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Metric Cards - Enhanced */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-light);
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent), var(--primary));
        opacity: 0;
        transition: opacity 0.2s ease;
    }
    
    .metric-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
        border-color: var(--border-medium);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        margin-bottom: 0.5rem;
        font-variant-numeric: tabular-nums;
    }
    
    .metric-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-tertiary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    
    /* Log Viewer - Professional Terminal */
    .log-container {
        background-color: #0f172a;
        border-radius: 8px;
        border: 1px solid #1e293b;
        margin-top: 2rem;
        font-family: 'JetBrains Mono', 'Roboto Mono', monospace;
        overflow: hidden;
        box-shadow: var(--shadow-lg);
    }
    
    .log-header {
        background: linear-gradient(to bottom, #1e293b, #0f172a);
        padding: 0.75rem 1.25rem;
        border-bottom: 1px solid #334155;
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .log-content {
        max-height: 650px;
        overflow-y: auto;
        padding: 0.75rem 0;
        background-color: #0f172a;
    }
    
    .log-content::-webkit-scrollbar {
        width: 8px;
    }
    
    .log-content::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    .log-content::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    .log-content::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    
    .log-line {
        padding: 0.375rem 1.25rem;
        font-size: 0.85rem;
        line-height: 1.6;
        color: #e2e8f0;
        border-left: 3px solid transparent;
        transition: background-color 0.1s ease;
        font-variant-ligatures: none;
    }
    
    .log-line:hover {
        background-color: rgba(51, 65, 85, 0.3);
    }
    
    .log-error {
        background-color: rgba(220, 38, 38, 0.1);
        border-left-color: var(--error);
        color: #fca5a5;
    }
    
    .log-warning {
        background-color: rgba(217, 119, 6, 0.1);
        border-left-color: var(--warning);
        color: #fcd34d;
    }
    
    /* Buttons - Enhanced */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--primary-hover));
        color: white;
        font-weight: 600;
        padding: 0.625rem 1.25rem;
        border-radius: 6px;
        border: none;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
        width: 100%;
        font-size: 0.875rem;
        letter-spacing: 0.01em;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
        background: linear-gradient(135deg, var(--primary-hover), var(--primary));
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Secondary Buttons */
    .stButton > button[kind="secondary"] {
        background: var(--bg-elevated);
        color: var(--text-secondary);
        border: 1px solid var(--border-medium);
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: white;
        border-color: var(--primary);
        color: var(--primary);
    }
    
    /* Inputs - Refined */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        background-color: var(--bg-card);
        border: 1.5px solid var(--border-light);
        border-radius: 6px;
        color: var(--text-primary);
        padding: 0.625rem 0.875rem;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1);
        background-color: white;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: var(--bg-elevated);
        border: 2px dashed var(--border-medium);
        border-radius: 8px;
        padding: 2rem;
        transition: all 0.2s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary);
        background-color: rgba(30, 58, 138, 0.02);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #ffffff, #f8fafc);
        border-right: 1px solid var(--border-light);
        box-shadow: var(--shadow-sm);
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        border-radius: 6px;
    }
    
    /* Info/Warning/Error boxes */
    .stAlert {
        border-radius: 6px;
        border-left-width: 4px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: var(--text-secondary);
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
        st.image("frontend/network_analyze_banner.jpg", width=400)
    
    with col1:
        if st.button("📂", help="Upload File", use_container_width=True, type="primary" if st.session_state.active_tab == 'upload' else "secondary"):
            st.session_state.active_tab = 'upload'
            st.rerun()
            
    with col2:
        if st.button("☁️", help="Import from GCS", use_container_width=True, type="primary" if st.session_state.active_tab == 'gcs' else "secondary"):
            st.session_state.active_tab = 'gcs'
            st.rerun()
            
    with col3:
        if st.button("📊", help="Load Sample Data", use_container_width=True, type="primary" if st.session_state.active_tab == 'sample' else "secondary"):
            st.session_state.active_tab = 'sample'
            st.session_state['use_sample'] = True # Trigger load immediately
            st.rerun()

    with col4:
        # Admin Settings
        if st.session_state.user_email and st.session_state.is_admin:
            if st.button("⚙️", help="Admin Settings", use_container_width=True):
                go_to_settings()
                st.rerun()
        else:
            # Empty placeholder to maintain layout
            st.write("")
    
    with col5:
        # Auth Status - Use icon for both states
        if st.session_state.user_email:
            if st.button("🚪", help=f"Sign Out ({st.session_state.user_email})", key="logout_btn", use_container_width=True):
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

