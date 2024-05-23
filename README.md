# CanCU
A simple Bot to move the camera to where the human is located using two servo motors, a beta-version of the automatic sentry-turret project
# What it does?
The file titled ```human_pose_detection_yolo.py``` only does the human pose detection part, which uses the ```YOLO-v8-Pose``` model to estimate the pose of human present in the frame, after that the code takes the most probable result and gives the location of a point. The file inside the ```Models``` folder processes the ouptut with a Simple MA filter and an then an EMA filter to smoothen the movement of the 'Red Dot' on the frame, after that i have used the firmata protocol to control two servo so as to adjust the camera center to the location of that points. The build i used was decent at the detection and moving the camera task. 
### Note:
1. If the servos move too fast try reducing the speed variable while declaring the ```CommandArduino``` Class object in the main file.
2. The outer file ```human_pose_detection_yolo.py``` might give error so try moving it inside the ```Models``` Folder and then running.

## Future Development:
This is to be extendend to an automatic aiming gun(Sentry Turret) like project. For that we would require a more satble build. Also, since the cmaera would be attached to a Rpie, we cannot process the vidoes stream on the Rpie itself, so We're planning to use a flask server to stream the video on a website and then process the stream on our laptop, to send it back to the Rpie4 backend.
