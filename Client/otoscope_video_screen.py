from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.label import Label

try:
    from android.permissions import request_permissions, Permission
    from jnius import autoclass
    ANDROID = True
except ImportError:
    print("Running outside of Android. 'android.permissions' and 'jnius' are not available.")
    ANDROID = False


class OtoScopeVideoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera_widget = None
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)


        if ANDROID:
            self.request_permissions()


        available_cameras = self.get_available_cameras()


        if available_cameras:
            self.spinner = Spinner(
                text="Select Camera",
                values=available_cameras,  
                size_hint=(1, 0.1),
            )
            self.spinner.bind(text=self.select_camera)
            self.layout.add_widget(self.spinner)
        else:

            error_label = Label(text="No cameras available.", color=(1, 0, 0, 1), font_size='20sp')
            self.layout.add_widget(error_label)


        back_button = Button(text="Back", size_hint=(1, 0.1))
        back_button.bind(on_release=self.go_back)
        self.layout.add_widget(back_button)

    def request_permissions(self):

        try:
            request_permissions([Permission.CAMERA, Permission.RECORD_AUDIO])
            print("Camera and Audio permissions granted.")
        except Exception as e:
            error_label = Label(text=f"Permission error: {str(e)}", color=(1, 0, 0, 1), font_size='20sp')
            self.layout.add_widget(error_label)

    def get_available_cameras(self):

        available_cameras = []


        for i in range(6):  
            try:
                camera_test = Camera(index=i, resolution=(640, 480), play=False)
                available_cameras.append(f"Internal Camera {i}")
            except Exception:
                pass

        if ANDROID:
            try:
                UsbManager = autoclass('android.hardware.usb.UsbManager')
                Context = autoclass('android.content.Context')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                usb_manager = PythonActivity.mActivity.getSystemService(Context.USB_SERVICE)
                usb_devices = usb_manager.getDeviceList()
                if not usb_devices.isEmpty():
                    for device_name in usb_devices.keySet():
                        available_cameras.append(f"USB Camera {len(available_cameras)}")
            except Exception as e:
                print(f"Error checking USB cameras: {e}")
        return available_cameras


    def select_camera(self, spinner, selected_camera):

        if self.camera_widget:
            self.layout.remove_widget(self.camera_widget)
            self.camera_widget = None

        try:
            if "USB Camera" in selected_camera and ANDROID:
                print("Attempting to open USB Camera...")
                usb_index = int(selected_camera.split()[-1])  # Extracts the last part of the string as the index
                self.camera_widget = Camera(index=usb_index, resolution=(640, 480), play=True)
            elif "Internal Camera" in selected_camera:
                camera_index = int(selected_camera.split()[-1])
                self.camera_widget = Camera(index=camera_index, resolution=(640, 480), play=True)
            else:
                raise ValueError(f"Unsupported camera: {selected_camera}")
            self.layout.add_widget(self.camera_widget, index=1)
        except Exception as e:
            error_label = Label(
                text=f"Error: Could not open camera {selected_camera}. {str(e)}",
                color=(1, 0, 0, 1),
                font_size='20sp'
            )
            self.layout.add_widget(error_label)
            print(f"Available cameras: {self.get_available_cameras()}")
            print(f"Selected camera: {selected_camera}")


    def go_back(self, *args):

        if self.camera_widget:
            self.camera_widget.play = False
            self.layout.remove_widget(self.camera_widget)
            self.camera_widget = None
        self.manager.current = 'earCheck'

    def on_leave(self):

        if self.camera_widget:
            self.camera_widget.play = False
            self.layout.remove_widget(self.camera_widget)
            self.camera_widget = None
