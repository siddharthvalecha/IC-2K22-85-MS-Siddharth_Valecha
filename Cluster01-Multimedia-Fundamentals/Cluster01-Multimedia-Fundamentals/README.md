# Unit 1: Multimedia Fundamentals - Image Metadata Analyser

## Problem Statement
Develop an image analysis tool capable of parsing structural properties, color space representations, file format encoding, dimensions, and EXIF metadata from digital images.

## Objectives
- Extract structural image metadata: File Format, MIME Type, Pixel Resolution, Color Mode, and File Size.
- Parse EXIF tags and DPI specifications.
- Export structured metadata records in JSON format for automated ingestion.

## Methodology
- Employs binary file header inspection and the PIL (Pillow) engine to decode format markers without decompressing full image payloads into memory.
- Uses `PIL.ExifTags` to map hexadecimal EXIF identifiers to standard photography metadata attributes (camera model, orientation, timestamps).

## Outputs
- `outputs/image_metadata_report.json`: Consolidated JSON metadata report.
