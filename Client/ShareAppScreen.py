import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class ShareAppScreen(Screen):
    github_link = StringProperty("https://github.com/ndvp39/autoscope")

    def share_via_email(self, recipient_email):
        sender_email = "market.monitor.b@gmail.com"
        sender_password = "bzys zisc foms wlkj"  # Use app-specific password for Gmail

        try:
            # Setting up the email
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg["Subject"] = "Check out this app!"
            body = f"Hi there,\n\nI thought you might like this app!\nHere's the link: {self.github_link}\n\nEnjoy!"
            msg.attach(MIMEText(body, "plain"))

            # Connect to Gmail's SMTP server
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            # Send the email
            server.send_message(msg)
            server.quit()

            self.ids.message_label.text = "Email sent successfully!"
        except Exception as e:
            self.ids.message_label.text = f"Error sending email: {e}"


    def go_back(self):
        self.manager.transition.duration = 0
        self.manager.current = 'account'     