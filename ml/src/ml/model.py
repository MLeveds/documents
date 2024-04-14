from ultralytics import YOLO
from typing import Optional
class YOLOmodel:
    def __init__(self, weights_path: str):
        self.model = YOLO(weights_path)

    def predict(self, image_path: str, confidence: float = 0.5, save_crop: bool = False, save: bool = False, project: Optional[str] = None, name: Optional[str] = None):
        return self.model.predict(source=image_path, conf=confidence, save_crop=save_crop, save=save, project=project, name=name)