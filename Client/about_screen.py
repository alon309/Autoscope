from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.app import App
from kivy.metrics import dp
from feedback_popup import FeedbackPopup


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
            print(f"Feedback submitted: {feedback}")
            self.ids.feedback_input.text = ""  # Clear the input field
            pupup_title = 'Feedback submitted'
            pupup_text = 'Thank you for your feedback!'
        else:
            pupup_title = 'Feedback Not submitted'
            pupup_text = 'No feedback entered!'

        popup = FeedbackPopup(
            title_text=pupup_title,
            message_text=pupup_text
        )
        popup.open()



'''
            text: "AutoScope is an innovative application designed to assist users 
                   in detecting ear infections using deep learning techniques. Our goal 
                   is to provide quick and accurate analysis of ear images to improve 
                   health outcomes for users.\\n\\n"
                   Developed by: Alon Ternerider, Nadav Goldin\\nSupervised by: Dr. Nataly Levi"
'''            
