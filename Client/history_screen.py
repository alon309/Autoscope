from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage
from kivy.metrics import dp
from io import BytesIO
import requests
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.app import App
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle


class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        self.history_data = []
        self.page_size = 10  # 10 items per page
        self.current_page = 0
        self.max_pages = 0

    def update_page(self):
        data_layout = self.ids.data_layout
        data_layout.clear_widgets()

        if not self.history_data:
            data_layout.add_widget(Label(text="No history available", size_hint_y=None, height=dp(40)))
            self.update_nav_buttons()
            return

        start_index = self.current_page * self.page_size
        end_index = min(start_index + self.page_size, len(self.history_data))
        history_items = self.history_data[start_index:end_index]

        for entry in history_items:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(100), spacing=dp(10))

            # Image widget
            try:
                image_url = entry.get('image', '')
                if image_url:
                    img_data = requests.get(image_url).content
                    image_texture = CoreImage(BytesIO(img_data), ext='png').texture
                    image_widget = Image(size_hint=(None, None), size=(dp(80), dp(80)))
                    image_widget.texture = image_texture
                else:
                    raise ValueError("No image URL")
            except Exception:
                image_widget = Label(text="No Image", size_hint=(None, None), size=(dp(80), dp(80)))

            # Result label
            result_label = Label(
                text=entry.get('diagnose', 'No Result'),
                size_hint=(0.5, 1),
                halign='center',
                valign='middle',
                color=(0, 0, 0, 1)  # Set text color to black
            )
            result_label.bind(size=result_label.setter('text_size'))

            # Date and Time labels
            datetime_str = entry.get('datetime', 'Unknown')
            try:
                date_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                date_label = Label(
                    text=date_obj.strftime('%Y-%m-%d'),
                    size_hint=(None, None),
                    size=(dp(100), dp(20)),
                    halign='center',
                    color=(0, 0, 0, 1)  # Set text color to black
                )
                time_label = Label(
                    text=date_obj.strftime('%H:%M:%S'),
                    size_hint=(None, None),
                    size=(dp(100), dp(20)),
                    halign='center',
                    color=(0, 0, 0, 1)  # Set text color to black
                )
            except ValueError:
                date_label = Label(
                    text='Unknown Date',
                    size_hint=(None, None),
                    size=(dp(100), dp(20)),
                    halign='center',
                    color=(0, 0, 0, 1)  # Set text color to black
                )
                time_label = Label(
                    text='Unknown Time',
                    size_hint=(None, None),
                    size=(dp(100), dp(20)),
                    halign='center',
                    color=(0, 0, 0, 1)  # Set text color to black
                )

            # Create a vertical layout for date and time
            datetime_layout = BoxLayout(orientation='vertical', size_hint=(None, 1), width=dp(100))
            datetime_layout.add_widget(date_label)
            datetime_layout.add_widget(time_label)

            # Adding widgets to row
            row.add_widget(image_widget)
            row.add_widget(result_label)
            row.add_widget(datetime_layout)

            # Add row to data layout
            data_layout.add_widget(row)

            # Add separator line (gray line) after each row
            separator = BoxLayout(size_hint_y=None, height=dp(2))
            separator.canvas.before.clear()  # Clear any previous drawing

            # Draw the gray line
            with separator.canvas.before:
                Color(0.5, 0.5, 0.5, 1)  # Set the color to gray
                Rectangle(size=(self.width, dp(2)), pos=(0, 0))  # Draw rectangle for the separator

            data_layout.add_widget(separator)


        self.update_nav_buttons()

    def update_nav_buttons(self):
        self.ids.prev_button.disabled = self.current_page == 0
        self.ids.next_button.disabled = self.current_page >= self.max_pages - 1

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()

    def next_page(self):
        if self.current_page < self.max_pages - 1:
            self.current_page += 1
            self.update_page()

    def go_back(self):
        self.manager.current = 'home'

    def update_history(self, history_data):
        # Sort data by date (latest first)
        self.history_data = sorted(
            history_data,
            key=lambda x: datetime.strptime(x.get('datetime', '1970-01-01 00:00:00'), '%Y-%m-%d %H:%M:%S'),
            reverse=True
        )
        self.max_pages = (len(self.history_data) + self.page_size - 1) // self.page_size
        self.current_page = 0
        self.update_page()

    def on_pre_enter(self):
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Home', 'History'])
