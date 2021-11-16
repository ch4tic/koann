import matplotlib.pyplot as plt 
import numpy as np
import pytesseract
import sys
import cv2
import os
from PIL import Image, ImageEnhance

def main():
    config = ('-l bos --oem 1 --psm 3')

    if len(sys.argv) < 2: 
        print("sintaksa: python3 main.py ../img/ ime_slike")
        sys.exit(1)
    putanja = sys.argv[1]
    os.chdir(putanja)
    ime_slike = sys.argv[2]
    slika = Image.open(putanja + ime_slike)
    
    kontrast = ImageEnhance.Contrast(slika)
    kontrast.enhance(2).save(putanja+"novaslika.jpg")
    svjetlina = ImageEnhance.Brightness(slika)
    svjetlina.enhance(2).save(putanja+"novaslika.jpg")
    slika = cv2.imread(putanja+"novaslika.jpg", cv2.IMREAD_COLOR)
    tekst = pytesseract.image_to_string(slika, config=config)
    print(tekst)


if __name__ == "__main__":
    main()
