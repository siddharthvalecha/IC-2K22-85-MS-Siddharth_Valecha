# Reflection - Unit 2: Digital Image Processing

### What I Learned
- Understood the difference between linear smoothing (Mean/Gaussian) and non-linear filtering (Median), observing how Median filtering removes impulse noise while retaining distinct edge boundaries.
- Learned to systematically compute MSE, PSNR, and SSIM metrics to judge restoration quality.

### Difficulties Faced
- Arithmetic overflow issues during linear contrast adjustments (\(g(x,y) = \alpha f(x,y) + \beta\)).

### How the Problems Were Resolved
- Implemented `cv2.convertScaleAbs()` to safely clip pixel intensity values within the standard 8-bit dynamic range \([0, 255]\).
