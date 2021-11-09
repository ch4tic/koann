import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import sys
import cv2
import os 

def main():
    config = ('-l eng --oem 1 --psm 3')
    putanja = input("Unesite putanju do slike: ")
    ime_slike = input("Unesite ime slike sa ekstenzijom: ")
    os.chdir(putanja)
    slika = cv2.imread(ime_slike, cv2.IMREAD_COLOR)

    tekst = pytesseract.image_to_string(slika, config=config)
    print(tekst)

if __name__ == "__main__":
    main()
