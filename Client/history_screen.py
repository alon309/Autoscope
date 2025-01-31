from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage
from kivy.metrics import dp
from io import BytesIO
import requests
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.app import App
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
import threading
from kivy.clock import Clock

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        self.history_data = [] # Stores the history of ear infection diagnosis and related data.

    def update_page(self):
        """
        Updates the layout to display the history of diagnoses, including images and date/time.
        If no history data is available, it shows a 'No history available' label.
        """
        data_layout = self.ids.data_layout
        data_layout.clear_widgets() # Clears existing widgets in the layout

        if not self.history_data:
            data_layout.add_widget(Label(text="No history available", size_hint_y=None, height=dp(40)))
            return
        
        # Loop through each history entry and add corresponding widgets (images, labels) to the layout.
        for entry in self.history_data:
            diagnose = entry.get('diagnose', 'No Result')
            image_texture = entry.get('image_texture')
            datetime_str = entry.get('datetime', 'Unknown')

            # Create a row for each entry with horizontal layout
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(100), spacing=dp(10))

            # Image widget or a placeholder if no image
            if image_texture:
                image_widget = Image(size_hint=(None, None), size=(dp(80), dp(80)))
                image_widget.texture = image_texture
            else:
                image_widget = Label(text="No Image", size_hint=(None, None), size=(dp(80), dp(80)))

            # Diagnosis result label with color indicating the result (green for healthy, red for infected)
            result_label = Label(
                text=diagnose,
                size_hint=(0.5, 1),
                halign='center',
                valign='middle',
                color=(1, 0, 0, 1) if diagnose.startswith("Infected") else (0, 1, 0, 1)
            )
            result_label.bind(size=result_label.setter('text_size'))

            # Date and time formatting
            try:
                if datetime_str != "Unknown":
                    date_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                    formatted_date = date_obj.strftime('%d/%m/%Y')
                    formatted_time = date_obj.strftime('%I:%M %p')
                else:
                    formatted_date = "Unknown Date"
                    formatted_time = "Unknown Time"
            except Exception as e:
                print(f"Error processing date: {e}")
                formatted_date = "Invalid Date"
                formatted_time = "Invalid Time"

            # Date and time label
            datetime_label  = Label(
                text=f"{formatted_date}\n{formatted_time}",
                size_hint=(0.2, 1),
                halign='right',
                valign='middle',
                color=(0, 0, 0, 1)
            )
            datetime_label .bind(size=datetime_label .setter('text_size'))

            # Add all the widgets to the row
            row.add_widget(image_widget)
            row.add_widget(result_label)
            row.add_widget(datetime_label )

            # Add the row to the main layout
            data_layout.add_widget(row)

    def go_back(self):
        """Navigates back to the home screen."""
        self.manager.current = 'home'

    def fetch_history(self):
        """
        Fetches image data for each history entry in a separate thread to avoid blocking the UI.
        The image is fetched from a URL and processed asynchronously.
        """
        def fetch_data():
            updated_data = []
            for entry in self.history_data:
                image_url = entry.get('image', '') # URL of the image to fetch
                try:
                    if image_url:
                        img_data = requests.get(image_url).content # Get image data
                        entry['image_data'] = img_data # Store the image data
                    else:
                        entry['image_data'] = None
                except Exception as e:
                    print(f"Error fetching image: {e}")
                    entry['image_data'] = None

                updated_data.append(entry)

            # Schedule the image processing once the data is fetched
            Clock.schedule_once(lambda dt: self.process_images(updated_data))

        # Start the data fetching process in a separate thread
        threading.Thread(target=fetch_data, daemon=True).start()

    def process_images(self, updated_data):
        """
        Converts raw image data into texture format to be used by Kivy's Image widget.
        This is done after all data has been fetched.
        """
        for entry in updated_data:
            img_data = entry.get('image_data')
            try:
                if img_data:
                    # Convert image data into texture format
                    texture = CoreImage(BytesIO(img_data), ext='png').texture
                    entry['image_texture'] = texture
                else:
                    entry['image_texture'] = None
            except Exception as e:
                print(f"Error processing image: {e}")
                entry['image_texture'] = None

        # Update the history data with the processed image textures
        self.history_data = updated_data
        self.update_page()
        self.ids.loading_label.opacity = 0 # remove loading label

    def update_history(self, history_data):
        """
        Updates the history data by sorting the entries by date (most recent first).
        """
        # Sort data by date (latest first)
        self.history_data = sorted(
            history_data,
            key=lambda x: datetime.strptime(x.get('datetime', '1970-01-01 00:00:00'), '%Y-%m-%d %H:%M:%S'),
            reverse=True
        )

    def on_pre_enter(self):
        """Updates the breadcrumb navigation when entering this screen."""
        app = App.get_running_app()
        app.breadcrumb.update_breadcrumb(['Home', 'History'])

    def on_enter(self):
        """Starts the loading indicator and fetches history data when the screen is entered."""
        self.ids.loading_label.opacity = 1 # Show loading indicator
        self.fetch_history() # Start fetching the history data
