from jnius import autoclass, cast, autoclass
from kivy.app import App
import cv2
from kivy.graphics.texture import Texture
from kivy.clock import Clock

class USBCameraManager:
    def __init__(self, on_frame_callback):
        """
        Initializes the USB camera manager.

        Args:
            on_frame_callback: A function that receives the frame for processing/displaying.
        """
        self.on_frame_callback = on_frame_callback
        self.usb_manager = autoclass("android.hardware.usb.UsbManager")
        self.usb_device = autoclass("android.hardware.usb.UsbDevice")
        self.activity = autoclass("org.kivy.android.PythonActivity").mActivity
        self.context = self.activity.getApplicationContext()
        self.camera_connected = False
        self.capture = None

    def detect_usb_camera(self):
        """
        Detects USB cameras connected to the device using the USB class type.
        """
        usb_service = self.context.getSystemService(self.context.USB_SERVICE)
        device_list = usb_service.getDeviceList()
        VIDEO_CLASS = 0x0E  # USB Video Class
        for device_name in device_list.keySet():
            usb_device = device_list.get(device_name)
            if usb_device.getDeviceClass() == VIDEO_CLASS or "camera" in usb_device.getDeviceName().lower():
                print(f"Camera found: {usb_device.getDeviceName()}")
                self.camera_connected = True
                return True
        print("No USB camera found.")
        self.camera_connected = False
        return False


    def start_video_stream(self):
        """
        Starts video streaming if a USB camera is connected.
        """
        if not self.camera_connected:
            print("No camera connected.")
            return

        self.capture = cv2.VideoCapture(2)  # 0 - back, 1 - front, 2 - usb
        if not self.capture.isOpened():
            print("Unable to open USB camera.")
            return

        # Schedule frame updates
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)

    def update_frame(self, dt):
        """
        Reads a frame from the video stream and sends it to the callback.
        """
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                # Convert the frame for Kivy display
                self.on_frame_callback(frame)
            else:
                print("Failed to read frame.")
        else:
            print("Video capture is not open.")

    def take_picture(self, filename):
        """
        Captures the current frame and saves it as an image.

        Args:
            filename: Path to save the captured image.
        """
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                cv2.imwrite(filename, frame)
                print(f"Picture saved: {filename}")
            else:
                print("Failed to capture image.")
        else:
            print("Video capture is not open.")

    def stop_video_stream(self):
        """
        Stops the video streaming.
        """
        if self.capture and self.capture.isOpened():
            self.capture.release()
            self.capture = None
        Clock.unschedule(self.update_frame)

