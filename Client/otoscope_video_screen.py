from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock
import cv2
from kivy.graphics.texture import Texture
import os
from datetime import datetime
from jnius import autoclass
from USBCameraManager import USBCameraManager  # Import the USB Camera Manager class

class OtoScopeVideoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.usb_camera_manager = None
        self.frame = None

    def on_enter(self):
        """Start the camera feed when the screen is loaded."""
        self.start_camera()

    def on_leave(self):
        """Release the camera when leaving the screen."""
        self.stop_camera()

    def start_camera(self):
        """Initialize and start the USB camera feed."""
        self.usb_camera_manager = USBCameraManager(self.on_frame_received)
        
        # Try detecting and starting the USB camera
        if self.usb_camera_manager.detect_usb_camera():
            self.usb_camera_manager.start_video_stream()
        else:
            print("No USB camera detected.")

    def stop_camera(self):
        """Stop the camera feed."""
        if self.usb_camera_manager:
            self.usb_camera_manager.stop_video_stream()

    def on_frame_received(self, frame):
        """Callback function that is called when a frame is received from the camera."""
        self.frame = frame

        # Convert the frame to a Kivy texture
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

        # Update the texture on the Image widget
        self.ids.video_area.texture = texture

    def save_image(self):
        """Save the current frame as an image with a custom name and location."""
        if self.frame is not None:
            # Generate filename with the format Capture_DD_MM_YYYY_HH_MM.jpg
            timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M")
            filename = f"Capture_{timestamp}.jpg"

            # Get the phone storage path (assuming internal storage)
            storage_dir = self.get_storage_directory()
            if storage_dir is None:
                print("Unable to access storage directory.")
                return

            # Create AutoScope folder if it doesn't exist
            auto_scope_folder = os.path.join(storage_dir, "AutoScope")
            if not os.path.exists(auto_scope_folder):
                os.makedirs(auto_scope_folder)

            # Define the full path where the image will be saved
            file_path = os.path.join(auto_scope_folder, filename)

            # Call the method to save the picture (assuming the take_picture method is updated to accept a file path)
            self.usb_camera_manager.take_picture(file_path)
        else:
            print("No frame available to save.")


    def get_storage_directory(self):
        """Get the phone's storage directory (for Android)."""
        # Android context and directory for saving files
        try:
            context = autoclass("org.kivy.android.PythonActivity").mActivity.getApplicationContext()
            file_dir = context.getExternalFilesDir(None)  # This retrieves the app's specific directory on external storage
            return file_dir.getAbsolutePath()
        except Exception as e:
            print(f"Error accessing storage: {e}")
            return None
        
    def go_back(self):
        """Return to the earCheck screen."""
        self.manager.current = 'earCheck'
