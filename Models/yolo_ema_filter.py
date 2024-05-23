import cv2
from ultralytics import YOLO
import numpy as np
import time
from MA_filter import coordinate
from interface import CommandArduino, infer
model = YOLO('yolov8n-pose.pt')
cap = cv2.VideoCapture(0)
inferOb = infer(640, 480)
arduino = CommandArduino(Speed=2)
desired_fps = 10
frame_delay = 1.0 / desired_fps
coord  = coordinate([320,240])
alpha = 0.5  # Smoothing factor
xavg_ema = None
yavg_ema = None

while cap.isOpened():
    start_time = time.time()
    success, frame = cap.read()
    if success:
        frame = cv2.resize(frame, (640, 480))
        cv2.line(frame, (640//2, 0), (640//2,480), color=(0,0,0), thickness=2)
        cv2.line(frame, (0, 480//2), (640, 480//2), color=(0,0,0), thickness=2)
        results = model(frame, save=True)[0] # Trying only one persone detection
        for point in results.keypoints:
            top = np.array(point.xy[0][0:7], dtype='float')
            if(top.any()):
                # xavg = int(np.mean(top[:, 0]))
                # yavg = int(np.mean(top[:, 1]))
                # The following line just detects the nose points from pose points array.
                xavg = int(top[0][0])
                yavg = int(top[0][1])
                # Applying simple MA filter to prevent ouliers
                xavg, yavg = coord.c([xavg, yavg])
                # Applying second filter (EMA) to smoothen the movements
                xavg_ema = coord.ema_filter(xavg, xavg_ema, alpha)
                yavg_ema = coord.ema_filter(yavg, yavg_ema, alpha)
                inference = inferOb.reinfer(xavg_ema,yavg_ema, MOE = 40)
                arduino.readtheroom(inference)
                cv2.circle(frame, center=(int(xavg_ema), int(yavg_ema)), radius=5, color=(0, 0, 255), thickness=5)
        # if u need to see the body frame (although not needed)
        # annotate = results[0].plot()
        # cv2.imshow("I can see you", annotate)
        cv2.imshow('Tracker', frame)
        # Wait for the remaining time to reach desired frame rate
        processing_time = time.time() - start_time
        remaining_time = frame_delay - processing_time
        if remaining_time > 0:
            time.sleep(remaining_time)
        # Check for exit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
