# Unit 4: Digital Audio Processing

## Problem Statement
Analyze digital audio signals in time and frequency domains, calculate structural acoustic parameters, and build an automated Audio Signal Analyzer capable of speech activity detection.

## Objectives
- Extract key audio metrics: Sampling Frequency, Duration, Channels, RMS Energy, and Amplitude.
- Perform frequency-domain analysis using Fast Fourier Transform (FFT) to identify dominant frequencies.
- Detect active audio vs. silence segments using short-time frame energy thresholding.

## Methodology
- **Time-to-Frequency Conversion**: Fast Fourier Transform (FFT) maps the discrete time-domain audio samples x[n] into frequency magnitudes:
  X(k) = Sum_{n=0}^{N-1} x[n] * exp(-j * 2 * pi * k * n / N)
- **Speech Activity Detection (VAD)**: Computes Short-Time Energy across window frames:
  E_m = (1 / N) * Sum_{n=0}^{N-1} (x[m * N + n])^2
  Frames exceeding the empirical energy threshold are classified as active sound.

## Outputs
- `outputs/audio_analysis_report.png`: 3-panel figure showing Time-domain Waveform, FFT Spectrum, and Short-Time Frame Energy curve.
