from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.graphics import Color, Rectangle, RoundedRectangle
from rounded_button import RoundedButton
from feedbackMessage import FeedbackMessage

import requests


class UserLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(UserLoginScreen, self).__init__(**kwargs)

        self.feedback = FeedbackMessage()

        layout = FloatLayout()  # Use FloatLayout for positioning

        with self.canvas.before:
            Color(0.2, 0.5, 0.8, 1)  # Background color (light blue)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect)
        self.bind(pos=self.update_rect)

        # Welcome text
        welcome_label = Label(
            text="Welcome to Autoscope",
            font_size=32,
            pos_hint={'center_x': 0.5, 'top': 0.95},
            size_hint=(None, None)
        )
        layout.add_widget(welcome_label)

        # Sign-in fields (email and password)
        self.email_input = TextInput(
            hint_text="Email",
            size_hint=(0.7, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.7},
            multiline=False
        )
        layout.add_widget(self.email_input)

        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            size_hint=(0.7, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.6},
            multiline=False
        )
        layout.add_widget(self.password_input)

        # Sign-in and Create User buttons
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(0.7, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.45},
            spacing=20
        )

        sign_in_button = RoundedButton(
            text="Sign In",
            size_hint=(0.5, None),
            height=50
        )
        sign_in_button.bind(on_release=self.sign_in_func)
        button_layout.add_widget(sign_in_button)

        create_user_button = RoundedButton(
            text="Create User",
            size_hint=(0.5, None),
            height=50
        )
        create_user_button.bind(on_release=self.sign_up_func)
        button_layout.add_widget(create_user_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def sign_in_func(self, instance):

        # email = self.email_input.text
        # password = self.password_input.text

        email = "ndvp39@gmail.com"
        password = "123123"

        server_url = "http://localhost:5000/api/login"

        data = {
            "email": email,
            "password": password
        }

        try:
            response = requests.post(server_url, json=data)
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
                "Login Successful",  # הכותרת
                f"Welcome back, {full_name}!",  # הטקסט
                color='green',  # צבע ירוק
                callback=lambda: self.open_main_screen()  # קריאה לפונקציה לאחר סגירת ההודעה
            )

        except requests.exceptions.HTTPError as http_err:
            error_details = response.json() if response.content else {}

            if isinstance(error_details, str):
                error_message = error_details
            else:
                error_message = error_details.get("error", {})
            self.feedback.show_message("Login Failed", str(error_message), color ='red')

        except Exception as err:
            self.feedback.show_message("Error", str(err), color ='red')

    def sign_up_func(self, instance):
        self.manager.current = 'signUp'    

    def open_main_screen(self):
        self.manager.current = 'main'
