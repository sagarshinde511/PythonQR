import streamlit as st
import cv2
from PIL import Image
import numpy as np

def read_qr_code_from_camera():
    st.title("QR Code Scanner")

    # Use Streamlit's camera input
    camera_image = st.camera_input("Take a picture to scan for QR codes")

    if camera_image:
        # Convert the captured image to OpenCV format
        image = Image.open(camera_image)
        frame = np.array(image)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Decode QR codes in the frame using OpenCV's QRCodeDetector
        qr_detector = cv2.QRCodeDetector()
        value, points, _ = qr_detector.detectAndDecode(frame)

        if value:
            st.success(f"QR Code Detected: {value}")
            if points is not None:
                # Draw a rectangle around the QR code
                points = points[0].astype(int)
                for i in range(4):
                    cv2.line(frame, tuple(points[i]), tuple(points[(i + 1) % 4]), (0, 255, 0), 3)
        else:
            st.warning("No QR Code detected.")

        # Convert the frame back to RGB for Streamlit display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame, channels="RGB")

if __name__ == "__main__":
    read_qr_code_from_camera()
