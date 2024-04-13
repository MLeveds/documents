from fastapi import UploadFile
from src.config.app.config import settings_app
import random
import string
import shutil
import base64


class Storage:
    def save(self, file: UploadFile):
        file_ext = '.' + file.filename.split('.')[-1]
        filename = self.get_filename()
        path_to_save = self.get_path(filename + file_ext)

        with open(path_to_save, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return filename, file_ext

    def save_from_base64(self, image: str):
        # meta = data:image/jpeg;base64
        try:
            meta, image = image.split(',')
            mime = meta.split(':')[1].split(';')[0]
        except Exception:
            raise Exception('Invalid base64 string.')

        file_data = base64.b64decode(image)
        file_ext = self.get_ext_by_mime(mime)
        filename = self.get_filename()
        path_to_save = self.get_path(filename + file_ext)

        with open(path_to_save, "wb") as f:
            f.write(file_data)

        return filename, file_ext

    def get_path(self, file_name):
        return settings_app.APP_PATH + '/storage/' + file_name

    def get_filename(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(30))

    def get_ext_by_mime(self, mime: str):
        mime_extensions = {
            "image/jpeg": "jpg",
            "image/png": "png",
            "image/gif": "gif",
        }

        if mime in mime_extensions:
            return mime_extensions[mime]
        raise Exception('Unallowed mime type')


storage = Storage()
