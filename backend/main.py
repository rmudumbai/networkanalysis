from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_log(file: UploadFile = File(...)):
    content = await file.read()
    decoded_content = content.decode("utf-8", errors="replace")
    lines = decoded_content.splitlines()
    
    analyzed_lines = []
    for line in lines:
        line_lower = line.lower()
        line_type = "normal"
        
        if any(keyword in line_lower for keyword in ["error", "fail", "critical", "issue"]):
            line_type = "error"
        elif "warn" in line_lower:
            line_type = "warning"
            
        analyzed_lines.append({
            "content": line,
            "type": line_type
        })
        
    return analyzed_lines

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
