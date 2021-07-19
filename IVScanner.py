import subprocess
import time
import cv2 as cv
import numpy as np
from datetime import datetime
from shutil import copyfile

import config


class watcher(object):
    def __init__(self):
        self.templates = []
        self.template_names = ["pen","ok","calcy","candy","menu","genie"]
        self.load_templates()
    
    def load_templates(self):
        
        for Name in self.template_names:
            test = []
            test.append(Name)
            image = cv.imread("Templates/"+Name+".jpg",cv.IMREAD_REDUCED_COLOR_2)
            test.append(image)
            self.templates.append(test)

    def log(self,info):
        now = datetime.now().time()
        now = str(now)
        print(now+" : "+info)

    def find_pos(self, template_name):
        ergebnis = []
        positon = self.template_names.index(template_name)
        template = self.templates[positon]

        name = template[0]
        image = template[1]
        ergebnis.append(name)
        screen = cv.imread("Bilder/screen.jpg",cv.IMREAD_REDUCED_COLOR_2)
        result = cv.matchTemplate(screen, image, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            
        image_w = int(image.shape[1]/2)
        image_h = int(image.shape[0]/2)
        self.log("Best match top left position: %s" % str(max_loc))
        self.log("Best match confidence: %s" %max_val)
        self.log("Found "+name)
        x = (max_loc[0]+image_w)*2
        y = (max_loc[1]+image_h)*2
        werte_pos = []
        werte_pos.append(x)
        werte_pos.append(y)
        ergebnis.append(werte_pos)
        ergebnis.append(max_val)

        return(ergebnis)


class IVScanner(object):
    def __init__(self):
        self.Watcher = watcher()
        self.read_config()
        self.run()

    def log(self,info):
        now = datetime.now().time()
        now = str(now)
        print(now+" : "+info)

    def read_config(self):
        self.log("reading config file")
        self.scanner = config.calcy_scanner
        self.scan_number = config.scan
        self.save = config.save
        self.max_sleep_time = config.max_sleep

    def run(self):
        for a in range(self.scan_number):
            if self.scanner == "auto":
                pass
            elif self.scanner == "click":
                self.scan_with_click()

    def scan_with_click(self):
        self.log("Start scanning Pokemon")
        self.find_menu()
        self.find_candy()
        self.press_somewhere()
        self.find_calca()
        self.press_somewhere()
        self.find_pen()
        self.delete_text()
        self.insert_from_clipboard()
        self.press_somewhere()
        self.find_ok()
        self.swipe_right()

    def make_screen(self):
        if self.save == False:
            self.log("Take Screenshot")
            subprocess.call("adb exec-out screencap -p > Bilder/screen.jpg",shell=True)
            self.log("Screenshot Saved")
        else:
            now = datetime.now().time()
            now = str(now)
            self.log("Take Screenshot")
            subprocess.call("adb exec-out screencap -p > Bilder/screen.jpg",shell=True)
            now = now.replace(":","_")
            now = now.replace(".","_")
            copyfile("Bilder/screen.jpg","Bilder/"+str(now)+".jpg")
            self.log("Screenshot Saved")

    def find_menu(self):
        self.make_screen()
        position = self.Watcher.find_pos("menu")
        name = position[0]
        real_position = position[1]
        x = real_position[0]
        y = real_position[1]
        self.input_tap(x,y)
        time.sleep(1)

    def find_candy(self):
        self.make_screen()
        position = self.Watcher.find_pos("candy")
        name = position[0]
        real_position = position[1]
        x = real_position[0]
        y = real_position[1]
        self.input_tap(x,y)
        time.sleep(1)

    def find_calca(self):
        self.make_screen()
        position = self.Watcher.find_pos("calcy")
        name = position[0]
        real_position = position[1]
        x = real_position[0]
        y = real_position[1]
        self.input_tap(x,y)
        time.sleep(10)

    def find_pen(self):
        self.make_screen()
        position = self.Watcher.find_pos("pen")
        name = position[0]
        real_position = position[1]
        x = real_position[0]
        y = real_position[1]
        self.input_tap(x,y)
    
    def find_ok(self):
        self.make_screen()
        position = self.Watcher.find_pos("ok")
        name = position[0]
        real_position = position[1]
        x = real_position[0]
        y = real_position[1]
        self.input_tap(x,y)

    def press_somewhere(self):
        subprocess.call("adb shell input tap 400 1000",shell=True)
        time.sleep(1)

    def input_tap(self,x,y):
        self.log("Tapping on: X= "+str(x)+" Y= "+str(y))
        subprocess.call("adb shell input tap "+str(x)+" "+str(y),shell=True)
        self.log("Tapped")

    def delete_text(self):
        for i in range(20):
            subprocess.call("adb shell input keyevent KEYCODE_DEL",shell=True)

    def insert_from_clipboard(self):
        subprocess.call("adb shell input keyevent KEYCODE_PASTE",shell=True)

    def swipe_right(self):
        subprocess.call("adb shell input swipe 400 1000 100 1000 ",shell=True)
        time.sleep(2)
IVScanner = IVScanner()