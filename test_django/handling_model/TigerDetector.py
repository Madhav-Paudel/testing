import cv2
from ultralytics import YOLO
import numpy as np
import os
import base64

class TigerDetector:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Path to the model
        model_path = os.path.join(BASE_DIR, 'mlmodels', 'best_enlightengan_and_yolov8.pt')
        self.model=YOLO(model_path)
        self.confidence_threshold=0.5




    def process_frame(self, frame):
        results = self.model.predict(source=frame, show=False)

        for detection in results[0].boxes:
            score = float(detection.conf.cpu().numpy().item())
            print(score)

            if score > self.confidence_threshold:
                box = detection.xyxy[0].cpu().numpy().astype(int)
                # Fixed parentheses around .cpu()
                class_id = int(detection.cls.cpu().numpy().item())
                if class_id == 534:  # Assuming 534 is the class for a tiger
                    print("tiger detected")
                    x_min, y_min, x_max, y_max = box
                    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                    label = f"Tiger ({score:.2f})"
                    cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        return frame



