from kivy.uix.screenmanager import Screen
from kivy.app import App
from widgets.feedback_popup import FeedbackPopup
from config import SERVER_URL
import requests
import certifi
import threading
from kivy.clock import Clock


class UserLoginScreen(Screen):
    """
    UserLoginScreen is a Kivy screen responsible for handling user login.
    It validates user input and sends the login request to the server. 
    It also provides feedback to the user in the form of popup messages.
    """

    def __init__(self, **kwargs):
        """
        Initialize the screen and set up the UI state.
        Sets loading layout opacity to 0 and enables the login/signup buttons.
        """
        super(UserLoginScreen, self).__init__(**kwargs)
        self.is_password_visible = False # Flag to toggle password visibility
        self.ids.loading_layout.opacity = 0 # Hide loading layout initially
        self.show_btns(True) # Enable buttons (login and signup)

    def show_btns(self, op):
        """
        Toggle the enabled state of the login and signup buttons.
        :param op: Boolean that determines if buttons are enabled or disabled.
        """
        self.ids.login_btn.disabled = not op
        self.ids.signup_btn.disabled = not op

    def sign_in_func(self):
        """
        Handle the login process.
        Validates user input and sends a request to the server to authenticate.
        Displays a loading indicator while the request is being processed.
        If login is successful, stores user details and navigates to the next screen.
        If there's an error, displays the error message.
        """
        self.show_btns(False) # Disable buttons while the login request is being processed
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        # Check if email and password are empty
        if email.strip() == '' or password.strip() == '':
            popup = FeedbackPopup(
                title_text="Log In Failed",
                message_text="Please fill in all fields!"
            )
            popup.open()
            self.show_btns(True) # Re-enable buttons
            return
        
        # Define the function for handling login in a separate thread
        def sign_in_thread():
            email = self.ids.email_input.text
            password = self.ids.password_input.text

            server_url = f"{SERVER_URL}/api/login"
            data = {
                "email": email,
                "password": password
            }
            """
            Update the UI by adjusting the loading layout's opacity 
            and displaying a popup.
            """
            def update_ui(opacity, popup=None):
                def _update(dt):
                    self.ids.loading_layout.opacity = opacity
                    self.show_btns(True if opacity == 0 else False)
                    if popup:
                        popup.open()
                Clock.schedule_once(_update)

            try:
                # Show loading indicator
                Clock.schedule_once(lambda dt: setattr(self.ids.loading_layout, "opacity", 1))
                # Send login request
                response = requests.post(server_url, json=data, verify=certifi.where())
                response.raise_for_status() # Raise exception if the response status is not 200

                # Parse the response if login is successful
                user_data = response.json()

                user_id = user_data.get("uid")
                full_name = user_data.get("display_name", "User")
                email = user_data.get("email", "No Email Provided")
                gender = user_data.get("gender", "No Gender Provided")
                phone_number = user_data.get("phone_number", "No Phone Number Provided")
                results = user_data.get("results", [])

                app = App.get_running_app()
                # Store user details in the app for later use
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

                # Navigate to the next screen after successful login
                def on_success():
                    app.on_login_success()  # set screens for user
                    popup = FeedbackPopup(
                        title_text="Success",
                        message_text=f"Welcome Back, {full_name}"
                    )
                    update_ui(opacity=0, popup=popup)

                Clock.schedule_once(lambda dt: on_success())

            except requests.exceptions.HTTPError as http_err:
                # Handle HTTP errors (e.g., wrong credentials)
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
                # Handle any other errors (e.g., connection issues)
                def on_error():
                    popup = FeedbackPopup(
                        title_text="Error",
                        message_text=str(err)
                    )
                    update_ui(opacity=0, popup=popup)

                Clock.schedule_once(lambda dt: on_error())

        # Run the sign-in process in a separate thread to avoid blocking the UI
        threading.Thread(target=sign_in_thread, daemon=True).start()

    def sign_up_func(self):
        """
        Navigate to the sign-up screen.
        """
        self.manager.current = 'signUp'

    def switch_focus_to_next(self, current_field, next_field):
        """
        Switch focus from the current field to the next field.
        :param current_field: The currently focused input field.
        :param next_field: The next input field to focus on.
        """
        if current_field.focus:  # Check if the current field has focus
            next_field.focus = True

    def on_pre_enter(self):
        """
        Update the breadcrumb navigation before entering this screen.
        """
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Log In'])

    def on_enter(self):
        """
        Reset the screen state when entering the screen.
        Hide the loading indicator and enable the buttons.
        """
        self.ids.loading_layout.opacity = 0
        self.show_btns(True)

    def toggle_password_visibility(self, img_instance):
        """
        Toggle the visibility of the password.
        :param img_instance: The image instance (eye icon) used to toggle password visibility.
        """
        if self.is_password_visible:
            self.ids.password_input.password = True
            img_instance.source = "Icons/eye_close.png"
        else:
            self.ids.password_input.password = False
            img_instance.source = "Icons/eye_open.png"
        
        # Toggle the visibility state
        self.is_password_visible = not self.is_password_visible