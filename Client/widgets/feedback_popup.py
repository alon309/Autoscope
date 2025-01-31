from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty

# FeedbackPopup class inherits from Popup to create a custom popup
class FeedbackPopup(Popup):
    title_text = StringProperty("") # Title text of the popup, bound to a StringProperty so it can be updated dynamically
    message_text = StringProperty("") # Message text displayed in the popup, bound to a StringProperty for dynamic updates
    callback = ObjectProperty(None) # Callback function that will be executed when the popup is dismissed, bound to an ObjectProperty

    def __init__(self, **kwargs):
        # Initialize the popup with any keyword arguments passed to it
        super().__init__(**kwargs)

    # Method to dismiss the popup and execute the callback (if provided)
    def dismiss_with_callback(self):
        self.dismiss()
        if self.callback:
            self.callback()
