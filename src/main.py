import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import sys
import cv2

def main():
    #putanja = input("Unesi putanju do slike: ")
    #while putanja == "":
    #    putanja = input("Unesi putanju do slike: ")
    config = ('-l eng --oem 1 --psm 3')
    slika = cv2.imread('receipt.jpeg', cv2.IMREAD_COLOR)
    #cv2.imshow('Original', slika)
    tekst = pytesseract.image_to_string(slika, config=config)
    print(tekst)

if __name__ == "__main__":
    main()
