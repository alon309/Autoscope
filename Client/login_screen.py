from kivy.uix.screenmanager import Screen
from kivy.app import App
from widgets.feedback_popup import FeedbackPopup
from kivy.core.window import Window
from config import SERVER_URL

import requests
import certifi
import threading
from kivy.clock import Clock


class UserLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(UserLoginScreen, self).__init__(**kwargs)
        self.is_password_visible = False
        self.ids.loading_layout.opacity = 0
        self.show_btns(True)

    def show_btns(self, op):
        self.ids.login_btn.disabled = not op
        self.ids.signup_btn.disabled = not op

    def sign_in_func(self):
        self.show_btns(False)
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        if email.strip() == '' or password.strip() == '':
            popup = FeedbackPopup(
                title_text="Log In Failed",
                message_text="Please fill in all fields!"
            )
            popup.open()
            self.show_btns(True)
            return
        
        def sign_in_thread():
            email = self.ids.email_input.text
            password = self.ids.password_input.text

            server_url = f"{SERVER_URL}/api/login"
            data = {
                "email": email,
                "password": password
            }

            def update_ui(opacity, popup=None):
                def _update(dt):
                    self.ids.loading_layout.opacity = opacity
                    self.show_btns(True if opacity == 0 else False)
                    if popup:
                        popup.open()
                Clock.schedule_once(_update)

            try:
                Clock.schedule_once(lambda dt: setattr(self.ids.loading_layout, "opacity", 1))
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

                def on_success():
                    app.on_login_success()  # set screens for user
                    popup = FeedbackPopup(
                        title_text="Success",
                        message_text=f"Welcome Back, {full_name}"
                    )
                    update_ui(opacity=0, popup=popup)

                Clock.schedule_once(lambda dt: on_success())

            except requests.exceptions.HTTPError as http_err:
                error_details = response.json() if response.content else {}

                if isinstance(error_details, str):
                    error_message = error_details
                else:
                    error_message = error_details.get("error", {})

                def on_http_error():
                    popup = FeedbackPopup(
                        title_text="Login Failed",
                        message_text=str(error_message)
                    )
                    update_ui(opacity=0, popup=popup)

                Clock.schedule_once(lambda dt: on_http_error())

            except Exception as err:
                def on_error():
                    popup = FeedbackPopup(
                        title_text="Error",
                        message_text=str(err)
                    )
                    update_ui(opacity=0, popup=popup)

                Clock.schedule_once(lambda dt: on_error())

        threading.Thread(target=sign_in_thread, daemon=True).start()

    def sign_up_func(self):
        self.manager.current = 'signUp'

    def switch_focus_to_next(self, current_field, next_field):
        """Switch focus from current field to the next"""
        if current_field.focus:  # Check if the current field has focus
            next_field.focus = True

    def on_pre_enter(self):
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Log In'])

    def on_enter(self):
        self.ids.loading_layout.opacity = 0
        self.show_btns(True)



    def toggle_password_visibility(self, img_instance):
        if self.is_password_visible:
            self.ids.password_input.password = True
            img_instance.source = "Icons/eye_close.png"
        else:
            self.ids.password_input.password = False
            img_instance.source = "Icons/eye_open.png"
        
        self.is_password_visible = not self.is_password_visible