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
from kivy.uix.anchorlayout import AnchorLayout

class MenuScreen(FloatLayout):
    def __init__(self, manager=None, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

        self.manager = manager

        self.size_hint = (0.5, 0.8)
        self.pos_hint = {'x': -0.5}

        # Background for the menu with rounded corners
        with self.canvas.before:
            self.background_color = Color(1, 1, 1, 1)
            self.background_rect = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=[(dp(20), dp(20)), (dp(20), dp(20)), (dp(20), dp(20)), (dp(20), dp(20))]
            )

        self.bind(size=self.update_background, pos=self.update_background)
        
        self.add_menu_options()
    
    def update_background(self, *args):
        self.background_rect.size = self.size
        self.background_rect.pos = self.pos

    def add_menu_options(self):
        options_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(300),
            spacing=dp(15),
            padding=[dp(10), dp(20)]
        )

        options = [
            ("My Account", "Icons/account.png", self.load_settings_screen, (0.1, 0.6, 0.8, 1)),
            ("Help", "Icons/help.png", self.load_help_screen, (0.3, 0.3, 0.3, 1)),
            ("About", "Icons/about.png", self.load_about_screen, (0.3, 0.3, 0.3, 1)),
            ("Invite Friends", "Icons/inviteFriends.png", self.load_invite_friends_screen, (0.3, 0.3, 0.3, 1)),
            ("Sign Out", "Icons/signOut.png", self.show_logout_popup, (0.8, 0.1, 0.1, 1)),
        ]

        for text, icon_path, callback, background_color in options:
            layout = BoxLayout(
                orientation='horizontal',
                size_hint=(1, None),
                height=dp(50),
                spacing=dp(10)
            )

            icon = Image(
                source=icon_path,
                size_hint=(None, None),
                size=(dp(40), dp(40)),
                allow_stretch=True
            )
            layout.add_widget(icon)

            button = RoundedButton(
                text=text,
                size_hint=(1, None),
                height=dp(40),
                font_size=dp(14),
                background_color=background_color,
                text_size=(None, None),
                color=(1, 1, 1, 1)
            )
            button.bind(on_release=callback)
            layout.add_widget(button)

            options_layout.add_widget(layout)

        self.add_widget(options_layout)


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
        # Main layout for popup content
        popup_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 1))
        content_layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        # Label
        popup_label = Label(
            text="Are you sure you want to sign out?",
            size_hint=(1, None),
            height=dp(50),
            halign='center',
            valign='middle'
        )
        popup_label.bind(size=popup_label.setter('text_size'))

        # Buttons
        button_layout = BoxLayout(size_hint=(1, None), height=dp(60), spacing=dp(10))
        yes_button = RoundedButton(
            text='Yes, Sign Out',
            background_color=(0.1, 0.6, 0.8, 1),
            size_hint=(1, None),
            height=dp(40)
        )
        no_button = RoundedButton(
            text='Cancel',
            background_color=(0.3, 0.3, 0.3, 1),
            size_hint=(1, None),
            height=dp(40)
        )

        # Button callbacks
        yes_button.bind(on_release=lambda x: self.logout_callback(popup))
        no_button.bind(on_release=lambda x: popup.dismiss())

        # Add widgets to layouts
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        content_layout.add_widget(popup_label)
        content_layout.add_widget(button_layout)
        popup_layout.add_widget(content_layout)

        # Popup configuration
        popup = Popup(
            title='Sign Out Confirmation',
            content=popup_layout,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )

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
