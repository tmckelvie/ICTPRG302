""" backup.py - Application to perform backup of file or directory, parameters of jobs are stored in
    backupcfg.py configuration file. Can be used manually or started from a scheduled task and uses 
    default Python libraries and functions so should work on any platform which has Python installed.
    
    USAGE: python.py backup.py [jobname]
    
    jobname: 'job' followed by numeric index of required task
"""


import backupcfg    # import the configuration file
import argparse     # library for parsing arguments
import zipfile      # zip library for compressing single files
import logging      # logging library
import datetime     # time and date library
import time         # Time related library
import os           # os library
import shutil       # shell utilities
import smtplib      # simple mail library
import ssl          # secure socket layer library

from email.message import EmailMessage  # email library provides the EmailMessage class for easy construction of email

logger = logging.getLogger("")  # Create a global variable for a logger instance
successful_backup = False       # Boolean flag to determine whether backup succeeded, default False
                                # and set to True only on successful backup.
error_log_status = "ERROR"
success_log_status = "SUCCESS"

def sendEmail(message_content):
    """ Send email to address provided in backupcfg.py, using smtplib"""
    
    # message is an instance of EmailMessage class, from email library.
    message = EmailMessage()
    # Set the fields so it is a properly formed email
    message['Subject'] = f"ATT: {backupcfg.administrator} - Backup Log"
    message['From'] = backupcfg.sender_email
    message['To'] = backupcfg.receiver_email

    # Insert message_content as the body of the email.
    message.set_content(message_content)
    
    # Create a secure SSL context
    context = ssl.create_default_context()
    
    try:
        # Using smtplib, create an instance of SMTP_SSL class to use as our outbound server.
        with smtplib.SMTP_SSL(backupcfg.smtp_server, backupcfg.port, context = context) as server:
            # Attempt connection to the smtp server named in backupcfg.py, on a port that supports the version of SSL we are using.
            server.connect(backupcfg.smtp_server, 465)
            # Attempt logging into smtp server.
            server.login(backupcfg.sender_email, backupcfg.password)
            # Attempt to send the email.
            server.send_message(message)

    
    
    except Exception as err:
        #Catch any other errors during smtp attempts, provide details in log file.
        addToLogFile(f"An error has occurred when trying to send email: - {err}", error_log_status)
      

def addToLogFile(log_message, log_status_msg = ""):
    """Simple function to add messages to the log file, prepends message with current time."""

    try:
        # Use datetime.today() to get current time & date for log entry, shorter operations may not reflect
        # any time lapsed but longer operations may, keep it verbose.
        now = datetime.datetime.today()
    
        # Extract only the necessary information and format it for file name/folder.
        log_time = datetime.datetime.strftime(now,"%H:%M:%S")
        
        # If the length of log_status_msg is greater than zero
        if len(log_status_msg) > 0:
            # Create string containing both status and msg.
            message = f"{log_status_msg} - {log_message}"
        else:
            # Otherwise assign log_msg as the entire log message to be added.
            message = log_message
        
        # Add log_message parameter to logfile, prepended with current time.
        logger.info(f"{log_time}    {message}")
        
    except Exception as err:
        print("An unexpected error has occurred: ", err)

