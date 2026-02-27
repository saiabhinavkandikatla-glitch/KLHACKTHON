import os
from PIL import Image
import imagehash
from pdf2image import convert_from_path


class ImageForensicsEngine:

    def __init__(self, threshold=10, poppler_path=r"C:\poppler-25.12.0\Library\bin"):
        self.threshold = threshold
        self.poppler_path = poppler_path

    # --------------------------------------------
    # Load image or PDF
    # --------------------------------------------
    def _load_file_as_image(self, file_path):

        if file_path.lower().endswith(".pdf"):
            pages = convert_from_path(
                os.path.abspath(file_path),
                poppler_path=self.poppler_path,
                dpi=200,
                first_page=1,
                last_page=1,
                fmt="png",
                strict=False
            )

            if not pages:
                raise Exception("PDF conversion failed.")

            return pages[0]

        return Image.open(file_path)

    # --------------------------------------------
    # Generate perceptual hash
    # --------------------------------------------
    def _generate_hash(self, img):
        img = img.convert("L")
        img = img.resize((256, 256))
        return imagehash.phash(img)

    # --------------------------------------------
    # Hamming Distance
    # --------------------------------------------
    def _hamming_distance(self, hash1, hash2):
        return sum(
            c1 != c2 for c1, c2 in zip(
                bin(int(str(hash1), 16))[2:].zfill(64),
                bin(int(str(hash2), 16))[2:].zfill(64)
            )
        )

    # --------------------------------------------
    # Risk Scoring
    # --------------------------------------------
    def _risk_classification(self, distance):
        if distance <= 3:
            return 95, "Critical Similarity"
        elif distance <= 8:
            return 75, "High Similarity"
        elif distance <= 15:
            return 40, "Moderate Similarity"
        else:
            return 0, "Unique"

    # --------------------------------------------
    # PUBLIC METHOD FOR DASHBOARD
    # --------------------------------------------
    def analyze_files(self, file1_path, file2_path):

        img1 = self._load_file_as_image(file1_path)
        img2 = self._load_file_as_image(file2_path)

        hash1 = self._generate_hash(img1)
        hash2 = self._generate_hash(img2)

        distance = self._hamming_distance(hash1, hash2)
        similarity = round(((64 - distance) / 64) * 100, 2)
        risk_score, classification = self._risk_classification(distance)

        return {
            "hash_1": str(hash1),
            "hash_2": str(hash2),
            "hamming_distance": distance,
            "similarity_percent": similarity,
            "fraud_risk_score": risk_score,
            "classification": classification,
            "fraud_detected": distance <= self.threshold
        }