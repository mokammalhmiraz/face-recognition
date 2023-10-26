import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
from firebase_admin import storage


cred = credentials.Certificate("Face Recognision/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attendance-system-b93d3-default-rtdb.firebaseio.com/",
    'storageBucket': "attendance-system-b93d3.appspot.com"
})

face_cap = cv2.CascadeClassifier("E:/Python Work/Python Works/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# graphics
# imgBackground = cv2.imread("Face Recognision/Resources/FaceCamNew.png")


# import encoding file
file = open('Face Recognision/EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)

counter = 0
modeType = 0
id = -1

#webcam
while True:
    success, img = cap.read()

    # Resize the images
    # imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # img = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = face_cap.detectMultiScale(
        color,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    faceCurFrame = face_recognition.face_locations(img)
    encodeCurFrame = face_recognition.face_encodings(img,faceCurFrame)

    # imgBackground[162:162+480,55:55+640] = img

    for encodeFace,faceloc in zip(encodeCurFrame,faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        # print("Matches", matches)
        # print("faceDis", faceDis)

        matchIndex = np.argmin(faceDis)
        # print("Match Index", matchIndex)

        if matches[matchIndex]:
            print("Known Face")
            print(studentIds[matchIndex])
            #y1, x2, y2, x1 = faceloc
            #y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            #bbox = 0 + x1, 480 + y1, x2 - x1, y2 - y1
            #img = cvzone.cornerRect(img, bbox,rt=0)
            id = studentIds[matchIndex]
            print(id)

            # pt1 = (400, 40)
            # pt2 = (800, 300)
            # color = (0,255,0)
            # thickness = 4
            # lineType = cv2.LINE_4
            #
            # img_rect = cv2.rectangle(img, pt1, pt1, color, thickness, lineType)
            if counter == 0:
                counter = 1

    if counter != 0:

        if counter == 1:

            studentInfo = db.reference(f'Students/{id}').get()
            facultyInfo = db.reference(f'Faculty/{id}').get()

            #Update data of Present
            if studentInfo:
                print(studentInfo)
                datetimeObject = datetime.strptime(studentInfo['Last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondElapsed = (datetime.now() - datetimeObject).total_seconds()
            if facultyInfo:
                print(facultyInfo)
                datetimeObject = datetime.strptime(facultyInfo['Last_attendance_time'],"%Y-%m-%d %H:%M:%S")
                secondElapsed = (datetime.now()-datetimeObject).total_seconds()
            if secondElapsed >30:

                if studentInfo:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['Total_attendance'] +=1
                    ref.child('Total_attendance').set(studentInfo['Total_attendance'])
                    ref.child('Last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                if facultyInfo:
                    ref = db.reference(f'Faculty/{id}')
                    facultyInfo['Total_attendance'] += 1
                    ref.child('Total_attendance').set(facultyInfo['Total_attendance'])
                    ref.child('Last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                counter = 0
        counter+=1

        if counter>=10:
            counter = 0
            studentInfo = []


    cv2.imshow("Attendance", img)
    # cv2.imshow("FaceBG", imgBackground)
    cv2.waitKey(1)