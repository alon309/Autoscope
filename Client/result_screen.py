from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.graphics import Color

from datetime import datetime
import requests

class ResultsScreen(Screen):
    def __init__(self, image, result_string, user_id, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)

        # Store the image and result string
        self.image = image
        self.result_string = result_string
        self.user_id = user_id

        # Layout for the screen using BoxLayout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Background color
        with self.canvas.before:
            Color(0.8, 0.8, 1, 1)  # Light blue background

        # Display image area (smaller than in ChosenImageScreen)
        self.image_display = Image(size_hint=(1, 0.4))  # Use size_hint to make it responsive
        self.image_display.texture = self.image.texture  # Set the texture to the passed image object
        layout.add_widget(self.image_display)

        # Result label
        result_label = Label(
            text=self.result_string,
            size_hint=(1, 0.2),
            halign="center",
            valign="middle",
            text_size=(self.width * 0.8, None)  # Wrap text
        )
        layout.add_widget(result_label)

        # Save button
        save_button = Button(
            text="Save",
            size_hint=(0.4, 0.1),
            pos_hint={'center_x': 0.5}  # Center the button horizontally
        )
        save_button.bind(on_release=self.save_result)  # You can implement the save logic
        layout.add_widget(save_button)

        self.add_widget(layout)

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

        response = requests.post(url, files=files, data=data)
        print(response.json())




    def return_home(self, instance):
        self.parent.remove_widget(self)   
