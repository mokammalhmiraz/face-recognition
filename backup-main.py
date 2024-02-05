import cv2
import dlib
import numpy as np
import face_recognition as fr
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import pickle

cred = credentials.Certificate("Face-Recognision/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attendance-system-b93d3-default-rtdb.firebaseio.com/",
    'storageBucket': "attendance-system-b93d3.appspot.com"
})

# Step 2: Liveness Detection with Eye Blinking
EYE_AR_THRESH = 0.85  # You may need to adjust this threshold based on your use case

file = open('Face-Recognision/EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)



def point_to_tuple(point):
    return (point.x, point.y)
def eye_aspect_ratio(eye):
    A = np.linalg.norm(np.array(point_to_tuple(eye[1])) - np.array(point_to_tuple(eye[5])))
    B = np.linalg.norm(np.array(point_to_tuple(eye[2])) - np.array(point_to_tuple(eye[4])))
    C = np.linalg.norm(np.array(point_to_tuple(eye[0])) - np.array(point_to_tuple(eye[3])))
    ear = (A + B) / (2.0 * C)
    return ear

def liveness_detection(frame, detector, predictor):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    ear = 0
    counter = 0
    modeType = 0
    id = -1

    for face in faces:
        landmarks = predictor(gray, face)
        left_eye = [landmarks.part(i) for i in range(36, 42)]
        right_eye = [landmarks.part(i) for i in range(42, 48)]

        left_eye_aspect_ratio = eye_aspect_ratio(left_eye)
        right_eye_aspect_ratio = eye_aspect_ratio(right_eye)

        ear = (left_eye_aspect_ratio + right_eye_aspect_ratio) / 2.0

        if ear < EYE_AR_THRESH:
            print("Liveness: Real Human")
            rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB
            face_locations = fr.face_locations(rgb_frame)

            if face_locations is not None and len(face_locations) > 0:
                print("Face Detected: Real Human")

                faceCurFrame = fr.face_locations(frame)
                encodeCurFrame = fr.face_encodings(frame, faceCurFrame)
                for encodeFace, faceloc in zip(encodeCurFrame, faceCurFrame):
                    matches = fr.compare_faces(encodeListKnown, encodeFace)
                    faceDis = fr.face_distance(encodeListKnown, encodeFace)
                    # print("Matches", matches)
                    # print("faceDis", faceDis)

                    matchIndex = np.argmin(faceDis)
                    # print("Match Index", matchIndex)

                    if matches[matchIndex]:
                        print("Known Face")
                        print(studentIds[matchIndex])
                        # y1, x2, y2, x1 = faceloc
                        # y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                        # bbox = 0 + x1, 480 + y1, x2 - x1, y2 - y1
                        # img = cvzone.cornerRect(img, bbox,rt=0)
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

                        # Update data of Present
                        if studentInfo:
                            print(studentInfo)
                            datetimeObject = datetime.strptime(studentInfo['Last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                            secondElapsed = (datetime.now() - datetimeObject).total_seconds()
                        if facultyInfo:
                            print(facultyInfo)
                            datetimeObject = datetime.strptime(facultyInfo['Last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                            secondElapsed = (datetime.now() - datetimeObject).total_seconds()
                        if secondElapsed > 5:

                            if studentInfo:
                                ref = db.reference(f'Students/{id}')
                                studentInfo['Total_attendance'] += 1
                                ref.child('Total_attendance').set(studentInfo['Total_attendance'])
                                ref.child('Last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            if facultyInfo:
                                ref = db.reference(f'Faculty/{id}')
                                facultyInfo['Total_attendance'] += 1
                                ref.child('Total_attendance').set(facultyInfo['Total_attendance'])
                                ref.child('Last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        else:
                            counter = 0
                    counter += 1

                    if counter >= 10:
                        counter = 0
                        studentInfo = []
            else:
                print("Face Detected: Not Real Human")

            for top, right, bottom, left in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            return frame


        else:
            print("Liveness: Not Real Human")

    return ear < EYE_AR_THRESH

# Step 3: Face Recognition using pre-trained models
def recognize_faces(frame):
    rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB
    face_locations = fr.face_locations(rgb_frame)

    if face_locations:
        print("Face Detected: Real Human")
    else:
        print("Face Detected: Not Real Human")

    for top, right, bottom, left in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    return frame

# Capture live video
video_capture = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("E:/Python/Python Works/shape_predictor_68_face_landmarks.dat")  # Replace with the path to your file

while True:
    ret, frame = video_capture.read()

    # Step 2: Liveness Detection
    is_live = liveness_detection(frame, detector, predictor)


    # Step 3: Face Recognition using pre-trained models
    frame = recognize_faces(frame)



    # Display the frame
    cv2.imshow('Video', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all windows
video_capture.release()
cv2.destroyAllWindows()