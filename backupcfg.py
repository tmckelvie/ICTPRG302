"""Backup Configuration File

This file is used to store job configuration(s) for "backup.py".
Individual job configurations use the Python dictionary format, but it 
seems simpler to have named constants for the system administrator 
and their contact email in the event of a failure.


Example
administrator   = "Joe Bloggs"
backup_folder   = "Backups"
log_folder      = "Logs"

jobs            = {
                   "job1" : {"target" : "FILE PATH/FILE NAME", "type" : "file", "archive" : False},
                   "job2" : {"target" : "DIR PATH/DIR NAME", "type" : "dir", "archive" : True}
                  }}    
"""


administrator   = "Joe Bloggs"
#email information - using Google SMTP because Jetmail is having issues
port = 465 # Use port 465 for SSL
smtp_server = "smtp.gmail.com"
password = "fpwm cfck zqrw azpj"
sender_email = "tafestudent601@gmail.com"
receiver_email = "03112869@students.sunitafe.edu.au"


backup_folder = "Backups"
log_folder = "Logs"

jobs = {
        "job1" : {"target" : "Test Files/test.txt", "type" : "file", "archive" : False},
        "job2" : {"target" : "Test Files/Test Directory", "type" : "dir", "archive" : True},
        "job3" : {"target" : "Test Files/test.txt", "type" : "nana", "archive" : True}
        }




