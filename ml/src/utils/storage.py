from fastapi import UploadFile
from src.config.app.config import settings_app
import random
import string
import shutil


class Storage:
    def save(self, file: UploadFile):
        file_ext = file.filename.split('.')[-1]
        filename = self.get_filename()
        path_to_save = self.get_path(filename + file_ext)

        with open(path_to_save, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return filename

    def get_path(self, file_name):
        return settings_app.APP_PATH + '/storage/' + file_name

    def get_filename(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(30))


storage = Storage()
