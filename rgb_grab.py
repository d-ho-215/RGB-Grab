import os
import keyboard
import pyautogui
from time import sleep
from PIL import Image, ImageGrab
import tkinter as tk
from tkinter import filedialog



queue = []
data = []

def color_text(rgb, text):
    r, g, b = rgb
    colored_text = f"\033[38;2;{r};{g};{b}{text}\033[0m"
    return colored_text


def sample_screen():
    x, y = pyautogui.position()
    bbox = (x, y, x+1, y+1)
    im = ImageGrab.grab(bbox = bbox)
    rgbim = im.convert('RGB')
    r,g,b = rgbim.getpixel((0,0))
    queue.append((r,g,b))

def record_sample():
    rgb = queue.pop()
    label = input(f'{color_text(rgb, str(rgb))}: ')
    data.append([label, rgb])

def leftpad(t, num_chars):
    t = str(t)
    while len(t) < num_chars:
        t = " " + t
    return t

def compose_text(line):
    name = line[0]
    name = name.replace(" ", "_").upper()
    r = leftpad(line[1][0], 3)
    g = leftpad(line[1][1], 4)
    b = leftpad(line[1][2], 4)
    line_text = f"{r}{g}{b} {name}\n"
    return line_text

def write_output_file(data, filename):
    header = """GIMP Palette
Name: STABILO PEN COLORS - COMPLETE.gpl
#\n
"""
    with open(filename, "w") as file:
        file.write(header)
        for color in data:
            line_text = compose_text(color)
            file.write(line_text)



try:
    print("ctrl+alt+c : sample color at mouse location")
    print("ctrl+alt+q : stop sampling and save")
    while True:
        if keyboard.is_pressed('ctrl+alt+c'):
            sample_screen()
            sleep(0.25)
        elif keyboard.is_pressed('ctrl+alt+q'):
            print('done sampling!')
            break
        elif len(queue) > 0:
            record_sample()
finally:
    root = tk.Tk()
    root.withdraw()
    response = input("ready to save data? press Enter then choose the output directory, or Q to quit")
    if response.upper() == "Q":
        print("ok, quitting now! buh-bye!")
        sleep(3)
        quit()
    directory = filedialog.askdirectory(title='Select output directory')
    print(f'output directory: {directory}')
    filename = input('enter file name: ')
    if len(filename.split('.')) < 2:
        filename = filename + '.gpl'
    os.chdir(directory)
    write_output_file(data, filename)
    print("done!\nthanks for stopping by!")
    sleep(3)

