from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from custom_widgets import RoundedTextInput, RoundedButton_


class FeedbackMessage:
    def __init__(self):
        self.colors = {
            'error': (1, 0, 0, 1),
            'success': (0.1, 0.6, 0.8, 1)
        }

    def show_message(self, title, message, color, callback=None):
        text_color = self.colors.get(color, (0, 0, 0, 1))

        # Container for the Popup content
        container = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(20),
            size_hint=(None, None),
            size=(dp(350), dp(200))
        )

        # Add rounded background to the container
        with container.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(
                size=container.size,
                pos=container.pos,
                radius=[dp(20)]
            )

        # Update background size and position dynamically
        def update_bg(*args):
            self.bg_rect.size = container.size
            self.bg_rect.pos = container.pos

        container.bind(size=update_bg, pos=update_bg)

        # Title label
        title_label = Label(
            text=title,
            font_size=dp(20),
            size_hint=(1, None),
            height=dp(30),
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        container.add_widget(title_label)

        # Message label
        message_label = Label(
            text=message,
            font_size=dp(16),
            size_hint=(1, None),
            height=dp(60),
            halign='center',
            valign='middle',
            color=text_color
        )
        container.add_widget(message_label)

        # OK Button
        ok_button = RoundedButton_(
            text="OK",
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.451, 0.969, 0.812, 1)
        )
        container.add_widget(ok_button)

        # Popup window
        popup = Popup(
            title='',
            content=container,
            size_hint=(None, None),
            size=container.size,
            auto_dismiss=False
        )

        # Button callback
        def close_and_execute_callback(instance):
            popup.dismiss()
            if callback:
                callback()

        ok_button.bind(on_release=close_and_execute_callback)

        popup.open()
