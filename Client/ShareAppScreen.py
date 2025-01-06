from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from config import SERVER_URL
import requests
from kivy.app import App
from feedback_popup import FeedbackPopup


class ShareAppScreen(Screen):
    github_link = StringProperty("https://github.com/ndvp39/autoscope")

    def share_via_email(self, recipient_email):

        if not recipient_email:

            popup = FeedbackPopup(
                title_text = "Failed",
                message_text = "App Shared failed: fill email!"
            )
            popup.open()
            return

        app = App.get_running_app()
        url = f"{SERVER_URL}/api/send_email"
        name = app.user_details.get('details', {}).get('Full Name', '')
        email_to = recipient_email
        email = app.user_details.get('details', {}).get("Email", "")
        data = {
            "email": email_to,
            "name": name,
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

        response = requests.post(url, json=data)
        if response.status_code == 200:
            title = "Success"
            text = f'App Shared successfully to: {email_to}!'
        else:
            title = "Failed"
            text = f'App Shared failed, please try again!'

        popup = FeedbackPopup(
            title_text = title,
            message_text = text
        )
        popup.open()

    def go_back(self):
        self.manager.transition.duration = 0
        self.manager.current = 'account'     