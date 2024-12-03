from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.metrics import dp
from datetime import datetime
import requests
from config import SERVER_URL
from feedback_popup import FeedbackPopup


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)

        self.image = None
        self.result_string = "No results yet"
        self.user_id = None

    def update_data(self, image, result_string, user_id):
        """Update the data displayed in the ResultsScreen."""
        self.image = image
        self.result_string = result_string
        self.user_id = user_id
        
        # Update the image display
        if self.image:
            self.ids.image_display.texture = self.image.texture
        
        # Update the result label
        self.ids.result_label.text = self.result_string
        print(f"Data updated: {self.image}, {self.result_string}, {self.user_id}")


    def save_result(self):
        """Save the current result."""
        print(self.result_string)
        
        # בדיקה אם יש תמונה
        if not self.image:
            print("No image to save.")
            return

        image_path = self.image.filename

        print("Saving the result...")

        # קבלת התאריך והשעה הנוכחיים
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # כתובת השרת
        url = f"{SERVER_URL}/api/save_result"

        try:
            # פתיחת הקובץ והעלאתו לשרת
            with open(image_path, 'rb') as image_file:
                files = {'image': image_file}
                data = {
                    'user_id': self.user_id,
                    'diagnose': 'Ear infection detected',
                    'datetime': current_datetime
                }

                response = requests.post(url, files=files, data=data)
                
                # בדיקה אם התגובה מהשרת תקינה
                if response.status_code != 200:
                    popup = FeedbackPopup(
                        title_text="Failed to save result",
                        message_text=f"Server responded with error: {response.status_code}"
                    )
                    return popup.open()

                try:
                    result_data = response.json()
                except ValueError:
                    popup = FeedbackPopup(
                        title_text="Failed to save result",
                        message_text="Invalid server response format."
                    )
                    return popup.open()

                # עדכון הנתונים המקומיים
                app = App.get_running_app()
                new_result = {
                    'diagnose': 'Ear infection detected',
                    'image': result_data.get('image'),
                    'datetime': current_datetime
                }

                # בדיקה והוספה של התוצאה למערך
                if 'results' not in app.user_details or not isinstance(app.user_details['results'], list):
                    app.user_details['results'] = []
                app.user_details['results'].append(new_result)

                popup = FeedbackPopup(
                    title_text="Result saved successfully",
                    message_text=f"{new_result}"
                )
                popup.open()

        except requests.RequestException as req_err:
            popup = FeedbackPopup(
                title_text="Failed to save result",
                message_text="Network error occurred, please try again."
            )
            popup.open()

        except Exception as e:
            popup = FeedbackPopup(
                title_text="Failed to save result",
                message_text="An unexpected error occurred."
            )
            popup.open()


    def go_back(self):
        """Return to the main screen."""
        self.manager.current = 'earCheck'
