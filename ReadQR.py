import cv2
import qrcode
import streamlit as st
from PIL import Image

def read_qr_code_from_camera():
    # Open the laptop's default camera
    camera = st.camera_input(0)

    if not camera.isOpened():
        st.error("Error: Could not access the camera.")
        return

    st.write("Scanning for QR codes. Press 'q' to quit.")
    while True:
        # Capture frame-by-frame
        ret, frame = camera.read()
        if not ret:
            st.error("Error: Failed to capture frame.")
            break

        # Decode QR codes using OpenCV
        qr_detector = cv2.QRCodeDetector()
        value, pts, _ = qr_detector(frame)

        if value:
            st.write(f"QR Code Detected: {value}")
            pts = pts.astype(int)
            # Draw a rectangle around the QR code
            for i in range(4):
                cv2.line(frame, tuple(pts[i]), tuple(pts[(i + 1) % 4]), (0, 255, 0), 3)

        # Convert the frame to a format suitable for Streamlit display
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        st.image(img, channels="RGB")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    read_qr_code_from_camera()
