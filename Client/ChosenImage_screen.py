from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage
from config import SERVER_URL
import requests
from kivy.app import App
from widgets.feedback_popup import FeedbackPopup

class ChosenImageScreen(Screen):

    """ 
    Screen for displaying and analyzing a chosen image.
    
    - Allows users to select an image and send it for analysis.
    - Displays the chosen image on the screen.
    - Sends the image to the server for analysis and updates the result screen.
    """

    def __init__(self, **kwargs):
        """ Initialize screen attributes. """
        super(ChosenImageScreen, self).__init__(**kwargs)
        self.image_path = None
        self.image = None
        self.user_id = None
        self.chosen_current_image = None

    def update_data(self, image_path, user_id):
        """ 
        Update screen data with a new image path and user ID.
        
        Args:
            image_path (str): Path to the chosen image.
            user_id (str): ID of the user.
        """
        self.image_path = image_path
        self.user_id = user_id
        self.image = None
        self.display_image()

    def display_image(self):
        """ 
        Display the chosen image on the screen. 
        If loading fails, it clears the texture.
        """
        if self.image_path:
            try:
                img = CoreImage(self.image_path)
                self.ids.image_display.texture = img.texture
                self.chosen_current_image = img
                print(f"Image loaded: {self.image_path}")
            except Exception as e:
                print(f"Error loading image: {e}")
                self.ids.image_display.texture = None
        else:
            self.ids.image_display.texture = None

    """ Switch screen back to 'earCheck'. """
    def go_back(self):
        self.manager.current = 'earCheck'

    def analyze_image(self):
        """ 
        Send the selected image to the server for analysis.
        
        - If no image is selected, the function exits.
        - Sends the image and user ID to the API.
        - If successful, updates the results screen and navigates to it.
        - If there's an error, displays a feedback popup.
        """
        if not self.image_path:
            return

        try:
            url = f"{SERVER_URL}/api/analyze_image"
            with open(self.image_path, 'rb') as image_file:
                
                files = {'image': image_file}
                data = {'user_id': str(self.user_id)}
                response = requests.post(url, files=files, data=data) # send to server
                response.raise_for_status()
                response_data = response.json()

                confidence = response_data.get("confidence")
                result = response_data.get("result")

                results_screen = self.manager.get_screen('result')
                results_screen.update_data(self.chosen_current_image, result, confidence, self.user_id) # updating the data in the result screen
                self.manager.current = 'result' # switch to result screen
        except requests.exceptions.RequestException as e:
            popup = FeedbackPopup(
                title_text = 'Error during analysis request',
                message_text = 'Make sure the image is correct\nand try again!'
            )
            popup.open()

    def on_pre_enter(self):
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Home', 'Ear Check', 'Analyze']) # updating the bar status