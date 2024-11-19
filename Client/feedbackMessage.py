from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from rounded_button import RoundedButton

class FeedbackMessage:
    def __init__(self, color='green'):
        self.color = color  # ברירת מחדל לצבע ירוק
        self.colors = {
            'red': (1, 0, 0, 1),  # אדום
            'green': (0, 1, 0, 1),  # ירוק
            'blue': (0, 0, 1, 1),   # כחול
            'yellow': (1, 1, 0, 1)  # צהוב
        }

    def show_message(self, title, message, color=None, callback=None):

        if color:
            color_value = self.colors.get(color, (0, 1, 0, 1))
        else:
            color_value = self.colors.get(self.color, (0, 1, 0, 1))

        layout = BoxLayout(orientation='vertical', padding=10)

        title_label = Label(text=title, font_size=24, bold=True, color=(1, 1, 1, 1))

        label = Label(text=message, font_size=20, color=color_value)

        close_button = RoundedButton(text='Close', size_hint=(1, None), height=50)

        close_button.background_radius = [15]

        layout.add_widget(title_label)
        layout.add_widget(label)
        layout.add_widget(close_button)

        popup = Popup(title='', content=layout, size_hint=(0.8, 0.4), background_color=(1, 1, 1, 1))
        popup.background_radius = [15]

        def close_and_execute_callback(instance):
            popup.dismiss()
            if callback:
                callback()

        close_button.bind(on_release=close_and_execute_callback)

        popup.open()
