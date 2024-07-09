##  This code should be put on the device we want to process on

import cv2, socket, numpy, pickle
import cv2
from ultralytics import YOLO
import numpy as np
import time
from MA_filter import coordinate
from interface import  infer
s=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
ip="YOUR SERVER IP HERE"
port=6666
s.bind((ip,port))
model = YOLO('yolov8n-pose.pt')
cap = cv2.VideoCapture(0)
inferOb = infer(640, 480)
# arduino = CommandArduino(Speed=2)
desired_fps = 100
frame_delay = 1.0 / desired_fps
coord  = coordinate([320,240])
alpha = 0.5  # Smoothing factor
xavg_ema = None
yavg_ema = None
while True:
    start_time = time.time()
    x=s.recvfrom(1000000)
    clientip = x[1][0]
    data=x[0]
    data=pickle.loads(data)
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
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
            # arduino.readtheroom(inference)
            print("inference",inference)
            ## Here We have to make a server to send this inference
            ### Btw, XY is for correct positioning, and MOE is the margin of error for that 'center' box

            ## We need to send it back to client on another (http) server on it
            cv2.circle(frame, center=(int(xavg_ema), int(yavg_ema)), radius=5, color=(0, 0, 255), thickness=5)
    # if u need to see the body frame (although not needed)
    if(len(results)>=1):
        annotate = results[0].plot()
        
        cv2.imshow("I can see you", annotate)
    else:
        cv2.imshow("i can see you", frame)
    # cv2.imshow('Tracker', frame)
    # Wait for the remaining time to reach desired frame rate
    processing_time = time.time() - start_time
    remaining_time = frame_delay - processing_time
    if remaining_time > 0:
        time.sleep(remaining_time)
    # Check for exit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # cv2.imshow('server', data) #to open image
    # if cv2.waitKey(10) == 13:
    #     break
cv2.destroyAllWindows()