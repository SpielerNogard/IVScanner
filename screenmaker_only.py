import subprocess
import time
import cv2 as cv
import numpy as np
from datetime import datetime
from shutil import copyfile

def make_screen():
    now = datetime.now().time()
    now = str(now)
    
    subprocess.call("adb exec-out screencap -p > Bilder/screen.jpg",shell=True)
    now = now.replace(":","_")
    now = now.replace(".","_")
    copyfile("Bilder/screen.jpg","Bilder/"+str(now)+".jpg")
    


while True:
    make_screen()
