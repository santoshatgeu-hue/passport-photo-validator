import streamlit as st
import cv2
import numpy as np
from PIL import Image

# App title and info
st.set_page_config(page_title="Passport Photo Validator", page_icon="🪪", layout="centered")
st.title("🪪 Passport Photo Validator")
st.write("Upload a passport-size photo to check if the full face is clearly visible.")

# Upload section
uploaded_file = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"])

def validate_passport_photo(image: np.ndarray):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        return False, "❌ No face detected. Please ensure your face is clearly visible."
    elif len(faces) > 1:
        return False, "❌ Multiple faces detected. Upload a single-person photo."

    (x, y, w, h) = faces[0]
    img_height, img_width = image.shape[:2]

    # Check face cropping
    if x <= 5 or y <= 5 or (x + w) >= img_width - 5 or (y + h) >= img_height - 5:
        return False, "❌ Face appears cropped. Please upload a full-face photo."

    # Check face size ratio
    face_ratio = h / img_height
    if face_ratio < 0.3:
        return False, "❌ Face too small. Move closer to the camera."
    elif face_ratio > 0.8:
        return False, "❌ Face too large. Move slightly away from the camera."

    return True, "✅ Valid passport photo!"

# Process the uploaded image
if uploaded_file:
    image = np.array(Image.open(uploaded_file))
    st.image(image, caption="Uploaded Photo", use_column_width=True)

    valid, message = validate_passport_photo(image)
    if valid:
        st.success(message)
    else:
        st.error(message)
