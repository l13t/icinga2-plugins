# icinga2-plugins

## check_bacula.pl

Originaly written by Michael Wyraz. [Link to nagios exchange](https://exchange.nagios.org/directory/Plugins/Backup-and-Recovery/Bacula/check_bacula_lastbackup-2Epl/details).

```bash
check_bacula_lastbackup.pl 1.0 Nagios Plugin

===========================================================================
ERROR: Missing or wrong arguments!
===========================================================================

This script checks before how many hours the last successfull
backup of a certain client was done.


The following options are available:
   -bconsole-command=path    path to the bconsole command (/usr/local/sbin/bconsole)
   -client=text              bacula client to check
   -level=[*|F|D|I]          level of backup to check (*=any, F=full, D=differential, I=incremental - default: any)
   -warningAge=hours         if the last backup is older than 24 hours, status is warning
   -criticalAge=hours        if the last backup is older than 48 hours, status is critical

 Options may abbreviated!
This script comes with ABSOLUTELY NO WARRANTY
This programm is licensed under the terms of the GNU General Public License
```

## check\_emc\_isilon.py

Plugin to check some status information about EMC Isilon storage system over snmp.

## check_ipvs.py

Checks status of ldirector load balancer.

## check\_nginx\_config.sh

Simple check if there are errors and warnings in nginx configuration. Because devops and devs don't care about that.

## check_oom.py

Check if there are OOM in your system. ATM it check all dmesg output. If you want after check make it green again, you need to run dmesg -c.

```bash
usage: check_oom.py [-h] [-m {warning,critical,default}] [-v]

Check for OOM killer events

optional arguments:
  -h, --help            show this help message and exit
  -m {warning,critical,default}, --mode {warning,critical,default}
                        Mode of results for this check: warning, critical,
                        default
  -v, --verbose         Show verbose output from demsg about OOM killer events

check_oom.py: v.0.2 by Dmytro Prokhorenkov
```

## check_gitlab.py

Checks [Gitlab](https://gitlab.com) application health.

Work in progress. At the moment script checks only application health. More options comming soon.

```bash
usage: check_gitlab.py [-h] [--host HOST] [--token TOKEN] [--ssl {on,off}]
[--mode MODE] [--timeout TIMEOUT]

Check Gitlab api status

optional arguments:
-h, --help         show this help message and exit
--host HOST        Gitlab URL address
--token TOKEN      Gitlab auth token
--ssl {on,off}     Use SSL to connect to API: on or off. By default `on`
--mode MODE        Set check mode: health, group_size
--timeout TIMEOUT  HTTP(s) connection timeout

Written 2018, Dmytro Prokhorenkov
```
