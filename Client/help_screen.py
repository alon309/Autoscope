from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.app import App


class HelpScreen(Screen):

    def __init__(self, **kwargs):
        super(HelpScreen, self).__init__(**kwargs)

        self.faqs = [
            "1. What is AutoScope?\n   - AutoScope is an application for detecting ear infections using deep learning techniques.",
            "2. How does AutoScope work?\n   - Users can take or upload pictures of their ears, which are then analyzed by our algorithms.",
            "3. Is my data secure?\n   - Yes, we prioritize user privacy and data security in our application.",
            "4. Can I share my feedback?\n   - Absolutely! We encourage users to submit feedback through the app.",
            "5. What should I do if I encounter a problem?\n   - Please contact us using the information below.",
            "6. Are you doctors? Are the results definitive?\n   - No, we are not medical professionals. The results provided by AutoScope are recommendations and should not be considered a substitute for professional medical advice."
        ]
        self.load_faqs()

    def go_back(self):
        self.manager.current = 'home'

    def load_faqs(self):
        faqs_layout = self.ids.get('faqs_layout')
        if not faqs_layout:
            print("Error: faqs_layout ID not found in KV file.")
            return

        faqs_layout.clear_widgets()
        for faq in self.faqs:
            faq_label = Label(
                text=faq,
                size_hint_y=None,
                height=dp(70),
                halign='left',
                valign='middle',
                color=(0.3, 0.3, 0.3, 1)
            )
            faq_label.bind(size=faq_label.setter('text_size'))  # Enable text wrapping
            faqs_layout.add_widget(faq_label)

    def on_pre_enter(self):
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Home', 'Help'])
