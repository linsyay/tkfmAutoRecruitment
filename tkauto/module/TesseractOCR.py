import pytesseract

pytesseract.pytesseract.tesseract_cmd = R'C:\Program Files\Tesseract-OCR\tesseract'

#6 7 10 11?
config = ('-l kor --oem 1 --psm 7')

def get_tag(img_trim):
    return pytesseract.image_to_string(img_trim, config=config)