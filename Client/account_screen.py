from kivy.uix.screenmanager import Screen
from kivy.app import App
from feedback_popup import FeedbackPopup
from kivy.properties import StringProperty

class AccountScreen(Screen):
    hello_message = StringProperty("")

    def __init__(self, **kwargs):
        super(AccountScreen, self).__init__(**kwargs)

        app = App.get_running_app()
        self.hello_message = f"Hello {app.user_details.get('details', {}).get('Full Name', '')}!"

    def update_full_name(self, full_name):
        app = App.get_running_app()
        self.hello_message = f"Hello {app.user_details.get('details', {}).get('Full Name', '')}!"        

    def open_history(self):

        app = App.get_running_app()
        history_data = app.user_details.get('results', [])

        if not history_data:
            popup = FeedbackPopup(
                title_text="No History",
                message_text='No data to show'
            )
            return popup.open()

        history_screen = self.parent.get_screen('history')
        history_screen.update_history(history_data)
        self.manager.transition.duration = 0
        self.parent.current = 'history'

    def open_settings(self):
        self.manager.transition.duration = 0
        self.manager.current = 'settings'
    
    def open_share(self):
         self.manager.transition.duration = 0
         self.manager.current = 'shareApp'
    
    def go_back(self):
        self.manager.transition.duration = 0
        self.manager.current = 'home'        