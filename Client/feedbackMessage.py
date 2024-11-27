from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from rounded_button import RoundedButton
from kivy.metrics import dp

class FeedbackMessage:
    def __init__(self):
        # Define default colors for messages
        self.colors = {
            'error': (1, 0, 0, 1),
            'success': (0.1, 0.6, 0.8, 1)
        }

    def show_message(self, title, message, color, callback=None):
        """
        Display a popup message.
        :param title: Title of the popup.
        :param message: Message text.
        :param color_key: Key for the message color ('error' or 'success').
        :param callback: Optional callback function to execute after dismissing.
        """
        # Get color from the predefined colors or default to white
        color = self.colors.get(color, (1, 1, 1, 1))

        # Outer layout for the popup
        popup_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(20),
        )

        # Title label
        title_label = Label(
            text=title,
            font_size=dp(24),
            size_hint=(1, None),
            height=dp(40),
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1)  # Title text color
        )
        popup_layout.add_widget(title_label)

        # Scrollable message content
        scroll_view = ScrollView(size_hint=(1, None), size=(dp(400), dp(120)))
        message_label = Label(
            text=message,
            font_size=dp(18),
            size_hint_y=None,
            halign='center',
            valign='middle',
            color=color,  # Message text color
            text_size=(dp(400), None)  # Ensures the text wraps properly
        )
        message_label.bind(texture_size=message_label.setter('size'))
        scroll_view.add_widget(message_label)
        popup_layout.add_widget(scroll_view)

        # Button layout
        button_layout = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        ok_button = RoundedButton(
            text="OK",
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        button_layout.add_widget(ok_button)
        popup_layout.add_widget(button_layout)

        # Popup container
        popup = Popup(
            title='Message',
            content=popup_layout,
            size_hint=(0.8, 0.6),  # Adjust size as needed
            auto_dismiss=False
        )

        # Button actions
        def close_and_execute_callback(instance):
            popup.dismiss()
            if callback:
                callback()

        ok_button.bind(on_release=close_and_execute_callback)

        # Open the popup
        popup.open()
