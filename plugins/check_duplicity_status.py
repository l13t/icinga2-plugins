#!/usr/bin/env python

# By Arne Schwabe <arne-nagios@rfc2549.org>
# modified by Dmytro Prokhorenkov
# LICENSE: BSD

from subprocess import Popen,PIPE
import sys
import time
import os
import argparse
import re

flags = {
    0 : 'OK',
    1 : 'WARNING',
    2 : 'CRITICAL',
    3 : 'UNKNOWN',
}

def main():
    parser = argparse.ArgumentParser(description='Nagios Duplicity status checker')

    parser.add_argument("-w", dest="warninc", default=28, type=int, 
                        help="Number of hours allowed for incremental backup warning level")
    parser.add_argument("-W", dest="warnfull", default=40, type=int, 
                        help="Number of hours allowed for incremental backup critical level")

    parser.add_argument("-c", dest="critinc", default=28, type=int, 
                        help="Number of hours allowed for full backup warning level")

    parser.add_argument("-C", dest="critfull", default=52, type=int, 
                        help="Number of hours allowed for full backup critical level")

    parser.add_argument("-f", dest="log_path", default="/var/log/duplicity/duplicity_collection_status.log", type=str,
                        help="Path to log of collection-status command")

    args = parser.parse_args()
    
    okay = 0

    output, err = Popen(["cat", args.log_path], stdout=PIPE, stderr=PIPE , env={'HOME': '/root', 'PATH': os.environ['PATH']}).communicate()


    lastfull, lastinc = findlastdates(output)


    sincelastfull = time.time() - lastfull 
    sincelastinc  =  time.time() - lastinc 

    msg = "OK: "
    
    if sincelastfull > (args.warnfull * 3600) or sincelastinc > (args.warninc * 3600):
        okay = 1
        msg = "WARNING: "
    
    if sincelastfull > (args.critfull * 3600) or sincelastinc > (args.critinc * 3600):
        okay = 2
        msg = "CRITICAL: "

    r_flag, r_status = checkoutput(output)
    if r_flag != 0:
        okay = r_flag
        msg = "%s: duplicity output: %s " % (flags[r_flag], r_status)


    if err:
        okay=3
        msg = "UNKNOWN: Unexpected output: %s, " % repr(err)

    print msg, "last full %s ago, last incremental %s ago|lastfull=%d, lastinc=%d" % ( formattime(sincelastfull), formattime(sincelastinc), sincelastfull, sincelastinc)
    sys.exit(okay)

def checkoutput(output):
    if output.find("403 Forbidden")!=-1:
        return 2, "Check credentials. Error in Duplicity configuration"
    if output.find("lockfile.lock")!=-1:
        f_name = re.search("\/root\/.*\/lockfile.lock", output).group(0)
        if os.path.isfile(f_name):
            lock_created = os.path.getmtime(f_name)
            dif_time = time.time() - lock_created
            dif_time_hour = int(dif_time // 60 // 60)
            dif_time_min = int((dif_time // 60) % 60)
            if check_process_exists():
                return 1, "Backup process is still running: %s hour(s) %s minute(s)" % (dif_time_hour, dif_time_min)
            else:
                return 2, "Duplicity backup failed %s hour(s) %s minute(s) ago." % (dif_time_hour, dif_time_min)
        else:
            return 2, "File issue"
        return 1, "Job finished but status file is now updated."
    if output.find("No orphaned or incomplete backup sets found.")==-1:
        return 2, "Some backup error. Please check logs."
    
    return 0, "OK"

def check_process_exists():
    exi = False
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for pid in pids:
        try:
            ch_proc = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read()
            if ch_proc.find("/usr/bin/duplicity")!=-1:
                exi = True
        except IOError:
            continue
    return exi

def formattime(seconds):
    days = seconds / (3600 * 24)
    hours = seconds / 3600 % 24

    if days:
        return "%d days %d hours" % (days,hours)
    else:
        return "%d hours" % hours


def findlastdates(output):
    lastfull =0
    lastinc = 0

    for line in output.split("\n"):
        parts = line.split()

        # ['Incremental', 'Sun', 'Oct', '31', '03:00:04', '2010', '1']
        if len (parts) == 7 and parts[0] in ["Full","Incremental"]:
            foo = time.strptime(" ".join(parts[1:6]),"%a %b %d %H:%M:%S %Y")

    
            backuptime =  time.mktime(foo)
    
            if parts[0] == "Incremental" and lastinc < backuptime:
                lastinc = backuptime
            elif parts[0] == "Full" and lastfull < backuptime:
                lastfull = backuptime
        

    # Count a full backup as incremental backup
    lastinc = max(lastfull,lastinc)
    return (lastfull, lastinc)
            
        
	

if __name__=='__main__':
   main()
