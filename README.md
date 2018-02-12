# icinga2-plugins

## check_bacula.pl

Originaly written by Michael Wyraz. [Link to nagios exchange](https://exchange.nagios.org/directory/Plugins/Backup-and-Recovery/Bacula/check_bacula_lastbackup-2Epl/details).

## check\_emc\_isilon.py

Plugin to check some status information about EMC Isilon storage system over snmp.

## check_ipvs.py

Checks status of ldirector load balancer.

## check\_nginx\_config.sh

Simple check if there are errors and warnings in nginx configuration. Because devops and devs don't care about that.

## check_oom.py

Check if there are OOM in your system. ATM it check all dmesg output. If you want after check make it green again, you need to run dmesg -c.

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
