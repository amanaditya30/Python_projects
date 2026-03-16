import cv2
import numpy as np

image = cv2.imread("puzzle.jpg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)

contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

pieces = []

for cnt in contours:

    area = cv2.contourArea(cnt)

    if area > 1000:

        x,y,w,h = cv2.boundingRect(cnt)

        piece = image[y:y+h,x:x+w]

        pieces.append(piece)

        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

print("Pieces detected:",len(pieces))

cv2.imshow("Puzzle Pieces",image)

cv2.waitKey(0)
cv2.destroyAllWindows()
