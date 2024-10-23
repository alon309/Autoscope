from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.graphics import Color, Rectangle

class ProfileSettingsScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(ProfileSettingsScreen, self).__init__(**kwargs)

        # Background color
        with self.canvas.before:
            Color(0.1, 0.5, 0.8, 1)  # Blue background
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Show History Button
        show_history_button = Button(text='Show History', size_hint=(1, None), height=50, pos_hint={'top': 0.9})
        show_history_button.bind(on_release=self.show_history)  # Bind to your history function
        self.add_widget(show_history_button)

        # Profile Settings Section
        profile_label = Label(text='Change Profile Settings', size_hint=(1, None), height=50, pos_hint={'top': 0.8})
        self.add_widget(profile_label)

        self.email_input = TextInput(hint_text='Email', size_hint=(1, None), height=40, pos_hint={'top': 0.7})
        self.add_widget(self.email_input)

        self.name_input = TextInput(hint_text='Name', size_hint=(1, None), height=40, pos_hint={'top': 0.6})
        self.add_widget(self.name_input)

        self.phone_input = TextInput(hint_text='Phone Number', size_hint=(1, None), height=40, pos_hint={'top': 0.5})
        self.add_widget(self.phone_input)

        # Notification Settings Section
        notification_label = Label(text='Notification Settings', size_hint=(1, None), height=50, pos_hint={'top': 0.4})
        self.add_widget(notification_label)

        self.notification_switch = Switch(active=True, size_hint=(None, None), size=(100, 50), pos_hint={'x': 0, 'top': 0.35})
        self.add_widget(self.notification_switch)

        # Submit Button
        submit_button = Button(text='Save Settings', size_hint=(1, None), height=50, pos_hint={'top': 0.2})
        submit_button.bind(on_release=self.save_settings)
        self.add_widget(submit_button)

        back_btn = Button(background_normal="Icons/back.png", size_hint=(None, None), height=65, width=75, pos_hint={'x': 0, 'top': 0.1})
        back_btn.bind(on_release=self.close_settings)
        self.add_widget(back_btn)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def save_settings(self, instance):
        # Handle the saving logic here
        email = self.email_input.text
        name = self.name_input.text
        phone = self.phone_input.text
        notifications_enabled = self.notification_switch.active
        
        # You can add logic to save these settings as needed
        print(f'Settings Saved: {email}, {name}, {phone}, Notifications: {"On" if notifications_enabled else "Off"}')

    def close_settings(self, instance):
        self.parent.remove_widget(self)  # Remove the settings screen

    def show_history(self, instance):
        from history_screen import HistoryScreen
        print("history")
        history_data = [
            {'date': '2024-10-19', 'image': 'Icons/tests/1.png', 'result': 'Normal'},
            {'date': '2024-10-18', 'image': 'Icons/tests/2.png', 'result': 'Infection Detected'},
            {'date': '2024-10-17', 'image': 'Icons/tests/3.png', 'result': 'Normal'},
            {'date': '2024-10-16', 'image': 'Icons/tests/4.png', 'result': 'Minor Irritation'},
            {'date': '2024-10-15', 'image': 'Icons/tests/5.png', 'result': 'Normal'},
            {'date': '2024-10-14', 'image': 'Icons/tests/6.png', 'result': 'Infection Detected'},
            {'date': '2024-10-13', 'image': 'Icons/tests/7.png', 'result': 'Normal'},
            {'date': '2024-10-12', 'image': 'Icons/tests/8.png', 'result': 'Slight Redness'},
            {'date': '2024-10-11', 'image': 'Icons/tests/9.png', 'result': 'Normal'},
            {'date': '2024-10-10', 'image': 'Icons/tests/10.png', 'result': 'Infection Detected'},
            {'date': '2024-10-09', 'image': 'Icons/tests/11.png', 'result': 'Normal'},
            {'date': '2024-10-08', 'image': 'Icons/tests/12.png', 'result': 'Fluid Presence'},
            {'date': '2024-10-07', 'image': 'Icons/tests/13.png', 'result': 'Normal'},
        ]
        self.parent.add_widget(HistoryScreen(history_data))
