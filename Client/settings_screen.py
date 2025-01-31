from kivy.uix.screenmanager import Screen
from kivy.app import App
from widgets.feedback_popup import FeedbackPopup
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from config import SERVER_URL
import requests


class SettingsScreen(Screen):
    # Constructor for the SettingsScreen, initializes the screen.
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

    # Save the settings entered by the user
    def save_settings(self):
        # Release the keyboard to prevent the virtual keyboard from lingering after the action
        Window.release_keyboard()

        # Get the running app instance
        app = App.get_running_app()

        # Fetch values from the input fields in the settings screen
        email = self.ids.email_input.text
        name = self.ids.name_input.text
        phone = self.ids.phone_input.text
        gender = self.ids.gender_input.text

        # Store the user details in the app's user_details dictionary
        app.user_details['details'] = {
            "Full Name": name,
            "Email": email,
            "Phone Number": phone,
            "gender": gender
        }

        # Update the home screen with the user's profile image and full name
        home_screen = self.manager.get_screen("home")
        home_screen.update_profile_image(gender) # Update profile image based on gender
        home_screen.update_full_name() # Update full name on the home screen

        # Prepare the data to send to the server
        url = f"{SERVER_URL}/api/save_settings"
        data = {
            'user_id': app.user_details['uid'],
            'full_name': name,
            'email': email,
            'phone_number': phone,
            "gender": gender
        }

        try:
            # Send the data to the server to save the settings
            response = requests.post(url, json=data)

            # Check if the response status is OK (200)
            if response.status_code != 200:
                raise Exception(f"Server Error: {response.status_code}")

            # Show a success popup if settings are saved successfully
            popup = FeedbackPopup(
                title_text="Settings Saved",
                message_text=f'Settings saved successfully'
            )
            popup.open()

        except Exception as e:
            # Show an error popup if something went wrong
            popup = FeedbackPopup(
                title_text="Failed to save settings",
                message_text=f'{str(e)}'
            )
            popup.open()

    # Go back to the previous screen (Home screen)
    def go_back(self):
        self.manager.current = 'home'

    # Switch focus from the current input field to the next field (used for form navigation)
    def switch_focus_to_next(self, current_field, next_field):
        if isinstance(next_field, Spinner):
            next_field.is_open = True
            Window.release_keyboard()
        elif hasattr(next_field, 'focus'):
            next_field.focus = True

    # Called before the screen is entered; updates the breadcrumb navigation
    def on_pre_enter(self):
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Home', 'Settings'])