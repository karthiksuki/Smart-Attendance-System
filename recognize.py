import datetime
import os
import time
import cv2
import pandas as pd

def recognize_attendence():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel"+os.sep+"Trainner.yml")
    harcascadePath = "haarcascade_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("StudentDetails"+os.sep+"StudentDetails.csv")
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5, minSize=(int(minW), int(minH)), flags=cv2.CASCADE_SCALE_IMAGE)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

            print(f"Detected ID: {Id} with confidence: {conf}")  # Debug print

            if conf > 37:
                aa = df.loc[df['Id'] == Id]['Name'].values[0] if not df.loc[df['Id'] == Id]['Name'].empty else "Unknown"
                confstr = "  {0}%".format(round(100 - conf))
                tt = f"{Id}-{aa}"
            else:
                Id = 'Unknown'
                tt = str(Id)
                confstr = "  {0}%".format(round(100 - conf))

            if (100-conf) > 40:  # Further relax the threshold if needed
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
                attendance = attendance._append({'Id': Id, 'Name': aa, 'Date': date, 'Time': timeStamp}, ignore_index=True)

                print(f"Added to attendance: Id={Id}, Name={aa}, Date={date}, Time={timeStamp}")  # Debug print

            tt = str(tt)
            if (100-conf) > 40:
                tt = tt + " [Pass]"
                cv2.putText(im, str(tt), (x+5,y-5), font, 1, (255, 255, 255), 2)
            else:
                cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

            if (100-conf) > 50:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 0), 1)
            elif (100-conf) > 40:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
            else:
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)

        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('Attendance (Verification)', im)
        if cv2.waitKey(1) == ord('q'):
            break

    print("Final attendance data:")
    print(attendance)

    if not attendance.empty:
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        fileName = "Attendance"+os.sep+"Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
        attendance.to_csv(fileName, index=False)
        print(f"Attendance successfully saved to {fileName}")
    else:
        print("No attendance data to save.")

    cam.release()
    cv2.destroyAllWindows()

