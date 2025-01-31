from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

class Breadcrumb(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set the layout to be horizontal and customize padding and spacing
        self.orientation = 'horizontal'
        self.padding = [5, 0]
        self.spacing = 5
        self.size_hint_y = None
        self.height = 40

        # Set up the background color and border for the breadcrumb
        with self.canvas.before:
            Color(0.027, 0.929, 0.749, 1) # Background color
            self.rect = Rectangle(size=self.size, pos=self.pos)
            Color(0, 0, 0, 0.1) # Border color (with transparency)
            self.border = Rectangle(size=self.size, pos=self.pos)

        # Bind the update function to size and position changes
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        # Update the size and position of the background and border when the layout changes
        self.rect.size = self.size
        self.rect.pos = self.pos
        self.border.size = self.size
        self.border.pos = self.pos

    def update_breadcrumb(self, path):
        """
        Update the breadcrumb navigation with a list of screen names.
        
        Args:
            path (list): List of strings representing screen names in the breadcrumb path.
        """
        self.clear_widgets() # Clear previous breadcrumb items

        # Iterate over the provided screen names (path)
        for index, screen_name in enumerate(path):
            # Create a label for each screen name
            label = Label(text=screen_name, size_hint=(None, 1), width=100,
                          color=(0, 0, 0, 1), font_size=16, bold=True)
            self.add_widget(label) # Add the label to the layout

            # If it's not the last item, add an arrow icon after the label
            if index < len(path) - 1:
                arrow_icon = Image(source='./icons/right_arrow.png', size_hint=(None, None), size=(33, 33))
                self.add_widget(arrow_icon)
