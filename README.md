# Installation

1. Install system dependencies

    $ sudo apt-get install tesseract-ocr

2. Download the latest Opencv from https://opencv.org/
3. Follow these instructions to install opencv http://stackoverflow.com/questions/15790501/why-cv2-so-missing-after-opencv-installed

    # Set PYTHONPATH like it's said
    export PYTHONPATH=~/projects/opencv/release/lib:$PYTHONPATH

4. Install python dependencies

    $ pip install -r requirements.txt



# Test

It will recognise text from test.jpg

    $ python recognise.py

