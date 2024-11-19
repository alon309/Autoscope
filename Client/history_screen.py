from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

from io import BytesIO  # ייבוא של BytesIO
import requests
from kivy.core.image import Image as CoreImage

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)

        # Background color
        with self.canvas.before:
            Color(0.1, 0.5, 0.8, 1)  # Blue background
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Pagination variables
        self.history_data = []  # Empty by default, updated via `update_history`
        self.page_size = 5
        self.current_page = 0
        self.max_pages = 0  # Initialize with 0 pages

        # Layout for the history entries
        self.layout = GridLayout(cols=3, spacing=10, padding=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        # Add the layout to the screen
        self.add_widget(self.layout)

        # Navigation buttons
        self.nav_layout = BoxLayout(size_hint_y=None, height=50, pos_hint={'center_x': 0.5, 'y': 0.05})
        self.prev_button = Button(text='Previous', on_release=self.prev_page)
        self.next_button = Button(text='Next', on_release=self.next_page)
        self.nav_layout.add_widget(self.prev_button)
        self.nav_layout.add_widget(self.next_button)
        self.add_widget(self.nav_layout)

        # Back Button
        back_btn = Button(text='Back', size_hint=(1, None), height=50, pos_hint={'top': 1})
        back_btn.bind(on_release=self.close_history)
        self.add_widget(back_btn)

        # Initial population
        self.update_page()

    def update_page(self):
        # Clear the current layout
        self.layout.clear_widgets()

        if not self.history_data:
            # Show a message if no data is available
            self.layout.add_widget(Label(text="No history available", size_hint_y=None, height=40))
            self.update_nav_buttons()
            return

        # Convert history_data to a list of items for slicing
        history_items = list(self.history_data.items())

        # Determine the starting and ending indices for the current page
        start_index = self.current_page * self.page_size
        end_index = min(start_index + self.page_size, len(history_items))

        # Populate the layout with history data for the current page
        for key, entry in history_items[start_index:end_index]:
            # Add date label
            date_label = Label(text=entry.get('datetime', 'Unknown'), size_hint_y=None, height=40)

            # Attempt to load image
            try:
                image_url = entry.get('image', '')
                if image_url:
                    img_data = requests.get(image_url).content
                    image_texture = CoreImage(BytesIO(img_data), ext='png').texture
                    image_widget = Image(size_hint=(None, None), size=(100, 100))
                    image_widget.texture = image_texture
                else:
                    raise ValueError("No image URL")
            except Exception as e:
                image_widget = Label(text="No Image", size_hint_y=None, height=40)

            # Add result label
            result_label = Label(text=entry.get('diagnose', 'No Result'), size_hint_y=None, height=40)

            # Add widgets to the layout
            self.layout.add_widget(date_label)
            self.layout.add_widget(image_widget)
            self.layout.add_widget(result_label)

        # Update button states
        self.update_nav_buttons()


    def update_nav_buttons(self):
        # Enable/disable navigation buttons based on the current page
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= self.max_pages - 1

    def prev_page(self, instance):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()

    def next_page(self, instance):
        if self.current_page < self.max_pages - 1:
            self.current_page += 1
            self.update_page()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def close_history(self, instance):
        self.manager.current = 'main'

    def update_history(self, history_data):
        # Update the history data and refresh the display
        self.history_data = history_data
        print(7979)
        print(history_data)
        print(7979)
        self.max_pages = (len(history_data) + self.page_size - 1) // self.page_size  # Recalculate total pages
        self.current_page = 0  # Reset to the first page
        self.update_page()
