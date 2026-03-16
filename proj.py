import face_recognition
import cv2
import numpy as np
import os
import pandas as pd
from datetime import datetime

path = "students"
images = []
names = []

myList = os.listdir(path)

for img in myList:
    
    curImg = cv2.imread(f"{path}/{img}")
    images.append(curImg)
    
    names.append(os.path.splitext(img)[0])
def findEncodings(images):

    encodeList = []

    for img in images:
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        
        encodeList.append(encode)

    return encodeList

encodeListKnown = findEncodings(images) def markAttendance(name):

    with open("attendance.csv","r+") as f:
        
        myDataList = f.readlines()
        nameList = []
        
        for line in myDataList:
            
            entry = line.split(",")
            nameList.append(entry[0])

        if name not in nameList:
            
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")

            f.writelines(f"\n{name},{dtString}") cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()

    imgSmall = cv2.resize(img,(0,0),None,0.25,0.25)
    imgSmall = cv2.cvtColor(imgSmall,cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgSmall)
    encodesCurFrame = face_recognition.face_encodings(imgSmall,facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame,facesCurFrame):

        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:

            name = names[matchIndex].upper()

            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4

            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(img,name,(x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,(255,255,255),2)

            markAttendance(name)

    cv2.imshow("Attendance System",img)

    if cv2.waitKey(1) == 13:
        break
