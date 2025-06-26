from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import whisper
import uvicorn
import os
import tempfile
import ssl

# Disable SSL verification (if needed)
ssl._create_default_https_context = ssl._create_unverified_context

# Load Whisper model
model = whisper.load_model("base")

# Create FastAPI app
app = FastAPI()

# Authentication dependency
security = HTTPBearer()
API_TOKEN = "myjayatoken123"  # Ganti token sesuai kebutuhan

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )

# Transcribe endpoint with token protection
@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(verify_token)
):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
        temp_audio.write(await file.read())
        temp_audio_path = temp_audio.name

    result = model.transcribe(temp_audio_path)
    os.remove(temp_audio_path)

    return {"text": result["text"]}
