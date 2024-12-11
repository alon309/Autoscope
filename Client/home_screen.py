from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from custom_widgets import RoundedTextInput, RoundedButton_
from kivy.app import App
from kivy.properties import StringProperty


class HomeScreen(Screen):
    gender_image_path = StringProperty("Icons/male.png")
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
    
        app = App.get_running_app()
        self.gender_image_path = f"Icons/{app.user_details.get('details', {}).get('gender', '')}.png"




    def update_profile_image(self, gender):
        self.gender_image_path = f"Icons/{gender}.png"

    def open_my_account(self):
        self.manager.transition.duration = 0
        self.manager.current = 'account'

    def check_ear(self):
        self.manager.transition.duration = 0
        self.manager.current = 'earCheck'

    def open_help(self):
        self.manager.transition.duration = 0
        self.manager.current = 'help'

    def open_about(self):
        self.manager.transition.duration = 0
        self.manager.current = 'about'

    def logout(self):
        """Show confirmation popup before logging out."""
        # Layout for popup content
        layout = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(20))

        # Confirmation message
        confirmation_label = Label(
            text="Are you sure you want to log out?",
            halign='center',
            valign='middle',
            font_size=dp(18),
        )
        confirmation_label.bind(size=confirmation_label.setter('text_size'))  # Text wrapping
        layout.add_widget(confirmation_label)

        # Buttons layout
        buttons_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(20),
            padding=dp(20)
        )

        # Yes button
        yes_button = RoundedButton_(
            text="Yes",
            size_hint=(0.5, 2),
            background_color=(1, 0, 0, 1)
        )
        yes_button.bind(on_release=lambda instance: self.confirm_logout(popup))
        buttons_layout.add_widget(yes_button)

        # No button
        no_button = RoundedButton_(
            text="No",
            size_hint=(0.5, 2),
            background_color=(0.3, 0.3, 0.3, 1)
        )
        no_button.bind(on_release=lambda instance: popup.dismiss())
        buttons_layout.add_widget(no_button)

        # Add buttons layout to the main layout
        layout.add_widget(buttons_layout)

        # Create the popup
        popup = Popup(
            title="Confirm Logout",
            content=layout,
            size_hint=(0.8, 0.4),
            auto_dismiss=False  # Requires user action to close
        )

        popup.open()


    def confirm_logout(self, popup):
        """Handle confirmed logout."""
        popup.dismiss()
        self.clear_screens_except_basic()

    def clear_screens_except_basic(self):
        """Clear all screens except the login and signup screens."""
        sm = self.manager
        screens_to_keep = ['signUp', 'login']
        screens_to_readd = []

        for screen_name in sm.screen_names:
            if screen_name in screens_to_keep:
                screens_to_readd.append(sm.get_screen(screen_name))

        sm.clear_widgets()

        for screen in screens_to_readd:
            sm.add_widget(screen)
