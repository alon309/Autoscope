from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from main_screen import MainScreen
from login_screen import UserLoginScreen


class AutoScopeApp(App):
    def build(self):
        # Create ScreenManager and add screens
        self.sm = ScreenManager()
        self.sm.add_widget(UserLoginScreen(name='login'))
        return self.sm

    def remove_all_screens(self):
        # Clear all screens from the ScreenManager
        self.sm.clear_widgets()

if __name__ == '__main__':
    AutoScopeApp().run()
