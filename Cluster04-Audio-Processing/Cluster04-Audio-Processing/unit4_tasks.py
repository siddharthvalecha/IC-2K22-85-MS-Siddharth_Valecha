import os
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.fft import rfft, rfftfreq

OUTPUT_DIR = "Cluster04-Audio-Processing/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. SYNTHETIC AUDIO GENERATION (Self-contained if no file exists)
# -------------------------------------------------------------
def generate_sample_audio(duration=2.5, sr=44100):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    # Generate composite signal: 440 Hz (A4) + 880 Hz (A5) with silence gap
    sig = 0.6 * np.sin(2 * np.pi * 440 * t) + 0.3 * np.sin(2 * np.pi * 880 * t)
    # Add a silent segment in the middle to test speech/silence detection
    sig[int(sr * 1.0):int(sr * 1.5)] = 0.0
    synth_path = os.path.join(OUTPUT_DIR, "synthetic_tone.wav")
    sf.write(synth_path, sig, sr)
    return synth_path

# -------------------------------------------------------------
# 2. APPLICATION: Audio Signal Analyzer & Speech Activity Detection
# -------------------------------------------------------------
class AudioSignalAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data, self.sr = sf.read(file_path)
        if len(self.data.shape) > 1:
            self.data = np.mean(self.data, axis=1) # Convert to mono
        self.duration = len(self.data) / self.sr

    def analyze_properties(self):
        info = sf.info(self.file_path)
        return {
            "Sampling Rate (Hz)": self.sr,
            "Channels": info.channels,
            "Duration (s)": round(self.duration, 2),
            "Format": info.format,
            "Subtype": info.subtype,
            "Peak Amplitude": round(float(np.max(np.abs(self.data))), 4),
            "RMS Energy": round(float(np.sqrt(np.mean(self.data**2))), 4)
        }

    def compute_fft(self):
        n = len(self.data)
        yf = np.abs(rfft(self.data))
        xf = rfftfreq(n, 1 / self.sr)
        
        # Identify dominant frequency
        dom_idx = np.argmax(yf[1:]) + 1
        dominant_freq = round(xf[dom_idx], 2)
        return xf, yf, dominant_freq

    def detect_activity(self, frame_size=1024, threshold=0.02):
        # Frame-wise short-term energy to detect active vs silence segments
        num_frames = len(self.data) // frame_size
        energy = [
            np.sum(self.data[i * frame_size:(i + 1) * frame_size] ** 2) / frame_size
            for i in range(num_frames)
        ]
        time_axis = np.linspace(0, self.duration, num_frames)
        active_segments = sum(1 for e in energy if e > threshold)
        active_pct = round((active_segments / num_frames) * 100, 2)
        return time_axis, energy, active_pct

    def generate_visual_report(self):
        xf, yf, dom_freq = self.compute_fft()
        t_energy, energy, active_pct = self.detect_activity()
        time_axis = np.linspace(0, self.duration, len(self.data))

        fig, axes = plt.subplots(3, 1, figsize=(10, 8))

        # 1. Waveform Plot
        axes[0].plot(time_axis, self.data, color="royalblue")
        axes[0].set_title("Audio Waveform (Time Domain)")
        axes[0].set_xlabel("Time (s)")
        axes[0].set_ylabel("Amplitude")

        # 2. Frequency Spectrum (FFT)
        # Limit display up to 2000 Hz for clear visualization
        mask = xf <= 2000
        axes[1].plot(xf[mask], yf[mask], color="crimson")
        axes[1].set_title(f"Frequency Spectrum (FFT) — Dominant Frequency: {dom_freq} Hz")
        axes[1].set_xlabel("Frequency (Hz)")
        axes[1].set_ylabel("Magnitude")

        # 3. Energy / Activity Detection
        axes[2].plot(t_energy, energy, color="forestgreen", label="Short-Time Energy")
        axes[2].axhline(y=0.02, color="orange", linestyle="--", label="Silence/Active Threshold")
        axes[2].set_title(f"Speech / Activity Detection ({active_pct}% Active)")
        axes[2].set_xlabel("Time (s)")
        axes[2].set_ylabel("Energy")
        axes[2].legend()

        plt.tight_layout()
        out_path = os.path.join(OUTPUT_DIR, "audio_analysis_report.png")
        plt.savefig(out_path)
        plt.close()
        print(f"[+] Saved visual report to {out_path}")
        return dom_freq, active_pct

def run_unit4():
    audio_path = "datasets/sample.wav"
    if not os.path.exists(audio_path):
        audio_path = generate_sample_audio()
        print(f"[!] Using generated synthetic tone: {audio_path}")

    analyzer = AudioSignalAnalyzer(audio_path)
    props = analyzer.analyze_properties()
    dom_freq, active_pct = analyzer.generate_visual_report()

    print("\n--- Audio Signal Analyzer Report ---")
    for k, v in props.items():
        print(f"{k:<25}: {v}")
    print(f"{'Dominant Frequency':<25}: {dom_freq} Hz")
    print(f"{'Active Segments':<25}: {active_pct} %")
    print("-" * 45)

if __name__ == "__main__":
    run_unit4()
