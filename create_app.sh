pyinstaller -y --clean --windowed --name mymusic --exclude-module _tkinter --exclude-module Tkinter --exclude-module enchant --exclude-module twisted main.py
