import os
from PIL import Image
import imagehash
import fitz  # PyMuPDF
import numpy as np


class ImageForensicsEngine:

    def __init__(self, similarity_threshold=85):
        """
        similarity_threshold:
            Percentage above which fraud is flagged.
        """
        self.similarity_threshold = similarity_threshold

    # --------------------------------------------
    # Load image or PDF
    # --------------------------------------------
    def _load_file_as_image(self, file_path):

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.lower().endswith(".pdf"):
            doc = fitz.open(file_path)
            if doc.page_count == 0:
                raise Exception("PDF conversion failed.")
            page = doc.load_page(0)
            pix = page.get_pixmap(dpi=200)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            return img

        return Image.open(file_path)

    # --------------------------------------------
    # Generate Multiple Hashes
    # --------------------------------------------
    def _generate_hashes(self, img):

        img = img.convert("L")
        img = img.resize((256, 256))

        phash = imagehash.phash(img)
        dhash = imagehash.dhash(img)
        whash = imagehash.whash(img)

        return phash, dhash, whash

    # --------------------------------------------
    # Hamming Distance
    # --------------------------------------------
    def _hamming_distance(self, hash1, hash2):
        return hash1 - hash2  # imagehash supports direct subtraction

    # --------------------------------------------
    # Calculate Similarity Score
    # --------------------------------------------
    def _calculate_similarity(self, distances):

        # Average distance across hash types
        avg_distance = np.mean(distances)

        # Normalize (hash length = 64 bits)
        similarity = max(0, min(100, (1 - avg_distance / 64) * 100))

        return round(similarity, 2)

    # --------------------------------------------
    # Risk Classification
    # --------------------------------------------
    def _risk_classification(self, similarity):

        if similarity >= 95:
            return 100, "Near-Identical (Critical Fraud Risk)"
        elif similarity >= 85:
            return 85, "Highly Similar (High Fraud Risk)"
        elif similarity >= 70:
            return 60, "Moderately Similar (Medium Risk)"
        elif similarity >= 50:
            return 30, "Low Similarity (Low Risk)"
        else:
            return 0, "Distinct / Unique"

    # --------------------------------------------
    # PUBLIC METHOD FOR DASHBOARD
    # --------------------------------------------
    def analyze_files(self, file1_path, file2_path):

        img1 = self._load_file_as_image(file1_path)
        img2 = self._load_file_as_image(file2_path)

        # Generate hashes
        ph1, dh1, wh1 = self._generate_hashes(img1)
        ph2, dh2, wh2 = self._generate_hashes(img2)

        # Compute distances
        distances = [
            self._hamming_distance(ph1, ph2),
            self._hamming_distance(dh1, dh2),
            self._hamming_distance(wh1, wh2),
        ]

        similarity = self._calculate_similarity(distances)

        risk_score, classification = self._risk_classification(similarity)

        fraud_detected = similarity >= self.similarity_threshold

        return {
            "phash_1": str(ph1),
            "phash_2": str(ph2),
            "dhash_distance": distances[1],
            "whash_distance": distances[2],
            "average_distance": round(float(np.mean(distances)), 2),
            "similarity_percent": similarity,
            "fraud_risk_score": risk_score,
            "classification": classification,
            "fraud_detected": fraud_detected
        }