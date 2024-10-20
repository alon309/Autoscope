from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.switch import Switch
from kivy.graphics import Color, Rectangle


class SettingsScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        # Background color
        with self.canvas.before:
            Color(0.1, 0.5, 0.8, 1)  # Blue background
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Profile Settings Section
        profile_label = Label(text='Profile Settings', size_hint=(1, None), height=50, pos_hint={'top': 1})
        self.add_widget(profile_label)

        self.email_input = TextInput(hint_text='Email', size_hint=(1, None), height=40, pos_hint={'top': 0.9})
        self.add_widget(self.email_input)

        self.name_input = TextInput(hint_text='Name', size_hint=(1, None), height=40, pos_hint={'top': 0.85})
        self.add_widget(self.name_input)

        self.phone_input = TextInput(hint_text='Phone Number', size_hint=(1, None), height=40, pos_hint={'top': 0.8})
        self.add_widget(self.phone_input)

        # Add Kids Section
        kids_label = Label(text='Add Kids', size_hint=(1, None), height=30, pos_hint={'top': 0.75})
        self.add_widget(kids_label)

        self.kids_count_input = TextInput(hint_text='Number of Kids', size_hint=(1, None), height=40, pos_hint={'top': 0.7})
        self.add_widget(self.kids_count_input)

        # Notification Settings Section
        notification_label = Label(text='Notification Settings', size_hint=(1, None), height=50, pos_hint={'top': 0.65})
        self.add_widget(notification_label)

        self.notification_switch = Switch(active=True, size_hint=(None, None), size=(100, 50), pos_hint={'x': 0, 'top': 0.6})
        self.add_widget(self.notification_switch)

        notification_text = Label(text='Enable Notifications', size_hint=(None, None), size=(200, 50), pos_hint={'x': 0.5, 'top': 0.6})
        self.add_widget(notification_text)

        # Submit Button
        submit_button = Button(text='Save Settings', size_hint=(1, None), height=50, pos_hint={'top': 0.55})
        submit_button.bind(on_release=self.save_settings)
        self.add_widget(submit_button)

        back_btn = Button(background_normal = "Icons/back.png", size_hint=(None, None), height=65, width=75, pos_hint={'x': 0, 'top': 0.1})
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
        kids_count = self.kids_count_input.text
        notifications_enabled = self.notification_switch.active
        
        # You can add logic to save these settings as needed
        print(f'Settings Saved: {email}, {name}, {phone}, Kids: {kids_count}, Notifications: {"On" if notifications_enabled else "Off"}')

    def close_settings(self, instance):
        self.parent.remove_widget(self)  # Remove the settings screen
