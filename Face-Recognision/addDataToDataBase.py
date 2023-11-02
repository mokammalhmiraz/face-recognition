import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://attendance-system-b93d3-default-rtdb.firebaseio.com/"
})

std = db.reference('Students')


stddata = {
    "201":
        {
            "Name": "Himel",
            "ID": 201123,
            "Department": "CSE",
            "Batch": 201,
            "Starting_Year": 2020,
            "Total_attendance": 0,
            "CGPA": 3.5,
            "Last_attendance_time": "2022-09-20 00:54:22"
        },
    "2054":
        {
            "Name": "Miraz",
            "ID": 201002054,
            "Department": "CSE",
            "Batch": 201,
            "Starting_Year": 2020,
            "Total_attendance": 0,
            "CGPA": 3.00,
            "Last_attendance_time": "2022-09-20 00:54:22"
        },

    "2051":
        {
            "Name": "Rabbi",
            "ID": 20151,
            "Department": "CSE",
            "Batch": 201,
            "Starting_Year": 2020,
            "Total_attendance": 0,
            "CGPA": 3.20,
            "Last_attendance_time": "2022-09-20 00:54:22"
        }
}

for key, value in stddata.items():
    std.child(key).set(value)

fec = db.reference('Faculty')

facdata = {
    "faculty1":
        {
            "Name": "MR Palash Roy",
            "Status": "Lecturer",
            "Starting_Year": 2020,
            "Total_attendance": 0,
            "Last_attendance_time": "2022-09-20 00:54:22"
        }
}

for key, value in facdata.items():
    fec.child(key).set(value)