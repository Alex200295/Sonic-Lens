import os
import tempfile
import warnings
import traceback
from fastapi import FastAPI, UploadFile, File, HTTPException
import librosa
import numpy as np

warnings.filterwarnings('ignore')

app = FastAPI(title="DSP Audio Analysis Service")

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_audio:
        content = await file.read()
        temp_audio.write(content)
        temp_audio_path = temp_audio.name

    try:
        # Load audio
        y, sr = librosa.load(temp_audio_path, sr=None)
        
        # 1. BPM / Tempo
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = float(tempo[0]) if isinstance(tempo, (np.ndarray, list)) else float(tempo)
        
        # 2. Duration
        duration = float(librosa.get_duration(y=y, sr=sr))
        
        # 3. Energy, Loudness, Dynamic Range
        rms = librosa.feature.rms(y=y)[0]
        rms_energy = float(np.mean(rms))
        
        db = librosa.amplitude_to_db(rms, ref=np.max)
        loudness = float(np.mean(db))
        dynamic_range = float(np.max(db) - np.min(db))
        
        # 4. Spectral Centroid
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_centroid = float(np.mean(cent))
        
        # 5. Pitch/Key Estimation
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        estimated_key_idx = int(np.argmax(chroma_mean))
        estimated_key = keys[estimated_key_idx]
        
        result = {
            "bpm": round(bpm, 2),
            "key": estimated_key,
            "loudness": round(loudness, 2),
            "dynamicRange": round(dynamic_range, 2),
            "rmsEnergy": round(rms_energy, 4),
            "spectralCentroid": round(spectral_centroid, 2),
            "duration": round(duration, 2),
            "status": "success",
            "method": "librosa_native"
        }
        return result

    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Analysis failed: {error_details}")
        raise HTTPException(status_code=500, detail=f"Native DSP analysis failed: {str(e)}")
    finally:
        # Clean up temp file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
