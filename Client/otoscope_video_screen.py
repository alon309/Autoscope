import os
import cv2
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage
from kivy.core.image import Texture as CoreTexture
from kivy.app import App

class OtoScopeVideoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera_index = 0  # Default camera index
        self.capture = None  # OpenCV VideoCapture object
        self.current_frame = None  # To store the captured frame

        # Main layout
        layout = BoxLayout(orientation="vertical")
        
        # Dropdown to select camera
        self.dropdown = DropDown()
        self.camera_btn = Button(text="Select Camera", size_hint=(1, 0.1))
        self.camera_btn.bind(on_release=self.dropdown.open)

        # Detect available cameras and add to dropdown
        self.cameras = self.get_available_cameras()
        for idx, cam_name in self.cameras.items():
            btn = Button(text=cam_name, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn, idx=idx: self.select_camera(idx))
            self.dropdown.add_widget(btn)

        # Video display
        self.video_display = Image()

        # Add widgets to layout
        layout.add_widget(self.camera_btn)
        layout.add_widget(self.video_display)

        self.add_widget(layout)

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

    def select_camera(self, index):
        """
        Switch to the selected camera.
        """
        self.camera_index = index
        self.camera_btn.text = self.cameras[index]
        self.dropdown.dismiss()
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
                self.video_display.texture = texture

    def capture_image(self, *args):
        """
        Capture the current frame and navigate to the ChosenImageScreen.
        """
        if self.current_frame is not None:
            image_path = "captured_image.jpg"  # Temporary file path
            cv2.imwrite(image_path, self.current_frame)  # Save the current frame

            # Navigate to the ChosenImageScreen
            chosen_image_screen = self.manager.get_screen('chosenImage')
            app = App.get_running_app()  # Get the current app instance
            chosen_image_screen.update_data(image_path=image_path, user_id=app.user_details.get("uid"))
            self.manager.current = 'chosenImage'
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
