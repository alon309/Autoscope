from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from menu_screen import MenuScreen
from rounded_button import RoundedButton
from feedbackMessage import FeedbackMessage

# Check if running on Android
try:
    from android.permissions import request_permissions, Permission # type: ignore
    ANDROID = True
except ImportError:
    print("Running outside of Android. 'android.permissions' is not available.")
    ANDROID = False

# Create a clickable image
class ClickableImage(ButtonBehavior, Image):
    pass

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.feedback = FeedbackMessage()
        self.menu_open = False  # Track menu state

        # Main layout
        layout = FloatLayout()

        # Dark mode background
        with layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self._update_rect, pos=self._update_rect)

        # App logo
        otoscope_image = Image(
            source=r'Icons/otoscope.png',
            size_hint=(None, None),
            size=(dp(120), dp(120)),
            allow_stretch=True,
            pos_hint={'center_x': 0.5, 'top': 0.85}
        )
        layout.add_widget(otoscope_image)

        # Main title
        main_label = Label(
            text="Autoscope",
            font_size=dp(36),
            pos_hint={'center_x': 0.5, 'top': 1.05},
            color=(1, 1, 1, 1)
        )
        layout.add_widget(main_label)

        # Subtitle
        sec_label = Label(
            text="Early detection of ear infections",
            font_size=dp(20),
            pos_hint={'center_x': 0.5, 'top': 1},
            color=(0.8, 0.8, 0.8, 1)  # Lighter text color for subtitle
        )
        layout.add_widget(sec_label)

        # Buttons layout
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(0.9, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            spacing=dp(20)
        )

        # Take Picture button
        take_picture_button = RoundedButton(
            text='Take Picture',
            size_hint=(0.5, None),
            height=dp(60),
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        button_layout.add_widget(take_picture_button)

        # Upload Picture button
        upload_picture_button = RoundedButton(
            text='Upload Picture',
            size_hint=(0.5, None),
            height=dp(60),
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        upload_picture_button.bind(on_release=self.open_file_explorer)
        button_layout.add_widget(upload_picture_button)

        layout.add_widget(button_layout)

        # Add the menu icon as a clickable image
        self.menu_icon = ClickableImage(
            source="Icons/menu.png",
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'x': 0.05, 'top': 0.95},
            allow_stretch=True
        )

        self.menu_icon.bind(on_release=self.toggle_menu)  # Bind the click action
        layout.add_widget(self.menu_icon)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def toggle_menu(self, instance):
        if self.menu_open:
            self.remove_widget(self.menu)
            self.menu_icon.source = "Icons/menu.png"
        else:
            self.menu = MenuScreen(size_hint=(0.3, 1), pos_hint={'x': 0, 'y': 0}, manager=self.manager)
            self.add_widget(self.menu)
            self.menu_icon.source = "Icons/menu_close.png"
        self.menu_open = not self.menu_open

    def request_storage_permissions(self):
        if ANDROID:
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        else:
            print("Permissions are not required outside of Android.")

    def open_file_explorer(self, instance):
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
            selected_image = filechooser.selection
            if selected_image:
                image_path = selected_image[0]
                if self.is_image_file(image_path):
                    app = App.get_running_app()
                    choseImage_screen = self.manager.get_screen('choseImage')
                    choseImage_screen.update_data(image_path=image_path, user_id=app.user_details.get("uid"))
                    self.manager.current = 'choseImage'
                    popup.dismiss()
                else:
                    self.feedback.show_message('Invalid file type!', 'Please select an image file.', color='error')
            else:
                popup.dismiss()

        select_button.bind(on_release=select_image)
        close_button.bind(on_release=popup.dismiss)

        popup.open()

    def is_image_file(self, file_path):
        """Check if the file is a valid image."""
        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
        return any(file_path.lower().endswith(ext) for ext in valid_extensions)
