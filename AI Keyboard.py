import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller
cap = cv2.VideoCapture(0)
cap.set(3, 1200)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
keys =[["Q","W","E","R","T","Y","U","I","O","P"],
     ["A","S","D","F","G","H","J","K","L",";"],
      ["Z","X","C","V","B","N","M",".","/"] ]
finalText = ""

keyboard = Controller()
def drawALL(img, buttonList):

     for button in buttonList:
         x, y = button.pos
         w, h = button.size
         cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
         cv2.putText(img, button.text, (x + 10, y + 50),
                 cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

     return img

class Button():
     def __init__(self,pos,text,size=[65,65]):
          self.pos = pos
          self.size = size
          self.text = text




buttonList = []

for i in range(len(keys)):
     for j, key in enumerate(keys[i]):
          buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


while True:
     success, img = cap.read()
     img = detector.findHands(img)
     lmList, bboxInfo = detector.findPosition(img)
     img =  drawALL(img, buttonList)

     if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                   cv2.rectangle(img, button.pos, (x + w, y + h), (175,0 , 175), cv2.FILLED)
                   cv2.putText(img, button.text, (x + 10, y + 50),
                               cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                   l,_,_ = detector.findDistance(8, 12, img,draw=False)
                   print(l)

                   ##when clicked
                   if l<45:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 10, y + 50),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        finalText += button.text
                        sleep(0.15)


     cv2.rectangle(img, (50,350), (700,450), (0, 0, 0), cv2.FILLED)
     cv2.putText(img, finalText, (60, 425),
                 cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

     cv2.imshow("Image", img)
     cv2.waitKey(1)

