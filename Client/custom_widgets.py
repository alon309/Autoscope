from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior

class RoundedTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # רקע שקוף
        self.foreground_color = (1, 1, 1, 1)  # צבע טקסט ברירת מחדל
        with self.canvas.before:
            self.bg_color = Color(rgba=(0.1, 0.6, 0.8, 1))  # צבע רקע ברירת מחדל
            self.rect = RoundedRectangle(radius=[dp(15)], size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        """עדכון גודל ומיקום של הצורה המעוגלת"""
        self.rect.size = self.size
        self.rect.pos = self.pos

    def set_background_color(self, color):
        """שנה את צבע הרקע של שדה הטקסט"""
        self.bg_color.rgba = color



from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.metrics import dp


class RoundedButton_(ButtonBehavior, RelativeLayout):
    text = StringProperty("Button")  # טקסט הכפתור
    icon = StringProperty("")  # נתיב לתמונת האייקון
    background_color = ListProperty([0.1, 0.6, 0.8, 1])  # צבע רקע ברירת מחדל
    text_color = ListProperty([1, 1, 1, 1])  # צבע טקסט ברירת מחדל
    icon_size = ListProperty([dp(24), dp(24)])  # גודל אייקון ברירת מחדל
    font_size = NumericProperty(dp(18))  # גודל טקסט ברירת מחדל

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.height = dp(50)
        self.width = dp(200)

        # רקע מעוגל
        with self.canvas.before:
            self.bg_color = Color(rgba=self.background_color)
            self.rect = RoundedRectangle(radius=[dp(15)], size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect, background_color=self.update_color)

        # אייקון
        self.icon_widget = Image(
            source=self.icon,
            size_hint=(None, None),
            size=self.icon_size,
            opacity=1 if self.icon else 0,
            pos_hint={"center_y": 0.5}
        )
        self.add_widget(self.icon_widget)

        # טקסט
        self.label = Label(
            text=self.text,
            color=self.text_color,
            font_size=self.font_size,
            halign="left" if self.icon else "center",  # יישור דינמי
            valign="middle",
            text_size=(self.width - (dp(40) if self.icon else 0), None),  # התחשבות ברוחב האייקון
        )
        self.add_widget(self.label)

        # עדכונים דינמיים
        self.bind(icon=self.update_icon_visibility)
        self.bind(text=self.update_label_text)
        self.bind(font_size=self.update_label_font_size)
        self.bind(icon_size=self.update_icon_size)

    def update_rect(self, *args):
        """עדכון מיקום וגודל של הרקע המעוגל"""
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_color(self, *args):
        """עדכון צבע הרקע"""
        self.bg_color.rgba = self.background_color

    def update_icon_visibility(self, *args):
        """עדכון אייקון והיישור בהתאם"""
        if self.icon:
            self.icon_widget.source = self.icon
            self.icon_widget.opacity = 1
            self.icon_widget.pos_hint = {"center_y": 0.5, "x": 0.02}  # מיקום אייקון
            self.label.halign = "right"  # יישור הטקסט לשמאל
            self.label.text_size = (self.width - dp(80), None)  # התאמת רוחב הטקסט
        else:
            self.icon_widget.opacity = 0
            self.label.halign = "center"  # יישור הטקסט למרכז
            self.label.text_size = (self.width, None)  # החזרת רוחב הטקסט למלא

    def update_icon_size(self, *args):
        """עדכון גודל האייקון"""
        self.icon_widget.size = self.icon_size

    def update_label_text(self, *args):
        """עדכון טקסט התווית"""
        self.label.text = self.text

    def update_label_font_size(self, *args):
        """עדכון גודל הטקסט"""
        self.label.font_size = self.font_size
