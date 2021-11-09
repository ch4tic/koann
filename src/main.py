import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import sys
import cv2

def main():
    config = ('-l eng --oem 1 --psm 3')
    slika = cv2.imread('biologija.jpg', cv2.IMREAD_COLOR)

    tekst = pytesseract.image_to_string(slika, config=config)
    print(tekst)

if __name__ == "__main__":
    main()
