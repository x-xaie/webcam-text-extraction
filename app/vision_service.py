# app/vision_service.py
from google.cloud import vision
import io
from PIL import Image
import numpy as np

# Initialize Google Vision API client
client = vision.ImageAnnotatorClient()

def detect_text(image):
    """Detect text in the provided image using Google Vision API."""
    # Convert OpenCV image (numpy array) to PIL image
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Convert the PIL image to byte array
    img_byte_array = io.BytesIO()
    pil_image.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()

    # Create a Vision API image
    vision_image = vision.Image(content=img_byte_array)

    # Perform text detection
    response = client.text_detection(image=vision_image)
    texts = response.text_annotations

    if texts:
        return texts[0].description  # Return the detected text
    else:
        return "No text detected"
