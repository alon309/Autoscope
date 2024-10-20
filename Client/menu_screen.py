from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.graphics import Color, Rectangle
from about_screen import AboutScreen
from help_screen import HelpScreen
from sign_out_screen import SignOutScreen
from settings_screen import SettingsScreen

class MenuScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        
        # Background for the menu
        with self.canvas.before:
            Color(0, 0, 0.5, 0.9)  # Black background with some transparency
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.option_actions = {
            "Help": self.load_help_screen,
            "Settings": self.load_settings_screen,
            "About": self.load_about_screen,
            "Invite Friends": self.load_invite_friends_screen,
            "Sign Out": self.load_sign_out_screen,
        }

        # Add menu items
        MyAccount = Button(text='My Account', size_hint=(None, None), size=(120, 110), pos_hint={'center_x': 0.5, 'top': 1})
        self.add_widget(MyAccount)

        # Example menu options with logo on the left
        help_option = self.create_menu_option("Help", "Icons/help.png")
        settings_option = self.create_menu_option("Settings", "Icons/settings.png")
        about_option = self.create_menu_option("About", "Icons/about.png")
        invite_option = self.create_menu_option("Invite Friends", "Icons/inviteFriends.png")
        signOut_option = self.create_menu_option("Sign Out", "Icons/signOut.png")

        back_btn = Button(background_normal = "Icons/back.png", size_hint=(None, None), height=65, width=75, pos_hint={'x': 0, 'top': 0.1})
        back_btn.bind(on_release=self.close_menu)

        # Add the options to the menu screen
        help_option.pos_hint = {'x': 0, 'top': 0.9}
        settings_option.pos_hint = {'x': 0, 'top': 0.8}
        about_option.pos_hint = {'x': 0, 'top': 0.7}
        invite_option.pos_hint = {'x': 0, 'top': 0.6}
        signOut_option.pos_hint = {'x': 0, 'top': 0.5}

        self.add_widget(help_option)
        self.add_widget(settings_option)
        self.add_widget(about_option)
        self.add_widget(invite_option)
        self.add_widget(signOut_option)
        self.add_widget(back_btn)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def close_menu(self, instance):
        self.parent.remove_widget(self)  # Remove the menu from the main screen

    def create_menu_option(self, option_text, logo_path):
        # Create a layout with a logo and text for each menu option
        layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)

        # Add the logo (aligned left)
        logo = Image(source=logo_path, size_hint=(None, None), size=(40, 40), allow_stretch=True)
        layout.add_widget(logo)

        # Add the text (button)
        button = Button(text=option_text, size_hint=(1, None), height=50)

        if option_text in self.option_actions:
            button.bind(on_release=self.option_actions[option_text])

        layout.add_widget(button)

        return layout

    def load_help_screen(self, instance):
        self.parent.add_widget(HelpScreen())  # Load the help screen

    def load_settings_screen(self, instance):
        self.parent.add_widget(SettingsScreen())  # Replace with actual implementation

    def load_about_screen(self, instance):
        self.parent.add_widget(AboutScreen())  # Load the About screen

    def load_invite_friends_screen(self, instance):
        print("Invite Friends screen loaded.")  # Load the settings screen

    def load_sign_out_screen(self, instance):
        self.parent.add_widget(SignOutScreen())  # Load the Sign Out screen