import numpy as np
import time
import sys
import os

def main():
    putanja = input("Unesi putanju do slike: ")
    while putanja == "":
        putanja = input("Unesi putanju do slike: ")

    slika = open(putanja, 'r')
    plt.imshow(putanja)
    plt.show()


main()
