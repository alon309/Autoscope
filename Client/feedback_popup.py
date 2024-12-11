from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty


class FeedbackPopup(Popup):
    title_text = StringProperty("")
    message_text = StringProperty("")
    callback = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def dismiss_with_callback(self):
        self.dismiss()
        if self.callback:
            self.callback()
