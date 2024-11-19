from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.app import App
from datetime import datetime
from kivy.core.image import Image as CoreImage
from io import BytesIO
import requests

class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)

        self.image = None
        self.result_string = "No results yet"
        self.user_id = None

        # Layout for the screen using BoxLayout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Background color
        with self.canvas.before:
            Color(0.8, 0.8, 1, 1)  # Light blue background

        # Display image area
        self.image_display = Image(size_hint=(1, 0.4))  # Empty image initially
        self.layout.add_widget(self.image_display)

        # Result label
        self.result_label = Label(
            text=self.result_string,
            size_hint=(1, 0.2),
            halign="center",
            valign="middle",
            text_size=(self.width * 0.8, None)  # Wrap text
        )
        self.layout.add_widget(self.result_label)

        # Save button
        save_button = Button(
            text="Save",
            size_hint=(0.4, 0.1),
            pos_hint={'center_x': 0.5}  # Center the button horizontally
        )
        save_button.bind(on_release=self.save_result)  # Implement save logic
        self.layout.add_widget(save_button)

        self.add_widget(self.layout)

        # Home button
        home_btn = Button(
            background_normal="Icons/home.jpg",
            size_hint=(None, None),
            height=65,
            width=75,
            pos_hint={'x': 0, 'top': 0.1}
        )
        home_btn.bind(on_release=self.return_home)
        self.add_widget(home_btn)

    def update_data(self, image, result_string, user_id):

        self.image = image
        self.result_string = result_string
        self.user_id = user_id

        if self.image:
            image_texture = self.image.texture
            self.image_display.texture = image_texture
        self.result_label.text = self.result_string
        print(f"Data updated: {self.image}, {self.result_string}, {self.user_id}")

    def save_result(self, instance):
        # Placeholder for save logic
        print(self.result_string)
        image_path = self.image.filename
        print(self.user_id)
        print("Saving the result...")

        # Get current date and time
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Send to server
        url = 'http://localhost:5000/api/save_result'
        files = {'image': open(image_path, 'rb')}
        data = {'user_id': self.user_id, 'diagnose': 'Ear infection detected', 'datetime': current_datetime}

        try:
            response = requests.post(url, files=files, data=data)
            result_data = response.json()

            # Check if the request was successful
            if response.status_code == 200:
                # Create a new result entry
                result_key = result_data.get('result_id')  # Assuming the server returns a unique ID for the result
                new_result = {
                    'datetime': current_datetime,
                    'diagnose': 'Ear infection detected',
                    'image': result_data.get('image_url')  # Assuming the server returns the image URL
                }

                # Update app.user_details with the new result
                app = App.get_running_app()

                # Ensure user_details and results are initialized
                if app.user_details is None:
                    app.user_details = {'results': {}}
                elif app.user_details.get('results') is None:
                    app.user_details['results'] = {}

                # Now safely update results
                app.user_details['results'][result_key] = new_result

                print(f"Result saved successfully: {new_result}")
            else:
                print(f"Failed to save result: {result_data.get('message')}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            files['image'].close()  # Close the file after use

    def return_home(self, instance):
        self.manager.current = 'main'
