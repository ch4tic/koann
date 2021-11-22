# Authori: Eman Ćatić i Rijad Gadžo
# Datum: -
# TODO:  

import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import shutil 
import time 
import sys
import cv2
import os
from PIL import Image, ImageEnhance

def clear(): 
    os.system("clear")

def procesovanje(filename, putanja, timestr, ime_slike, config):
    fputanja = putanja+ime_slike 
        
    # -- IMAGE PROCESSING -- 
    slika = cv2.imread(fputanja) # ucitavanje slike
    # skaliranje slike
    slika = cv2.resize(slika, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC) 
    # pretvaranje slike u grayscale
    slika = cv2.cvtColor(slika, cv2.COLOR_BGR2GRAY) 

    # blurrovanje slika 
    kernel = np.ones((1, 1), np.uint8)
    slika = cv2.dilate(slika, kernel, iterations=1)
    slika = cv2.erode(slika, kernel, iterations=1)
    cv2.threshold(cv2.medianBlur(slika, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.adaptiveThreshold(cv2.medianBlur(slika, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    
    # ucitavanje poboljsane slike 
    slika = cv2.imread(fputanja, cv2.COLOR_BGR2GRAY) 
    # detekcija teksta iz slike i ispisivanje istog
    tekst = pytesseract.image_to_string(slika, config=config)
    print(tekst)

    # -- FILE ORGANIZACIJA --
    os.chdir("../arhiva/") # promjena foldera u '/arhiva/'
    os.mkdir(timestr) # pravljenje novog foldera
    file = open(filename, "w+") # pravljenje output filea
    file.write(tekst) # ispisivanje detektovanog teksta u file
    file.close() # zatvaranje filea
    # premjestanje koristene slike i output filea u novi folder
    shutil.move(filename, timestr)
    os.system("cp " + fputanja + " " + timestr)


def komandeIprocesovanje(komande, filename, timestr, putanja, config):
    print("Komande: exit, tree, delete, process")

    komanda = input("Unesite komandu: ") 
    while komanda == "": 
        komanda = input("Unesite komandu: ")

    if komanda == "exit":   
        clear()
        sys.exit()
    elif komanda == "tree":
        clear()
        os.system("cd .. && cd arhiva/ && tree")
    elif komanda == "delete": 
        clear() 
        os.system("cd .. && cd arhiva/ && tree")
        ftd = input("Ime foldera koji želite ukloniti: ")
        while ftd == "":
            ftd = input("Ime foldera koji želite ukloniti: ")
        os.chdir("../arhiva/")
        shutil.rmtree(ftd)
        print("Folder uspješno uklonjen!")
        time.sleep(1)
    elif komanda == "process": 
        clear()
        os.chdir(putanja)
        ime_slike = input("Unesite ime slike: ")
        while ime_slike == "": 
            ime_slike = input("Unesite ime slike: ")
        procesovanje(filename, putanja, timestr, ime_slike, config)

def main(): 
    # -- KONFIGURACIJA -- 
    config = ('-l bos --oem 1 --psm 3')
    
    # -- VARIJABLE -- 
    filename = "output.txt" # ime output file-a
    komande = ["exit", "tree", "delete", "process"]
    timestr = time.strftime("%Y%m%d%H%M") 
    putanja = "../img/"
    clear() 

    while True:
        komandeIprocesovanje(komande, filename, timestr, putanja, config)




if __name__ == "__main__":
    main()
