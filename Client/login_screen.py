from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from main_screen import MainScreen
from sign_up_screen import SignUpScreen

import requests


class UserLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(UserLoginScreen, self).__init__(**kwargs)

        layout = FloatLayout()  # Use FloatLayout for positioning

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

        sign_in_button = Button(
            text="Sign In",
            size_hint=(0.5, None),
            height=50
        )
        sign_in_button.bind(on_release=self.sign_in_func)
        button_layout.add_widget(sign_in_button)

        create_user_button = Button(
            text="Create User",
            size_hint=(0.5, None),
            height=50
        )
        create_user_button.bind(on_release=self.sign_up_func)
        button_layout.add_widget(create_user_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)


    def sign_in_func(self, instance):
        # קבל את הדוא"ל והסיסמה שהזין המשתמש
        email = self.email_input.text
        password = self.password_input.text

        # URL של השרת שלך שיטפל בבקשה
        server_url = "http://localhost:5000/api/login"  # שים כאן את ה-URL של השרת שלך

        # נתונים לשליחת הבקשה
        data = {
            "email": email,
            "password": password
        }

        try:
            response = requests.post(server_url, json=data)
            response.raise_for_status()  # יעלה שגיאה אם הקוד לא 200

            user_data = response.json()
            print(user_data)
            user_id = user_data.get("uid")
            self.show_popup("Login Successful", "Welcome back!", lambda: self.open_main_screen(user_id))

        except requests.exceptions.HTTPError as http_err:
            error_details = response.json() if response.content else {}
            
            # אם error_details הוא מחרוזת, השתמש בה ישירות
            if isinstance(error_details, str):
                error_message = error_details
            else:
                error_message = error_details.get("error", {})
            
            self.show_popup("Login Failed", str(error_message))

        except Exception as err:
            self.show_popup("Error", str(err))



    def sign_up_func(self, instance):
        signup_screen = SignUpScreen(name="SignUp")
        self.parent.add_widget(signup_screen)
        self.parent.current = "SignUp"
        
        
    def show_popup(self, title, message, callback=None):
        # Show a popup message to the user
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        popup_label = Label(text=message)
        popup_button = Button(text='Close', size_hint=(1, 0.25))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.7, 0.3))

        def on_close_popup(instance):
            popup.dismiss()
            if callback:
                callback()

        popup_button.bind(on_release=on_close_popup)
        popup.open()


    def open_main_screen(self, user_id):
        main_screen = MainScreen(name="main")
        main_screen.user_id = user_id  # שמור את ה-uid במסך הראשי
        self.parent.add_widget(main_screen)
        # Switch to the MainScreen
        self.parent.current = "main"  # This switches to the screen named "main"
