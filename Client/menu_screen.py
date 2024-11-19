from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from rounded_button import RoundedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class MenuScreen(FloatLayout):
    def __init__(self, manager=None, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

        self.manager = manager

        # Background for the menu with rounded corners
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light grey background color
            self.background_rect = RoundedRectangle(
                size=(self.width * 0.8, self.height * 0.5),  # Adjust width and height
                pos=(self.width * 0.1, self.height * 0.25),  # Centered vertically
                radius=[(20, 20), (20, 20), (20, 20), (20, 20)]  # Rounded corners
            )

        self.bind(size=self._update_background, pos=self._update_background)

        self.option_actions = {
            "Help": self.load_help_screen,
            "About": self.load_about_screen,
            "Invite Friends": self.load_invite_friends_screen,
            "Sign Out": self.show_logout_popup,
        }

        # Add menu items
        MyAccount = RoundedButton(text='My Account', size_hint=(None, None), size=(120, 110), pos_hint={'center_x': 0.5, 'top': 1})
        MyAccount.bind(on_release=self.load_settings_screen)
        self.add_widget(MyAccount)

        # Example menu options with logo on the left
        help_option = self.create_menu_option("Help", "Icons/help.png")
        about_option = self.create_menu_option("About", "Icons/about.png")
        invite_option = self.create_menu_option("Invite Friends", "Icons/inviteFriends.png")
        signOut_option = self.create_menu_option("Sign Out", "Icons/signOut.png")

        # Add the options to the menu screen
        help_option.pos_hint = {'x': 0, 'top': 0.7}
        about_option.pos_hint = {'x': 0, 'top': 0.6}
        invite_option.pos_hint = {'x': 0, 'top': 0.5}
        signOut_option.pos_hint = {'x': 0, 'top': 0.4}

        self.add_widget(help_option)
        self.add_widget(about_option)
        self.add_widget(invite_option)
        self.add_widget(signOut_option)


    def _update_background(self, instance, value):
        """Update background position and size when the window is resized."""
        self.background_rect.size = (self.width * 1, self.height * 1)
        self.background_rect.pos = (self.width * 0, self.height * 0)

    def create_menu_option(self, option_text, logo_path):
        # Create a layout with a logo and text for each menu option
        layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=60)

        # Add the logo (aligned left)
        logo = Image(source=logo_path, size_hint=(None, None), size=(40, 40), allow_stretch=True)
        layout.add_widget(logo)

        # Add the text (button)
        button = RoundedButton(text=option_text, size_hint=(1, None), height=50,
                        font_size=18, bold=True, padding=(10, 10), border=(20, 20, 20, 20))  # Rounded button

        button.bind(on_release=self.option_actions.get(option_text, lambda x: None))  # Default action for unknown options

        layout.add_widget(button)

        return layout

    def load_help_screen(self, instance):
        self.manager.current = 'help'

    def load_settings_screen(self, instance):
        self.manager.current = 'profile'

    def load_about_screen(self, instance):
        self.manager.current = 'about'

    def load_invite_friends_screen(self, instance):
        print("Invite Friends screen loaded.")  # Load the settings screen

    def show_logout_popup(self, instance):
        # Create the layout for the popup
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        popup_label = Label(text="Are you sure you want to sign out?")
        
        # Create buttons
        button_layout = BoxLayout(size_hint=(1, 0.4), spacing=10)
        yes_button = RoundedButton(text='Yes, Sign Out', background_color=(0.9, 0.3, 0.3, 1))
        no_button = RoundedButton(text='Cancel', background_color=(0.3, 0.9, 0.3, 1))

        # Create the popup
        popup = Popup(title='Sign Out Confirmation',
                    content=popup_layout,
                    size_hint=(0.7, 0.4))

        # Bind buttons to functions
        yes_button.bind(on_release=lambda x: self.logout_callback(popup))  # Pass popup reference to callback
        no_button.bind(on_release=popup.dismiss)

        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(button_layout)

        # Show the popup
        popup.open()

    def logout_callback(self, popup):                
        # Dismiss the popup
        popup.dismiss()  # Close the popup when signing out

        self.clear_screens_except_basic()

    def clear_screens_except_basic(self):
        sm = self.manager

        screens_to_keep = ['signUp', 'login']
        screens_to_readd = []

        for screen_name in sm.screen_names:
            if screen_name in screens_to_keep:
                screens_to_readd.append(sm.get_screen(screen_name))

        sm.clear_widgets()

        for screen in screens_to_readd:
            sm.add_widget(screen)
