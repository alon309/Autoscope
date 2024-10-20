from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label

class ChosenImageScreen(Screen):
    def __init__(self, image=None, image_path=None, **kwargs):
        super(ChosenImageScreen, self).__init__(**kwargs)
        
        # Store the image or image path for later use
        self.image_path = image_path
        self.image = image  # This could be an image object (e.g., from the otoscope)

        # Create a layout for the screen
        layout = FloatLayout()

        # Set the background color to blue
        with layout.canvas.before:
            Color(0.2, 0.6, 1, 1)  # Light blue color
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
        analysis_button = Button(text="Analyze", size_hint=(0.4, 0.1), pos_hint={'center_x': 0.5, 'top': 0.2})
        analysis_button.bind(on_release=self.analyze_image)
        layout.add_widget(analysis_button)

        self.add_widget(layout)

        # Display the image when initializing
        self.display_image()

        back_btn = Button(background_normal = "Icons/back.png", size_hint=(None, None), height=65, width=75, pos_hint={'x': 0, 'top': 0.1})
        back_btn.bind(on_release=self.close_chosenImage)
        self.add_widget(back_btn)


    def close_chosenImage(self, instance):
        self.parent.remove_widget(self)  # Remove the chosenImage screen


    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def display_image(self):
        # Check if an image object is provided or just a path
        if isinstance(self.image, KivyImage):
            # If self.image is a Kivy Image object, set its texture
            self.image_display.texture = self.image.texture
        elif isinstance(self.image_path, str):
            # If self.image_path is a string, load the image from path using CoreImage
            self.image_display.texture = CoreImage(self.image_path).texture  # Set the loaded texture

    def analyze_image(self, instance):
        # Placeholder for analysis logic
        print("Analyzing the image...")
