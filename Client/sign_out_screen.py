from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class SignOutScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(SignOutScreen, self).__init__(**kwargs)

        # Background color for the sign-out screen
        with self.canvas.before:
            Color(0.1, 0.2, 0.4, 1)  # Dark blue background
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Confirmation message
        confirmation_label = Label(text="Are you sure you want to sign out?",
                                   size_hint=(None, None), size=(400, 50),
                                   pos_hint={'center_x': 0.5, 'top': 1}, color=(1, 1, 1, 1))
        self.add_widget(confirmation_label)

        # Buttons
        button_layout = BoxLayout(size_hint=(None, None), size=(400, 50),
                                  pos_hint={'center_x': 0.5, 'y': 0.3})
        
        confirm_button = Button(text='Yes, Sign Out', size_hint=(0.5, 1), 
                                on_release=self.confirm_sign_out)
        cancel_button = Button(text='Cancel', size_hint=(0.5, 1), 
                               on_release=self.cancel_sign_out)
        
        button_layout.add_widget(confirm_button)
        button_layout.add_widget(cancel_button)
        
        self.add_widget(button_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def confirm_sign_out(self, instance):
        # Handle sign out logic here
        print("User signed out")
        self.parent.remove_widget(self)  # Example to remove sign-out screen

    def cancel_sign_out(self, instance):
        self.parent.remove_widget(self)  # Example to cancel sign out
