import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Network Log Analyzer", layout="wide", page_icon="🛡️")

# Custom CSS for Enterprise Look
st.markdown("""
<style>
    /* Main Background and Font */
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        background-color: #ffffff;
        padding: 1.5rem;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        display: flex;
        align_items: center;
    }
    
    /* Log Line Styling */
    .log-container {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 0;
        margin-top: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        overflow: hidden;
    }
    
    .log-line {
        padding: 8px 16px;
        border-bottom: 1px solid #f0f0f0;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
    }
    
    .log-line:last-child {
        border-bottom: none;
    }
    
    .log-error {
        background-color: #fff5f5;
        color: #c53030;
        border-left: 4px solid #c53030;
    }
    
    .log-warning {
        background-color: #ebf8ff;
        color: #2b6cb0;
        border-left: 4px solid #2b6cb0;
    }
    
    .log-normal {
        background-color: #ffffff;
        color: #4a5568;
        border-left: 4px solid #cbd5e0;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2d3748;
    }
    .metric-label {
        color: #718096;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("frontend/logo.png", width=150)
    st.markdown("### Control Panel")
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Upload Log File", type=["log", "txt"])
    
    st.markdown("---")
    st.markdown("### Quick Actions")
    if st.button("Load Sample Data", use_container_width=True):
        st.session_state['use_sample'] = True
    
    st.markdown("---")
    st.info("Supported formats: .log, .txt\n\nMax file size: 200MB")

# Main Content
st.title("Network Log Analyzer")
st.markdown("Enterprise-grade log analysis and anomaly detection.")

# Logic to handle file source
files = None
if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, "text/plain")}
elif st.session_state.get('use_sample'):
    try:
        f = open("sample_syslog.log", "rb")
        files = {"file": ("sample_syslog.log", f, "text/plain")}
    except FileNotFoundError:
        st.error("Sample file not found.")

if files:
    with st.spinner("Processing logs..."):
        try:
            # Reset file pointer if it's a reused file object (not needed for requests usually but good practice)
            if 'f' in locals() and not f.closed:
                f.seek(0)
                
            response = requests.post("http://localhost:8000/analyze", files=files)
            
            if 'f' in locals() and not f.closed:
                f.close()
                
            if response.status_code == 200:
                logs = response.json()
                
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
                
                # Limit display for performance if too many logs
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
                
            else:
                st.error(f"Analysis failed with status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please upload a log file or load sample data to begin analysis.")

