from threading import Thread
from pathlib import Path
import re
import os
import fnmatch
import subprocess
from kivy.clock import Clock, mainthread
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


class DownloadWindow(GridLayout):
    def __init__(self, **var_args):

        super(DownloadWindow, self).__init__(**var_args)
        self.cols = 1  # You can change it accordingly
        self.add_widget(Label(text="Youtube URL:"))
        self.url = TextInput(multiline=False)
        self.add_widget(self.url)
        self.button = Button(text="Download", font_size=24)
        self.button.bind(on_press=self.button_on_press)
        self.add_widget(self.button)
        self.progressbar = ProgressBar(max=100)
        self.progressbar.value = 0
        self.add_widget(self.progressbar)
        self.timer = Clock.schedule_interval(self.update, 1)
        self.downloading = False

    @mainthread
    def update(self, value):
        if self.downloading:
            pb = self.progressbar
            val = pb.value
            if val > 99:
                pb.value = 0
            else:
                pb.value += 10

    def stop(self):
        self.dowloading = False

    def download(self, video_url):
        self.downloading = True
        home_directory = os.path.expanduser('~')
        download_dir = home_directory + "/Downloads/music"
        Path(download_dir).mkdir(parents=True, exist_ok=True)
        subprocess.run(["yt-dlp", "-f", "best", "-P",
                       download_dir, video_url], check=True)
        results = re.findall(r".*v=(.*)", video_url)
        pattern = results[0]
        ff = find("*" + pattern + "*", download_dir)
        for filename in ff:
            if not filename.endswith("mp3"):
                out_filename, _ = os.path.splitext(filename)
                subprocess.run(["ffmpeg", "-y", "-i", filename,
                               "-ab", "320k", out_filename + ".mp3"],
                               check=True)
                os.remove(filename)
                break

        print("Finished")
        self.downloading = False
        self.progressbar.value = 100

    def button_on_press(self, instance):
        video_url = self.url.text
        if not video_url:
            return
        self.progressbar.value = 0
        Thread(target=self.download, args=(video_url,)).start()


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
        Window.size = (350, 100)
        return DownloadWindow()


if __name__ == "__main__":
    MyApp().run()
