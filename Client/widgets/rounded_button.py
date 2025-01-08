from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.image import Image
from kivy.metrics import dp

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)

        # Remove default background and set transparent background
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)  # Transparent background by default
        self.canvas.before.clear()

        # Set the initial color of the button
        self.default_color = kwargs.get('background_color', (0.3, 0.3, 0.3, 1))  # Default gray
        with self.canvas.before:
            Color(*self.default_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[(dp(25), dp(25)), (dp(25), dp(25)), (dp(25), dp(25)), (dp(25), dp(25))])

        # Handle icon (background image) for the button
        if 'background_normal' in kwargs:
            self.icon = Image(source=kwargs.get('background_normal'), size=self.size)
            self.icon.pos = self.pos
            self.add_widget(self.icon)
            self.icon.allow_stretch = True  # Stretch image to fill button
            self.icon.keep_ratio = False  # Do not maintain aspect ratio

        # Handle text properties (color, font size, etc.)
        self.color = kwargs.get('color', (1, 1, 1, 1))  # Default text color is white
        self.font_size = kwargs.get('font_size', dp(18))
        self.bold = kwargs.get('bold', True)
        self.padding = kwargs.get('padding', (dp(10), dp(10)))
        self.border = kwargs.get('border', (dp(20), dp(20), dp(20), dp(20)))

        # Apply text properties to the button
        self.font_name = "Roboto"  # Optional: you can set a specific font here if you want
        
        # Bind events for press and release
        self.bind(on_press=self.on_button_press)
        self.bind(on_release=self.on_button_release)

        # Bind the button's size and position to update the shape
        self.bind(size=self.update_rect)
        self.bind(pos=self.update_rect)

    def update_rect(self, *args):
        """ Update the position and size of the rounded rectangle when the button is resized or moved """
        self.rect.pos = self.pos
        self.rect.size = self.size

        # Update the icon's size and position to match the button's size
        if hasattr(self, 'icon'):
            self.icon.size = self.size
            self.icon.pos = self.pos

    def on_button_press(self, instance):
        """ Darken the button color when pressed """
        with self.canvas.before:
            self.canvas.before.clear()
            darker_color = tuple(max(c - 0.1, 0) for c in self.default_color[:3]) + (1,)  # Darker version of the color
            Color(*darker_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[(dp(25), dp(25)), (dp(25), dp(25)), (dp(25), dp(25)), (dp(25), dp(25))])

    def on_button_release(self, instance):
        """ Restore the original color when the button is released """
        with self.canvas.before:
            self.canvas.before.clear()
            Color(*self.default_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[(dp(25), dp(25)), (dp(25), dp(25)), (dp(25), dp(25)), (dp(25), dp(25))])
