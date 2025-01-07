import cv2
from pyzbar import decode
import streamlit as st
from PIL import Image

def main():
    st.title("QR Code Scanner")
    st.write("Scan QR codes using your laptop's camera.")

    # Start or stop the camera
    start_camera = st.checkbox("Start Camera")
    qr_code_result = st.empty()  # Placeholder for displaying QR code results

    if start_camera:
        # Open the camera
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            st.error("Error: Could not access the camera.")
            return

        st.write("Scanning for QR codes. Uncheck the 'Start Camera' box to stop.")
        
        # Stream video frames
        while start_camera:
            ret, frame = camera.read()
            if not ret:
                st.error("Error: Failed to capture frame.")
                break

            # Decode QR codes
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                qr_text = obj.data.decode('utf-8')
                qr_code_result.success(f"QR Code Detected: {qr_text}")

                # Draw a rectangle around the QR code
                points = obj.polygon
                if len(points) > 4:
                    hull = cv2.convexHull(points)
                    points = hull

                n = len(points)
                for j in range(n):
                    cv2.line(frame, tuple(points[j]), tuple(points[(j + 1) % n]), (0, 255, 0), 3)

            # Convert the frame to RGB (for displaying in Streamlit)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Display the frame in Streamlit
            frame_placeholder = st.image(frame_rgb, channels="RGB")

            # Update the checkbox state
            start_camera = st.checkbox("Start Camera", value=True)

        # Release the camera
        camera.release()

if __name__ == "__main__":
    main()
