from kivy.uix.screenmanager import Screen
from kivy.app import App
from datetime import datetime
import requests
from config import SERVER_URL
from widgets.feedback_popup import FeedbackPopup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from widgets.custom_widgets import RoundedCostumButton
from kivy.properties import NumericProperty

class ResultsScreen(Screen):
    # Initializer for the screen. Sets up the default values for properties
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)

        self.progress_value = NumericProperty(0) # Used to store progress value for the progress bar
        self.image = None # Will hold the image result
        self.result_string = "No results yet" # Default result string
        self.confidence = 0 # Confidence level of the result
        self.user_id = None # User ID, to associate with the result
        self.new_result = None # Holds the new result after saving

    # Called when the screen is entered; enables the save button and resets result
    def on_enter(self):
        self.ids.save_btn.disabled = False # Enable the save button
        self.new_result = None # Reset the new result

    # Update progress bar with the given value
    def update_progress(self, value):
        self.ids.progress_bar.progress = value

    # Update the result with the image, string, confidence, and user ID
    def update_data(self, image, result, confidence, user_id):
        self.image = image
        self.result_string = result
        self.confidence = confidence
        self.user_id = user_id

        if self.image:
            self.ids.image_display.texture = self.image.texture # Display the image

        # Update the result label with the result string and confidence
        self.ids.result_label.text = f"{self.result_string} {self.confidence:.2f}%"
        self.update_progress(self.confidence) # Update progress bar with confidence
    
    # Save the result (image and diagnose) to the server
    def save_result(self):    
        if not self.image:
            # if there is no image to save
            popup = FeedbackPopup(
                title_text="Failed to save result",
                message_text="There is no image to save."
            )
            return popup.open()
        
        self.ids.save_btn.disabled = True # Disable save button while saving
        image_path = self.image.filename # Get the image file path
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Current timestamp

        url = f"{SERVER_URL}/api/save_result" # URL to send the save request
        try:
            # Open the image file and prepare the data for the request
            with open(image_path, 'rb') as image_file:
                files = {'image': image_file}
                data = {
                    'user_id': self.user_id,
                    'diagnose': f'{self.result_string}\n{self.confidence:.2f}%',
                    'datetime': current_datetime
                }

                response = requests.post(url, files=files, data=data) # Make the POST request
                
                if response.status_code != 200:
                    # Handle error if the server responds with an error code
                    popup = FeedbackPopup(
                        title_text="Failed to save result",
                        message_text=f"Server responded with error: {response.status_code}"
                    )
                    return popup.open() # Show error popup

                try:
                    result_data = response.json() # Parse the JSON response
                except ValueError:
                    # Handle case where the response is not valid JSON
                    popup = FeedbackPopup(
                        title_text="Failed to save result",
                        message_text="Invalid server response format."
                    )
                    return popup.open()

                # Store the result in the app's user details
                app = App.get_running_app()
                self.new_result = {
                    'diagnose': f'{self.result_string}\n{self.confidence:.2f}%',
                    'image': result_data.get('image'),
                    'datetime': current_datetime
                }

                # Add the new result to the user's history
                if 'results' not in app.user_details or not isinstance(app.user_details['results'], list):
                    app.user_details['results'] = []
                app.user_details['results'].append(self.new_result)

                # Show success message in popup
                popup = FeedbackPopup(
                    title_text="Result saved successfully",
                    message_text="Result saved successfully!\nyou can see the result in your history."
                )
                popup.open()

        except requests.RequestException as req_err:
            # Handle network error
            popup = FeedbackPopup(
                title_text="Failed to save result",
                message_text="Network error occurred, please try again."
            )
            popup.open()

        except Exception as e:
            # Handle other unexpected errors
            popup = FeedbackPopup(
                title_text="Failed to save result",
                message_text="An unexpected error occurred."
            )
            popup.open()

    # Go back to the previous screen
    def go_back(self):
        self.manager.current = 'earCheck'

    # Update breadcrumb navigation when entering this screen
    def on_pre_enter(self):
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Home', 'Ear Check', 'Analyze', 'Result'])

    # Share the result by email
    def share_result(self):
        app = App.get_running_app()
        url = f"{SERVER_URL}/api/send_email"
        name = app.user_details.get('details', {}).get('Full Name', '')
        email = app.user_details.get('details', {}).get("Email", "")
        
        # Check if the result is ready to be shared (if it already saved)
        if not self.new_result or not self.new_result.get('image') or not self.new_result.get('datetime') or not self.new_result.get('diagnose'):
            popup = FeedbackPopup(
                title_text='Failed',
                message_text='Please Save result before sharing!'
            )
            return popup.open()

        # Prepare the content for the email
        image_url = f"{self.new_result['image']}?alt=media"
        datetime = f"{self.new_result['datetime']}"
        diagnose = f"{self.new_result['diagnose']}"

        # Create a popup for the user to input the recipient's email
        email_popup = Popup(
            title="Enter Email Address",
            size_hint=(None, None),
            size=(400, 200),
            auto_dismiss=False,  # Requires user action to close
            background='',  # Disable default background image
            background_color=(1, 1, 1, 1)  # Set background color to white (RGBA)
        )

        content = BoxLayout(orientation="vertical", padding=20, spacing=10)
        email_input = TextInput(hint_text="Enter email to share with", size_hint=(1, None), height=40, multiline=False)
        content.add_widget(email_input)
        buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        # Cancel button
        cancel_button = RoundedCostumButton(text="Cancel", button_color=[0.3, 0.3, 0.3, 1], on_press=email_popup.dismiss)
        buttons_layout.add_widget(cancel_button)

        # Send button and its action
        def on_send(instance):
            email_to = email_input.text.strip() # Get the email entered by the user
            
            if not email_to:
                email_input.hint_text = "Please enter a valid email"
                return # Don't proceed if email is empty

            email_popup.dismiss() # Close the popup

            # Prepare the email data
            data = {
                "to_email": email_to,
                "from_email": email,
                "subject": f"From {name} - AutoScope App!",
                "html": f"""
                            <html>
                                <body style="font-family: Arial, sans-serif; line-height: 1.6; background-color: #f4f4f9; padding: 20px;">
                                    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                                        <h2 style="color: #2c3e50;">Hi there, it's {name}!</h2>
                                        <p style="font-size: 16px; color: #34495e;">I wanted to share my results with you.</p>
                                        
                                        <div style="text-align: center; margin-top: 20px;">
                                            <img src="{image_url}" alt="Ear Image" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                                        </div>

                                        <p style="font-size: 16px; color: #34495e; margin-top: 20px;">My Ear Diagnoses is: {diagnose} ({datetime})</p>

                                    </div>
                                </body>
                            </html>
                        """
            }
            
            # Send the email via the server
            response = requests.post(url, json=data)
            if response.status_code == 200:
                title = "Success"
                text = f'Result Shared successfully to:\n{email_to}!'
            else:
                title = "Failed"
                text = f'Result Shared failed, please try again!'

            popup = FeedbackPopup(
                title_text=title,
                message_text=text
            )
            popup.open()
        
        # Add the send button
        send_button = RoundedCostumButton(text="Send", button_color=[0.1, 0.6, 0.8, 1], on_press=on_send)
        buttons_layout.add_widget(send_button)
        
        content.add_widget(buttons_layout)
        email_popup.add_widget(content)
        email_popup.open()
