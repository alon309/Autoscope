from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from menu_screen import MenuScreen



class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        layout = FloatLayout()  # Use FloatLayout for flexible positioning

        with layout.canvas.before:
            Color(0, 0, 1, 1)  # RGB for blue (0-1 range)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        # Update the rectangle size when the layout size changes
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Create the image with size and allow_stretch
        otoscope_image = Image(
            source=r'Icons/otoscope.png',
            size_hint=(None, None),  # Disable size hint
            size=(250, 250),         # Set the desired size
            allow_stretch=True
        )
        # Center the image horizontally and position it slightly down from the top
        otoscope_image.pos_hint = {'center_x': 0.5, 'top': 0.8}
        layout.add_widget(otoscope_image)

        # Create the button layout below the image
        button_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), pos_hint={'center_x': 0.35, 'center_y': 0.2}, spacing=50)
        take_picture_button = Button(text='Take Picture', size_hint=(None, None), width=150, height=50)
        upload_picture_button = Button(text='Upload Picture', size_hint=(None, None), width=150, height=50)

        button_layout.add_widget(take_picture_button)
        button_layout.add_widget(upload_picture_button)
        layout.add_widget(button_layout)

        # Create a button to open the MenuScreen in the top-left corner
        menu_button = Button(
            size_hint=(None, None),
            size=(75, 75),
            pos_hint={'x': 0, 'top': 1},
            background_normal=r'Icons/menu.png',  # Path to the button image
        )
        menu_button.bind(on_release=self.open_menu)
        layout.add_widget(menu_button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def open_menu(self, instance):
        # Check if the menu is already open to avoid adding multiple menus
        if not any(isinstance(child, MenuScreen) for child in self.children):
            menu = MenuScreen(size_hint=(0.3, 1), pos_hint={'x': 0, 'y': 0})
            self.add_widget(menu)  # Add the menu to the main screen