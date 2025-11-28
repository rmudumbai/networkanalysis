import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Network Log Analyzer", layout="wide", page_icon="🛡️")

# Custom CSS for Enterprise Material Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main Background */
    .stApp {
        background-color: #f5f7fa;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    
    /* Header Styling */
    h1 {
        color: #1e293b;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    h3 {
        color: #334155;
        font-weight: 600;
    }
    
    /* Log Container */
    .log-container {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0;
        margin-top: 1.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        overflow: hidden;
    }
    
    /* Log Lines */
    .log-line {
        padding: 12px 20px;
        border-bottom: 1px solid #f1f5f9;
        font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
        font-size: 0.875rem;
        display: flex;
        align-items: center;
        transition: background-color 0.15s ease;
    }
    
    .log-line:hover {
        background-color: #f8fafc;
    }
    
    .log-line:last-child {
        border-bottom: none;
    }
    
    .log-error {
        background-color: #fef2f2;
        color: #991b1b;
        border-left: 3px solid #dc2626;
    }
    
    .log-error:hover {
        background-color: #fee2e2;
    }
    
    .log-warning {
        background-color: #eff6ff;
        color: #1e40af;
        border-left: 3px solid #3b82f6;
    }
    
    .log-warning:hover {
        background-color: #dbeafe;
    }
    
    .log-normal {
        background-color: #ffffff;
        color: #475569;
        border-left: 3px solid #e2e8f0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #1e293b;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        border-color: #cbd5e1;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #0f172a;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .stButton > button:hover {
        background-color: #1e293b;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 6px;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
        font-size: 0.875rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Chat Container */
    [data-testid="stChatMessageContainer"] {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 1.5rem;
        border: 2px dashed #cbd5e1;
        transition: all 0.2s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #94a3b8;
        background-color: #f1f5f9;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        border-radius: 6px;
        border: 1px solid #e2e8f0;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 6px;
        border-left: 3px solid #3b82f6;
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
ADMIN_EMAILS = ["admin@example.com", "mohanr@google.com"] # Add your email here for testing

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
        # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'])

        # Launch the flow in the browser
        # Note: This works for localhost. For production, you'd need a different flow.
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
    # Header with Admin Controls
    col1, col2 = st.columns([6, 1])
    with col1:
        st.title("Network Log Analyzer")
    with col2:
        if st.session_state.user_email and st.session_state.is_admin:
            if st.button("⚙️", help="Admin Settings"):
                go_to_settings()
                st.rerun()

    # Sidebar
    with st.sidebar:
        st.image("frontend/logo.png", width=150)
        st.markdown("### Control Panel")
        st.markdown("---")
        
        # Auth Status
        if st.session_state.user_email:
            st.success(f"Signed in as: {st.session_state.user_email}")
            if st.button("Sign Out", use_container_width=True):
                logout()
                st.rerun()
        else:
            st.markdown("#### Admin Access")
            
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
        
        st.markdown("---")
        
        uploaded_file = st.file_uploader("Upload Log File", type=["log", "txt"])
        
        st.markdown("---")
        st.markdown("### Quick Actions")
        if st.button("Load Sample Data", use_container_width=True):
            st.session_state['use_sample'] = True
        
        st.markdown("---")
        st.markdown("### Import from GCS")
        gcs_bucket = st.text_input("Bucket Name", placeholder="e.g., my-log-bucket")
        gcs_blob = st.text_input("File Path", placeholder="e.g., logs/syslog.log")
        if st.button("Load from GCS", use_container_width=True):
            if gcs_bucket and gcs_blob:
                 st.session_state['use_gcs'] = True
                 st.session_state['gcs_bucket'] = gcs_bucket
                 st.session_state['gcs_blob'] = gcs_blob
            else:
                st.error("Please provide both Bucket Name and File Path.")
        
        st.markdown("---")
        st.info("Supported formats: .log, .txt\n\nMax file size: 200MB")

    # Main Content
    st.markdown("Enterprise-grade log analysis and anomaly detection.")

    # Initialize session state for chat
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'analyzed_logs' not in st.session_state:
        st.session_state.analyzed_logs = None

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
                    
                    # Create two columns: logs on left, chatbot on right
                    log_col, chat_col = st.columns([2, 1])
                    
                    with log_col:
                        # Metrics
                        total_logs = len(logs)
                        errors = sum(1 for l in logs if l['type'] == 'error')
                        warnings = sum(1 for l in logs if l['type'] == 'warning')
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"""<div class="metric-card"><div class="metric-value">{total_logs}</div><div class="metric-label">Total Lines</div></div>""", unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"""<div class="metric-card"><div class="metric-value" style="color: #c53030;">{errors}</div><div class="metric-label">Errors</div></div>""", unsafe_allow_html=True)
                        with col3:
                            st.markdown(f"""<div class="metric-card"><div class="metric-value" style="color: #2b6cb0;">{warnings}</div><div class="metric-label">Warnings</div></div>""", unsafe_allow_html=True)
                        
                        st.markdown("### Analysis Results")
                        
                        # Filter controls
                        filter_type = st.multiselect("Filter by Type", ["error", "warning", "normal"], default=["error", "warning", "normal"])
                        
                        # Log Display
                        st.markdown('<div class="log-container">', unsafe_allow_html=True)
                        
                        # Limit display for performance
                        display_limit = 1000
                        count = 0
                        
                        for log in logs:
                            if log['type'] in filter_type:
                                if count < display_limit:
                                    line_content = log["content"]
                                    line_type = log["type"]
                                    
                                    css_class = "log-normal"
                                    icon = "📝"
                                    if line_type == "error":
                                        css_class = "log-error"
                                        icon = "❌"
                                    elif line_type == "warning":
                                        css_class = "log-warning"
                                        icon = "⚠️"
                                        
                                    st.markdown(f'<div class="log-line {css_class}"><span style="margin-right: 10px;">{icon}</span> {line_content}</div>', unsafe_allow_html=True)
                                    count += 1
                                else:
                                    st.markdown(f'<div class="log-line log-normal">... and {len(logs) - display_limit} more lines hidden for performance ...</div>', unsafe_allow_html=True)
                                    break
                                    
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with chat_col:
                        st.markdown("### 🤖 Log Assistant")
                        
                        # Use global settings for API Key
                        gemini_api_key = st.session_state.settings.get('api_key')
                        
                        if not gemini_api_key:
                            st.warning("⚠️ API Key not configured.")
                            st.info("Please ask an Admin to configure the API Key in Settings.")
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
        st.info("Please upload a log file or load sample data to begin analysis.")

# Main App Logic
if st.session_state.current_page == 'settings':
    render_settings_page()
else:
    render_home_page()

