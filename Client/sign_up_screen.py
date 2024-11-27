from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from rounded_button import RoundedButton
from feedbackMessage import FeedbackMessage
from kivy.uix.spinner import Spinner
from requests.exceptions import RequestException, ConnectionError, Timeout
from kivy.metrics import dp
from config import SERVER_URL
import requests

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)

        self.feedback = FeedbackMessage()

        # Main layout
        layout = FloatLayout()

        # Dark mode background
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect)
        self.bind(pos=self.update_rect)

        # Title Label
        sign_up_label = Label(
            text="Create New User",
            font_size=dp(36),
            pos_hint={'center_x': 0.5, 'top': 0.9},
            size_hint=(None, None),
            color=(1, 1, 1, 1)  # White text
        )
        layout.add_widget(sign_up_label)

        # Full Name Field
        self.full_name_input = TextInput(
            hint_text="Full Name",
            size_hint=(0.9, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'top': 0.75},
            multiline=False,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.6, 0.6, 0.6, 1)
        )
        layout.add_widget(self.full_name_input)

        # Email Field
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

        # Phone number with spinner
        self.country_code_spinner = Spinner(
            text="+972",
            values=["+972", "+1", "+44", "+33", "+91", "+86"],
            size_hint=(0.2, None),
            height=dp(60),
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.phone_input = TextInput(
            hint_text="Phone Number",
            size_hint=(0.7, None),
            height=dp(60),
            multiline=False,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.6, 0.6, 0.6, 1)
        )
        phone_row = BoxLayout(
            orientation='horizontal',
            size_hint=(0.9, None),
            height=dp(60),
            spacing=dp(10),
            pos_hint={'center_x': 0.5, 'top': 0.55}
        )
        phone_row.add_widget(self.country_code_spinner)
        phone_row.add_widget(self.phone_input)
        layout.add_widget(phone_row)

        # Password Field
        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            size_hint=(0.9, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'top': 0.45},
            multiline=False,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.6, 0.6, 0.6, 1)
        )
        layout.add_widget(self.password_input)

        # Buttons Layout
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(0.9, None),
            height=dp(60),
            pos_hint={'center_x': 0.5, 'top': 0.3},
            spacing=dp(20)
        )

        # Cancel Button
        cancel_button = RoundedButton(
            text="Cancel",
            size_hint=(0.5, None),
            height=dp(60),
            background_color=(0.8, 0.1, 0.1, 1),
            color=(1, 1, 1, 1)
        )
        cancel_button.bind(on_release=self.open_login_screen_2)
        button_layout.add_widget(cancel_button)

        # Sign Up Button
        sign_up_button = RoundedButton(
            text="Sign Up",
            size_hint=(0.5, None),
            height=dp(60),
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        sign_up_button.bind(on_release=self.sign_up_func)
        button_layout.add_widget(sign_up_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def sign_up_func(self, instance):
        full_name = self.full_name_input.text
        email = self.email_input.text
        password = self.password_input.text
        phone_number = self.country_code_spinner.text + self.phone_input.text

        # Validate inputs
        if full_name and email and password and phone_number:
            try:
                response = requests.post(f"{SERVER_URL}/api/signup", json={
                    'full_name': full_name,
                    'email': email,
                    'password': password,
                    'phone_number': phone_number
                }, timeout=10)

                if response.status_code == 201:
                    self.feedback.show_message(
                        "Account Created",
                        "Your account has been created successfully!",
                        callback=self.open_login_screen
                    )
                else:
                    server_message = response.json().get("message", "An error occurred on the server!")
                    self.feedback.show_message(
                        "Sign Up Failed",
                        f"Server error: {server_message}",
                        color='red'
                    )
            except ConnectionError:
                self.feedback.show_message(
                    "Server Unavailable",
                    "Could not connect to the server. Please try again later.",
                    color='red'
                )
            except Timeout:
                self.feedback.show_message(
                    "Request Timeout",
                    "The server did not respond in time. Please try again later.",
                    color='red'
                )
            except RequestException as e:
                self.feedback.show_message(
                    "Request Failed",
                    f"An error occurred: {str(e)}",
                    color='red'
                )
        else:
            self.feedback.show_message(
                "Sign Up Failed",
                "Please fill in all fields!",
                color='red'
            )

    def open_login_screen(self):
        self.parent.current = "login"

    def open_login_screen_2(self, instance):
        self.parent.current = "login"
