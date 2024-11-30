import cv2

def get_available_cameras(max_cameras=10):
    """
    Detect available webcams and return a list of camera indices.
    :param max_cameras: Maximum number of cameras to check. Default is 10.
    :return: A list of available camera indices (as strings).
    """
    available_cameras = []
    
    for i in range(max_cameras):
        try:
            with cv2.VideoCapture(i) as cap:
                # Check if the camera opened successfully
                if cap.isOpened():
                    available_cameras.append(str(i))  # Append camera index as a string
        except cv2.error:
            # If an error occurs (e.g., no camera at that index), skip it
            continue
    
    # If no cameras are found, return a fallback message
    if not available_cameras:
        return ["No camera found"]
    
    return available_cameras


def capture_frame(camera_index):
    """
    Capture a frame from the specified webcam.
    The camera is released immediately after the frame is captured.
    
    :param camera_index: The index of the camera to use.
    :return: A frame (image) from the camera or None if capturing fails.
    """
    try:
        with cv2.VideoCapture(camera_index) as cap:
            # Check if the camera is opened successfully
            if not cap.isOpened():
                return None
            
            ret, frame = cap.read()
            if not ret:
                return None
            return frame
    except cv2.error as e:
        # Handle any OpenCV errors (e.g., camera access issues)
        print(f"Error accessing camera {camera_index}: {e}")
        return None
