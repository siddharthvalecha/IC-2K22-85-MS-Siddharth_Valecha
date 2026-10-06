import os
import json
from PIL import Image
from PIL.ExifTags import TAGS

class ImageMetadataAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path

    def analyze(self):
        if not os.path.exists(self.file_path):
            return {"Error": f"File not found at '{self.file_path}'"}

        file_stat = os.stat(self.file_path)
        metadata = {
            "File Name": os.path.basename(self.file_path),
            "File Size (KB)": round(file_stat.st_size / 1024, 2),
            "File Size (Bytes)": file_stat.st_size
        }

        try:
            with Image.open(self.file_path) as img:
                metadata["Format"] = img.format
                metadata["MIME Type"] = Image.MIME.get(img.format)
                metadata["Dimensions (WxH)"] = img.size
                metadata["Width"] = img.width
                metadata["Height"] = img.height
                metadata["Color Mode"] = img.mode
                metadata["Color Bands"] = img.getbands()
                metadata["DPI"] = img.info.get("dpi", "Not Specified")
                metadata["Is Animated"] = getattr(img, "is_animated", False)
                metadata["Frame Count"] = getattr(img, "n_frames", 1)

                # Extract EXIF tags if present
                exif_data = {}
                raw_exif = img.getexif()
                if raw_exif:
                    for tag_id, value in raw_exif.items():
                        tag_name = TAGS.get(tag_id, tag_id)
                        exif_data[str(tag_name)] = str(value)
                metadata["EXIF Metadata"] = exif_data if exif_data else "No EXIF data present"

        except Exception as e:
            metadata["Read Error"] = str(e)

        return metadata

    def save_report(self, output_dir="Cluster01-Multimedia-Fundamentals/outputs"):
        os.makedirs(output_dir, exist_ok=True)
        report = self.analyze()
        out_file = os.path.join(output_dir, "image_metadata_report.json")
        with open(out_file, "w") as f:
            json.dump(report, f, indent=4)
        print(f"[+] Metadata report saved to: {out_file}")
        return report

if __name__ == "__main__":
    # Ensure sample image exists or create a synthetic test image
    test_img_path = "datasets/sample.jpg"
    if not os.path.exists(test_img_path):
        os.makedirs("datasets", exist_ok=True)
        # Create a sample test image
        img = Image.new("RGB", (640, 480), color=(73, 109, 137))
        img.save(test_img_path, format="JPEG", quality=95)
        print(f"[*] Created placeholder test image: {test_img_path}")

    analyzer = ImageMetadataAnalyzer(test_img_path)
    result = analyzer.save_report()

    print("\n--- Image Metadata Analysis Output ---")
    for key, value in result.items():
        if key != "EXIF Metadata":
            print(f"{key:<20}: {value}")
        else:
            print(f"{key:<20}: {value}")
    print("-" * 45)
