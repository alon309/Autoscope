from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from rounded_button import RoundedButton


class FeedbackMessage:
    def __init__(self, color='green'):
        self.color = color  # Default to green
        self.colors = {
            'red': (1, 0, 0, 1),  # Red
            'green': (0, 1, 0, 1),  # Green
            'blue': (0, 0, 1, 1),   # Blue
            'yellow': (1, 1, 0, 1),  # Yellow
        }

    def show_message(self, title, message, color=None, callback=None):
        # Determine the color for the message text
        if color:
            color_value = self.colors.get(color, (0, 1, 0, 1))
        else:
            color_value = self.colors.get(self.color, (0, 1, 0, 1))

        # Outer layout for the popup content
        popup_background = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=20,
        )

        # Title label
        title_label = Label(
            text=f"[b]{title}[/b]",
            markup=True,
            font_size=24,
            size_hint=(1, None),
            height=40,
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1)  # White text for the title
        )

        # Scrollable container for the message
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 120))
        message_label = Label(
            text=message,
            font_size=18,
            size_hint_y=None,
            halign='center',
            valign='middle',
            color=color_value,
            text_size=(400, None)  # Ensures the text wraps properly
        )
        message_label.bind(texture_size=message_label.setter('size'))
        scroll_view.add_widget(message_label)

        # Close button
        close_button = RoundedButton(
            text="Close",
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.6, 1, 1),  # Light blue button
            color=(1, 1, 1, 1)  # White text
        )

        # Layout setup
        popup_background.add_widget(title_label)
        popup_background.add_widget(scroll_view)
        popup_background.add_widget(close_button)

        # Popup container with gray rounded background
        popup = Popup(
            title="",
            content=popup_background,
            size_hint=(0.85, 0.5),
            auto_dismiss=False,
        )

        # Add a rounded gray background to the popup
        with popup.canvas.before:
            Color(0.2, 0.2, 0.2, 1)  # Dark gray background
            popup.bg = RoundedRectangle(size=popup.size, pos=popup.pos, radius=[20])
            popup.bind(size=self.update_bg, pos=self.update_bg)

        # Button callback
        def close_and_execute_callback(instance):
            popup.dismiss()
            if callback:
                callback()

        close_button.bind(on_release=close_and_execute_callback)

        popup.open()

    def update_bg(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos
