import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import sys
import cv2
import os

def AutomatskoPodesavanjeKontrastaISvjetlosti(slika, histogram=30):
    gray = cv2.cvtColor(slika, cv2.COLOR_BGR2GRAY)

    #racunanje grayscale histograma
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)

    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))

    maximum = accumulator[-1]
    histogram *= (maximum/100.0)
    histogram /= 2.0

    minimum_gray = 0
    while accumulator[minimum_gray] < histogram:
        minimum_gray += 1

    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - histogram):
        maximum_gray -= 1

    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.plot(hist)
    plt.plot(new_hist)
    plt.xlim([0,256])

    rezultat = cv2.convertScaleAbs(slika, alpha=alpha, beta=beta)
    return (rezultat)


def main():
    config = ('-l eng --oem 1 --psm 3')
    putanja = input("Unesite putanju do slike: ")
    ime_slike = input("Unesite ime slike sa ekstenzijom: ")
    os.chdir(putanja)
    slika = cv2.imread(ime_slike, cv2.IMREAD_COLOR)
    rezultat = AutomatskoPodesavanjeKontrastaISvjetlosti(slika)


    tekst = pytesseract.image_to_string(slika, config=config)
    print(tekst)
    cv2.imshow('rezultat', rezultat)
    cv2.waitKey()

if __name__ == "__main__":
    main()
