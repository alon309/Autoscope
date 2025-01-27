from kivy.uix.screenmanager import Screen
from kivy.app import App
from widgets.feedback_popup import FeedbackPopup
from kivy.core.window import Window
from config import SERVER_URL

import requests
import certifi


class UserLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(UserLoginScreen, self).__init__(**kwargs)
        self.is_password_visible = False


    def sign_in_func(self):
        Window.release_keyboard()
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        server_url = f"{SERVER_URL}/api/login"

        data = {
            "email": email,
            "password": password
        }

        try:
            response = requests.post(server_url, json=data, verify=certifi.where())
            response.raise_for_status()

            user_data = response.json()

            user_id = user_data.get("uid")
            full_name = user_data.get("display_name", "User")
            email = user_data.get("email", "No Email Provided")
            gender = user_data.get("gender", "No Gender Provided")
            phone_number = user_data.get("phone_number", "No Phone Number Provided")
            results = user_data.get("results", [])

            app = App.get_running_app()
            app.user_details = {
                "uid": user_id,
                "details": {
                    "Full Name": full_name,
                    "Email": email,
                    "Phone Number": phone_number,
                    "gender": gender
                },
                "results": results
            }

            app.on_login_success() # set screens for user

            popup = FeedbackPopup(
                title_text="Success",
                message_text=f"Welcome Back, {full_name}"
            )
            popup.open()

        except requests.exceptions.HTTPError as http_err:
            error_details = response.json() if response.content else {}

            if isinstance(error_details, str):
                error_message = error_details
            else:
                error_message = error_details.get("error", {})
            popup = FeedbackPopup(
                title_text="Login Failed",
                 message_text=str(error_message)
            )
            popup.open()

        except Exception as err:
            popup = FeedbackPopup(
                title_text="Error",
                 message_text=str(err)
            )
            popup.open()

    def sign_up_func(self):
        self.manager.current = 'signUp'

    def switch_focus_to_next(self, current_field, next_field):
        """Switch focus from current field to the next"""
        if current_field.focus:  # Check if the current field has focus
            next_field.focus = True

    def on_pre_enter(self):
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Log In'])



    def toggle_password_visibility(self, img_instance):
        # מתפקדת להראות או להסתיר את הסיסמה
        if self.is_password_visible:
            self.ids.password_input.password = True  # להסתיר את הסיסמה
            img_instance.source = "Icons/eye_close.png"  # להחזיר לתמונה של עין סגורה
        else:
            self.ids.password_input.password = False  # להראות את הסיסמה
            img_instance.source = "Icons/eye_open.png"  # להציג תמונה של עין פתוחה
        
        self.is_password_visible = not self.is_password_visible