# Authori: Eman Ćatić i Rijad Gadžo
# Datum: -
# TODO:  

import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import shutil 
import time 
import glob
import sys
import cv2
import os
from PIL import Image, ImageEnhance

def clear(): 
    os.system("clear")

def procesovanje(filename, putanja, timestr, ime_slike, config):
    fputanja = putanja+ime_slike 
        
    # -- PROCESUIRANJE SLIKA -- 
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
    try:
        os.chdir("../arhiva/") # promjena foldera u '/arhiva/'
    except:
        os.chdir("../")
        os.mkdir("arhiva")
        os.chdir("arhiva/")
        os.mkdir(timestr) # pravljenje novog foldera
    file = open(filename, "w+") # pravljenje output filea
    file.write(tekst) # ispisivanje detektovanog teksta u file
    file.close() # zatvaranje filea
    # premjestanje koristene slike i output filea u novi folder
    shutil.move(filename, timestr)
    os.system("cp " + fputanja + " " + timestr)

def komandeIprocesovanje(filename, timestr, putanja):
    print("Komande: exit, tree, delete, delete all, process")
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
        os.system("cd ../arhiva/ && tree") 
        ftd = input("Ime foldera koji želite ukloniti: ") 
        while ftd == "":
            ftd = input("Ime foldera koji želite ukloniti: ")
        os.chdir("../arhiva/") 
        shutil.rmtree(ftd) # brisanje foldera
        print("Folder uspješno uklonjen!")
        time.sleep(1) # delay 1. sekunda
    elif komanda == "delete all": 
        clear()
        shutil.rmtree("../arhiva/")
        print("Svi folderi su uspješno uklonjeni!")
    elif komanda == "process": 
        clear()
        os.chdir(putanja) # promjena foldera u putanju("../img/")
        jezik = input("Unesite jezik od ponuđenih: ")
        config = ('-l ' + jezik + ' --oem 1 --psm 3') # config za tesseract
        ime_slike = input("Unesite ime slike: ") # unos imena slike
        while ime_slike == "": 
            ime_slike = input("Unesite ime slike: ")
        procesovanje(filename, putanja, timestr, ime_slike, config)

def main(): 
    # -- VARIJABLE -- 
    filename = "output.txt" # ime output file-a
    timestr = time.strftime("%Y%m%d%H%M%s") # format imena foldera
    putanja = "../img/" # putanja do slika
    clear() 
    while True:
        komandeIprocesovanje(filename, timestr, putanja)

if __name__ == "__main__":
    main()
