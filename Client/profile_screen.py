from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.uix.screenmanager import Screen
from rounded_button import RoundedButton
from feedbackMessage import FeedbackMessage

from config import SERVER_URL


import requests

class ProfileSettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfileSettingsScreen, self).__init__(**kwargs)

        self.feedback = FeedbackMessage()

        app = App.get_running_app()
        # Background color
        with self.canvas.before:
            Color(0.2, 0.5, 0.8, 1)  # Blue background
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Show History Button
        show_history_button = RoundedButton(text='Show History', size_hint=(1, None), height=50, pos_hint={'top': 0.9})
        show_history_button.bind(on_release=self.show_history)  # Bind to your history function
        self.add_widget(show_history_button)

        # Profile Settings Section
        profile_label = Label(text='Change Profile Settings', size_hint=(1, None), height=50, pos_hint={'top': 0.8})
        self.add_widget(profile_label)

        self.email_input = TextInput(text=app.user_details.get('details', {}).get("Email", ""), hint_text='Email', size_hint=(1, None), height=40, pos_hint={'top': 0.7})
        self.add_widget(self.email_input)

        self.name_input = TextInput(text=app.user_details.get('details', {}).get("Full Name", ""), hint_text='Name', size_hint=(1, None), height=40, pos_hint={'top': 0.6})
        self.add_widget(self.name_input)

        self.phone_input = TextInput(text=app.user_details.get('details', {}).get("Phone Number", ""), hint_text='Phone Number', size_hint=(1, None), height=40, pos_hint={'top': 0.5})
        self.add_widget(self.phone_input)

        # Notification Settings Section
        notification_label = Label(text='Notification Settings', size_hint=(1, None), height=50, pos_hint={'top': 0.4})
        self.add_widget(notification_label)

        self.notification_switch = Switch(active=True, size_hint=(None, None), size=(100, 50), pos_hint={'x': 0, 'top': 0.35})
        self.add_widget(self.notification_switch)

        # Submit Button
        submit_button = RoundedButton(text='Save Settings', size_hint=(1, None), height=50, pos_hint={'top': 0.2})
        submit_button.bind(on_release=self.save_settings)
        self.add_widget(submit_button)

        back_btn = RoundedButton(background_normal="Icons/back.png", size_hint=(None, None), height=65, width=75, pos_hint={'x': 0, 'top': 0.1})
        back_btn.bind(on_release=self.close_settings)
        self.add_widget(back_btn)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def save_settings(self, instance):

        email = self.email_input.text
        name = self.name_input.text
        phone = self.phone_input.text
        notifications_enabled = self.notification_switch.active

        app = App.get_running_app()
        app.user_details['details'] = {
            "Full Name": name,
            "Email": email,
            "Phone Number": phone
        }


        url = f"{SERVER_URL}/api/save_settings"
        data = {
            'user_id': app.user_details['uid'],
            'full_name': name,
            'email': email,
            'phone_number': phone
        }

        try:
            response = requests.post(url, json=data)


            if response.status_code != 200:
                raise ValueError(f"Error from server: {response.json().get('message', 'Unknown error')}")


            response_data = response.json()
            self.feedback.show_message("Settings Saved", f'{email}, {name}, {phone}, Notifications: {"On" if notifications_enabled else "Off"}')

        except Exception as e:
            self.feedback.show_message("Failed to save settings", f'{str(e)}')


    def close_settings(self, instance):
        self.manager.current = 'main'


    def show_history(self, instance):

        app = App.get_running_app()
        history_data = app.user_details.get('results', {})

        if not history_data:

            from kivy.uix.popup import Popup
            from kivy.uix.label import Label

            popup = Popup(title='Warning',
                        content=Label(text='ההיסטוריה ריקה! אין נתונים להציג.'),
                        size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        history_screen = self.parent.get_screen('history')

        print(4545)
        print(history_data)
        print(4545)
        print(history_screen)
        history_screen.update_history(history_data)

        self.parent.current = 'history'




