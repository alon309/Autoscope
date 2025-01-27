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
from kivy.uix.progressbar import ProgressBar

class RoundedTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.foreground_color = (1, 1, 1, 1)
        with self.canvas.before:
            self.bg_color = Color(rgba=(0.1, 0.6, 0.8, 1))
            self.rect = RoundedRectangle(radius=[dp(15)], size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def set_background_color(self, color):
        self.bg_color.rgba = color



class RoundedButton_(ButtonBehavior, RelativeLayout):
    text = StringProperty("Button")
    icon = StringProperty("")
    background_color = ListProperty([0.1, 0.6, 0.8, 1])
    text_color = ListProperty([1, 1, 1, 1])
    icon_size = ListProperty([dp(24), dp(24)])
    font_size = NumericProperty(dp(18))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.height = dp(50)
        self.width = dp(200)

        with self.canvas.before:
            self.bg_color = Color(rgba=self.background_color)
            self.rect = RoundedRectangle(radius=[dp(15)], size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect, background_color=self.update_color)

        self.icon_widget = Image(
            source=self.icon,
            size_hint=(None, None),
            size=self.icon_size,
            opacity=1 if self.icon else 0,
            pos_hint={"center_y": 0.5}
        )
        self.add_widget(self.icon_widget)


        self.label = Label(
            text=self.text,
            color=self.text_color,
            font_size=self.font_size,
            halign="left" if self.icon else "center",
            valign="middle",
            text_size=(self.width - (dp(40) if self.icon else 0), None),
        )
        self.add_widget(self.label)


        self.bind(icon=self.update_icon_visibility)
        self.bind(text=self.update_label_text)
        self.bind(font_size=self.update_label_font_size)
        self.bind(icon_size=self.update_icon_size)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_color(self, *args):
        self.bg_color.rgba = self.background_color

    def update_icon_visibility(self, *args):
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
        self.icon_widget.size = self.icon_size

    def update_label_text(self, *args):
        self.label.text = self.text

    def update_label_font_size(self, *args):
        self.label.font_size = self.font_size


class RoundedCostumButton(Button):
    button_color = ListProperty([0.3, 0.3, 0.3, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        with self.canvas.before:
            self.color_instruction = Color(*self.button_color)
            self.rect = RoundedRectangle(radius=[10], size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect, button_color=self.update_color)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_color(self, *args):
        self.color_instruction.rgba = self.button_color


