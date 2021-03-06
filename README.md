# project koann!

Text recognition algorithm implementation using Tesseract.

## How to install koann! ? 
1. Git clone the project.
2. Download languages you'd like to use from: ***https://github.com/tesseract-ocr/tessdata***.
3. Move downloaded languages to: ```/usr/share/tesseract-ocr/4.00/tessdata/``` (if on Linux) and ```C:/Program Files/Tesseract-OCR/``` (if on Windows).
4. Use pip to install all modules required (go into ```koann/src/``` and run ```pip install -r requirements.txt```).
5. You can add your images to img/ folder or use our samples
6. Run the program: ```python3 main.py```

Note: **If you want MongoDB upload to work, change variables username and password inside `src/.env` file**

**Guide to creating a MongoDB database:** ***https://www.mongodb.com/basics/create-database***.

## koann! demo
https://user-images.githubusercontent.com/66844759/146607600-78b8839d-72d8-400e-bc80-ec3bb2cc28c7.mp4

## Installation of *tree* and *imagemagick*
Syntax for Arch: ```pacman -S tree```  ```pacman -S imagemagick```

Syntax for Debian: ```apt-get install tree``` ```apt-get install imagemagick```

Syntax for OS X: ```brew install tree``` ```brew install imagemagick```

For Windows ```tree``` is ***already installed***.

## Kind regards :)
If you feel like you can make a good contribution to the code, feel free to do so :) 
