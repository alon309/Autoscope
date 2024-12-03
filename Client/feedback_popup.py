from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty


class FeedbackPopup(Popup):
    title_text = StringProperty("")
    message_text = StringProperty("")
    callback = ObjectProperty(None)  # פונקציה שתבוצע לאחר הסגירה

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def dismiss_with_callback(self):
        """סגירת הפופאפ וביצוע הפונקציה."""
        self.dismiss()
        if self.callback:  # אם יש callback
            self.callback()
