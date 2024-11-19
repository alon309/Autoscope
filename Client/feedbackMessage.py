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
        """פונקציה להציג הודעה עם כותרת, צבע מותאם אישית או ברירת מחדל, ולהפעיל פונקציה אם ניתנה"""
        # אם לא הוזן צבע חדש, השתמש בצבע שנשמר במחלקה
        if color:
            color_value = self.colors.get(color, (0, 1, 0, 1))  # ברירת מחדל - ירוק
        else:
            color_value = self.colors.get(self.color, (0, 1, 0, 1))  # ברירת מחדל - ירוק

        # יצירת BoxLayout להודעה
        layout = BoxLayout(orientation='vertical', padding=10)

        # יצירת כותרת
        title_label = Label(text=title, font_size=24, bold=True, color=(1, 1, 1, 1))  # צבע שחור לכותרת

        # יצירת Label עם הטקסט והצבע
        label = Label(text=message, font_size=20, color=color_value)

        # כפתור סגירה
        close_button = RoundedButton(text='Close', size_hint=(1, None), height=50)

        # עיגול פינות לכפתור
        close_button.background_radius = [15]  # עיגול לכפתור

        # הוספת הכותרת, ה-Label והכפתור ל-BoxLayout
        layout.add_widget(title_label)
        layout.add_widget(label)
        layout.add_widget(close_button)

        # יצירת הפופאפ עם עיגול פינות
        popup = Popup(title='', content=layout, size_hint=(0.8, 0.4), background_color=(1, 1, 1, 1))
        popup.background_radius = [15]  # עיגול לפינות הפופאפ

        # הפונקציה שסוגרת את הפופאפ
        def close_and_execute_callback(instance):
            popup.dismiss()  # סגירת הפופאפ
            if callback:  # אם פונקציה ניתנה, נבצע אותה
                callback()

        # חיבור כפתור ה-"Close" לסגירת הפופאפ ולהפעלת הפונקציה
        close_button.bind(on_release=close_and_execute_callback)

        # פתיחת הפופאפ
        popup.open()
