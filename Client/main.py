from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

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
from kivy.uix.screenmanager import SlideTransition
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from otoscope_video_screen import OtoScopeVideoScreen
from share_app_screen import ShareAppScreen

from widgets.breadcrumb import Breadcrumb

class ClickableImage(ButtonBehavior, Image):
    pass

class AutoScopeApp(App):
    def __init__(self, **kwargs):
        super(AutoScopeApp, self).__init__(**kwargs)
        
        self.user_details = {}  # Global variable accessible from all screens
        self.sm = ScreenManager()  # Global ScreenManager
        self.sm.transition = SlideTransition()

    def build(self):

        self.breadcrumb = Breadcrumb(size_hint=(1, None), height=40)
        root_layout = BoxLayout(orientation='vertical')
        root_layout.add_widget(self.breadcrumb)
        root_layout.add_widget(self.sm)

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
        
        self.sm.add_widget(UserLoginScreen(name='login'))
        self.sm.add_widget(SignUpScreen(name='signUp'))

        
        
        return root_layout

    def on_login_success(self):
        
        # Define screens to add
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
        
        # Add all screens to the ScreenManager
        for screen_class, screen_name in screens_to_add:
            if screen_name not in self.sm.screen_names:
                screen_instance = screen_class(name=screen_name)
                print(screen_name)
                self.sm.add_widget(screen_instance)
        print(f"Available screens: {self.sm.screen_names}")
        # Set the current screen
        self.sm.current = 'home'



if __name__ == '__main__':
    AutoScopeApp().run()
