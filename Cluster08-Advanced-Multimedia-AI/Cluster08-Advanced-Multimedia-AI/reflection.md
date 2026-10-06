# Reflection - Unit 8: Advanced Multimedia & AI Applications

### What I Learned
- Understood the difference between concatenative/parametric TTS and neural voice cloning, observing how neural models capture acoustic identity (timbre, intonation, pitch).

### Difficulties Faced
- Cloud voice cloning APIs require active authentication and bandwidth, which can fail without network access.

### How the Problems Were Resolved
- Implemented a dual-pipeline fallback that switches automatically to local speech generation when API credentials are absent.
