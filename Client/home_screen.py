from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from widgets.feedback_popup import FeedbackPopup
from widgets.custom_widgets import RoundedCostumButton
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
import webview

class HomeScreen(Screen):
    # Properties to hold the user's greeting message and gender-specific image path
    hello_message = StringProperty("")
    gender_image_path = StringProperty("Icons/male.png")
    
    def __init__(self, **kwargs):
        """Initialize the screen with user-specific data like greeting message and gender image."""
        super(HomeScreen, self).__init__(**kwargs)
        app = App.get_running_app()
        # Set gender-specific image based on the user's gender
        self.gender_image_path = f"Icons/{app.user_details.get('details', {}).get('gender', '')}.png"
        # Set a personalized greeting message
        self.hello_message = f"Hello {app.user_details.get('details', {}).get('Full Name', '')}!"

    def open_video_popup(self):
        """Open the tutorial video of the application in YouTube in a popup."""
        webview.create_window('Watch Video', 'https://youtu.be/5sv_rZDjRUM')
        webview.start()

    def update_profile_image(self, gender):
        """Update the profile image based on the selected gender."""
        self.gender_image_path = f"Icons/{gender}.png"

    def open_settings(self):
        """Navigate to the settings screen."""
        self.manager.transition.duration = 0
        self.manager.current = 'settings'

    def check_ear(self):
        """Navigate to the ear check screen."""
        self.manager.transition.duration = 0
        self.manager.current = 'earCheck'

    def open_help(self):
        """Navigate to the help screen."""
        self.manager.transition.duration = 0
        self.manager.current = 'help'

    def open_about(self):
        """Navigate to the about screen."""
        self.manager.transition.duration = 0
        self.manager.current = 'about'
    
    def open_share(self):
        """Navigate to the share app screen."""
        self.manager.transition.duration = 0
        self.manager.current = 'shareApp'
    
    def open_history(self):
        """Open the history screen and update it with the user's history data."""
        app = App.get_running_app()
        history_data = app.user_details.get('results', [])

        if not history_data:
            # If no history is available, show a feedback popup
            popup = FeedbackPopup(
                title_text="No History",
                message_text='No data to show'
            )
            return popup.open()

        # If history is available, update the history screen with the data and switch to history screen
        history_screen = self.parent.get_screen('history')
        history_screen.update_history(history_data)
        self.parent.current = 'history' # switch to history screen

    def update_full_name(self):
        """Update the greeting message with the user's full name."""
        app = App.get_running_app()
        self.hello_message = f"Hello {app.user_details.get('details', {}).get('Full Name', '')}!"    

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
            color=(0, 0, 0, 1)  # Black text
        )
        confirmation_label.bind(size=confirmation_label.setter('text_size'))  # Text wrapping
        layout.add_widget(confirmation_label)

        # Buttons layout
        buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(60),
            spacing=dp(20),
            padding=[dp(10), dp(10)]
        )

        # Yes button to confirm logout
        yes_button = RoundedCostumButton(
            text="Yes",
            size_hint=(0.5, None),
            height=dp(40),
            button_color=[1, 0, 0, 1],
            halign='center',
            valign='middle'
        )
        yes_button.bind(on_release=lambda instance: self.confirm_logout(popup))
        buttons_layout.add_widget(yes_button)

        # No button to cancel logout
        no_button = RoundedCostumButton(
            text="No",
            size_hint=(0.5, None),
            height=dp(40),
            button_color=[0.5, 0.5, 0.5, 1],
            halign='center',
            valign='middle'
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
            auto_dismiss=False,  # Requires user action to close
            background='',  # Disable default background image
            background_color=(1, 1, 1, 1)  # Set background color to white (RGBA)
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

        # Identify screens to keep and re-add them to the screen manager
        for screen_name in sm.screen_names:
            if screen_name in screens_to_keep:
                screens_to_readd.append(sm.get_screen(screen_name))

        sm.clear_widgets()

        # Re-add the screens to the manager
        for screen in screens_to_readd:
            sm.add_widget(screen)

    def on_pre_enter(self):
        """Update breadcrumb navigation before entering the screen."""
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Home'])