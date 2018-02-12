#!/bin/bash

result=$(/usr/sbin/nginx -t 2>&1)
exit_code=$(echo $?)

if [ $exit_code -eq 1 ]
then
  echo "CRITICAL: Errors in nginx config files"
  exit 2
fi

if [ $exit_code -eq 0 ]
then
  warn=$(echo $result | grep warn)
  if [ "0$warn" != "0" ]
  then
    echo "WARNING: There are minor problems in your config"
    exit 2
  else
    echo "OK: Nginx config is ok"
    exit 0
  fi
fi

echo $result
echo $exit_code
