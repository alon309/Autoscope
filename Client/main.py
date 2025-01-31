from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

# Importing all the screen modules used in the app
from home_screen import HomeScreen
from ear_check_screen import EarCheckScreen
from login_screen import UserLoginScreen
from about_screen import AboutScreen
from ChosenImage_screen import ChosenImageScreen
from help_screen import HelpScreen
from history_screen import HistoryScreen
from settings_screen import SettingsScreen
from result_screen import ResultsScreen
from sign_up_screen import SignUpScreen
from kivy.uix.screenmanager import NoTransition
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from otoscope_video_screen import OtoScopeVideoScreen
from share_app_screen import ShareAppScreen
from kivy.core.window import Window
from widgets.breadcrumb import Breadcrumb

# Set the window size
Window.size = (600, 700)

# This class makes images clickable by combining ButtonBehavior and Image
class ClickableImage(ButtonBehavior, Image):
    pass

# Main app class
class AutoScopeApp(App):
    def __init__(self, **kwargs):
        super(AutoScopeApp, self).__init__(**kwargs)
        
        # User details and ScreenManager initialization
        self.user_details = {} # This will store user information globally
        self.sm = ScreenManager() # ScreenManager to handle screen transitions
        self.sm.transition = NoTransition() # Set transition type (no transition for simplicity)

    def build(self):
        # Setting up breadcrumb widget (for navigation tracking) and the main layout
        self.breadcrumb = Breadcrumb(size_hint=(1, None), height=40)
        root_layout = BoxLayout(orientation='vertical')
        root_layout.add_widget(self.breadcrumb) # Add breadcrumb at the top
        root_layout.add_widget(self.sm) # Add ScreenManager for switching screens

        # Load all .kv files for different screens
        Builder.load_file("widgets/feedback.kv")
        Builder.load_file("screens/login.kv")
        Builder.load_file("screens/sign_up.kv")
        Builder.load_file("screens/home.kv")
        Builder.load_file("screens/ear_check.kv")
        Builder.load_file("screens/otoscope.kv")
        Builder.load_file("screens/chosen_image.kv")
        Builder.load_file("screens/result.kv")
        Builder.load_file("screens/history.kv")
        Builder.load_file("screens/settings.kv")
        Builder.load_file("screens/help.kv")
        Builder.load_file("screens/about.kv")
        Builder.load_file("screens/shareApp.kv")
        
        # Initial screen is UserLoginScreen
        self.sm.add_widget(UserLoginScreen(name='login'))
        # Add SignUpScreen, not activated initially
        self.sm.add_widget(SignUpScreen(name='signUp'))
        return root_layout

    # Method to handle successful login and add additional screens to the ScreenManager
    def on_login_success(self):
        
        # Define the screens to be added after login success
        screens_to_add = [
            (HomeScreen, 'home'),
            (EarCheckScreen, 'earCheck'),
            (OtoScopeVideoScreen, 'otoscope'),
            (SettingsScreen, 'settings'),
            (ResultsScreen, 'result'),
            (AboutScreen, 'about'),
            (ChosenImageScreen, 'chosenImage'),
            (HelpScreen, 'help'),
            (HistoryScreen, 'history'),
            (ShareAppScreen, "shareApp")
        ]
        
        # Loop through each screen to check if it's already added to ScreenManager
        # If not, we add it dynamically
        for screen_class, screen_name in screens_to_add:
            if screen_name not in self.sm.screen_names:
                screen_instance = screen_class(name=screen_name) # Instantiate screen
                # print(screen_name) # For debugging purposes
                self.sm.add_widget(screen_instance) # Add screen to ScreenManager
        print(f"Available screens: {self.sm.screen_names}") # List all available screens
        
        # After adding screens, set the current screen to 'home'
        self.sm.current = 'home'

# Main entry point of the app
if __name__ == '__main__':
    AutoScopeApp().run() # Run the app
