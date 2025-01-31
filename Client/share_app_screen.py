from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from config import SERVER_URL
import requests
from kivy.app import App
from widgets.feedback_popup import FeedbackPopup


class ShareAppScreen(Screen):
    # The GitHub link to the project is stored as a StringProperty for dynamic access
    github_link = StringProperty("https://github.com/ndvp39/autoscope")

    # Method to share the app via email
    def share_via_email(self, recipient_email):
        # Check if the recipient email is provided, if not show an error popup
        if not recipient_email:
            popup = FeedbackPopup(
                title_text = "Failed",
                message_text = "App Shared failed: fill email!"
            )
            popup.open()
            return

        app = App.get_running_app() # Get the running app instance
        url = f"{SERVER_URL}/api/send_email" # Define the API endpoint for sending emails

        # Get user's details like name and email
        name = app.user_details.get('details', {}).get('Full Name', '')
        email_to = recipient_email
        email = app.user_details.get('details', {}).get("Email", "")

        # Prepare the email data to send to the server
        data = {
            "to_email": email_to,
            "from_email": email,
            "subject": f"From {name} - AutoScope App!",
            "html": f"""
                        <html>
                            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                                <h2 style="color: #2c3e50;">Hi there it's {name},</h2>
                                <p>I wanted to share this awesome app with you. It might be just what you're looking for!</p>
                                <p>
                                    <a href="{self.github_link}" style="
                                        display: inline-block;
                                        background-color: #6a0dad;
                                        color: white;
                                        padding: 10px 20px;
                                        text-decoration: none;
                                        font-size: 16px;
                                        border-radius: 5px;
                                    ">Check it out now</a>
                                </p>
                                <p>If you have any questions or feedback, feel free to reach out.</p>
                                <p>Enjoy!</p>
                                <p><strong>sent from {email}.</strong><br>The AutoScope Team</p>
                            </body>
                        </html>
                        """
        }

        # Make a POST request to send the email
        response = requests.post(url, json=data)

        # Show a success or failure message depending on the response status
        if response.status_code == 200:
            title = "Success"
            text = f'App Shared successfully to:\n{email_to}!'
            self.ids.recipient_email.text = '' # Clear the email input field after success
        else:
            title = "Failed"
            text = f'App Shared failed, please try again!'

        # Show a feedback popup with the result
        popup = FeedbackPopup(
            title_text = title,
            message_text = text
        )
        popup.open()

    # Go back to the home screen without any transition animation
    def go_back(self):
        self.manager.transition.duration = 0
        self.manager.current = 'home'

    # Update the breadcrumb navigation before entering the screen
    def on_pre_enter(self):
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Home', 'Share'])

    # Handle the focus event for the email input field
    def on_focus(self, instance, value):
        # Adjust the position of the email input box when it gains or loses focus
        if value:
            self.ids.box_email.pos_hint = {'center_x': 0.5, 'y': 0.4}
        else:
            self.ids.box_email.pos_hint = {'center_x': 0.5, 'y': 0.1}