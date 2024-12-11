from kivy.uix.screenmanager import Screen
from feedback_popup import FeedbackPopup
from requests.exceptions import RequestException, ConnectionError, Timeout
from kivy.metrics import dp
from kivy.uix.spinner import Spinner
from kivy.core.window import Window

from config import SERVER_URL
import requests

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)


    def sign_up_func(self):
        Window.release_keyboard()
        full_name = self.ids.full_name_input.text
        email = self.ids.email_input.text
        password = self.ids.password_input.text
        phone_number = self.ids.phone_prefix.text + self.ids.phone_number_input.text
        gender = self.ids.gender_input.text
        confirm_password = self.ids.confirm_password_input.text

        # Validate inputs
        if full_name and email and password and phone_number and gender and confirm_password and gender != 'Gender':
            try:
                if password != confirm_password:
                    popup = FeedbackPopup(
                        title_text="Password Not Match",
                        message_text="Passwords Not match, please try again!"
                    )
                    return popup.open()


                response = requests.post(f"{SERVER_URL}/api/signup", json={
                    'full_name': full_name,
                    'email': email,
                    'password': password,
                    'phone_number': phone_number,
                    'gender': gender
                }, timeout=10)

                if response.status_code == 201:

                    popup = FeedbackPopup(
                        title_text="Account Created",
                        message_text="Your account has been created successfully!",
                        callback=self.open_login_screen
                    )
                    popup.open()

                    '''self.feedback.show_message(s
                        "Account Created",
                        "Your account has been created successfully!",
                        color='success',
                        callback=self.open_login_screen
                    )'''
                else:
                    server_message = response.json().get("message", "An error occurred on the server!")
                    popup = FeedbackPopup(
                        title_text="Sign Up Failed",
                        message_text=f"Server error: {server_message}"
                    )
                    popup.open()

            except ConnectionError:
                popup = FeedbackPopup(
                    title_text="Server Unavailable",
                    message_text="Could not connect to the server. Please try again later."
                )
                popup.open()

            except Timeout:
                popup = FeedbackPopup(
                    title_text="Request Timeout",
                    message_text="The server did not respond in time. Please try again later."
                )
                popup.open()

            except RequestException as e:
                popup = FeedbackPopup(
                    title_text="Request Failed",
                    message_text=f"An error occurred: {str(e)}"
                )
                popup.open()

        else:
            popup = FeedbackPopup(
                title_text="Sign Up Failed",
                message_text="Please fill in all fields!"
            )
            popup.open()

    def open_login_screen(self):
        self.parent.current = "login"

    def switch_focus_to_next(self, current_field, next_field):
        """Switch focus from current field to the next."""
        if isinstance(next_field, Spinner):
            next_field.is_open = True
        elif hasattr(next_field, 'focus'):
            next_field.focus = True
