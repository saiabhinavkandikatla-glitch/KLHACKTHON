import os
from PIL import Image
import imagehash
from pdf2image import convert_from_path
<<<<<<< HEAD
import numpy as np
=======
>>>>>>> 9a505941b669690bc3a9f36b0dadc7abe6b2ccb6


class ImageForensicsEngine:

<<<<<<< HEAD
    def __init__(self, similarity_threshold=85, poppler_path=r"C:\poppler-25.12.0\Library\bin"):
        """
        similarity_threshold:
            Percentage above which fraud is flagged.
        """
        self.similarity_threshold = similarity_threshold
=======
    def __init__(self, threshold=10, poppler_path=r"C:\poppler-25.12.0\Library\bin"):
        self.threshold = threshold
>>>>>>> 9a505941b669690bc3a9f36b0dadc7abe6b2ccb6
        self.poppler_path = poppler_path

    # --------------------------------------------
    # Load image or PDF
    # --------------------------------------------
    def _load_file_as_image(self, file_path):

<<<<<<< HEAD
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

=======
>>>>>>> 9a505941b669690bc3a9f36b0dadc7abe6b2ccb6
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
<<<<<<< HEAD
    # Generate Multiple Hashes
    # --------------------------------------------
    def _generate_hashes(self, img):

        img = img.convert("L")
        img = img.resize((256, 256))

        phash = imagehash.phash(img)
        dhash = imagehash.dhash(img)
        whash = imagehash.whash(img)

        return phash, dhash, whash
=======
    # Generate perceptual hash
    # --------------------------------------------
    def _generate_hash(self, img):
        img = img.convert("L")
        img = img.resize((256, 256))
        return imagehash.phash(img)
>>>>>>> 9a505941b669690bc3a9f36b0dadc7abe6b2ccb6

    # --------------------------------------------
    # Hamming Distance
    # --------------------------------------------
    def _hamming_distance(self, hash1, hash2):
<<<<<<< HEAD
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
=======
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
>>>>>>> 9a505941b669690bc3a9f36b0dadc7abe6b2ccb6

    # --------------------------------------------
    # PUBLIC METHOD FOR DASHBOARD
    # --------------------------------------------
    def analyze_files(self, file1_path, file2_path):

        img1 = self._load_file_as_image(file1_path)
        img2 = self._load_file_as_image(file2_path)

<<<<<<< HEAD
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
=======
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
>>>>>>> 9a505941b669690bc3a9f36b0dadc7abe6b2ccb6
        }