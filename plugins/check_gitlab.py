#!/usr/bin/env python3

import sys
import re
import argparse
import json
import requests

version = 'v0.1.0'

check_url = { "health": "#PROTO#://#HOST#/-/readiness?token=#TOKEN#", "group_size": "" }

def generate_url(_replace_dict, _url):
  new_url = _url
  for mask, value in _replace_dict.items():
    new_url = new_url.replace(mask, value)
  return new_url

def check_health(_host, _token, _ssl, _timeout):
  proto = "https"
  unhealthy_services = []
  if (_ssl == "off"):
    proto = "http"
  replace_dict = { "#PROTO#": proto, "#HOST#": _host, "#TOKEN#": _token }
  health_url = generate_url(replace_dict, check_url['health'])
  try:
    gitlab_status = requests.get(health_url, timeout=_timeout)
    get_status_code = gitlab_status.raise_for_status()
    for item, item_status in gitlab_status.json().items():
      if (item_status['status'] != "ok"):
        unhealthy_services.append(item)
    if (unhealthy_services == []):
      result = { "exit_code": 0, "text": "Everything is ok" }
    else:
      result = { "exit_code": 2, "text": "Next services are not ok: {}".format(",".join(unhealthy_services)) }
  except requests.exceptions.RequestException as err:
    result = { "exit_code": 2, "text": "HTTP(s) request error code: {}".format(err) }
  except requests.exceptions.ConnectionError as errc:
    result = { "exit_code": 2, "text": "Connection error to server: {}".format(errc) }
  except requests.exceptions.Timeout as errt:
    result = { "exit_code": 2, "text": "".format(errt) }
  finally:
    return result

def main():
  args = argparse.ArgumentParser(add_help=True, description='Check Gitlab api status', epilog="Written 2018, Dmytro Prokhorenkov")
  args.add_argument('--host', type=str, help="Gitlab URL address")
  args.add_argument('--token', type=str, help="Gitlab auth token")
  args.add_argument('--ssl', type=str, help="Use SSL to connect to API: on or off. By default `on`", choices=['on', 'off'], default="off")
  args.add_argument('--mode', type=str, help="Set check mode: health, group_size")
  args.add_argument('--timeout', type=int, help="HTTP(s) connection timeout", default=10)
  _args = vars(args.parse_args())

  if ((_args['host'] == None) or (_args['token'] == None) or (_args['mode'] == None)):
    args.print_help()
    sys.exit(3)

  host = _args['host']
  token = _args['token']
  mode = _args['mode']
  ssl = _args['ssl']
  timeout = _args['timeout']

  output = check_health(host, token, ssl, timeout)
  print(output['text'])
  sys.exit(output['exit_code'])

if __name__ == "__main__":
  main()
