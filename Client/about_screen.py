from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from rounded_button import RoundedButton
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from feedbackMessage import FeedbackMessage

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)

        self.layout = FloatLayout()
        self.feedback = FeedbackMessage()

        # Dark mode background
        with self.layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        self.layout.bind(size=self._update_rect, pos=self._update_rect)

        # Add the title
        title = Label(
            text="About AutoScope",
            size_hint=(None, None),
            size=(dp(300), dp(50)),
            pos_hint={'center_x': 0.5, 'top': 1},
            font_size=dp(30),
            bold=True,
            color=(1, 1, 1, 1)  # לבן
        )
        self.layout.add_widget(title)

        # Add the content
        content = Label(
            text=(
                "AutoScope is an innovative application designed to assist users "
                "in detecting ear infections using deep learning techniques. Our goal "
                "is to provide quick and accurate analysis of ear images to improve "
                "health outcomes for users.\n\n"
                "Developed by: Alon Ternerider, Nadav Goldin\nSupervised by: Dr. Nataly Levi"
            ),
            size_hint=(0.9, None),
            height=dp(200),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='center',
            valign='middle'
        )
        content.bind(size=content.setter('text_size'))  # Allow text wrapping
        self.layout.add_widget(content)

        # Feedback encouragement label
        feedback_encouragement = Label(
            text="We would love to hear your feedback:",
            size_hint=(None, None),
            size=(dp(250), dp(50)),
            pos_hint={'center_x': 0.5, 'y': 0.3},
            font_size=dp(18),
            color=(0.8, 0.8, 0.8, 1)
        )
        self.layout.add_widget(feedback_encouragement)

        self.feedback_input = TextInput(
            size_hint=(0.8, None),
            height=dp(100),
            pos_hint={'center_x': 0.5, 'y': 0.2},
            multiline=True
        )
        self.layout.add_widget(self.feedback_input)

        submit_button = RoundedButton(
            text='Submit Feedback',
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            pos_hint={'center_x': 0.5, 'y': 0.1}
        )
        submit_button.bind(on_release=self.submit_feedback)
        self.layout.add_widget(submit_button)

        back_btn = RoundedButton(
            background_normal="Icons/back.png",
            size_hint=(None, None),
            height=dp(65),
            width=dp(75),
            pos_hint={'x': 0, 'top': 0.1}
        )
        back_btn.bind(on_release=self.close_about)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def close_about(self, instance):
        self.manager.current = 'main'

    def submit_feedback(self, instance):
        feedback = self.feedback_input.text
        if feedback:
            print(f"Feedback submitted: {feedback}")
            self.feedback_input.text = ""  # Clear the input field

            # Show thank you message
            self.feedback.show_message('Feedback submitted', 'Thank you for your feedback!', color='success')

        else:
            self.feedback.show_message('Feedback Not submitted', 'No feedback entered!', color='error')
