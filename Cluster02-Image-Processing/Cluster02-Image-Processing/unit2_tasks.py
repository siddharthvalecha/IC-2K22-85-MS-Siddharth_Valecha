import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim

OUTPUT_DIR = "Cluster02-Image-Processing/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_synthetic_image():
    # Fallback high-contrast synthetic image if no dataset image is present
    img = np.zeros((300, 300), dtype=np.uint8)
    cv2.circle(img, (150, 150), 90, 255, -1)
    cv2.putText(img, "DIP", (105, 165), cv2.FONT_HERSHEY_SIMPLEX, 1.2, 0, 3)
    return img

def calculate_metrics(ref, test):
    mse = np.mean((ref.astype("float") - test.astype("float")) ** 2)
    psnr = cv2.PSNR(ref, test) if mse != 0 else float("inf")
    score, _ = ssim(ref, test, full=True)
    return round(mse, 2), round(psnr, 2), round(score, 4)

def run_unit2():
    sample_path = "datasets/sample.jpg"
    img = cv2.imread(sample_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        img = generate_synthetic_image()
    else:
        img = cv2.resize(img, (300, 300))

    # Basic Transformations
    neg = 255 - img
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    contrast = cv2.convertScaleAbs(img, alpha=1.5, beta=10)

    # Simulated Noise (Salt & Pepper / Gaussian)
    noise = np.random.normal(0, 25, img.shape).astype(np.int16)
    noisy = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Filtering
    mean_filtered = cv2.blur(noisy, (5, 5))
    median_filtered = cv2.medianBlur(noisy, 5)
    gaussian_filtered = cv2.GaussianBlur(noisy, (5, 5), 1.5)

    # Sharpening Filter
    sharp_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(img, -1, sharp_kernel)

    # Generate Image Processing Grid Plot
    fig, axes = plt.subplots(2, 4, figsize=(14, 7))
    displays = [
        ("Original", img), ("Negative", neg), ("Thresholded", thresh), ("High Contrast", contrast),
        ("Noisy Input", noisy), ("Mean Filter", mean_filtered), ("Median Filter", median_filtered), ("Sharpened", sharpened)
    ]
    for ax, (title, pic) in zip(axes.ravel(), displays):
        ax.imshow(pic, cmap="gray")
        ax.set_title(title)
        ax.axis("off")

    plot_path = os.path.join(OUTPUT_DIR, "image_processing_grid.png")
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()
    print(f"[+] Saved visualization grid to {plot_path}")

    # Metrics comparison table
    filters = {
        "Mean Filter": mean_filtered,
        "Median Filter": median_filtered,
        "Gaussian Filter": gaussian_filtered
    }
    print("\n--- Quantitative Restoration Quality Analysis ---")
    print(f"{'Filter':<18} | {'MSE':<8} | {'PSNR (dB)':<10} | {'SSIM':<6}")
    print("-" * 50)
    for name, f_img in filters.items():
        mse, psnr, s = calculate_metrics(img, f_img)
        print(f"{name:<18} | {mse:<8} | {psnr:<10} | {s:<6}")
    print("-" * 50)

if __name__ == "__main__":
    run_unit2()
