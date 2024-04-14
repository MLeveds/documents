from ultralytics import YOLO
from typing import Optional
from src.config.app.config import settings_app
from src.ml.ocr_parser import get_ocr

class Model:
    def __init__(self, weights_path: str):
        self.model = YOLO(weights_path)

    
    def predict(self, image_path: str, confidence_tr: float = 0.5, 
                save_crop: bool = False, save: bool = False, 
                project: Optional[str] = settings_app.APP_PATH + '/storage/', name: Optional[str] = 'predicts'):
        data = self.model.predict(source=image_path, conf=confidence_tr, 
                                  save_crop=save_crop, save=save, project=project, name=name)
        confidence_cls = data[0].boxes.cls[0]
        confidences = data[0].boxes.conf

        highest_confidence = 0
        class_id = 5

        for i in range(len(confidence_cls)):
            if confidence_cls[i] != 5:
                if confidences[i] > highest_confidence:
                    highest_confidence = confidences[i]
                    class_id = confidence_cls[i]

        confidence = highest_confidence
        page = 0

        if class_id == 0 or class_id == 3 or class_id == 6:
            page = 2
        elif class_id == 1 or class_id == 2 or class_id == 4 or class_id == 7:
            page = 1
        else:
            page = None
        
        crops_path = project + 'predicts/crops/series'

        return {
            'file_type_id': class_id,
            'confidence': confidence,
            'data': get_ocr(crops_path, class_id),
            'page': page
        }
        
