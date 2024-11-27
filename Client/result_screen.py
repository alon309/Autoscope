from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.app import App
from datetime import datetime
from kivy.metrics import dp
from rounded_button import RoundedButton
from kivy.uix.floatlayout import FloatLayout

from config import SERVER_URL
import requests


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)

        self.image = None
        self.result_string = "No results yet"
        self.user_id = None

        self.layout = FloatLayout()

        # Background color
        with self.layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.layout.bind(size=self._update_rect, pos=self._update_rect)

        # Centered result layout
        centered_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.8, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=dp(20)
        )

        # Display image
        self.image_display = Image(
            size_hint=(1, 0.7),
            allow_stretch=True
        )
        centered_layout.add_widget(self.image_display)

        # Result label
        self.result_label = Label(
            text=self.result_string,
            size_hint=(1, 0.3),
            font_size=dp(18),
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1)
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        centered_layout.add_widget(self.result_label)

        self.layout.add_widget(centered_layout)

        # Save button
        save_button = RoundedButton(
            text="Save",
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            pos_hint={'center_x': 0.5, 'y': 0.1},
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        save_button.bind(on_release=self.save_result)
        self.layout.add_widget(save_button)

        # Home button
        home_btn = RoundedButton(
            background_normal="Icons/home.jpg",
            size_hint=(None, None),
            height=dp(65),
            width=dp(75),
            pos_hint={'x': 0, 'top': 0.1}
        )
        home_btn.bind(on_release=self.return_home)
        self.layout.add_widget(home_btn)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_data(self, image, result_string, user_id):
        self.image = image
        self.result_string = result_string
        self.user_id = user_id

        if self.image:
            self.image_display.texture = self.image.texture
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
        url = f"{SERVER_URL}/api/save_result"
        files = {'image': open(image_path, 'rb')}
        data = {'user_id': self.user_id, 'diagnose': 'Ear infection detected', 'datetime': current_datetime}

        try:
            response = requests.post(url, files=files, data=data)
            result_data = response.json()

            # Check if the request was successful
            if response.status_code == 200:
                result_key = result_data.get('result_id')  # Assuming the server returns a unique ID for the result
                new_result = {
                    'datetime': current_datetime,
                    'diagnose': 'Ear infection detected',
                    'image': result_data.get('image_url')  # Assuming the server returns the image URL
                }

                # Update app.user_details with the new result
                app = App.get_running_app()
                if app.user_details is None:
                    app.user_details = {'results': {}}
                elif app.user_details.get('results') is None:
                    app.user_details['results'] = {}

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
