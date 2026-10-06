import os
import requests
import pyttsx3

OUTPUT_DIR = "Cluster08-Advanced-Multimedia-AI/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. ELEVENLABS VOICE CLONING / SYNTHESIS (Cloud Mode)
# -------------------------------------------------------------
def clone_voice_elevenlabs(text, voice_id="21m00Tcm4TlvDq8ikWAM", api_key=None):
    """
    Synthesizes speech using ElevenLabs API.
    Default voice_id is 'Rachel' (standard pre-made voice).
    To use an Instant Voice Clone, replace voice_id with your cloned voice ID.
    """
    if not api_key:
        api_key = os.getenv("ELEVENLABS_API_KEY")

    if not api_key:
        print("[!] No ElevenLabs API Key provided. Switching to Offline Synthesizer...")
        return False

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    print("[*] Requesting speech synthesis from ElevenLabs API...")
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        out_path = os.path.join(OUTPUT_DIR, "elevenlabs_output.mp3")
        with open(out_path, "wb") as f:
            f.write(response.content)
        print(f"[+] Successfully generated ElevenLabs audio: {out_path}")
        return True
    else:
        print(f"[!] ElevenLabs API Error ({response.status_code}): {response.text}")
        return False

# -------------------------------------------------------------
# 2. LOCAL OFFLINE SYNTHESIS / VOICE EMULATION (Zero-API Fallback)
# -------------------------------------------------------------
def synthesize_speech_local(text, output_file="local_speech_output.wav"):
    out_path = os.path.join(OUTPUT_DIR, output_file)
    print("[*] Initializing local speech engine...")
    engine = pyttsx3.init()
    
    # Adjust speech rate and volume
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    
    # Select available voice
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
    
    engine.save_to_file(text, out_path)
    engine.runAndWait()
    print(f"[+] Successfully generated local audio output: {out_path}")
    return out_path

if __name__ == "__main__":
    sample_text = (
        "Welcome to the Multimedia Systems Laboratory. "
        "This is an automated speech synthesis and voice demonstration."
    )
    
    # If you have an ElevenLabs key, paste it here:
    USER_API_KEY = ""

    success = False
    if USER_API_KEY:
        success = clone_voice_elevenlabs(sample_text, api_key=USER_API_KEY)
    
    if not success:
        synthesize_speech_local(sample_text)
