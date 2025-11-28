# Network Log Analyzer

A professional, enterprise-grade web application for analyzing network log files. Built with **FastAPI** (Backend) and **Streamlit** (Frontend).

![Logo](frontend/logo.png)

## Features

-   **File Upload**: Support for `.log` and `.txt` files (up to 200MB).
-   **Automated Analysis**: Instantly detects and categorizes log entries.
-   **Visual Highlighting**:
    -   ❌ **Errors**: Highlighted in light red.
    -   ⚠️ **Warnings**: Highlighted in light blue.
-   **Enterprise UI**:
    -   Dashboard with key metrics (Total Lines, Errors, Warnings).
    -   Sidebar for easy navigation and file management.
    -   Polished, responsive design.
-   **Sample Data**: Includes a built-in option to test with sample syslog data.

## Tech Stack

-   **Backend**: Python, FastAPI
-   **Frontend**: Streamlit
-   **Data Processing**: Python (Standard Library)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rmudumbai/networkanalysis.git
    cd networkanalysis
    ```

2.  **Set up the backend:**
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    
    You need two terminal windows.

    **Terminal 1 (Backend):**
    ```bash
    cd backend
    source venv/bin/activate
    uvicorn main:app --reload --port 8000
    ```

    **Terminal 2 (Frontend):**
    ```bash
    source backend/venv/bin/activate
    streamlit run frontend/app.py
    ```

4.  **Access the App:**
    Open your browser and navigate to `http://localhost:8501`.

## Usage

1.  Upload a log file using the sidebar uploader.
2.  Or click "Load Sample Data" to see a demo.
3.  View the analyzed logs with color-coded highlighting.
4.  Filter logs by type (Error, Warning, Normal) using the multi-select tool.

## License

MIT
