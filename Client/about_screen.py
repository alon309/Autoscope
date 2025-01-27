from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.metrics import dp
from widgets.feedback_popup import FeedbackPopup
from config import SERVER_URL
import requests


class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)

    def on_focus(self, instance, value):
        if value:
            self.ids.feedback_box.pos_hint = {'center_x': 0.5, 'y': 0.4}
        else:
            self.ids.feedback_box.pos_hint = {'center_x': 0.5, 'y': 0.1}

    def adjust_text_input_height(self, value):
        """Adjust the height of the TextInput based on the amount of text."""
        num_lines = len(value.split("\n")) + 1
        new_height = min(dp(150), max(dp(50), dp(25) * num_lines))
        self.ids.feedback_input.height = new_height
        self.ids.feedback_box.height = new_height

    def go_back(self):
        self.manager.current = 'home'

    def submit_feedback(self):
        feedback = self.ids.feedback_input.text
        if feedback.strip():

            app = App.get_running_app()
            url = f"{SERVER_URL}/api/send_email"
            name = app.user_details.get('details', {}).get('Full Name', '')
            email = app.user_details.get('details', {}).get("Email", "")

            data = {
                "from_email": email,
                "to_email": "market.monitor.b@gmail.com",
                "subject": f"Feedback from {name}",
                "html": f"Feedback from {name} ( {email} ): {feedback}"
            }

            response = requests.post(url, json=data)
            if response.status_code == 200:
                self.ids.feedback_input.text = ""  # Clear the input field
                pupup_title = 'Feedback submitted'
                pupup_text = 'Thank you for your feedback!'
            else:
                pupup_title = 'Feedback Not submitted'
                pupup_text = 'There was an error, please try again!'
        else:
            pupup_title = 'Feedback Not submitted'
            pupup_text = 'No feedback entered!'

        popup = FeedbackPopup(
            title_text=pupup_title,
            message_text=pupup_text
        )
        popup.open()

    def on_pre_enter(self):
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Home', 'About'])