# project koann!

OCR algorithm implementation using Tesseract - supports images and pdf documents!

## How to install koann! ? 
1. Git clone the project.
2. Install **Tesseract** on your system
   - Windows: ***https://github.com/UB-Mannheim/tesseract/wiki***
   - Debian: ```sudo apt-get install tesseract-ocr```
   - Arch/Fedora: ```sudo snap install tesseract --edge``` - using snap
   - OS X: ```brew install tesseract```
2. Download languages you'd like to use from: ***https://github.com/tesseract-ocr/tessdata***.
3. Move downloaded languages to: ```/usr/share/tesseract-ocr/4.00/tessdata/``` (if on Linux) and ```C:/Program Files/Tesseract-OCR/``` (if on Windows).
4. Use pip to install all modules required (go into ```koann/src/``` and run ```pip install -r requirements.txt```).
5. You can add your images to img/ folder or use our samples
6. Run the program: ```python3 main.py```

Note: **If you want MongoDB upload to work, change variable `DB_URI` inside `src/.env` file to the database connect link in MongoDB!**

Example: `mongodb+srv://<username>:<password>@koann.ptkxpuh.mongodb.net/?retryWrites=true&w=majority` 
          
Be sure to change `<username>` and `<password>` variables!

**Guide to creating a MongoDB database:** ***https://www.mongodb.com/basics/create-database***.

## koann! demo

https://user-images.githubusercontent.com/66844759/200172458-2e3dadff-53fc-4350-b18f-9b5268493822.mp4

## Installation of *tree* and *imagemagick*
Syntax for Arch: ```pacman -S tree```  ```pacman -S imagemagick```

Syntax for Debian: ```apt-get install tree``` ```apt-get install imagemagick```

Syntax for OS X: ```brew install tree``` ```brew install imagemagick```

For Windows ```tree``` is ***already installed***.

## Kind regards
If you feel like you can make a good contribution to the code, feel free to do so!
