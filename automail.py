import yagmail
import os
import datetime

now = datetime.datetime.now()
formatted_date = now.strftime('%Y-%m-%d')
date = now.strftime('%d')

receiver = "karthikeyangan05@gmail.com"  # receiver email address
body = f"Attendence-File-{date}"  # email body
filename = "Attendance"+os.sep+"{}".format(formatted_date)

yag = yagmail.SMTP("karthikeyan.g.2023.csbs@ritchennai.edu.in", "Karthik@1csbs")

yag.send(to=receiver, subject="Attendance Report", contents=body, attachments=filename)

