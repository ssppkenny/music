import re
import os, fnmatch
import subprocess
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
# base Class of your App inherits from the App class.
from kivy.core.window import Window
from kivy.app import App

# GridLayout arranges children in a matrix.
from kivy.uix.gridlayout import GridLayout

# Label is used to label something
from kivy.uix.label import Label

# used to take input from users
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import yt_dlp
from yt_dlp.utils import download_range_func


class DownloadWindow(GridLayout):
    def __init__(self, **var_args):

        super(DownloadWindow, self).__init__(**var_args)
        self.cols = 1  # You can change it accordingly
        self.add_widget(Label(text="Youtube URL:"))
        self.url = TextInput(multiline=False)
        self.add_widget(self.url)
        self.button = Button(text="Download", font_size=14)
        self.button.bind(on_press=self.button_on_press)
        self.add_widget(self.button)
        self.progressbar = ProgressBar(max=100)
        self.add_widget(self.progressbar)

    def update(self):
        print("update")
        pb = self.progresspar
        val = pb.value
        if val > 99:
            pb.value = 0
        else:
            pb.value += 1

    def stop(self):
        Clock.unschedule(self.update)


    def button_on_press(self, instance):
        video_url = self.url.text 
        event = Clock.schedule_interval(self.update, .1)
        print(event)
        print(video_url)
        subprocess.run(['yt-dlp', '-f', 'best', '-P', ".", video_url], check=True)
        results = re.findall(r".*v=(.*)", video_url)
        pattern = results[0]
        ff = find("*" + pattern + "*", ".")
        if ff:
            filename = str(ff[0])
            if filename.startswith("."):
                filename = filename[2:]

            print(filename)
            subprocess.run(['ffmpeg', '-i', filename, '-ab', '320k', filename+'.mp3'])

        self.stop()

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

# the Base Class of our Kivy App
class MyApp(App):
    def build(self):
        Window.size = (300, 100)
        return DownloadWindow()


if __name__ == "__main__":
    MyApp().run()
