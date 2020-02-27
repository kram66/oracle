# -------------------------------------------------------------------------------------------------------------#
# About:		Script to parse parameter and perform the relevant backup and delete log files older than 5 days   # 														                                   #
#			      This currently runs in a Windows environment, but can be adapted for UNIX                          #
# Usage:    python rman_backup.py FullBackup                                                                   #
#           python rman_backup.py Archive (if you just want to backup archive logs)                            # 
# Author: 	Mark Young																	                                                       #
# Date:			18/12/2019																	                                                       #
# Why:			To perform a single point to backup an Oracle database using Python,                               #
#           that includes incremental (level 0 and 1)	as well as archive backups													     #
# History:	V1.0	Initial Code														                                                     #
# Requirements:	Python 3																	                                                     #
#				create a log directory														                                                     #
#				create a parameter directory												                                                   #
# -------------------------------------------------------------------------------------------------------------#
import sys
import os
import subprocess
import time
from datetime import datetime
import logging

# Lets define my procedure for parsing parameters
def get_args(name='default', first='NONE'):
    return first


BackupType = get_args(*sys.argv)


now = time.time()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=r'E:\scripts\logs\backup\backup_' + str(now) + '.log',
                    filemode='w')


# Lets setup some ground work
sid = "<put your sid here>"
#Define which day of the week you want to perform a full backup
FullOn = "Fri"
#How long do we want to keep some of the log files
PurgeTime = 3

# Lets setup some initial environment settings
os.putenv('NLS_DATE_FORMAT', 'DD-MM-YYYY HH24:MI:SS')
os.putenv('ORACLE_SID', sid)
os.system("echo %ORACLE_SID%")

# Setup the logfile and define where the scripts are located
# Lets salt the logfile so it's unique.
Salt1 = datetime.today().strftime('%m%d%Y')
Salt2 = datetime.today().strftime('%H%M%S')

# print("Backup_" +Salt1 + "_" + Salt2 + ".log")
logfile = r"e:\scripts\logs\backup"
logfileName = r'E:\scripts\logs\backup\backup_' + str(now) + '.log'

# Backup parameter files. Put your rman commands in these files
FullPath = r"e:\scripts\parameter\\"
FullBackup = FullPath + "full_backup.cmd"
Incremental = FullPath + "incremental_backup.cmd"
Archive = FullPath + "archive_backup.cmd"

# Now check for the day of the week so we can run either an incremental level 0 or 1
WeekDay = datetime.today().strftime('%a')

logging.info("We have a backup type of " + BackupType)

try:
    if BackupType.lower() == "fullbackup":
        if WeekDay == FullOn:
            logging.info("We are going to run a full backup or a level 0 backup")
            rmanCMD = 'rman cmdfile="' + FullBackup + '" log="' + logfileName + '" target /'
            output = subprocess.check_output(rmanCMD, shell=True)
        else:
            logging.info("We are going to run an incremental backup or a level 1 backup")
            rmanCMD = 'rman cmdfile="' + Incremental + '" log="' + logfileName + '" target /'
            output = subprocess.check_output(rmanCMD, shell=True)
    elif BackupType.lower() == "archive":
        logging.info("Taking an archive log backup")
        rmanCMD = 'rman cmdfile="' + Archive + '" log="' + logfileName + '" target /'
        output = subprocess.check_output(rmanCMD, shell=True)

    # Lets remove any log files older than the nominiated dates in PurgeTime 
    now = time.time()

    logging.info("Removing any old log files.....")

    for filename in os.listdir(logfile):
        if os.path.getmtime(os.path.join(logfile, filename)) < now - PurgeTime * 86400:
            if os.path.isfile(os.path.join(logfile, filename)):
                logging.info("del " + filename)
                os.remove(os.path.join(logfile, filename))

except subprocess.CalledProcessError as grepexec:
    logging.error(grepexec.returncode, grepexec.output)


