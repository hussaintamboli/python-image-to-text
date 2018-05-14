# Code from http://blog.c22.cc/2010/10/12/python-ocr-or-how-to-break-captchas/
# and http://stackoverflow.com/questions/14640509/python-error-when-importing-image-to-string-from-tesseract

# $ tesseract input-NEAREST.tif example -psm 6 

from PIL import Image, ImageFilter, ImageChops
from pytesseract import image_to_string
import cv2
import numpy


def preprocess_image_using_pil(image_path):
    # unblur, sharpen filters
    img = Image.open(image_path)
    img = img.convert("RGBA")

    pixdata = img.load()

    # Make the letters bolder for easier recognition
    
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][0] < 90:
                pixdata[x, y] = (0, 0, 0, 255)

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][1] < 136:
                pixdata[x, y] = (0, 0, 0, 255)

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)

    # And sharpen it
    img.filter(ImageFilter.SHARPEN)
    img.save("input-black.gif")

    #   Make the image bigger (needed for OCR)
    basewidth = 1000  # in pixels
    im_orig = Image.open('input-black.gif')
    wpercent = (basewidth/float(im_orig.size[0]))
    hsize = int((float(im_orig.size[1])*float(wpercent)))
    big = img.resize((basewidth, hsize), Image.ANTIALIAS)

    # tesseract-ocr only works with TIF so save the bigger image in that format
    ext = ".tif"
    tif_file = "input-NEAREST.tif"
    big.save(tif_file)
    
    return tif_file


def get_captcha_text_from_captcha_image(captcha_path):
    # Preprocess the image befor OCR
    tif_file = preprocess_image_using_opencv(captcha_path)
    # Perform OCR using tesseract-ocr library
    image = Image.open(tif_file)
    ocr_text = image_to_string(image, config="-psm 6")
    alphanumeric_text = ''.join(e for e in ocr_text)

    return alphanumeric_text

def binarize_image_using_pil(captcha_path, binary_image_path='input-black-n-white.gif'):
    im = Image.open(captcha_path).convert('L')
 
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if im.getpixel((i,j)) > 127:
                im.putpixel((i,j), 255)
            else:
                im.putpixel((i,j), 0)

    im.save(binary_image_path)
    return binary_image_path


def binarize_image_using_opencv(captcha_path, binary_image_path='input-black-n-white.jpg'):
    img = cv2.imread(captcha_path)
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # although thresh is used below, gonna pick something suitable
    im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite(binary_image_path, im_bw)
    return binary_image_path


def preprocess_image_using_opencv(captcha_path):
    bin_image_path = binarize_image_using_opencv(captcha_path)

    im_bin = Image.open(bin_image_path)
    
    basewidth = 340  # in pixels
    wpercent = (basewidth/float(im_bin.size[0]))
    hsize = int((float(im_bin.size[1])*float(wpercent)))
    big = im_bin.resize((basewidth, hsize), Image.NEAREST)
    
    # tesseract-ocr only works with TIF so save the bigger image in that format
    ext = ".tif"
    tif_file = "input-NEAREST.tif"
    big.save(tif_file)

    return tif_file


if __name__ == "__main__":
    print get_captcha_text_from_captcha_image("test.jpg") 
