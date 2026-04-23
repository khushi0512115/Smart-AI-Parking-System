# detector.py

from ultralytics import YOLO
import cv2
from slots import slots

model = YOLO("yolov8n.pt")

def detect_parking(frame):
    results = model(frame)

    detected_cars = []

    for r in results:
        boxes = r.boxes.xyxy
        classes = r.boxes.cls

        for box, cls in zip(boxes, classes):
            if int(cls) == 2:  # car
                x1, y1, x2, y2 = map(int, box)
                detected_cars.append((x1, y1, x2, y2))

    free = 0
    occupied = 0

    for (sx, sy, sw, sh) in slots:
        is_occ = False

        for (x1, y1, x2, y2) in detected_cars:
            if (x1 < sx+sw and x2 > sx and y1 < sy+sh and y2 > sy):
                is_occ = True
                break

        if is_occ:
            color = (0,0,255)
            occupied += 1
        else:
            color = (0,255,0)
            free += 1

        cv2.rectangle(frame, (sx,sy), (sx+sw, sy+sh), color, 2)

    return frame, free, occupied