import pygetwindow as gw
import os

windows = gw.getAllTitles()
for index, title in enumerate(windows):
    print(f"{index + 1}: {title}")
os.system("pause")