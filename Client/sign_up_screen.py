from kivy.uix.screenmanager import Screen
from widgets.feedback_popup import FeedbackPopup
from requests.exceptions import RequestException, ConnectionError, Timeout
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.app import App
from config import SERVER_URL
import requests

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)

        # Track visibility of both password fields
        self.is_first_password_visible = False
        self.is_second_password_visible = False


    def sign_up_func(self):
        # Release keyboard on sign-up attempt
        Window.release_keyboard()

        # Get user input data
        full_name = self.ids.full_name_input.text
        email = self.ids.email_input.text
        password = self.ids.password_input.text
        phone_number = self.ids.phone_prefix.text + self.ids.phone_number_input.text
        gender = self.ids.gender_input.text
        confirm_password = self.ids.confirm_password_input.text

        # Validate that all fields are filled and that the gender is selected
        if full_name and email and password and phone_number and gender and confirm_password and gender != 'Gender':
            try:
                # Check if the passwords match
                if password != confirm_password:
                    popup = FeedbackPopup(
                        title_text="Password Not Match",
                        message_text="Passwords Not match, please try again!"
                    )
                    return popup.open()

                # Make the POST request to sign up the user
                response = requests.post(f"{SERVER_URL}/api/signup", json={
                    'full_name': full_name,
                    'email': email,
                    'password': password,
                    'phone_number': phone_number,
                    'gender': gender
                }, timeout=10)

                # Handle the response from the server
                if response.status_code == 201:
                    popup = FeedbackPopup(
                        title_text="Account Created",
                        message_text="Your account has been created successfully!",
                        callback=self.open_login_screen
                    )
                    popup.open()

                else:
                    # Show error message from the server if the creation fails
                    server_message = response.json().get("message", "An error occurred on the server!")
                    popup = FeedbackPopup(
                        title_text="Sign Up Failed",
                        message_text=f"Server error: {server_message}"
                    )
                    popup.open()

            except ConnectionError:
                # Handle connection errors
                popup = FeedbackPopup(
                    title_text="Server Unavailable",
                    message_text="Could not connect to the server. Please try again later."
                )
                popup.open()

            except Timeout:
                # Handle timeout errors
                popup = FeedbackPopup(
                    title_text="Request Timeout",
                    message_text="The server did not respond in time. Please try again later."
                )
                popup.open()

            except RequestException as e:
                # Handle any other request-related errors
                popup = FeedbackPopup(
                    title_text="Request Failed",
                    message_text=f"An error occurred: {str(e)}"
                )
                popup.open()

        else:
            # If any required field is empty, show an error popup
            popup = FeedbackPopup(
                title_text="Sign Up Failed",
                message_text="Please fill in all fields!"
            )
            popup.open()

    def open_login_screen(self):
        # Switch to the login screen after successful sign-up
        self.parent.current = "login"

    def switch_focus_to_next(self, current_field, next_field):
        """Switch focus from current field to the next."""
        if isinstance(next_field, Spinner):
            next_field.is_open = True
        elif hasattr(next_field, 'focus'):
            next_field.focus = True

    def on_pre_enter(self):
        # Update the breadcrumb trail when entering the screen
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Sign Up'])

    def toggle_password_visibility(self, img_instance, passOption):
        """
        Toggle the visibility of the password fields.
        passOption = 0 for the first password field, 1 for the second (confirmation) password.
        """
        if passOption == 0:
            if self.is_first_password_visible:
                self.ids.password_input.password = True
                img_instance.source = "Icons/eye_close.png"
            else:
                self.ids.password_input.password = False
                img_instance.source = "Icons/eye_open.png"
            
            self.is_first_password_visible = not self.is_first_password_visible

        else:
            if self.is_second_password_visible:
                self.ids.confirm_password_input.password = True
                img_instance.source = "Icons/eye_close.png"
            else:
                self.ids.confirm_password_input.password = False
                img_instance.source = "Icons/eye_open.png"
            
            self.is_second_password_visible = not self.is_second_password_visible