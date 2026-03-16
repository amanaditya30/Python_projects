import cv2
import numpy as np

image = cv2.imread("coins.jpg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

kernel = np.ones((3,3), np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)

count = 0

for i in range(1, num_labels):
    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]

    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    count += 1

print("Objects detected:", count)

cv2.imshow("Objects", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
