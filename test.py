import cv2
import cv2 as cv
import pytesseract
import subprocess
import numpy
from datetime import datetime
import time

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
        #x = (max_loc[0]+image_w)*2
        #y = (max_loc[1]+image_h)*2
        x = (max_loc[0])*2
        y = (max_loc[1])*2
        werte_pos = []
        werte_pos.append(x)
        werte_pos.append(y)
        ergebnis.append(werte_pos)
        ergebnis.append(max_val)

        return(ergebnis)

pytesseract.pytesseract.tesseract_cmd = "tesseract/tesseract.exe"

def make_screen():
    subprocess.call("adb exec-out screencap -p > Bilder/screen.jpg",shell=True)

def swipe_right():
        subprocess.call("adb shell input swipe 400 1000 100 1000 ",shell=True)
        time.sleep(2)

Watcher = watcher()

for a in range(20):
    make_screen()
    img = cv2.imread("Bilder/screen.jpg")
    position = Watcher.find_pos("genie")
    name = position[0]
    h = 400
    w = 400
    real_position = position[1]
    x = real_position[0]
    y = real_position[1]
            
    crop_img = img[y:y+h, x:x+w]
    #cv2.imshow("cropped", crop_img)
    #cv2.waitKey(0)
    text = pytesseract.image_to_string(crop_img)
    #print(text)
    #print(text.splitlines()[2])

    Name_poki = text.splitlines()[0]
    IV = text.splitlines()[1]
    #print(Name_poki)
    #print(IV)

    #Pokemon_Name
    test = Name_poki.split(" ")
    Name = test[0] 
    #print(Name)

    #IV
    test = IV.split(" ")
    #Name = test[0] 
    #print(Name)
    percent = test[1]
    values = test[2]
    #for a in test:
        #print(a)
    values = values.replace("(","")
    values = values.replace(")","")
    all_values = values.split("-")
    Attack = all_values[0]
    Defence = all_values[1]
    Health = all_values[2]
    #for a in all_values:
        #print(a)

    Output = Name+percent+Attack+Defence+Health
    print(Output)
    swipe_right()