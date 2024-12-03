from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.graphics import Color, Rectangle
from feedback_popup import FeedbackPopup
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from config import SERVER_URL
import requests


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        # רקע למסך
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # צבע רקע כהה
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def save_settings(self):
        Window.release_keyboard()
        app = App.get_running_app()

        email = self.ids.email_input.text
        name = self.ids.name_input.text
        phone = self.ids.phone_input.text
        notifications_enabled = self.ids.notification_switch.active
        gender = self.ids.gender_input.text

        app.user_details['details'] = {
            "Full Name": name,
            "Email": email,
            "Phone Number": phone,
            "gender": gender
        }

        home_screen = self.manager.get_screen("home")
        home_screen.update_profile_image(gender)

        home_screen = self.manager.get_screen("account")
        home_screen.update_full_name(name)

        url = f"{SERVER_URL}/api/save_settings"
        data = {
            'user_id': app.user_details['uid'],
            'full_name': name,
            'email': email,
            'phone_number': phone,
            "gender": gender
        }

        try:
            response = requests.post(url, json=data)

            if response.status_code != 200:
                raise Exception(f"Server Error: {response.status_code}")

            popup = FeedbackPopup(
                title_text="Settings Saved",
                message_text=f'{email}, {name}, {phone}, Notifications: {"On" if notifications_enabled else "Off"}'
            )
            popup.open()

        except Exception as e:
            popup = FeedbackPopup(
                title_text="Failed to save settings",
                message_text=f'{str(e)}'
            )
            popup.open()

    def go_back(self):
        self.manager.current = 'account'



    def switch_focus_to_next(self, current_field, next_field):
        """Switch focus from current field to the next."""
        if isinstance(next_field, Spinner):  # אם השדה הבא הוא Spinner
            next_field.is_open = True  # פתח את ה-Spinner
            Window.release_keyboard()  # סגור את המקלדת
        elif hasattr(next_field, 'focus'):  # אם השדה הבא תומך בפוקוס
            next_field.focus = True
