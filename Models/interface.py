import pyfirmata2
#The default frequency is 50Hz approx.
#Lowest dutycycle (1ms) at 0 degrees and highest (2ms) at 180 degrees.
class CommandArduino():
    def __init__(self, PORT = pyfirmata2.Arduino.AUTODETECT, Servo1 = 2, Servo2 = 3, Speed = 5):
        self.board = pyfirmata2.Arduino(PORT)
        self.servo_1 = self.board.get_pin(f'd:{Servo1}:s')
        self.servo_2 = self.board.get_pin(f'd:{Servo2}:s')
        self.s1_deg = 90
        self.s2_deg = 90
        self.servo_1.write(90)
        self.servo_2.write(90)
        self.speed = Speed
    def __del__(self):
        self.board.exit()
    def rotatePlusX(self):
        self.s1_deg += self.speed
        self.servo_1.write(int(self.s1_deg))
    def rotateMinusX(self):
        if(self.s1_deg >self.speed):
            self.s1_deg -= self.speed
            self.servo_1.write(int(self.s1_deg))
    def rotatePlusY(self):
        self.s2_deg += self.speed
        self.servo_2.write(int(self.s2_deg))
    def rotateMinusY(self):
        if(self.s2_deg >self.speed):
            self.s2_deg -= self.speed
            self.servo_2.write(int(self.s2_deg))
    def readtheroom(self, inference):
        print("inference: ", inference) 
        if(inference == 'XY'):
            pass
        elif(inference == 'XP'):
            self.rotatePlusX()
        elif(inference == 'XM'):
            self.rotateMinusX()
        elif(inference == 'YP'):
            self.rotatePlusY()
        elif(inference == 'YM'):
            self.rotateMinusY()
        else:
            print("No data to infer")
class infer():
    def __init__(self, frameX = 640, frameY = 480):
        self.frameX = frameX
        self.frameY = frameY
        self.oX = self.frameX//2
        self.oY = self.frameY//2
    def reinfer(self, newPosX, newPosY, MOE = 30):
        if(self.oX-MOE<newPosX<self.oX+MOE):
            if(self.oY-MOE<newPosY<self.oY+MOE):
                return 'XY'
            else:
                if(self.oY-MOE>newPosY):
                    return 'YM'
                else:
                    return 'YP'
        else:
            if(self.oX-MOE>newPosX):
                return 'XP'
            else:
                return 'XM'
if(__name__ == "__main__"):
    
    arduino = CommandArduino()
    arduino.rotatePlusX()
    arduino.rotatePlusX()
    arduino.rotateMinusY()
    arduino.rotateMinusY()