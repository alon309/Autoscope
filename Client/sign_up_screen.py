from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from main_screen import MainScreen

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)

        # Create the layout for the screen
        layout = FloatLayout()

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
            pos_hint={'center_x': 0.5, 'top': 0.85},
            multiline=False
        )
        layout.add_widget(self.full_name_input)

        # Email field
        self.email_input = TextInput(
            hint_text="Email",
            size_hint=(0.7, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.75},
            multiline=False
        )
        layout.add_widget(self.email_input)

        # Password field
        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            size_hint=(0.7, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.65},
            multiline=False
        )
        layout.add_widget(self.password_input)

        # Buttons layout
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(0.7, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.5},
            spacing=20
        )

        # Cancel button
        cancel_button = Button(
            text="Cancel",
            size_hint=(0.5, None),
            height=50
        )
        cancel_button.bind(on_release=self.return_to_login)
        button_layout.add_widget(cancel_button)

        # Sign Up button
        sign_up_button = Button(
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


    def sign_up_func(self, instance):
        # Get the full name, email, and password entered by the user
        full_name = self.full_name_input.text
        email = self.email_input.text
        password = self.password_input.text

        # Tester
        # use server functionallity here
        if full_name and email and password:
            self.show_popup("Account Created", "Your account has been created successfully!", self.open_main_screen)
        else:
            self.show_popup("Sign Up Failed", "Please fill in all fields!")

    def return_to_login(self, instance):
        self.parent.remove_widget(self)

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

    def open_main_screen(self):
        main_screen = MainScreen(name="main")
        self.parent.add_widget(main_screen)
        # Switch to the MainScreen
        self.parent.current = "main"  # This switches to the screen named "main"
