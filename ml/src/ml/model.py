from ultralytics import YOLO
from typing import Optional
import cv2

class Model:
    def __init__(self, weights_path: str):
        self.model = YOLO(weights_path)

    
    def predict(self, image_path: str, confidence: float = 0.5, 
                save_crop: bool = False, save: bool = False, 
                project: Optional[str] = None, name: Optional[str] = None):
        data = self.model.predict(source=image_path, conf=confidence, 
                                  save_crop=save_crop, save=save, project=project, name=name)
        data.results.boxes.xyxy
    
    def get_prediction(self, image_path: str):
        crops = self.predict(image_path) # bbox of cropped series and number
        img = cv2.imread(image_path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian Blur
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # Use adaptive thresholding to create a binary image
        thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 13, 9)
        
