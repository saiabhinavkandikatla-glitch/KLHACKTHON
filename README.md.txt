# Medical Image Forensics Engine

## Installation

1. Install dependencies:
   pip install -r requirements.txt

2. Install Poppler (Windows)
   Download from: https://github.com/oschwartz10612/poppler-windows/releases

3. Update poppler_path inside forensics_engine.py if needed.

## Usage

from forensics_engine import ImageForensicsEngine

engine = ImageForensicsEngine()
result = engine.analyze_files("file1.pdf", "file2.pdf")

print(result)