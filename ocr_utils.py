import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image):
    img = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

    # Normal threshold
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Adaptive threshold
    adaptive = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return gray, thresh, adaptive


def extract_text(processed_image):
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config)
    return text
