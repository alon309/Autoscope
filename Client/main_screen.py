from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from menu_screen import MenuScreen
from ChosenImage_screen import ChosenImageScreen
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.graphics.texture import Texture
from kivy.uix.image import Image as KivyImage
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label



class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.user_id = None  # אתחול ה-uid ל-None

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
        upload_picture_button.bind(on_release=self.open_file_explorer)

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
            menu = MenuScreen(self.user_id, size_hint=(0.3, 1), pos_hint={'x': 0, 'y': 0})
            self.add_widget(menu)  # Add the menu to the main screen

    def open_file_explorer(self, instance):
        # Create the file chooser
        filechooser = FileChooserIconView()

        # Create the select button
        select_button = Button(text='Select', size_hint=(1, None), height=50)  
        # Create the close button
        close_button = Button(text='Close', size_hint=(1, None), height=50)  
        # Layout for popup window with file chooser and buttons
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(filechooser)    
         # Horizontal layout for buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        button_layout.add_widget(select_button)
        button_layout.add_widget(close_button)
        
        layout.add_widget(button_layout)

        # Create the popup window
        popup = Popup(title='Select Image', content=layout, size_hint=(0.9, 0.9))

        # Function to handle selection of the image
        def select_image(instance):
            selected_image = filechooser.selection  # Get the selected image path
            if selected_image:
                image_path = selected_image[0]
                if self.is_image_file(image_path):
                    # Check if the screen already exists and remove it if necessary
                    if 'chosen_image_screen' in self.parent.screen_names:
                        self.parent.remove_widget(self.parent.get_screen('chosen_image_screen'))

                    # Open the ChosenImageScreen with the selected image
                    chosen_image_screen = ChosenImageScreen(image_path=image_path, user_id=self.user_id)
                    chosen_image_screen.name = 'chosen_image_screen'

                    self.parent.add_widget(chosen_image_screen)  # Add the screen to the parent
                    self.parent.current = 'chosen_image_screen'  # Switch to the new screen
                    popup.dismiss()  # Close the popup once an image is selected
                else:
                    # Show error message if not a valid image
                    self.show_error_message("Invalid file type! Please select an image file.")
            else:
                popup.dismiss()  # Close the popup if no file is selected

        # Bind the select button to the image selection function
        select_button.bind(on_release=select_image)

        # Bind the close button to dismiss the popup
        close_button.bind(on_release=popup.dismiss)

        # Open the popup
        popup.open()


    def is_image_file(self, file_path):
        # Check if the file has a valid image extension
        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
        return any(file_path.lower().endswith(ext) for ext in valid_extensions)

    def show_error_message(self, message):
        # Create a BoxLayout for the error message popup
        error_layout = BoxLayout(orientation='vertical', padding=10)

        # Create a label for the error message
        error_label = Label(text=message)

        # Create a close button
        close_button = Button(text='Close', size_hint=(1, None), height=50)

        # Add the label and button to the layout
        error_layout.add_widget(error_label)
        error_layout.add_widget(close_button)

        # Create the error popup
        error_popup = Popup(title='Error', content=error_layout, size_hint=(0.8, 0.4))

        # Function to close the popup
        close_button.bind(on_release=error_popup.dismiss)

        # Open the error popup
        error_popup.open()