from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.app import App
from rounded_button import RoundedButton
from kivy.metrics import dp

from config import SERVER_URL


import requests

class ChosenImageScreen(Screen):
    def __init__(self, **kwargs):
        super(ChosenImageScreen, self).__init__(**kwargs)
        
        # Store the image or image path for later use
        self.image_path = None
        self.image = None  # This could be an image object (e.g., from the otoscope)
        self.user_id = None

        # Variable to save the Kivy image 
        self.chosen_current_image = None

        # Create a layout for the screen
        layout = FloatLayout()

        # Set the background color to blue
        with layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        # Update the rectangle size when the layout size changes
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Placeholder for the selected image (initially empty)
        self.image_display = KivyImage(size_hint=(0.8, 0.7), pos_hint={'center_x': 0.5, 'top': 0.9})
        layout.add_widget(self.image_display)

        # Create a header for the screen
        header = Label(text="Chosen Image", size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'top': 1})
        layout.add_widget(header)

        # Analysis button
        analysis_button = RoundedButton(text="Analyze", size_hint=(0.4, 0.1), pos_hint={'center_x': 0.5, 'top': 0.2}, background_color=(0.1, 0.6, 0.8, 1))
        analysis_button.bind(on_release=self.analyze_image)
        layout.add_widget(analysis_button)

        self.add_widget(layout)

        back_btn = RoundedButton(background_normal = "Icons/back.png", size_hint=(None, None), height=dp(65), width=dp(75), pos_hint={'x': 0, 'top': 0.1})
        back_btn.bind(on_release=self.close_chosenImage)
        self.add_widget(back_btn)


    def close_chosenImage(self, instance):
        self.manager.current = 'main'

    def update_data(self, image_path, user_id):
        self.image_path = image_path
        self.user_id = user_id
        self.image = None
        self.display_image()


    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def display_image(self):
        if self.image_path:
            try:
                img = CoreImage(self.image_path)
                self.image_display.texture = img.texture
                self.chosen_current_image = img
                print(f"Image loaded: {self.image_path}")
            except Exception as e:
                print(f"Error loading image: {e}")
                self.image_display.texture = None

    def analyze_image(self, instance):
        print("Analyzing the image...")
        results = "This is just an example\nDiagnosis for this image is:\nRecommendations are:"

        # Send to the server
        if self.image_path:
            try:
                print(f"Image path: {self.image_path}")

                url = f"{SERVER_URL}/api/analyze_image"

                # Open the image file in binary mode
                with open(self.image_path, 'rb') as image_file:
                    files = {'image': image_file}
                    # Ensure user_id is a string
                    data = {'user_id': str(self.user_id)}

                    # Send the POST request
                    response = requests.post(url, files=files, data=data)
                    response_data = response.json()
                    print(response_data)

                    # Update the results screen
                    results_screen = self.manager.get_screen('result')
                    results_screen.update_data(self.chosen_current_image, results, self.user_id)
                    self.manager.current = 'result'
            except Exception as e:
                print(f"Error during analysis request: {e}")



        
