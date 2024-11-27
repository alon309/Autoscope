from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.app import App
from rounded_button import RoundedButton
from feedbackMessage import FeedbackMessage
from config import SERVER_URL
from kivy.metrics import dp
import requests
import certifi


class UserLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(UserLoginScreen, self).__init__(**kwargs)

        self.feedback = FeedbackMessage()

        layout = FloatLayout()  # Layout for dynamic positioning

        # Dark mode background
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect)
        self.bind(pos=self.update_rect)

        # Welcome label
        welcome_label = Label(
            text="Welcome to Autoscope",
            font_size=dp(40),
            pos_hint={'center_x': 0.5, 'top': 0.85},
            size_hint=(None, None),
            color=(1, 1, 1, 1)  # White text
        )
        layout.add_widget(welcome_label)

        # Email input
        self.email_input = TextInput(
            hint_text="Email",
            size_hint=(0.9, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'top': 0.65},
            multiline=False,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.6, 0.6, 0.6, 1)
        )
        layout.add_widget(self.email_input)

        # Password input
        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            size_hint=(0.9, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'top': 0.55},
            multiline=False,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.6, 0.6, 0.6, 1)
        )
        layout.add_widget(self.password_input)

        # Buttons layout
        button_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.9, None),
            height=dp(140),
            pos_hint={'center_x': 0.5, 'top': 0.4},
            spacing=dp(20)
        )

        sign_in_button = RoundedButton(
            text="Sign In",
            size_hint=(1, None),
            height=dp(60),
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)  # White text
        )
        sign_in_button.bind(on_release=self.sign_in_func)
        button_layout.add_widget(sign_in_button)

        create_user_button = RoundedButton(
            text="Create User",
            size_hint=(1, None),
            height=dp(60),
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        create_user_button.bind(on_release=self.sign_up_func)
        button_layout.add_widget(create_user_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def sign_in_func(self, instance):
        #email = self.email_input.text
        #password = self.password_input.text

        email = 'ndvp39@gmail.com'
        password = '123123'

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
            full_name = user_data.get("display_name", "Unknown")
            email = user_data.get("email", "No Email Provided")
            phone_number = user_data.get("phone_number", "No Phone Number Provided")
            results = user_data.get("results", {})

            app = App.get_running_app()
            app.user_details = {
                "uid": user_id,
                "details": {
                    "Full Name": full_name,
                    "Email": email,
                    "Phone Number": phone_number
                },
                "results": results
            }

            user_details_message = (f"User ID: {user_id}\n"
                                    f"Full Name: {full_name}\n"
                                    f"Email: {email}\n"
                                    f"Phone Number: {phone_number}")
            app.on_login_success()

            self.feedback.show_message(
                "Login Successful",
                f"Welcome back, {full_name}!",
                color='success',
                callback=lambda: self.open_main_screen()
            )

        except requests.exceptions.HTTPError as http_err:
            error_details = response.json() if response.content else {}

            if isinstance(error_details, str):
                error_message = error_details
            else:
                error_message = error_details.get("error", {})
            self.feedback.show_message("Login Failed", str(error_message), color='error')

        except Exception as err:
            print(str(err))
            self.feedback.show_message("Error", str(err), color='error')

    def sign_up_func(self, instance):
        self.manager.current = 'signUp'

    def open_main_screen(self):
        self.manager.current = 'main'
