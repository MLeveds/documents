from PIL import Image
import easyocr
import numpy as np
import re


class Parser:
    def __init__(self, is_gpu=False):
        self.reader = easyocr.Reader(lang_list=['ru'], gpu=is_gpu)
        self.serial = None
        self.number = None

    def parse_passport(self, image_path):
        image = Image.open(image_path)
        rotated_image = image.transpose(Image.ROTATE_90)
        result = self.reader.readtext(np.array(rotated_image), allowlist=' 123456789')
        for i in range(len(result) - 2):
            if (
                len(result[i][1]) == 2
                and len(result[i+1][1]) == 2
                and len(result[i+2][1]) == 6
                and result[i][1].isdigit()
                and result[i+1][1].isdigit()
                and result[i+2][1].isdigit()
            ):
                self.serial = result[i][1] + result[i+1][1]
                self.number = int(result[i+2][1])
        print("Серия:", self.serial)
        print("Номер:", self.number)

    def parse_pts(self, image_path):
        image = Image.open(image_path)
        result = self.reader.readtext(np.array(image))
        for i in range(len(result) - 2):
            if (
                len(result[i][1]) == 2
                and len(result[i+1][1]) == 2
                and len(result[i+2][1]) == 6
                and result[i][1].isdigit()
                and result[i+1][1].isalpha()
                and result[i+2][1].isdigit()
            ):
                self.serial = result[i][1] + result[i+1][1]
                self.number = int(result[i+2][1])
        print("Серия:", self.serial)
        print("Номер:", self.number)

    def parse_sts(self, image_path):
        image = Image.open(image_path)
        result = self.reader.readtext(np.array(image))
        regex_pattern = r"\d{2}\s*\D*\d{2}\s*\D*\d{6}"
        for detection in result:
            match = re.match(regex_pattern, detection[1])
            if match:
                filtered_string = ''.join([char for char in match.string if char.isdigit()])
                self.serial = filtered_string[:4]
                self.number = filtered_string[4:]
        print("Серия:", self.serial)
        print("Номер:", self.number)

    def parse_licence(self, image_path):
        image = Image.open(image_path)
        result = self.reader.readtext(np.array(image))
        for detection in result:
            filtered_string = ''.join([char for char in detection[1] if char.isdigit()])
            if len(filtered_string) >= 4 and filtered_string.isdigit():
                self.serial = filtered_string[:4]
                self.number = filtered_string[4:]
                break
        print("Серия:", self.serial)
        print("Номер:", self.number)
