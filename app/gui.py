# app/gui.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import cv2
from app.camera import get_available_cameras, capture_frame
from app.vision_service import detect_text
from app.text_processor import process_text

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Webcam Text Extraction")

        # List available cameras
        self.available_cameras = get_available_cameras()

        # Dropdown for webcam selection
        self.camera_selection_label = tk.Label(self.root, text="Select Camera:")
        self.camera_selection_label.pack()

        self.camera_select = ttk.Combobox(self.root, values=self.available_cameras)
        self.camera_select.set(self.available_cameras[0])  # Default to the first camera
        self.camera_select.pack()

        # Label to display webcam feed
        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        # Button to trigger text extraction
        self.extract_button = tk.Button(self.root, text="Capture and Extract Text", command=self.capture_and_extract)
        self.extract_button.pack()

        # Text box to display extracted text
        self.text_box = tk.Text(self.root, height=10, width=50)
        self.text_box.pack()

        # Initialize the OpenCV VideoCapture object (default to camera 0)
        self.cap = None
        self.select_camera(self.camera_select.get())  # Initialize camera selection

    def select_camera(self, camera_index):
        """Select the camera based on the user's choice."""
        camera_index = int(camera_index)  # Convert selected camera index to integer
        if self.cap is not None:
            self.cap.release()  # Release the previous camera
        self.cap = cv2.VideoCapture(camera_index)

    def capture_and_extract(self):
        """Capture a frame from webcam and extract text."""
        if self.cap is None or not self.cap.isOpened():
            messagebox.showerror("Error", "No camera selected or webcam is not working.")
            return
        
        frame = capture_frame(self.cap)  # Capture the frame using OpenCV

        if frame is not None:
            # Extract text using Google Vision API
            raw_text = detect_text(frame)

            # Process the extracted text (cleaning, formatting, etc.)
            processed_text = process_text(raw_text)

            # Display the extracted text in the Tkinter text box
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, processed_text)

    def update_video_feed(self):
        """Update the video feed in the Tkinter GUI."""
        if self.cap is None or not self.cap.isOpened():
            return
        
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB (from BGR)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to Image
            img = Image.fromarray(frame_rgb)
            img = img.resize((640, 480))
            img_tk = ImageTk.PhotoImage(img)

            # Update the label with the new image
            self.video_label.img_tk = img_tk
            self.video_label.config(image=img_tk)

        # Schedule next frame update
        self.root.after(10, self.update_video_feed)

    def run(self):
        """Start the GUI and video feed."""
        self.update_video_feed()
        self.root.mainloop()
