import cv2
import numpy as np

image = cv2.imread("document.jpg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray,(5,5),0)

edges = cv2.Canny(blur,50,150)

contours,_ = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

largest = max(contours,key=cv2.contourArea)

peri = cv2.arcLength(largest,True)

approx = cv2.approxPolyDP(largest,0.02*peri,True)

pts = approx.reshape(4,2)

pts = np.float32(pts)

dst = np.float32([[0,0],[500,0],[500,700],[0,700]])

matrix = cv2.getPerspectiveTransform(pts,dst)

scan = cv2.warpPerspective(image,matrix,(500,700))

cv2.imshow("Scanned",scan)
cv2.waitKey(0)
cv2.destroyAllWindows()
