from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from rounded_button import RoundedButton



class HelpScreen(Screen):
    def __init__(self, **kwargs):
        super(HelpScreen, self).__init__(**kwargs)

        # Background color for the help screen
        with self.canvas.before:
            Color(0.2, 0.5, 0.8, 1)  # A darker blue background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add title
        title = Label(text="Help & FAQs", size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5, 'top': 1})
        self.add_widget(title)

        # FAQs
        faqs = [
            "1. What is AutoScope?\n   - AutoScope is an application for detecting ear infections using deep learning techniques.",
            "2. How does AutoScope work?\n   - Users can take or upload pictures of their ears, which are then analyzed by our algorithms.",
            "3. Is my data secure?\n   - Yes, we prioritize user privacy and data security in our application.",
            "4. Can I share my feedback?\n   - Absolutely! We encourage users to submit feedback through the app.",
            "5. What should I do if I encounter a problem?\n   - Please contact us using the information below.",
            "6. Are you doctors? Are the results definitive?\n   - No, we are not medical professionals. The results provided by AutoScope are recommendations and should not be considered a substitute for professional medical advice."
        ]

        # Create a layout for FAQs
        faqs_layout = BoxLayout(orientation='vertical', size_hint=(0.9, None), height=350, pos_hint={'center_x': 0.5, 'center_y': 0.5})

        for faq in faqs:
            faq_label = Label(text=faq, size_hint_y=None, height=50, halign='left', valign='middle')
            faq_label.bind(size=faq_label.setter('text_size'))  # Allow text wrapping
            faqs_layout.add_widget(faq_label)

        self.add_widget(faqs_layout)

        # Contact information
        contact_info = Label(text="Contact Us:\nEmail: contact@autoscope.com\nPhone: (123) 456-7890",
                             size_hint=(0.9, None), height=100, pos_hint={'center_x': 0.5, 'y': 0.1}, halign='center')
        contact_info.bind(size=contact_info.setter('text_size'))  # Allow text wrapping
        self.add_widget(contact_info)

        back_btn = RoundedButton(background_normal = "Icons/back.png", size_hint=(None, None), height=65, width=75, pos_hint={'x': 0, 'top': 0.1})
        back_btn.bind(on_release=self.close_help)
        self.add_widget(back_btn)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def close_help(self, instance):
        self.manager.current = 'main'
