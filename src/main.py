# Authors: Eman Ćatić i Rijad Gadžo
# Date: 22.11.1337

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
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

def clear(): 
    os.system("clear")

def GoogleDriveUpload(path2, timestr):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    directory = os.listdir(r"../archive/")
    for foldername in directory: 
        folder = drive.CreateFile({'title': foldername, 'mimeType':'application/vnd.google-apps.folder'})
        folder.Upload()
        cfolder_id = folder['id']
        os.chdir(path2)
        for file in glob.glob("*.png"):
            with open(file, "r") as f: 
                fn = os.path.basename(f.name)
                file_drive = drive.CreateFile({'title':fn})    
            file_drive.SetContentString(f.read())
            file_drive.Upload()

def imageProcessing(filename, path, timestr, image_name, config):
    fpath = path + image_name  
        
    # -- IMAGE PROCESSING -- 
    image = cv2.imread(fpath) # image load 
    # image scaling to 300 DPI
    image = cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC) 
    # image convert to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    # blurring the image using median blur method 
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
    cv2.threshold(cv2.medianBlur(image, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.adaptiveThreshold(cv2.medianBlur(image, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    
    # loading the processed image 
    image = cv2.imread(fpath, cv2.COLOR_BGR2GRAY) 
    # finally using tesseract to recognize text from image
    text = pytesseract.image_to_string(image, config=config)
    print(text) # output the text

    # -- FILE ORGANISATION --

    # if changing directory to '/archive' fails, create that directory
    os.chdir("../archive/")
    os.mkdir(timestr) 

    file = open(filename, "w+") # making the text output file
    file.write(text) # writing detected text into output file 
    file.close() # closing the file 
    # moving the ouptut file to folder created earlier 
    shutil.move(filename, timestr) 
    # copying image used into that folder 
    os.system("cp " + fpath + " " + timestr + "/") 

def commands(filename, timestr, path, path2):
    print("Commands: exit, tree, drive upload, delete, delete all, process.")

    command = input("Enter command: ") 
    while command == "": 
        command = input("Enter command: ")
    
    if command == "exit":   
        clear()
        sys.exit()
    elif command == "tree":
        clear()
        os.system("cd .. && cd archive/ && tree")
    elif command == "drive upload": 
        clear()
        GoogleDriveUpload(path2, timestr) 
    elif command == "delete": 
        clear() 
        os.system("cd ../archive/ && tree") 
        ftd = input("Name of folder to remove: ") 
        while ftd == "":
            ftd = input("Name of folder to remove: ")
        os.chdir("../archive/") 
        shutil.rmtree(ftd) # folder delete 
        print("Folder removed succesfully!")
    elif command == "delete all": 
        clear()
        shutil.rmtree("../archive") # deleting all files including the folder
        print("All folders/files succesfully removed!")
    elif command == "process": 
        clear()
        os.chdir(path) 
        lang = input("Enter desired language(bos, srp, hrv, eng, deu, fra): ")
        config = ('-l ' + lang + ' --oem 1 --psm 3') # config for tesseract
        image_name = input("Enter image name: ") 
        while image_name == "": 
            image_name = input("Enter image name: ")
        imageProcessing(filename, path, timestr, image_name, config)

def main(): 
    # -- VARIJABLE -- 
    filename = "output.txt" # name of output file 
    timestr = time.strftime("%Y%m%d%H%M%S") # folder name format
    path = "../img/" # path to images folder 
    path2 = "../archive/"
    clear() 
    while True:
        commands(filename, timestr, path, path2) # calling the commands() function

if __name__ == "__main__":
    main()
