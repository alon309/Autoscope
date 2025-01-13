import os
import cv2
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen
from kivy.app import App
import time

class OtoScopeVideoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera_index = 0  # Default camera index
        self.capture = None  # OpenCV VideoCapture object
        self.current_frame = None  # To store the captured frame

        # Detect available cameras and add to dropdown
        self.cameras = self.get_available_cameras()
        self.update_camera_spinner()

    def update_camera_spinner(self):
        """
        Update the spinner with the available camera names.
        """
        self.ids.camera_spinner.values = list(self.cameras.values())

    def get_available_cameras(self):
        """
        Detect available cameras on the computer.
        Returns a dictionary with index as keys and camera names (or "Camera X") as values.
        """
        cameras = {}
        index = 0
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.isOpened():
                break
            cameras[index] = f"Camera {index}"
            cap.release()
            index += 1
        print(cameras)
        return cameras

    def select_camera(self, camera_name):
        """
        Switch to the selected camera.
        """
        # Find the camera index from the name
        camera_index = None
        for index, name in self.cameras.items():
            if name == camera_name:
                camera_index = index
                break

        if camera_index is not None:
            self.camera_index = camera_index
            self.ids.camera_spinner.text = self.cameras[camera_index]
            self.start_video_stream()


    def start_video_stream(self):
        """
        Start streaming video from the selected camera.
        """
        if self.capture:
            self.capture.release()  # Release the previous capture object

        self.capture = cv2.VideoCapture(self.camera_index)
        Clock.schedule_interval(self.update_video, 1.0 / 30.0)  # Update at ~30 FPS

    def update_video(self, dt):
        """
        Update the video frame on the Kivy UI.
        """
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                self.current_frame = frame  # Store the latest frame
                # Convert the frame to a Kivy texture
                buf = cv2.flip(frame, 0).tobytes()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
                texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
                self.ids.video_area.texture = texture


    def capture_image(self, *args):
        """
        Capture the current frame and navigate to the ChosenImageScreen.
        """
        if self.current_frame is not None:
            # Use the app's user data directory to store temporary files.
            # This ensures compatibility across different operating systems and provides a secure, isolated location for saving files.
            directory = App.get_running_app().user_data_dir 
            
            for filename in os.listdir(directory):
                if filename.startswith("captured_image"):
                    file_path = os.path.join(directory, filename)
                    try:
                        os.remove(file_path)
                        print(f"File {filename} has been deleted.")
                    except Exception as e:
                        print(f"Error deleting file {filename}: {e}")

            image_path = os.path.join(directory, f"captured_image_{int(time.time())}.jpg")
            
            cv2.imwrite(image_path, self.current_frame)  # Save the current frame

            # Navigate to the ChosenImageScreen
            chosen_image_screen = self.manager.get_screen('chosenImage')
            app = App.get_running_app()  # Get the current app instance
            chosen_image_screen.update_data(image_path=image_path, user_id=app.user_details.get("uid"))
            self.manager.current = 'chosenImage'
            
            # שחרור capture
            if self.capture:
                self.capture.release()
        else:
            print("No frame available to capture.")


    def on_stop(self):
        """
        Release resources when the app is stopped.
        """
        if self.capture:
            self.capture.release()

    def go_back(self, *args):
        if self.capture:
            self.capture.release()
        self.manager.current = 'earCheck'

    def on_pre_enter(self):
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Home', 'Ear Check', 'OtoScope'])
        
    def on_enter(self):
        self.current_frame = None
        self.ids.video_area.texture = None
        self.ids.camera_spinner.text = 'Select Camera'
