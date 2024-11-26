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

from config import SERVER_URL


import requests

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)

        self.feedback = FeedbackMessage()

        # Create the layout for the screen
        layout = FloatLayout()

        with self.canvas.before:
            Color(0.2, 0.5, 0.8, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect)
        self.bind(pos=self.update_rect)

        # Welcome text
        SignUp_label = Label(
            text="Create New User",
            font_size=32,
            pos_hint={'center_x': 0.5, 'top': 0.95},
            size_hint=(None, None)
        )
        layout.add_widget(SignUp_label)

        # Full Name field
        self.full_name_input = TextInput(
            hint_text="Full Name",
            size_hint=(0.7, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.75},
            multiline=False
        )
        layout.add_widget(self.full_name_input)

        # Email field
        self.email_input = TextInput(
            hint_text="Email",
            size_hint=(0.7, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.65},
            multiline=False
        )
        layout.add_widget(self.email_input)

        # Spinner for country codes
        self.country_code_spinner = Spinner(
            text="+972",  # Default to Israel
            values=["+972", "+1", "+44", "+33", "+91", "+86"],  # Add more country codes as needed
            size_hint=(0.3, None),
            height=50
        )

        # TextInput for phone number
        self.phone_input = TextInput(
            hint_text="Phone Number",
            size_hint=(0.7, None),
            height=50,
            multiline=False
        )

        # Combine spinner and phone input in a row
        phone_row = BoxLayout(
            orientation='horizontal',
            size_hint=(0.7, None),  # Match other fields' size
            height=50,
            spacing=10,
            pos_hint={'center_x': 0.5, 'top': 0.55}  # Match the vertical position of other fields
        )
        phone_row.add_widget(self.country_code_spinner)
        phone_row.add_widget(self.phone_input)
        layout.add_widget(phone_row)

        # Password field
        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            size_hint=(0.7, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.45},
            multiline=False
        )
        layout.add_widget(self.password_input)

        # Buttons layout
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(0.7, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.3},
            spacing=20
        )

        # Cancel button
        cancel_button = RoundedButton(
            text="Cancel",
            size_hint=(0.5, None),
            height=50
        )
        cancel_button.bind(on_release=self.open_login_screen_2)
        button_layout.add_widget(cancel_button)

        # Sign Up button
        sign_up_button = RoundedButton(
            text="Sign Up",
            size_hint=(0.5, None),
            height=50
        )
        sign_up_button.bind(on_release=self.sign_up_func)
        button_layout.add_widget(sign_up_button)

        # Add the buttons to the layout
        layout.add_widget(button_layout)

        # Add the layout to the screen
        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


    def sign_up_func(self, instance):
        full_name = self.full_name_input.text
        email = self.email_input.text
        password = self.password_input.text
        phone_number = self.country_code_spinner.text + self.phone_input.text

        # בדיקה אם כל השדות מלאים
        if full_name and email and password and phone_number:
            try:
                # שליחת בקשה לשרת
                response = requests.post(f"{SERVER_URL}/api/signup", json={
                    'full_name': full_name,
                    'email': email,
                    'password': password,
                    'phone_number': phone_number
                }, timeout=10)  # הגדרת מגבלת זמן של 10 שניות
                
                # בדיקה אם התגובה מהשרת הצליחה
                if response.status_code == 201:
                    self.feedback.show_message(
                        "Account Created",
                        "Your account has been created successfully!",
                        callback=self.open_login_screen
                    )
                else:
                    # טיפול בשגיאות מהשרת
                    server_message = response.json().get("message", "An error occurred on the server!")
                    self.feedback.show_message(
                        "Sign Up Failed",
                        f"Server error: {server_message}",
                        color='red'
                    )
            except ConnectionError:
                # טיפול במקרה שבו השרת לא זמין
                self.feedback.show_message(
                    "Server Unavailable",
                    "Could not connect to the server. Please try again later.",
                    color='red'
                )
            except Timeout:
                # טיפול במקרה שבו השרת לא מגיב בזמן
                self.feedback.show_message(
                    "Request Timeout",
                    "The server did not respond in time. Please try again later.",
                    color='red'
                )
            except RequestException as e:
                # טיפול בשגיאות אחרות בתקשורת
                self.feedback.show_message(
                    "Request Failed",
                    f"An error occurred: {str(e)}",
                    color='red'
                )
        else:
            # טיפול במקרה שבו השדות אינם מלאים
            self.feedback.show_message(
                "Sign Up Failed",
                "Please fill in all fields!",
                color='red'
            )


    def open_login_screen(self):
        self.parent.current = "login"  

    def open_login_screen_2(self, instance):
        self.parent.current = "login"  
