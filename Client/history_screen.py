from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from rounded_button import RoundedButton

from io import BytesIO
import requests
from kivy.core.image import Image as CoreImage

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)

        # רקע
        with self.canvas.before:
            Color(0.2, 0.5, 0.8, 1)  # רקע כחול
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # פריסה ראשית
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # כפתור חזרה
        back_btn = RoundedButton(text='Back', size_hint=(1, None), height=50)
        back_btn.bind(on_release=self.close_history)
        main_layout.add_widget(back_btn)

        # אזור נתונים
        self.data_layout = GridLayout(cols=3, spacing=10, padding=10, size_hint_y=None)
        self.data_layout.bind(minimum_height=self.data_layout.setter('height'))

        # גלילה עבור הנתונים
        from kivy.uix.scrollview import ScrollView
        scroll_view = ScrollView(size_hint=(1, 0.8))
        scroll_view.add_widget(self.data_layout)
        main_layout.add_widget(scroll_view)

        # כפתורי ניווט
        self.nav_layout = BoxLayout(size_hint_y=None, height=50)
        self.prev_button = RoundedButton(text='Previous', on_release=self.prev_page)
        self.next_button = RoundedButton(text='Next', on_release=self.next_page)
        self.nav_layout.add_widget(self.prev_button)
        self.nav_layout.add_widget(self.next_button)
        main_layout.add_widget(self.nav_layout)

        # הוספת הפריסה הראשית למסך
        self.add_widget(main_layout)

        # משתני עמודים
        self.history_data = []  # רשימת נתונים ריקה כברירת מחדל
        self.page_size = 5
        self.current_page = 0
        self.max_pages = 0

        # עמוד התחלתי
        self.update_page()

    def update_page(self):
        # ניקוי נתונים קיימים
        self.data_layout.clear_widgets()

        if not self.history_data:
            self.data_layout.add_widget(Label(text="No history available", size_hint_y=None, height=40))
            self.update_nav_buttons()
            return

        # חישוב עמוד
        history_items = list(self.history_data.items())
        start_index = self.current_page * self.page_size
        end_index = min(start_index + self.page_size, len(history_items))

        for key, entry in history_items[start_index:end_index]:
            # תווית תאריך
            date_label = Label(text=entry.get('datetime', 'Unknown'), size_hint_y=None, height=40)

            # נסיון לטעון תמונה
            try:
                image_url = entry.get('image', '')
                if image_url:
                    img_data = requests.get(image_url).content
                    image_texture = CoreImage(BytesIO(img_data), ext='png').texture
                    image_widget = Image(size_hint=(None, None), size=(100, 100))
                    image_widget.texture = image_texture
                else:
                    raise ValueError("No image URL")
            except Exception:
                image_widget = Label(text="No Image", size_hint_y=None, height=40)

            # תווית תוצאה
            result_label = Label(text=entry.get('diagnose', 'No Result'), size_hint_y=None, height=40)

            # הוספת ווידג'טים
            self.data_layout.add_widget(date_label)
            self.data_layout.add_widget(image_widget)
            self.data_layout.add_widget(result_label)

        # עדכון כפתורי ניווט
        self.update_nav_buttons()

    def update_nav_buttons(self):
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
        self.history_data = history_data
        self.max_pages = (len(history_data) + self.page_size - 1) // self.page_size
        self.current_page = 0
        self.update_page()
