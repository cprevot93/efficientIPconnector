#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from . import core
from . import helpers
from ftntlib import FortiManagerJSON

# if len(sys.argv) < 2:
#   print('Usage: ' + sys.argv[0] + 'IP <JSON API URL>')
#   exit(1)

def main(argv):
  # ip = "100.68.99.10" 
  ip = "10.10.20.254" 
  user ='admin'
  # passwd ='fortinet'
  passwd ='AdminFMG'
  adom = "global"
  helpers.api.login(ip, user, passwd)
  helpers.api.debug('off')
  sub = core.Subnet("gall32", "0.0.0.0", "0.0.0.0", adom)
  sub.push_to_FMG()
  helpers.api.logout()

if __name__ == "__main__":
  main(sys.argv)