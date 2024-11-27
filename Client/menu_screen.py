from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from rounded_button import RoundedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp


class MenuScreen(FloatLayout):
    def __init__(self, manager=None, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

        self.manager = manager

        # Background for the menu with rounded corners
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.background_rect = RoundedRectangle(
                size=(self.width * 0.8, self.height * 0.7),
                pos=(self.width * 0.1, self.height * 0.15),
                radius=[(dp(20), dp(20)), (dp(20), dp(20)), (dp(20), dp(20)), (dp(20), dp(20))]
            )

        self.bind(size=self._update_background, pos=self._update_background)

    def _update_background(self, instance, value):
        """Update background position and size when the window is resized."""
        self.background_rect.size = (self.width * 0.8, self.height * 0.7)
        self.background_rect.pos = (self.width * 0.1, self.height * 0.15)

        # Redraw dividers to match the new size
        self.redraw_dividers()

    def add_menu_options(self):
        """Add menu options with dividers."""
        # Add a primary "My Account" option
        y_start = self.height * 0.75  # Start position for the first option

        self.add_menu_item(
            y_position=y_start,
            text="My Account",
            icon_path="Icons/account.png",
            callback=self.load_settings_screen,
            is_primary=True
        )

        # Other options
        options = [
            ("Help", "Icons/help.png", self.load_help_screen),
            ("About", "Icons/about.png", self.load_about_screen),
            ("Invite Friends", "Icons/inviteFriends.png", self.load_invite_friends_screen),
            ("Sign Out", "Icons/signOut.png", self.show_logout_popup),
        ]

        for index, (text, icon, callback) in enumerate(options):
            y_position = y_start - (index + 1) * 0.12 * self.height
            self.add_menu_item(y_position, text, icon, callback)

    def add_menu_item(self, y_position, text, icon_path, callback, is_primary=False):
        """Add a single menu item with a divider."""
        with self.canvas:
            # Divider line
            Color(0.8, 0.8, 0.8, 0.5)  # Light gray
            Line(
                points=[
                    self.width * 0.1, y_position + dp(10),  # Start point of the line
                    self.width * 0.9, y_position + dp(10)   # End point of the line
                ],
                width=dp(2)
            )

        # Layout for the option
        layout = BoxLayout(
            orientation="horizontal",
            size_hint=(0.8, None),
            height=dp(70) if is_primary else dp(60),
            pos=(self.width * 0.1, y_position - dp(40))
        )

        # Icon
        icon = Image(
            source=icon_path,
            size_hint=(None, None),
            size=(dp(50), dp(50)) if is_primary else (dp(40), dp(40)),
            allow_stretch=True
        )
        layout.add_widget(icon)

        # Button
        button = RoundedButton(
            text=text,
            size_hint=(1, None),
            height=dp(70) if is_primary else dp(60),
            font_size=dp(20) if is_primary else dp(18),
            bold=is_primary,
            background_color=(0.1, 0.6, 0.8, 1) if is_primary else (0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        button.bind(on_release=callback)
        layout.add_widget(button)

        self.add_widget(layout)

    def redraw_dividers(self):
        """Redraw all dividers when the menu is resized."""
        self.canvas.after.clear()
        self.add_menu_options()

    def load_help_screen(self, instance):
        self.manager.transition.duration = 0
        self.manager.current = 'help'

    def load_settings_screen(self, instance):
        self.manager.transition.duration = 0
        self.manager.current = 'profile'

    def load_about_screen(self, instance):
        self.manager.transition.duration = 0
        self.manager.current = 'about'

    def load_invite_friends_screen(self, instance):
        self.manager.transition.duration = 0
        print("Invite Friends screen loaded.")  # Load the Invite Friends screen

    def show_logout_popup(self, instance):
        """Display a popup for logout confirmation."""
        popup_layout = BoxLayout(orientation='vertical', padding=dp(10))
        popup_label = Label(text="Are you sure you want to sign out?", size_hint=(1, None), height=dp(50))

        # Buttons
        button_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        yes_button = RoundedButton(text='Yes, Sign Out', background_color=(0.1, 0.6, 0.8, 1))
        no_button = RoundedButton(text='Cancel', background_color=(0.3, 0.3, 0.3, 1))

        # Popup
        popup = Popup(
            title='Sign Out Confirmation',
            content=popup_layout,
            size_hint=(0.7, 0.4),
            auto_dismiss=False
        )

        # Button callbacks
        yes_button.bind(on_release=lambda x: self.logout_callback(popup))
        no_button.bind(on_release=popup.dismiss)

        # Add widgets to layouts
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(button_layout)

        popup.open()

    def logout_callback(self, popup):
        """Handle logout logic."""
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
