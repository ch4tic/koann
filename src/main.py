# Datum: -
# TODO: folder organizacija 

import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import sys
import cv2
import os
from PIL import Image, ImageEnhance

def main():
    config = ('-l bos --oem 1 --psm 3') # config sa tesseract
    if len(sys.argv) < 2:
        print("sintaksa: python3 main.py ../img/ ime_slike")
        sys.exit(1)

    putanja = sys.argv[1]
    os.chdir(putanja)
    ime_slike = sys.argv[2]
    slika = cv2.imread(putanja+ime_slike)
    slika = cv2.resize(slika, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    slika = cv2.cvtColor(slika, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    slika = cv2.dilate(slika, kernel, iterations=1)
    slika = cv2.erode(slika, kernel, iterations=1)
    cv2.threshold(cv2.medianBlur(slika, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.adaptiveThreshold(cv2.medianBlur(slika, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    
    slika = cv2.imread(putanja+ime_slike, cv2.COLOR_BGR2GRAY)
    tekst = pytesseract.image_to_string(slika, config=config)
    print(tekst)

if __name__ == "__main__":
    main()