def main():
    """ Main function of backup application."""
    
    # Use datetime.today() to get current time & date for creating backup name.
    now = datetime.datetime.today()
    
    # Extract only the necessary information and format it for file name/folder.
    target_datetime = datetime.datetime.strftime(now,"%y%m%d-%H%M%S")
    
    # Check if the log_folder named in backupcfg exists.
    if not os.path.exists(backupcfg.log_folder):
        # If it doesn't exist, attempt to create it.
        os.makedirs(backupcfg.log_folder)

    # Create log file name for use here and in sendEmail()
    log_file_name = f"{backupcfg.log_folder}/backup.{target_datetime}.log"
    
    #Configure logger
    logging.basicConfig(format='%(message)s',
    filename = log_file_name,
    level = logging.DEBUG)
    
    # Create an instance of the argparse class.
    parser = argparse.ArgumentParser(
            prog = "ICTPRG302 Backup Application",
            description = "Example application for assessment task B")
            
    # Add jobname as an argument.
    parser.add_argument("jobname")
    
    # Extract arguments from commandline.
    args = parser.parse_args()
    
    # Set jobname to whatever args.jobname contains.
    jobname = args.jobname
    addToLogFile(f"Starting '{jobname}'")
    
    # Confirm job is in list and extract the filename/path to perform a backup of.
    if args.jobname and jobname.startswith("job") and jobname[3:].isdecimal():
        
        try:
            # Grab filename/path from jobs dictionary.
            target = backupcfg.jobs[jobname]["target"]
            
            # Grab target type from backupcfg jobs dictionary.
            target_type = backupcfg.jobs[jobname]["type"]
                
            # Check if we are achiving (zip file) or not (direct copy of file/directory)
            is_archive = backupcfg.jobs[jobname]["archive"]
            
            # Set log information for job configuration being used.
            log_configuration_text = f"""--- Job configuration ---
            Target: {target}
            Type of target: {target_type}
            Backup output directory: {backupcfg.backup_folder}
            Create compressed archive: {is_archive}
            -------------------------"""
            
            addToLogFile(log_configuration_text)
            
            if not os.path.exists(target):
                # File does not exist, log this and finish.
                addToLogFile("Target file does not exist, exiting.", error_log_status)
                
            else:
                # Check if the backup_folder named in backupcfg exists.
                if not os.path.exists(backupcfg.backup_folder):
                    # If it doesn't exist, attempt to create it.
                    addToLogFile("Output directory doesn't exist, creating.")
                    os.makedirs(backupcfg.backup_folder)
                    
                    
                # Split target to root directory and file/directory.
                target_parts = os.path.split(target)
                    
                # Create the backup name based on target information with current date & time appended.
                backup_name = f"{backupcfg.backup_folder}/{target_parts[1]}.{target_datetime}"
                
                # Use target_type to determine whether it is a file or a directory.
                if target_type == "file":
                    # Target type is file.
                    if  not is_archive:
                        # Use shutil.copy2() to copy the target file, retaining as much metadata as possible.
                        shutil.copy2(target, backup_name)
                        addToLogFile(f"Created backup file: '{backup_name}'", success_log_status)
                        
                    else:
                        # Create compressed (zip) file of target file.
                        with zipfile.ZipFile(backup_name + ".zip", "w", compression=zipfile.ZIP_DEFLATED) as zf:
                            zf.write(target, os.path.basename(target))
                        
                        addToLogFile(f"Created backup archive: '{backup_name}''", success_log_status)    
                    
                elif target_type == "dir":
                    # Target type is directory.
                    if not is_archive:
                        # Use shutil.copytree() to copy entire directory and contents, default copy mode is copy2. 
                        shutil.copytree(target, backup_name, symlinks = True, dirs_exist_ok = True)
                        addToLogFile(f"Created backup directory: '{backup_name}'", success_log_status)
                        
                    else:
                        # Use shutil.make_archive() to create archive of entire directory and contents, zip file format.
                        shutil.make_archive(backup_name, "zip", target)
                        addToLogFile(f"Created backup archive: '{backup_name}'", success_log_status)
                    
                else:
                    # Unknown target type.
                    addToLogFile(f"Unknown target type: {target_type}.", error_log_status)
                    
        except KeyError:
            # The specified key doesn't exist in backupcfg.py, for example job name or other job parameters.
            addToLogFile("Key error. Please confirm backupcfg.py is correctly configured.", error_log_status)

        except Exception as err:
            # Final catch all for any unexpected error, log it and provide information about the job name and particular error.
            addToLogFile(f"An unexpected error has occured processing: {jobname}", error_log_status)
            addToLogFile(err)
            
    else:
        # No valid commandline argument was passed, log and exit.
        addToLogFile("Nothing to do, valid job name must be passed via commandline.", error_log_status)
        addToLogFile("Example: 'backup.py job1' - This will perform a backup using the job1 configuration.")
        
    # Use 'with' so we don't have to handle closing the log file after using it.
    with open(f"{backupcfg.log_folder}/backup.{target_datetime}.log") as fobj:
        # Read the log file that was created during execution.
        log_file_content = fobj.read()
        # Send content of email to administrator or email provided in backupcfg.log
        sendEmail(log_file_content)


if __name__ == "__main__":
    main()
