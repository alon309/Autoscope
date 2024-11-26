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

        # Outer layout for the popup
        popup_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=20,
        )

        # Title label
        title_label = Label(
            text=title,
            font_size=24,
            size_hint=(1, None),
            height=40,
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1)  # White text
        )
        popup_layout.add_widget(title_label)

        # Scrollable message content
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
        popup_layout.add_widget(scroll_view)

        # Button layout
        button_layout = BoxLayout(size_hint=(1, None), height=50, spacing=10)
        ok_button = RoundedButton(
            text="OK",
            size_hint=(1, None),
            height=50,
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        button_layout.add_widget(ok_button)
        popup_layout.add_widget(button_layout)

        # Popup container
        popup = Popup(
            title='Message',
            content=popup_layout,
            size_hint=(0.7, 0.5),
            auto_dismiss=False
        )

        # Button actions
        def close_and_execute_callback(instance):
            popup.dismiss()
            if callback:
                callback()

        ok_button.bind(on_release=close_and_execute_callback)

        popup.open()

