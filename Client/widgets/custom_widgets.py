from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button

# Custom TextInput with rounded corners and a custom background color
class RoundedTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0) # Transparent background
        self.foreground_color = (1, 1, 1, 1) # Text color

        # Add a rounded background color using Kivy's graphics
        with self.canvas.before:
            self.bg_color = Color(rgba=(0.1, 0.6, 0.8, 1)) # Background color (light blue)
            self.rect = RoundedRectangle(radius=[dp(15)], size=self.size, pos=self.pos)

        # Bind the widget size and position to update the background rectangle
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        """ Update the background rectangle size and position when the widget changes size or position. """
        self.rect.size = self.size
        self.rect.pos = self.pos

    def set_background_color(self, color):
        """ Set the background color of the text input. """
        self.bg_color.rgba = color


# Custom button with an icon, rounded corners, and a customizable background
class RoundedButton_(ButtonBehavior, RelativeLayout):
    text = StringProperty("Button")
    icon = StringProperty("")
    background_color = ListProperty([0.1, 0.6, 0.8, 1]) # Default background color
    text_color = ListProperty([1, 1, 1, 1]) # Default text color
    icon_size = ListProperty([dp(24), dp(24)]) # Default icon size
    font_size = NumericProperty(dp(18)) # Default font size

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.height = dp(50)
        self.width = dp(200)

        # Create the button background with rounded corners
        with self.canvas.before:
            self.bg_color = Color(rgba=self.background_color)
            self.rect = RoundedRectangle(radius=[dp(15)], size=self.size, pos=self.pos)

        # Bind properties to update on change
        self.bind(size=self.update_rect, pos=self.update_rect, background_color=self.update_color)

        # Set up the icon (if any) to be shown next to the label
        self.icon_widget = Image(
            source=self.icon,
            size_hint=(None, None),
            size=self.icon_size,
            opacity=1 if self.icon else 0, # If no icon, make it invisible
            pos_hint={"center_y": 0.5}
        )
        self.add_widget(self.icon_widget)

        # Set up the label for the button text
        self.label = Label(
            text=self.text,
            color=self.text_color,
            font_size=self.font_size,
            halign="left" if self.icon else "center", # Align left if there's an icon, otherwise center
            valign="middle",
            text_size=(self.width - (dp(40) if self.icon else 0), None),
        )
        self.add_widget(self.label)

        # Bind events to update the icon and text
        self.bind(icon=self.update_icon_visibility)
        self.bind(text=self.update_label_text)
        self.bind(font_size=self.update_label_font_size)
        self.bind(icon_size=self.update_icon_size)

    def update_rect(self, *args):
        """ Update the background rectangle size and position when the widget changes size or position. """
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_color(self, *args):
        """ Update the background color when it changes. """
        self.bg_color.rgba = self.background_color

    def update_icon_visibility(self, *args):
        """ Update the icon visibility and adjust label positioning when an icon is added or removed. """
        if self.icon:
            self.icon_widget.source = self.icon
            self.icon_widget.opacity = 1
            self.icon_widget.pos_hint = {"center_y": 0.5, "x": 0.02}
            self.label.halign = "right"
            self.label.text_size = (self.width - dp(80), None)
        else:
            self.icon_widget.opacity = 0
            self.label.halign = "center"
            self.label.text_size = (self.width, None)

    def update_icon_size(self, *args):
        """ Update the icon size when it changes. """
        self.icon_widget.size = self.icon_size

    def update_label_text(self, *args):
        """ Update the text label when the text property changes. """
        self.label.text = self.text

    def update_label_font_size(self, *args):
        """ Update the font size of the label when it changes. """
        self.label.font_size = self.font_size


# Custom button with rounded corners and a customizable background
class RoundedCostumButton(Button):
    button_color = ListProperty([0.3, 0.3, 0.3, 1]) # Default button color

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0) # Transparent background

        # Create the button background with rounded corners
        with self.canvas.before:
            self.color_instruction = Color(*self.button_color)
            self.rect = RoundedRectangle(radius=[10], size=self.size, pos=self.pos)

        # Bind properties to update on change
        self.bind(pos=self.update_rect, size=self.update_rect, button_color=self.update_color)

    def update_rect(self, *args):
        """ Update the background rectangle size and position when the widget changes size or position. """
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_color(self, *args):
        """ Update the background color when it changes. """
        self.color_instruction.rgba = self.button_color


