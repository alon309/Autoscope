from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage
from kivy.metrics import dp
from io import BytesIO
import requests
from kivy.uix.image import Image
from kivy.uix.label import Label


class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        self.history_data = []
        self.page_size = 5
        self.current_page = 0
        self.max_pages = 0

    def update_page(self):
        data_layout = self.ids.data_layout
        data_layout.clear_widgets()

        if not self.history_data:
            data_layout.add_widget(Label(text="No history available", size_hint_y=None, height=dp(40)))
            self.update_nav_buttons()
            return

        history_items = self.history_data
        start_index = self.current_page * self.page_size
        end_index = min(start_index + self.page_size, len(history_items))

        for entry in history_items[start_index:end_index]:
            date_label = Label(text=entry.get('datetime', 'Unknown'), size_hint_y=None, height=40)

            try:
                image_url = entry.get('image', '')
                if image_url:
                    img_data = requests.get(image_url).content
                    image_texture = CoreImage(BytesIO(img_data), ext='png').texture
                    image_widget = Image(size_hint=(None, None), size=(dp(100), dp(100)))
                    image_widget.texture = image_texture
                else:
                    raise ValueError("No image URL")
            except Exception:
                image_widget = Label(text="No Image", size_hint_y=None, height=dp(40))

            result_label = Label(text=entry.get('diagnose', 'No Result'), size_hint_y=None, height=dp(40))

            data_layout.add_widget(date_label)
            data_layout.add_widget(image_widget)
            data_layout.add_widget(result_label)

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
        self.history_data = history_data
        self.max_pages = (len(history_data) + self.page_size - 1) // self.page_size
        self.current_page = 0
        self.update_page()
