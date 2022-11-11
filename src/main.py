import numpy as np
import pytesseract
import argparse 
import pymongo 
import shutil 
import time 
import glob
import sys
import cv2
import os

from PIL import Image
from datetime import datetime 
from textblob import TextBlob
from dotenv import load_dotenv 
from pymongo import MongoClient

def clear(): 
    # checking the OS, clearing the screen accordingly
    if "Windows" in os.uname(): 
        os.system("cls")
    elif "Linux" in os.uname(): 
        os.system("clear")

def mongoFind(date): 
    load_dotenv() # loading .env file 
    cluster = MongoClient(os.getenv("DB_URI")) 
    database = cluster[os.getenv("DB_NAME")] # accessing a cluster/db 
    collection = database[date] # accessing a collection in db
    results = collection.find({}) # finding all posts from collection 
    clear() 
    for x in results: 
        print(x["folderName"]) # outputting all folderNames from collection 
        print(x["imageText"])  # outputting all imageText content from collection 

def mongoDB(timestr2, filename, text):   
    load_dotenv() # loading .env file 
    currentDate = time.strftime("%Y%m%d") # setting current date
    cluster = MongoClient(os.getenv("DB_URI")) 
    database = cluster[os.getenv("DB_NAME")] # creating/accessing a cluster/db 
    collection = database[currentDate] # creating/accessing a collection in db 
    post = {"folderName": timestr2, "imageText": text} # format of data to be uploaded
    
    collection.insert_one(post) # uploading data to collection

def imageProcessing(filename, path, timestr, timestr2, image_name, config):
    # global variables for other functions
    global fpath
    global corrected_text
    global text 

    fpath = path + image_name # full path to image 
    im = Image.open(fpath) # opening image 

    # -- IMAGE PROCESSING -- 
    image = cv2.imread(fpath) # image load 

    # normalizing the picture 
    normalize_image = np.zeros((image.shape[0], image.shape[1]))
    imager = cv2.normalize(image, normalize_image, 0, 255, cv2.NORM_MINMAX)
    
    # image scaling to 300 DPI
    image = cv2.resize(image, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)  
    # image convert to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    image = cv2.resize(image, (400, 400))
    kernel = np.ones((1,1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)

    # blurring image and applying a median filter for edge smoothening 
    image = cv2.threshold(cv2.medianBlur(image, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    image = cv2.adaptiveThreshold(cv2.bilateralFilter(image, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2) 
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # loading the processed image 
    image = cv2.imread(fpath, cv2.COLOR_BGR2GRAY) 
    
    # finally using tesseract to recognize text from image
    text = pytesseract.image_to_string(image, config=config)

    # spellchecking using TextBlob - for better results 
    tb = TextBlob(text)
    corrected_text = tb.correct()

    print(corrected_text) # output the text
    im.show() # showing image 

def fileOrganisation(filename, timestr, timestr2, text, fpath, corrected_text): 
    os.chdir("../archive/") # changing directory to archive
    os.mkdir(timestr) # making a folder for storing OCR data - according to current time and date
    file = open(filename, "w+") # making the text output file
    file.write(str(corrected_text)) # writing detected text into output file 
    file.close() # closing the file 

    # moving the ouptut file to folder created earlier 
    shutil.move(filename, timestr) 

    # copying image used into that folder 
    os.system("cp " + fpath + " " + timestr + "/") 

    # user chooses if he wants to upload files to MongoDB 
    choice = input("Upload to MongoDB(Y/n): ")
    if choice == "": 
        clear() 
        print("Uploading to MongoDB...\n")
        time.sleep(1)
        mongoDB(timestr2, filename, text)
    elif choice == "y": 
        clear()
        print("Uploading to MongoDB...\n")
        time.sleep(1)
        mongoDB(timestr2, filename, text) 
    elif choice == "n": 
        clear()
        print("OK!\n")
    else: 
        clear()
        print("Invalid input!\n")

def commands(filename, timestr, timestr2, path):
    print("Commands: exit, tree, database find, delete, delete all, process.")
    command = input("Enter command: ") 

    while command == "": 
        command = input("Enter command: ")
    
    if command == "exit":   
        clear()
        sys.exit()
    elif command == "tree":
        clear() 
        os.system("tree ../archive/")
    elif command == "database find": 
        clear() 
        date = input("Date of data to load(format: %Y%m%d): ")
        while date == "":
            date = input("Date of data to load(format: %Y%m%d): ")
        mongoFind(date) 
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
        shutil.rmtree("../archive") # deleting all files
        print("All folders/files succesfully removed!")
        os.chdir("../")
        os.mkdir("archive")
        os.chdir("src/")
    elif command == "process": 
        clear()
        os.chdir(path) 
        lang = input("Enter desired language(bos, srp, hrv, eng, deu, fra): ")
        config = ('-l ' + lang + ' --oem 1 --psm 3') # config for tesseract
        image_name = input("Enter image name: ") 
        while image_name == "": 
            image_name = input("Enter image name: ")
        imageProcessing(filename, path, timestr, timestr2,image_name, config)
        fileOrganisation(filename, timestr, timestr2, text, fpath, corrected_text)

def main(): 
    # -- VARIABLES -- 
    filename = "output.txt" # name of output file 
    timestr = time.strftime("%Y%m%d%H%M%S") # folder name format
    now = datetime.now()
    timestr2 = now.strftime("%d-%m-%y-%H:%M:%S")
    path = "../img/" # path to images folder 
    clear() 
    while True:
        commands(filename, timestr, timestr2, path) # calling the commands() function

if __name__ == "__main__":
    main()
