# Datum: -
# TODO: SPEED OPTIMISATION 

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

    slika = cv2.imread(putanja+ime_slike, cv2.IMREAD_COLOR)
    tekst = pytesseract.image_to_string(slika, config=config)
    print(tekst)

if __name__ == "__main__":
    main()
