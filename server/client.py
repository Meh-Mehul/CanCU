## This code should be put on to the device we want to send stream from 


## We will set up another (http) server on this machine to communicate back the inferences attained from the processing

import cv2,socket,pickle,os
import numpy as np
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,1000000)
server_ip = "YOUR SERVER IP HERE"
server_port = 6666

cap = cv2.VideoCapture(0)
while True:
	ret,photo = cap.read()
	cv2.imshow('streaming',photo)
	ret,buffer = cv2.imencode(".jpg",photo,[int(cv2.IMWRITE_JPEG_QUALITY),30])
	x_as_bytes = pickle.dumps(buffer)
	s.sendto((x_as_bytes),(server_ip,server_port))
	if cv2.waitKey(10)==13:
		break
cv2.destroyAllWindows()
cap.release()