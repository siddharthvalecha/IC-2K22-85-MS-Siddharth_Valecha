import os
import json
import cv2
import numpy as np

class VideoMetadataAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path

    def analyze(self):
        if not os.path.exists(self.file_path):
            return {"Error": f"File not found at '{self.file_path}'"}

        file_stat = os.stat(self.file_path)
        cap = cv2.VideoCapture(self.file_path)

        if not cap.isOpened():
            return {"Error": f"Could not open video file '{self.file_path}'"}

        # Extract video properties via OpenCV
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = round(cap.get(cv2.CAP_PROP_FPS), 2)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_sec = round(total_frames / fps, 2) if fps > 0 else 0
        fourcc_int = int(cap.get(cv2.CAP_PROP_FOURCC))
        fourcc_str = "".join([chr((fourcc_int >> 8 * i) & 0xFF) for i in range(4)])

        cap.release()

        metadata = {
            "File Name": os.path.basename(self.file_path),
            "File Format": os.path.splitext(self.file_path)[1].upper().replace(".", ""),
            "File Size (MB)": round(file_stat.st_size / (1024 * 1024), 2),
            "File Size (Bytes)": file_stat.st_size,
            "Resolution": f"{width}x{height}",
            "Width": width,
            "Height": height,
            "Aspect Ratio": f"{round(width / height, 2)}:1" if height > 0 else "N/A",
            "FPS (Frame Rate)": fps,
            "Total Frames": total_frames,
            "Duration (Seconds)": duration_sec,
            "Codec (FourCC)": fourcc_str
        }

        return metadata

    def save_report(self, output_dir="Cluster01-Multimedia-Fundamentals/outputs"):
        os.makedirs(output_dir, exist_ok=True)
        report = self.analyze()
        out_file = os.path.join(output_dir, "video_metadata_report.json")
        with open(out_file, "w") as f:
            json.dump(report, f, indent=4)
        print(f"[+] Video metadata report saved to: {out_file}")
        return report

def generate_sample_video(path="datasets/sample.mp4", duration_sec=2, fps=30):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(path, fourcc, fps, (320, 240))
    for i in range(duration_sec * fps):
        # Generate gradient frames
        frame = np.full((240, 320, 3), (i * 4 % 256, 120, 200), dtype=np.uint8)
        out.write(frame)
    out.release()
    print(f"[*] Generated synthetic test video at: {path}")

if __name__ == "__main__":
    test_video_path = "datasets/sample.mp4"
    if not os.path.exists(test_video_path):
        generate_sample_video(test_video_path)

    analyzer = VideoMetadataAnalyzer(test_video_path)
    result = analyzer.save_report()

    print("\n--- Video Metadata Analysis Output ---")
    for key, value in result.items():
        print(f"{key:<20}: {value}")
    print("-" * 45)
