# Authori: Eman Ćatić i Rijad Gadžo
# Datum: -
# TODO: dodati unos korisnika za nove slike, upload na Google Drive? 

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
    os.chdir(putanja) # program mijenja folder u folder koji je unio korisnik
    ime_slike = sys.argv[2]
    slika = Image.open(putanja + ime_slike) # ucitavanje slike korisnika

    kontrast = ImageEnhance.Contrast(slika)
    kontrast.enhance(2).save(putanja+"novaslika.jpg") # povecanje kontrasta 2x i sacuvanje poboljsane slike pod imenom 'novaslika.jpg'
    svjetlina = ImageEnhance.Brightness(slika)
    svjetlina.enhance(2).save(putanja+"novaslika.jpg") # povecanje svjetline 2x i sacuvanje poboljsane slike pod imenom 'novaslika.jpg'
    slika = cv2.imread(putanja+"novaslika.jpg", cv2.IMREAD_COLOR) # ucitavanje poboljsane slike
    tekst = pytesseract.image_to_string(slika, config=config) # prepoznavanje teksta na slici
    print(tekst) # ispisivanje prepoznatog teksta sa slike


if __name__ == "__main__":
    main()
