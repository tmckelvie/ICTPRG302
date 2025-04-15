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


administrator   = "Joe Bloggs"                              # Administrator's name

#email information - using Google SMTP because Jetmail is having issues

port = 465                                                  # Use port 465 for SSL, various servers use different ports, make sure correct port is used
smtp_server = "smtp.gmail.com"                              # SMTP server URL, set up for gmail
password = "some password"                                  # App password supplied by google for the sender email address on the following line
sender_email = "tafestudent601@gmail.com"                   # Email account responsible for sending logs to administrator
receiver_email = "03112869@students.sunitafe.edu.au"        # Email account of recipient, administrator in this case


backup_folder = "Backups"                                   # Folder to store backups in, relative path. Absolute paths work also but must be valid and exist
log_folder = "Logs"                                         # Folder to store logs in, relative path. Absolute paths work also but must be valid and exist

jobs = {
        "job1" : {"target" : "Test Files/test.txt", "type" : "file", "archive" : False},
        "job2" : {"target" : "Test Files/Test Directory", "type" : "dir", "archive" : True},
        "job3" : {"target" : "Test Files/test.txt", "type" : "nana", "archive" : True}
        }




