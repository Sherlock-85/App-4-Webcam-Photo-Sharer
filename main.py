from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from filesharer import FileSharer
import time,webbrowser

Builder.load_file('frontend.kv')

class CameraScreen(Screen):
    def start(self):
        """Starts the camera and changes the text of the button"""
        self.ids.camera.play = True
        self.ids.camera_button.text = "Stop Camera"
        self.ids.camera.texture = self.ids.camera._camera.texture
        self.ids.camera_button.background_color = 'red'
        self.ids.camera.opacity = 1

    def stop(self):
        """ Stops the camera and changes the text of the Button"""
        self.ids.camera.play = False
        self.ids.camera_button.text = "Start Camera"
        self.ids.camera.texture = None
        self.ids.camera_button.background_color = "green"
        self.ids.camera.opacity = 0

    def capture(self):
        """Creates a filename with the current time, captures and saves the phone with that filename"""
        time_stamp = time.strftime("%Y%m%d_%H%M%S")
        self.filepath = f"images/{time_stamp}.png"
        # Access the widgets within Camera Screen(current class)
        self.ids.camera.export_to_png(self.filepath)
        # Want to access the image screen
        self.manager.current = 'image_screen'
        # Access widgets within Image Screen (current screen)
        self.manager.current_screen.ids.img.source = self.filepath


class ImageScreen(Screen):
    link_message = "Create a link first!"
    #Extract the filepath name
    def create_link(self):
        """Access the photo's filepath, uploads it to the web and inserts the link in the
        label widget"""
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        filesharer = FileSharer(filepath=file_path)
        # Allows the attribute to be accessed outside of the method
        self.url = filesharer.share()
        self.ids.link.text = self.url

    def copy_link(self):
        """Copy link to the clipboard"""
        try:
            Clipboard.copy(self.url)
        except AttributeError:
            self.ids.link.text = self.link_message

    def open_link(self):
        """Open link with default browser"""
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message


class RootWidget(ScreenManager):
    pass

class MainApp(App):

    def build(self):
        return RootWidget()


MainApp().run()



