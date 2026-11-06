## Voice Listener

> [!warning] Deprecated Architecture  
> This component is no longer part of the active architecture.
> 
> It is preserved for historical reference and for developers who may wish to study, adapt, or reintroduce the pattern in their own implementations.
> 

---

zpp_id: voice_listener
schema_version: zpp.entropy.char.nfc.v1
lineage_tracking: zpp-core-mainnet
status: 🔒 ARCHITECT_LOCKED
timestamp: 2026-05

---

```python

#!/usr/bin/env python3
"""
voice_listener.py
ZPP Phase 5 Local Agent Tool - Offline Speech-to-Text Engine
"""

import os
import sys
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import whisper
from datetime import datetime

def record_audio(duration: int = 5, sample_rate: int = 16000) -> str:
    """Records audio from the local microphone for a set duration."""
    print(f"🎙️ [Listening] Speak now... ({duration} seconds remaining)")
    
    # Record audio as float32 array
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()  # Wait until the recording is finished
    
    # Convert to 16-bit PCM integer format for standard WAV compatibility
    audio_int16 = (recording * 32767).astype(np.int16)
    
    temp_wav_path = "/Users/<LOCAL_USER>/vault/agent-workspace/temp_voice_input.wav"
    wav.write(temp_wav_path, sample_rate, audio_int16)
    return temp_wav_path

def transcribe_audio(audio_path: str) -> str:
    """Transcribes local WAV audio using a lightweight offline Whisper model."""
    print("📡 Processing speech-to-text locally...")
    try:
        # Utilizing the 'tiny' or 'base' model keeps execution incredibly fast offline
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_path, fp16=False)
        spoken_text = result.get("text", "").strip()
        return spoken_text
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"
    finally:
        # Clean up the temporary audio file after processing
        if os.path.exists(audio_path):
            os.remove(audio_path)

def listen_and_return():
    """Main wrapper function to execute full audio cycle."""
    # 5 seconds is usually perfect for a brief agent command
    temp_file = record_audio(duration=5)
    text_output = transcribe_audio(temp_file)
    return text_output

if __name__ == "__main__":
    captured_text = listen_and_return()
    print(f"\n📝 Transcribed Text: {captured_text}")

```