import re
import os
import pytesseract
import cv2
from src.database.models.document_type import DocumentType


EMPTY_OUTPUT = {'series': '', 'number': ''}
NUM2SYMB = {
    7: 'T',
    1: 'T',
    4: 'A',
    6: 'B',
    8: 'B',
    0: 'O'
}
ENG2RUS = {
    "A": "А",
    "B": "В",
    "C": "С",
    "E": "Е",
    "H": "Н",
    "K": "К",
    "M": "М",
    "O": "О",
    "P": "Р",
    "T": "Т",
    "X": "Х",
    "Y": "У",
}

def get_ocr(crops_path: str, document_class_id: str) -> dict[str, str]:
    document_type = DocumentType.to_str(document_class_id)
    directory = os.fsencode(crops_path)
    for file in os.listdir(directory):
        parsed_data = parse_ocr(crops_path + '/' + file, document_type)
        if parsed_data != EMPTY_OUTPUT:
            return parsed_data
    return EMPTY_OUTPUT

def preprocess_crop(image_path: str):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Use adaptive thresholding to create a binary image
    thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 13, 9)

    
    return smart_rotate(thresholded)

# TODO: write smart rotate function
def smart_rotate(image):
    return image

def parse_ocr(cropped_image_path: str, document_type: str) -> dict[str, str]:
    image = preprocess_crop(cropped_image_path)
    raw_text = pytesseract.image_to_string(image, config='-c --tessedit_char_whitelist=0123456789ABCEHKMOPTY')
    if len(raw_text) < 10:
        return EMPTY_OUTPUT
    
    match document_type:
        case 'Паспорт':
            return parse_passport(raw_text)
        case 'Водительское удостоверение':
            return parse_driver_license(raw_text)
        case 'ПТС':
            return parse_pts(raw_text)
        case 'СТС':
            return parse_sts(raw_text)
        case _:
            return EMPTY_OUTPUT


def parse_passport(raw_text: str) -> dict[str, str]:
    sernum = ''.join(re.findall(r'\d+', raw_text))
    if len(raw_text) != 10:
        return EMPTY_OUTPUT
    ser = sernum[0:4]
    num = sernum[4:]
    return {'series': ser, 'number': num}


def parse_driver_license(raw_text: str) -> dict[str, str]:
    sernum = ''.join(re.findall(r'\d+', raw_text))
    if len(raw_text) != 10:
        return EMPTY_OUTPUT
    ser = sernum[0:4]
    num = sernum[4:]
    return {'series': ser, 'number': num}


def parse_pts(raw_text: str) -> dict[str, str]:
    raw_text = ''.join(raw_text.split())
    if len(raw_text) != 10:
        return EMPTY_OUTPUT
    ser1 = raw_text[0:2]
    ser2 = ''.join(map(lambda x: ENG2RUS[NUM2SYMB.get(x, x)], raw_text[2:4]))
    num = raw_text[4:]
    return {'series': ser1 + ser2, 'number': num}
    
    

def parse_sts(raw_text: str) -> dict[str, str]:
    raw_text = ''.join(raw_text.split())
    if len(raw_text) != 10:
        return EMPTY_OUTPUT
    ser1 = raw_text[0:2]
    ser2 = ''.join(map(lambda x: ENG2RUS[NUM2SYMB.get(x, x)], raw_text[2:4]))
    num = raw_text[4:]
    return {'series': ser1 + ser2, 'number': num}
