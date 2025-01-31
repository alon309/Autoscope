from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.metrics import dp
from widgets.rounded_button import RoundedButton
from widgets.feedback_popup import FeedbackPopup

# Check if running on Android
try:
    from android.permissions import request_permissions, Permission # type: ignore
    ANDROID = True
except ImportError:
    print("Running outside of Android. 'android.permissions' is not available.")
    ANDROID = False

class EarCheckScreen(Screen):
    """ 
    Screen for ear check functionalities, including:
    
    - Requesting storage permissions (for Android).
    - Opening a file chooser to select an image.
    - Navigating to other screens (chosen image, otoscope, or home).
    """
    def __init__(self, **kwargs):
        """ Initialize the EarCheckScreen. """
        super(EarCheckScreen, self).__init__(**kwargs)

    def request_storage_permissions(self):
        """ Request storage permissions on Android devices. """
        if ANDROID:
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        else:
            print("Permissions are not required outside of Android.")

    def open_file_explorer(self):
        """ 
        Open a file explorer to allow the user to choose an image. 
        
        - Requests permissions if running on Android.
        - Filters for image files only.
        - Opens a popup with select and close buttons.
        - Validates file type before switching screens.
        """
        self.request_storage_permissions()

        filechooser = FileChooserIconView(
            path='/storage/emulated/0/' if ANDROID else './',
            filters=['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp', '*.tiff'],  # Allow only image files
            show_hidden=False
        )

        # Buttons for the popup
        select_button = RoundedButton(text='Select', size_hint=(1, None), height=dp(50), background_color=(0.1, 0.6, 0.8, 1))
        close_button = RoundedButton(text='Close', size_hint=(1, None), height=dp(50))

        # Layout for the popup
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(filechooser)
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(50))
        button_layout.add_widget(select_button)
        button_layout.add_widget(close_button)
        layout.add_widget(button_layout)

        # Popup window
        popup = Popup(title='Select Image', content=layout, size_hint=(0.9, 0.9))

        def select_image(instance):
            """ Handles image selection and validates file type. """
            selected_image = filechooser.selection
            if selected_image:
                image_path = selected_image[0]
                if self.is_image_file(image_path):
                    app = App.get_running_app()
                    # updating the data in the chosen image screen
                    chosenImage_screen = self.manager.get_screen('chosenImage')
                    chosenImage_screen.update_data(image_path=image_path, user_id=app.user_details.get("uid"))
                    self.manager.current = 'chosenImage'
                    popup.dismiss()
                else:
                    error_popup = FeedbackPopup(
                        title_text='Invalid file type!',
                        message_text='Please select an image file.'
                    )
                    error_popup.open()
            else:
                popup.dismiss()

        select_button.bind(on_release=select_image)
        close_button.bind(on_release=popup.dismiss)

        popup.open()

    def is_image_file(self, file_path):
        """Check if the file is a valid image."""
        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
        return any(file_path.lower().endswith(ext) for ext in valid_extensions)

    def load_otoscope_video_screen(self):
        """ Switch to the otoscope video screen. """
        self.manager.transition.duration = 0
        self.manager.current = 'otoscope'

    def go_back(self):
        """ Navigate back to the home screen. """
        self.manager.transition.duration = 0
        self.manager.current = 'home'

    def on_pre_enter(self):
        """ Update the breadcrumb navigation when entering the screen. """
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Home', 'Ear Check'])