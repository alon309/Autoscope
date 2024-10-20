from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.app import App
from kivy.graphics import Color, Rectangle

class AboutScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)

        # Background color for the about screen
        with self.canvas.before:
            Color(0.1, 0.3, 0.6, 1)  # A darker blue background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add the title
        title = Label(text="About AutoScope", size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5, 'top': 1})
        self.add_widget(title)

        # Add the content
        content = Label(text=(
            "AutoScope is an innovative application designed to assist users "
            "in detecting ear infections using deep learning techniques. Our goal "
            "is to provide quick and accurate analysis of ear images to improve "
            "health outcomes for users.\n\n"
            "Developed by: Alon Ternerider, Nadav Goldin\nSupervised by: Dr. Nataly Levi"),
            size_hint=(0.9, None),
            height=200,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='center',
            valign='middle'
        )
        content.bind(size=content.setter('text_size'))  # Allow text wrapping
        self.add_widget(content)

        # Feedback encouragement label
        feedback_encouragement = Label(text="We would love to hear your feedback:", size_hint=(None, None), size=(250, 50), pos_hint={'center_x': 0.5, 'y': 0.27})
        self.add_widget(feedback_encouragement)

        self.feedback_input = TextInput(size_hint=(0.8, None), height=100, pos_hint={'center_x': 0.5, 'y': 0.15}, multiline=True)
        self.add_widget(self.feedback_input)

        submit_button = Button(text='Submit Feedback', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'y': 0.05})
        submit_button.bind(on_release=self.submit_feedback)
        self.add_widget(submit_button)


        back_btn = Button(background_normal = "Icons/back.png", size_hint=(None, None), height=65, width=75, pos_hint={'x': 0, 'top': 0.1})
        back_btn.bind(on_release=self.close_about)
        self.add_widget(back_btn)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def close_about(self, instance):
        self.parent.remove_widget(self)  # Remove the About screen

    def submit_feedback(self, instance):
        feedback = self.feedback_input.text
        if feedback:
            print(f"Feedback submitted: {feedback}")  # Replace with actual feedback submission logic
            self.feedback_input.text = ""  # Clear the input field

            # Show thank you message
            thank_you_label = Label(text="Thank you for your feedback!", size_hint=(None, None), size=(250, 50), pos_hint={'center_x': 0.5, 'y': 0.1})
            self.add_widget(thank_you_label)

            # Remove the thank you label after 2 seconds
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.remove_widget(thank_you_label), 2)  # Remove after 2 seconds

        else:
            print("No feedback entered.")