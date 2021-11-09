import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import cv2
import os

def main():
    #putanja = input("Unesi putanju do slike: ")
    #while putanja == "":
    #    putanja = input("Unesi putanju do slike: ")

    slika = cv2.imread('test.jpg')
    #cv2.imshow('Original', slika)
    grayscale_slika = cv2.cvtColor(slika, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grayscale', grayscale_slika)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
main()
