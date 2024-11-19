from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from main_screen import MainScreen
from login_screen import UserLoginScreen
from about_screen import AboutScreen
from ChosenImage_screen import ChosenImageScreen
from help_screen import HelpScreen
from history_screen import HistoryScreen
from profile_screen import ProfileSettingsScreen
from result_screen import ResultsScreen
from sign_up_screen import SignUpScreen
from menu_screen import MenuScreen

class AutoScopeApp(App):
    def __init__(self, **kwargs):
        super(AutoScopeApp, self).__init__(**kwargs)
        self.user_details = {}  # Global variable accessible from all screens
        self.sm = ScreenManager()  # Global ScreenManager

    def build(self):
        # Adding initial screens
        self.sm.add_widget(UserLoginScreen(name='login'))
        self.sm.add_widget(SignUpScreen(name='signUp'))
        
        return self.sm

    def on_login_success(self):
        # Define screens to add
        screens_to_add = [
            (MainScreen, 'main'),
            (ProfileSettingsScreen, 'profile'),
            (ResultsScreen, 'result'),
            (AboutScreen, 'about'),
            (ChosenImageScreen, 'choseImage'),
            (HelpScreen, 'help'),
            (HistoryScreen, 'history')
        ]
        
        # Add all screens to the ScreenManager
        for screen_class, screen_name in screens_to_add:
            if screen_name not in self.sm.screen_names:
                screen_instance = screen_class(name=screen_name)
                print(screen_name)
                self.sm.add_widget(screen_instance)
        
        # Set the current screen
        self.sm.current = 'main'



if __name__ == '__main__':
    AutoScopeApp().run()
